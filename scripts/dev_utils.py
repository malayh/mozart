from __future__ import annotations

import random
import time

import mido

from mozart.primitives import Chord, MidiNote


def play_notes(notes: list[MidiNote]):
    print(notes)
    outport = mido.open_output("pyMidiPort 1")
    for note in notes:
        outport.send(mido.Message("note_on", note=note.midi, velocity=100, channel=0))
        time.sleep(1)
        outport.send(mido.Message("note_off", note=note.midi, velocity=0, channel=0))


def play_chord(chord: Chord, arpeggiate=False):
    print(chord.notes, chord.degree, chord.chord_type)

    arp_sleep = 0
    outport = mido.open_output("pyMidiPort 1")
    for note in chord.notes:
        outport.send(mido.Message("note_on", note=note.midi, velocity=random.randint(80, 100), channel=0))

        if arpeggiate:
            arp_sleep = random.randint(100, 200) / 1500

        time.sleep(arp_sleep)

    time.sleep(2)

    for note in chord.notes:
        outport.send(mido.Message("note_off", note=note.midi, velocity=0, channel=0))

    outport.close()
