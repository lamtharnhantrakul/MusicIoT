# ------------ { SAMPLE PROJECT FOR PUBNUB INTERVIEW } -----------------------------------------------------------------------
# Lamtharn (Hanoi) Hantrakul
# Requires pubnub, rtmidi and mido
# Designed to work with the DJ Tech Tools MIDI Fighter 3D (MF3D) - https://store.djtechtools.com/products/midi-fighter-3d
# This application publishes midi button presses on the MF3D onto the PubNub Network and displays Presence occupancy
#-----------------------------------------------------------------------------------------------------------------------------

# Standard imports
import sys
import time
from datetime import datetime
from pubnub import Pubnub
from rtmidi.midiutil import open_midiport
import mido

# Using rtmidi, query the user for what MIDI controller will be used
port = sys.argv[1] if len(sys.argv) > 1 else None
try:
    midiin, port_name = open_midiport(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()
output_MF3D = mido.open_output('') # open the corresponding Midi Port

# Setup pubnub network
pubnub = Pubnub(publish_key="pub-c-5b904818-cb5a-4909-b8cc-d3932d5ee41d",
                subscribe_key="sub-c-d48408e4-dac9-11e6-a669-0619f8945a4f")
channel = "sample_project"

# Callback function that is executed when presence changes on PubNub network
def presence_callback(message, channel):
    print(message)
    # Turn off all lights (52 - 67 corresponds to lights on second page of MF3D)
    for note in range(52,67):
        output_MF3D.send(mido.Message('note_off',
                                      note=note,
                                      velocity=127))

    # Turn on number of lights equal to occupancy
    for i in range(message['occupancy']):
        output_MF3D.send(mido.Message('note_on',
                                      note=52+i,
                                      velocity=127))

print("Entering main loop. Press Control-C to exit.")
try:
    # Monitor presence for changes in occupancy
    pubnub.presence(channel=channel, callback=presence_callback)

    # Poll the MF3D infinitely for MIDI messages
    while True:
        msg = midiin.get_message()

        # Only consider messages with actual note information
        if msg:
            message, deltatime = msg
            print("%r" % message)

            # Timestamp to calculate roundtrip latency
            if message[0] == 144:
                stamp = datetime.utcnow()

            # Data to be transmitted. Parse "message" list into constituent parts
            data = {
                'type': message[0],
                'note': message[1],
                'velocity': message[2],
                'time': stamp.microsecond
            }

            #Publish to pubnub channel
            pubnub.publish(channel, data)

        # Polling interval
        time.sleep(0.01)

except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
