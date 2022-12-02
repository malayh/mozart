import script_include

from motzart.primitives import Scale, Mode, Chord, Note
from dev_utils import play_chord


def try_extention():
    root = Note.C.get_midi(4)
    scale = Mode.ionian.get_scale(root)

    for i in [5, 1]:
        chord = scale.get_diatonic_triad(i)
        chord.extend(7, argumentation="")

        play_chord(chord, arpeggiate=False)


if __name__ == "__main__":
    try_extention()
