import unittest

from expects import equal, expect

from motzart.player import Clip, PlayedNote
from motzart.primitives import MidiNote, Note


class TestClip(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.D, 4)

    def test_clip_ends_at(self):
        played_note = PlayedNote(self.note, starts_at=0, ends_at=2)
        clip = Clip(played_notes=[played_note])

        expect(clip.ends_at).to(equal(2))

        clip = Clip(played_notes=[played_note], _ends_at=4)
        expect(clip.ends_at).to(equal(4))

    def test_concat_without_ends_at(self):
        played_note = PlayedNote(self.note, starts_at=0, ends_at=2)
        clip = Clip(played_notes=[played_note])
        clip_2 = Clip(played_notes=[PlayedNote(self.note, starts_at=0, ends_at=4)])

        clip.concat(clip_2)

        expect(clip.ends_at).to(equal(6))

    def test_concat_with_ends_at_at_2nd(self):
        played_note = PlayedNote(self.note, starts_at=0, ends_at=2)
        clip = Clip(played_notes=[played_note])
        clip_2 = Clip(played_notes=[PlayedNote(self.note, starts_at=0, ends_at=4)], _ends_at=7)

        clip.concat(clip_2)

        expect(clip.ends_at).to(equal(9))

    def test_concat_with_ends_at_both(self):
        played_note = PlayedNote(self.note, starts_at=0, ends_at=2)
        clip = Clip(played_notes=[played_note], _ends_at=3)
        clip_2 = Clip(played_notes=[PlayedNote(self.note, starts_at=0, ends_at=4)], _ends_at=7)

        clip.concat(clip_2)

        expect(clip.ends_at).to(equal(10))

    def test_concat_with_ends_at_1st(self):
        played_note = PlayedNote(self.note, starts_at=0, ends_at=2)
        clip = Clip(played_notes=[played_note], _ends_at=3)

        clip_2 = Clip(played_notes=[PlayedNote(self.note, starts_at=0, ends_at=4)])

        clip.concat(clip_2)

        expect(clip.ends_at).to(equal(7))
