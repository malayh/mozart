from __future__ import annotations

import script_include  # noqa F401

from mozart.midifile import parse_midfile
from mozart.player import PlayedNote, Player
from mozart.primitives import Note


def try_player():
    note_a = Note.C.get_midi(4)
    note_b = Note.C_sharp.get_midi(4)

    notes = [
        PlayedNote(note_a, 0, 1),
        PlayedNote(note_b, 1, 2),
        PlayedNote(note_b, 2, 3),
        PlayedNote(note_b, 3, 4),
    ]

    player = Player(bpm=100)
    player.render(notes)
    player.play()


def try_clip():
    path = r"midi_clips\drums\fpc_affection_lofi.mid"

    midi_clip = parse_midfile(path)
    midi_clip.clip.round_up_to_nearest_bar(4)

    cut = midi_clip.clip.cut(0, 4)
    for n in cut.played_notes:
        print(n)

    player = Player(bpm=120)
    player.render(cut.played_notes)
    player.play()


if __name__ == "__main__":
    try_clip()
