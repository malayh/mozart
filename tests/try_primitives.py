import script_include  # noqa F401

from dev_utils import play_chord, play_notes
from motzart.primitives import Mode, Note


def try_mode():
    root = Note.D.get_midi(4)
    scale = Mode.lydian.get_scale(root)
    play_notes(scale.notes)


def try_diatonic_chords():
    root = Note.C.get_midi(4)
    scale = Mode.locarian.get_scale(root)

    for i in range(1, 8):
        chord = scale.get_diatonic_triad(i)
        play_chord(chord)


def try_extention():
    root = Note.C.get_midi(4)
    scale = Mode.ionian.get_scale(root)

    for i in [5, 1]:
        chord = scale.get_diatonic_triad(i)
        chord.extend(7, argumentation="")

        play_chord(chord, arpeggiate=False)


if __name__ == "__main__":
    # try_extention()
    try_diatonic_chords()
    # try_mode()
