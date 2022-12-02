import mido
import time

from motzart.primitives import Chord


def play_chord(chord: Chord, arpeggiate=False):
    print(chord.notes)

    arp_sleep = 0.1 if arpeggiate else 0
    outport = mido.open_output("pyMidiPort 1")
    for note in chord.notes:
        outport.send(mido.Message("note_on", note=note.midi, velocity=100, channel=3))
        time.sleep(arp_sleep)

    time.sleep(2)

    for note in chord.notes:
        outport.send(mido.Message("note_off", note=note.midi, velocity=0, channel=3))

    outport.close()
