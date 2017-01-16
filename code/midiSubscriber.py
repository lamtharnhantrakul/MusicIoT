# ------------ { SAMPLE PROJECT FOR PUBNUB INTERVIEW } -----------------------------------------------------------------------
# Lamtharn (Hanoi) Hantrakul
# Requires pubnub and mido
# Designed to work with the DJ Tech Tools MIDI Fighter 3D (MF3D) - https://store.djtechtools.com/products/midi-fighter-3d
# Designed to communicate with Ableton Live via IAC Bus Driver
# This application listens for midi messages from the PubNub network. It lights up the corresponding key on the connected MIDI
# Fighter and also sends the midi message to Ableton Live. The roundtrip latency is printed to the console.
#-----------------------------------------------------------------------------------------------------------------------------

# Standard imports
from pubnub import Pubnub
import mido
from datetime import datetime
import sys

# Setup pubnub network
pubnub = Pubnub(publish_key="pub-c-5b904818-cb5a-4909-b8cc-d3932d5ee41d",
                subscribe_key="sub-c-d48408e4-dac9-11e6-a669-0619f8945a4f")
channel = "sample_project"

# Open midiport for IAC Driver (to send actual midi notes)
output_IAC = mido.open_output('IAC Driver IAC Bus 1')

# Open midiport for MF3D (to send midi data for lighting)
output_MF3D = mido.open_output('Midi Fighter 3D')

# Callback function is executed when a message arrives in PubNub network channel
def _callback(message, channel):

    # 144 correponds to a "note_on" message
    if message['type'] == 144:
        # Calculate roundtrip latency, should ideally be <50ms for musical applications
        stamp = datetime.utcnow()
        latency = (stamp.microsecond - message["time"]) / 1000
        print("Roundtrip latency: " + str(latency))

        # Send MIDI data to IAC bus
        output_IAC.send(mido.Message('note_on',
                                     note=message["note"],
                                     velocity=127))

        # Send MIDI data to MF3D bus
        output_MF3D.send(mido.Message('note_on',
                                      note=message["note"],
                                      velocity=127))

    # 144 correponds to a "note_off" message
    elif message['type'] == 128:
         # Send MIDI data to IAC bus
        output_IAC.send(mido.Message('note_off',
                                     note=message["note"],
                                     velocity=127))

         # Send MIDI data to MF3D bus
        output_MF3D.send(mido.Message('note_off',
                                      note=message["note"],
                                      velocity=127))

    # 20 is the first side button on the left of the MF3D
    elif message['note'] == 20:
        # Unsubscribe and exit when pressed
        pubnub.unsubscribe(channel=channel)
        sys.exit(0)

# Callback function in case of error
def _error(message):
    print(message)

# Subscribe to channel
pubnub.subscribe(channels=channel, callback=_callback, error=_error)
