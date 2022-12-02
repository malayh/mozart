from expects import expect, equal, have_len

import unittest
from unittest.mock import patch

from motzart.primitives import Mode, Note, MidiNote, MAJOR_SCALE_INTERVALS


class TestMidiNote(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.D, 4)

    def test_midi_prop(self):
        expect(self.note.midi).to(equal(2 + (12 * 4)))

    def test_next_interval(self):
        note = self.note.next_by_interval(3)
        expect(note.note).to(equal(Note.F))
        expect(note.octave).to(equal(self.note.octave))

        note = self.note.next_by_interval(12)
        expect(note.note).to(equal(Note.D))
        expect(note.octave).to(equal(self.note.octave + 1))

    def test_sharpen(self):
        self.note.sharpen()
        expect(self.note.note).to(equal(Note.D_sharp))

        note = MidiNote(Note.B, 4)
        note.sharpen()
        expect(note.note).to(equal(Note.C))
        expect(note.octave).to(equal(5))

    def test_flatten(self):
        self.note.flatten()
        expect(self.note.note).to(equal(Note.C_sharp))

        note = MidiNote(Note.C, 4)
        note.flatten()
        expect(note.note).to(equal(Note.B))
        expect(note.octave).to(equal(3))

    def test_distance(self):
        note = MidiNote(Note.D, 5)
        expect(self.note.distance(note)).to(equal(12))

        note = MidiNote(Note.D_sharp, 4)
        expect(self.note.distance(note)).to(equal(1))

        note = MidiNote(Note.G, 4)
        expect(self.note.distance(note)).to(equal(5))

    def test_duplicate(self):
        note = self.note.duplicate()
        expect(id(note)).to_not(equal(id(self.note)))


class TestMode(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.D, 4)

    def test_get_scale_intervals_ionian(self):
        scale = Mode.ionian.get_scale(self.note)
        expect(scale.notes).to(have_len(8))

        for i, interval in enumerate(MAJOR_SCALE_INTERVALS):
            expect(scale.notes[i].distance(scale.notes[i + 1])).to(equal(interval))

    def test_get_scale_offset(self):
        scale = Mode.lydian.get_scale(self.note)
        expect(scale.notes).to(have_len(8))

        offset = Mode.lydian.value
        for i in range(7):
            interval = MAJOR_SCALE_INTERVALS[(i + offset) % 7]
            expect(scale.notes[i].distance(scale.notes[i + 1])).to(equal(interval))


class TestScale(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.C, 4)
        self.scale = Mode.ionian.get_scale(self.note)

    def test_get_diatonic_chord(self):
        chord = self.scale.get_diatonic_triad(2)
        expect(chord.notes[0].note).to(equal(self.scale.notes[1].note))

        expect(chord.notes).to(have_len(3))

    def test_get_note_by_distance(self):
        note = self.scale.get_note_by_distance(0, 2)
        expect(note).to(equal(self.scale.notes[2]))

        note = self.scale.get_note_by_distance(3, 2)
        expect(note).to(equal(self.scale.notes[5]))

        note = self.scale.get_note_by_distance(3, 8)
        expect(note.note).to(equal(self.scale.notes[4].note))
        expect(note.octave).to(equal(self.scale.notes[4].octave + 1))

        # C  D  E  F  G  A  B  C
        # 0  1  2  3  4  5  6  7

        # -> 7 + 1 = 8
        # -> 8 % 7 = 1 = D
        note = self.scale.get_note_by_distance(7, 1)
        expect(note.note).to(equal(self.scale.notes[1].note))
        expect(note.octave).to(equal(self.scale.notes[1].octave + 1))

        # -> 6 + 3 = 9
        # -> 9 % 7 = 2 = E
        note = self.scale.get_note_by_distance(6, 3)
        expect(note.note).to(equal(self.scale.notes[2].note))
        expect(note.octave).to(equal(self.scale.notes[2].octave + 1))


class TestChord(unittest.TestCase):
    def setUp(self) -> None:
        self.note = MidiNote(Note.C, 4)
        self.scale = Mode.ionian.get_scale(self.note)
        self.chord = self.scale.get_diatonic_triad(1)

    def test_extend(self):
        self.chord.extend(7)
        expect(self.chord.notes).to(have_len(4))

        _i = self.scale.notes.index(self.chord.notes[0])
        new_note = self.scale.get_note_by_distance(_i, 6)

        expect(self.chord.notes[-1]).to(equal(new_note))

    def test_extend_flat(self):
        self.chord.extend(6, argumentation="flat")
        expect(self.chord.notes).to(have_len(4))

        _i = self.scale.notes.index(self.chord.notes[0])
        new_note = self.scale.get_note_by_distance(_i, 5).flatten()

        expect(self.chord.notes[-1]).to(equal(new_note))

    def test_extend_many(self):
        patcher = patch("motzart.primitives.Chord.extend")
        mock = patcher.start()

        self.chord.extend_many(["7"])
        mock.assert_called_with(7, argumentation=None)

        self.chord.extend_many(["b13"])
        mock.assert_called_with(13, argumentation="flat")

        self.chord.extend_many(["#4"])
        mock.assert_called_with(4, argumentation="sharp")
