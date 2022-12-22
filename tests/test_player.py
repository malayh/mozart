import unittest

from expects import equal, expect, have_key, have_len

from mozart.midifile import parse_midfile
from mozart.player import Clip, PlayedNote, Track
from mozart.primitives import MidiNote, Note


class TestClip(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.D, 4)
        self.midi_clip = parse_midfile(r"tests\test_files\test_midi.mid")

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

    def test_rounding_by_4(self):
        clip = self.midi_clip.clip
        expect(clip.ends_at).to(equal(11))

        clip.round_up_to_nearest_bar(4)
        expect(clip.ends_at).to(equal(12))

    def test_rounding_by_5(self):
        clip = self.midi_clip.clip
        expect(clip.ends_at).to(equal(11))

        clip.round_up_to_nearest_bar(5)
        expect(clip.ends_at).to(equal(15))

    def test_clip_cut_1_bar_1(self):
        clip = self.midi_clip.clip.cut(0, 4)
        expect(clip.played_notes).to(have_len(5))
        expect(clip.ends_at).to(equal(4))

        c = [n for n in clip.played_notes if n.note.note == Note.C][0]
        expect(c.starts_at).to(equal(0))
        expect(c.ends_at).to(equal(4))
        expect(c.starts_at_offset).to(equal(0.0))
        expect(c.ends_at_offset).to(equal(0.0))
        expect(c.effective_start).to(equal(0.0))
        expect(c.effective_end).to(equal(4.0))

        c_sharp = [n for n in clip.played_notes if n.note.note == Note.C_sharp][0]
        expect(c_sharp.starts_at).to(equal(0))
        expect(c_sharp.ends_at).to(equal(4))
        expect(c_sharp.starts_at_offset).to(equal(25.0))
        expect(c_sharp.ends_at_offset).to(equal(0))
        expect(c_sharp.effective_start).to(equal(0.25))
        expect(c_sharp.effective_end).to(equal(4.0))

        d = [n for n in clip.played_notes if n.note.note == Note.D][0]
        expect(d.starts_at).to(equal(0))
        expect(d.ends_at).to(equal(4))
        expect(d.starts_at_offset).to(equal(75.0))
        expect(d.ends_at_offset).to(equal(0))
        expect(d.effective_start).to(equal(0.75))
        expect(d.effective_end).to(equal(4.0))

        d_sharp = [n for n in clip.played_notes if n.note.note == Note.D_sharp][0]
        expect(d_sharp.starts_at).to(equal(1))
        expect(d_sharp.ends_at).to(equal(2))
        expect(d_sharp.starts_at_offset).to(equal(50.0))
        expect(d_sharp.ends_at_offset).to(equal(50.0))
        expect(d_sharp.effective_start).to(equal(1.5))
        expect(d_sharp.effective_end).to(equal(2.5))

        e = [n for n in clip.played_notes if n.note.note == Note.E][0]
        expect(e.starts_at).to(equal(2))
        expect(e.ends_at).to(equal(3))
        expect(e.starts_at_offset).to(equal(75.0))
        expect(e.ends_at_offset).to(equal(75.0))
        expect(e.effective_start).to(equal(2.75))
        expect(e.effective_end).to(equal(3.75))

    def test_clip_cut_2_bar_1(self):
        clip = self.midi_clip.clip.cut(1, 3)
        expect(clip.played_notes).to(have_len(5))
        expect(clip.ends_at).to(equal(2))

        c = [n for n in clip.played_notes if n.note.note == Note.C][0]
        expect(c.starts_at).to(equal(0))
        expect(c.ends_at).to(equal(2))
        expect(c.starts_at_offset).to(equal(0.0))
        expect(c.ends_at_offset).to(equal(0.0))
        expect(c.effective_start).to(equal(0.0))
        expect(c.effective_end).to(equal(2.0))

        c_sharp = [n for n in clip.played_notes if n.note.note == Note.C_sharp][0]
        expect(c_sharp.starts_at).to(equal(0))
        expect(c_sharp.ends_at).to(equal(2))
        expect(c_sharp.starts_at_offset).to(equal(0.0))
        expect(c_sharp.ends_at_offset).to(equal(0))
        expect(c_sharp.effective_start).to(equal(0.0))
        expect(c_sharp.effective_end).to(equal(2.0))

        d = [n for n in clip.played_notes if n.note.note == Note.D][0]
        expect(d.starts_at).to(equal(0))
        expect(d.ends_at).to(equal(2))
        expect(d.starts_at_offset).to(equal(0.0))
        expect(d.ends_at_offset).to(equal(0))
        expect(d.effective_start).to(equal(0.0))
        expect(d.effective_end).to(equal(2.0))

        d_sharp = [n for n in clip.played_notes if n.note.note == Note.D_sharp][0]
        expect(d_sharp.starts_at).to(equal(0))
        expect(d_sharp.ends_at).to(equal(1))
        expect(d_sharp.starts_at_offset).to(equal(50.0))
        expect(d_sharp.ends_at_offset).to(equal(50.0))
        expect(d_sharp.effective_start).to(equal(0.5))
        expect(d_sharp.effective_end).to(equal(1.5))

        e = [n for n in clip.played_notes if n.note.note == Note.E][0]
        expect(e.starts_at).to(equal(1))
        expect(e.ends_at).to(equal(2))
        expect(e.starts_at_offset).to(equal(75.0))
        expect(e.ends_at_offset).to(equal(0.0))
        expect(e.effective_start).to(equal(1.75))
        expect(e.effective_end).to(equal(2.0))


class TestTrack(unittest.TestCase):
    def setUp(self):
        self.midi_clip = parse_midfile(r"tests\test_files\test_midi.mid")

        self.clip_1 = self.midi_clip.clip.cut(0, 4)
        self.clip_2 = self.midi_clip.clip.cut(8, 12)

        self.clip_1.round_up_to_nearest_bar(4)
        self.clip_2.round_up_to_nearest_bar(4)

    def test_append_on_empty(self):
        track = Track(midi_channel=4)
        track.append(self.clip_1)

        expect(track.clips).to(have_key(0))

        played_note = track.render()

        for renderd_note, og_note in zip(played_note, self.clip_1.played_notes):
            expect(renderd_note.midi_channel).to(equal(4))
            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at))
            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end))

    def test_append_on_existing(self):
        track = Track()
        track.append(self.clip_2)
        track.append(self.clip_1)

        expect(track.clips[0]).to(equal(self.clip_2))
        expect(track.clips[4]).to(equal(self.clip_1))

        played_note = track.render()

        for renderd_note, og_note in zip(played_note, self.clip_2.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))
            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at))
            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end))

        for renderd_note, og_note in zip(played_note[len(self.clip_2.played_notes) :], self.clip_1.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))

            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at + 4))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at + 4))

            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start + 4))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end + 4))

    def test_put_on_empty(self):
        track = Track()
        track.put(self.clip_2, 3)

        played_note = track.render()
        for renderd_note, og_note in zip(played_note, self.clip_2.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))
            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at + 3))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at + 3))
            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start + 3))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end + 3))

    def test_put_on_existing(self):
        track = Track()
        track.append(self.clip_2)
        track.put(self.clip_1, 12)

        played_note = track.render()
        for renderd_note, og_note in zip(played_note[len(self.clip_2.played_notes) :], self.clip_1.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))

            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at + 12))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at + 12))

            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start + 12))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end + 12))

    def test_put_on_existing_with_overlap(self):
        track = Track()
        track.append(self.clip_2)
        with self.assertRaises(ValueError) as ctx:
            track.put(self.clip_1, 3)

        expect(str(ctx.exception)).to(equal("Clip overlaps with existing clip"))

        track.put(self.clip_1, 4)

    def test_append_after_put(self):
        track = Track()
        track.put(self.clip_2, 2)
        track.append(self.clip_1)

        played_note = track.render()
        for renderd_note, og_note in zip(played_note[len(self.clip_2.played_notes) :], self.clip_1.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))

            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at + 6))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at + 6))

            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start + 6))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end + 6))

    def test_put_after_append(self):
        track = Track()
        track.append(self.clip_2)
        track.put(self.clip_1, 5)

        played_note = track.render()
        for renderd_note, og_note in zip(played_note[len(self.clip_2.played_notes) :], self.clip_1.played_notes):
            expect(renderd_note.midi_channel).to(equal(0))

            expect(renderd_note.note).to(equal(og_note.note))
            expect(renderd_note.starts_at).to(equal(og_note.starts_at + 5))
            expect(renderd_note.ends_at).to(equal(og_note.ends_at + 5))

            expect(renderd_note.starts_at_offset).to(equal(og_note.starts_at_offset))
            expect(renderd_note.ends_at_offset).to(equal(og_note.ends_at_offset))
            expect(renderd_note.effective_start).to(equal(og_note.effective_start + 5))
            expect(renderd_note.effective_end).to(equal(og_note.effective_end + 5))
