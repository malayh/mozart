from __future__ import annotations
import script_include
from motzart.performer import Performer, PerformedNote
from motzart.primitives import Note

if __name__ == "__main__":
    note_a = Note.C.get_midi(4)
    note_b = Note.C_sharp.get_midi(4)
    

    notes = [
        PerformedNote(note_a, 0, 1),
        PerformedNote(note_b, 1, 2),
        PerformedNote(note_b, 2, 3),
        PerformedNote(note_b, 3, 4),
    ]

    player = Performer(bpm=100)
    player.render(notes)
    player.play()
