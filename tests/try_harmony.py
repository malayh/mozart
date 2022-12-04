import script_include

from dev_utils import play_chord
from motzart.primitives import Chord, Mode, Note, MidiNote
from motzart.harmony import ChordProgression, ChordProgressionGenerator


def try_generator_v2():
    cpg = ChordProgressionGenerator(Note.E, Mode.lydian, octave=4, lenght=6)
    progression = cpg.generate_v2(resolution_strenght=5)
    progression.add_spice(level=1)
    for chord in progression.chords:
        play_chord(chord, arpeggiate=True)


if __name__ == "__main__":
    # try_chord_generator()
    try_generator_v2()
