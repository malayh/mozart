import unittest

from expects import be_true, equal, expect, have_len

import math
from mozart.midifile import parse_midfile
from mozart.primitives import Note


class TestMidiFile(unittest.TestCase):
    def setUp(self) -> None:
        self.midi_clip = parse_midfile(r"tests\test_files\test_midi.mid")

    def test_midi_clip_lenght(self):
        expect(self.midi_clip.clip.ends_at).to(equal(11))
        expect(self.midi_clip.clip.played_notes).to(have_len(16))

    def test_note_properties_bar_1(self):
        bar_1_notes = self.midi_clip.clip.played_notes[:5]

        c = [n for n in bar_1_notes if n.note.note == Note.C][0]
        expect(c.starts_at).to(equal(0))
        expect(c.ends_at).to(equal(4))
        expect(c.starts_at_offset).to(equal(0.0))
        expect(c.ends_at_offset).to(equal(25.0))
        expect(c.effective_start).to(equal(0.0))
        expect(c.effective_end).to(equal(4.25))

        c_sharp = [n for n in bar_1_notes if n.note.note == Note.C_sharp][0]
        expect(c_sharp.starts_at).to(equal(0))
        expect(c_sharp.ends_at).to(equal(4))
        expect(c_sharp.starts_at_offset).to(equal(25.0))
        expect(c_sharp.ends_at_offset).to(equal(0))
        expect(c_sharp.effective_start).to(equal(0.25))
        expect(c_sharp.effective_end).to(equal(4.0))

        d = [n for n in bar_1_notes if n.note.note == Note.D][0]
        expect(d.starts_at).to(equal(0))
        expect(d.ends_at).to(equal(4))
        expect(d.starts_at_offset).to(equal(75.0))
        expect(d.ends_at_offset).to(equal(0))
        expect(d.effective_start).to(equal(0.75))
        expect(d.effective_end).to(equal(4.0))

        d_sharp = [n for n in bar_1_notes if n.note.note == Note.D_sharp][0]
        expect(d_sharp.starts_at).to(equal(1))
        expect(d_sharp.ends_at).to(equal(2))
        expect(d_sharp.starts_at_offset).to(equal(50.0))
        expect(d_sharp.ends_at_offset).to(equal(50.0))
        expect(d_sharp.effective_start).to(equal(1.5))
        expect(d_sharp.effective_end).to(equal(2.5))

        e = [n for n in bar_1_notes if n.note.note == Note.E][0]
        expect(e.starts_at).to(equal(2))
        expect(e.ends_at).to(equal(3))
        expect(e.starts_at_offset).to(equal(75.0))
        expect(e.ends_at_offset).to(equal(75.0))
        expect(e.effective_start).to(equal(2.75))
        expect(e.effective_end).to(equal(3.75))

    def test_note_properties_bar_2(self):
        bar_2_notes = self.midi_clip.clip.played_notes[5:13]

        c = [n for n in bar_2_notes if n.note.note == Note.C][0]
        expect(c.starts_at).to(equal(4))
        expect(c.ends_at).to(equal(5))
        expect(c.starts_at_offset).to(equal(50.0))
        expect(c.ends_at_offset).to(equal(0))
        expect(c.effective_start).to(equal(4.5))
        expect(c.effective_end).to(equal(5.0))

        c_sharp = [n for n in bar_2_notes if n.note.note == Note.C_sharp][0]
        expect(c_sharp.starts_at).to(equal(5))
        expect(c_sharp.ends_at).to(equal(5))
        expect(c_sharp.starts_at_offset).to(equal(0))
        expect(c_sharp.ends_at_offset).to(equal(50.0))
        expect(c_sharp.effective_start).to(equal(5.0))
        expect(c_sharp.effective_end).to(equal(5.50))

        d = [n for n in bar_2_notes if n.note.note == Note.D][0]
        expect(d.starts_at).to(equal(5))
        expect(d.ends_at).to(equal(5))
        expect(d.starts_at_offset).to(equal(0))
        expect(d.ends_at_offset).to(equal(50.0))
        expect(d.effective_start).to(equal(5.0))
        expect(d.effective_end).to(equal(5.5))

        d_sharp = [n for n in bar_2_notes if n.note.note == Note.D_sharp][0]
        expect(d_sharp.starts_at).to(equal(5))
        expect(d_sharp.ends_at).to(equal(6))
        expect(d_sharp.starts_at_offset).to(equal(50.0))
        expect(d_sharp.ends_at_offset).to(equal(0.0))
        expect(d_sharp.effective_start).to(equal(5.5))
        expect(d_sharp.effective_end).to(equal(6.0))

        e = [n for n in bar_2_notes if n.note.note == Note.E][0]
        expect(e.starts_at).to(equal(6))
        expect(e.ends_at).to(equal(7))
        expect(e.starts_at_offset).to(equal(12.5))
        expect(e.ends_at_offset).to(equal(12.5))
        expect(e.effective_start).to(equal(6.125))
        expect(e.effective_end).to(equal(7.125))

    def test_note_properties_bar_3(self):
        bar_3_notes = self.midi_clip.clip.played_notes[13:16]

        b = [n for n in bar_3_notes if n.note.note == Note.B][0]
        expect(b.starts_at).to(equal(7))
        expect(b.ends_at).to(equal(10))
        expect(b.starts_at_offset).to(equal(75.0))
        expect(math.isclose(b.ends_at_offset, 91.6, rel_tol=1e-2)).to(be_true)

        a_sharp = [n for n in bar_3_notes if n.note.note == Note.A_sharp][0]
        expect(a_sharp.starts_at).to(equal(8))
        expect(a_sharp.ends_at).to(equal(11))
        expect(a_sharp.starts_at_offset).to(equal(0.0))
        expect(a_sharp.ends_at_offset).to(equal(75.0))
        expect(a_sharp.effective_start).to(equal(8.0))
        expect(a_sharp.effective_end).to(equal(11.75))

        a = [n for n in bar_3_notes if n.note.note == Note.A][0]
        expect(a.starts_at).to(equal(8))
        expect(a.ends_at).to(equal(11))
        expect(a.starts_at_offset).to(equal(0.0))
        expect(a.ends_at_offset).to(equal(25.0))
        expect(a.effective_start).to(equal(8.0))
        expect(a.effective_end).to(equal(11.25))
