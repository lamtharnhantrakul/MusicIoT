# Music MIDIoT
Check out the video here!
[![Video link](https://github.com/lamtharnhantrakul/MusicIoT/blob/master/img/Screenshot.png)](https://www.youtube.com/watch?v=svLImSlHAvk&t=162s)

# About

This project connects a DJ Tech Tools Midi Fighter 3D (https://store.djtechtools.com/products/midi-fighter-3d) to the PubNub infrastructure. It re-imagines what a musical instrument can be in the age of IoT - what if musical instruments were connected to the internet 24/7? What new kinds of interactions would this enable? This project implements the following features:

1. A "publisher" Midi Fighter can send MIDI messages to the PubNub network
2. A "subscriber" Midi Figher can tune in on these MIDI presses, causing the corresponding lights to turn on in time with publisher Midi Fighter.
3. The "subscriber" Midi Fighter can choose to send these MIDI presses to Ableton Live via the IAC Bus Driver and trigger samples
4. The "publisher" Midi Fighter can monitor the number of remote MIDI Fighters currently listening on the channel

# Use cases

1. A teacher can broadcast midi messages on the publisher Midi Fighter to a number of subscriber Midi Fighter owned by students in different countries. The messages are relayed on the musical instrument interface itself, as opposed to a video intermediate. 
2. In idle state, the Midi Fighter can inform owner of other user's activities (practising, performing, improvising) through the musical instrument itself. 
3. Databese of symbolic notation of music (i.e MIDI) pale in comparison to available databases of music audio (ie. mp3, WAV). Imagine if every midi-enabled device constantly streams its messages to a cloud server in this manner. Then a "machine listening" algorithm can run through this data.  

# Getting started

In addition to installing the pubnub [python API](https://www.pubnub.com/docs/python/pubnub-python-sdk), you will need also need rtmidi and mido.

To install rtmidi (for capturing real-time midi messages)
```python
$ pip install python-rtmidi
```

To install mido (for capturing real-time midi messages)
```python
$ pip install mido
```

# Connecting to Ableton Live

First head over to **audio MIDI setup**, you can search for this using spotlight in Mac OSX (Windows users will need to use an alternative like virtualMIDI). Ensure that the red **IAC Driver** is **enabled**.

![alt text](https://github.com/lamtharnhantrakul/MusicIoT/blob/master/img/IAC%20Driver.png)

In Ableton Live, ensure that the MIDI channel has **MIDI From** set to **IAC Driver (IAC Bus)**

![alt text](https://github.com/lamtharnhantrakul/MusicIoT/blob/master/img/Ableton%20Channel%20Strip.png)

Load up a drum kit and jam away! Your MIDI Fighter is now IoT enabled!



