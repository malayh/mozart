import script_include

from dev_utils import play_chord
from motzart.primitives import Chord, Mode, Note, MidiNote
from motzart.harmony import ChordProgression, ChordProgressionGenerator
import time


def try_chord_generator():

    while True:
        cpg = ChordProgressionGenerator(Note.E, Mode.aeolian, octave=4, lenght=6)
        progression = cpg.generate()
        for chord in progression.chords:
            play_chord(chord, arpeggiate=True)

    # for mode in Mode:
    #     cpg = ChordProgressionGenerator(Note.C,mode)
    #     progression = cpg.generate_v1()

    #     for chord in progression.chords:
    #         play_chord(chord)

    #     time.sleep(1)


if __name__ == "__main__":
    try_chord_generator()
