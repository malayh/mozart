from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

MAJOR_SCALE_INTERVALS = [2, 2, 1, 2, 2, 2, 1]


class ChordType(Enum):
    major = 0
    minor = 1
    diminished = 2


MAJOR_SCALE_CHORD_TYPES = [
    ChordType.major,  # 1st - major
    ChordType.minor,  # 2nd - minor
    ChordType.minor,  # 3rd - minor
    ChordType.major,  # 4th - major
    ChordType.major,  # 5th - major
    ChordType.minor,  # 6th - minor
    ChordType.diminished,  # 7th - diminished
]


class Mode(Enum):
    ionian = 0
    dorian = 1
    phrygian = 2
    lydian = 3
    mixolydian = 4
    aeolian = 5
    locarian = 6

    def get_scale(self, root: MidiNote) -> Scale:
        offset = self.value
        notes = [root]
        _last_note = root

        for i in range(7):
            interval = MAJOR_SCALE_INTERVALS[(i + offset) % 7]
            _last_note = _last_note.next_by_interval(interval)
            notes.append(_last_note)

        return Scale(notes, self)


class Note(Enum):
    # value is base midi note value
    C = 0
    C_sharp = 1
    D = 2
    D_sharp = 3
    E = 4
    F = 5
    F_sharp = 6
    G = 7
    G_sharp = 8
    A = 9
    A_sharp = 10
    B = 11

    def get_midi(self, octave: int):
        return MidiNote(note=self, octave=octave)


@dataclass
class MidiNote:
    note: Note
    octave: int = 0
    velocity : int = 100

    @property
    def midi(self) -> int:
        return self.note.value + (12 * self.octave)

    def next_by_interval(self, interval: int):
        next_note = Note((self.note.value + interval) % 12)
        next_note_octave = self.octave + ((self.note.value + interval) // 12)

        return MidiNote(next_note, next_note_octave)

    def sharpen(self, semitone: int = 1):
        # TODO: Add boundry checks
        self.octave += (self.note.value + semitone) // 12
        self.note = Note((self.note.value + semitone) % 12)
        return self

    def flatten(self, semitone: int = 1):
        # TODO: Add boundry checks
        self.octave = self.octave + (self.note.value - semitone) // 12
        self.note = Note((self.note.value - semitone) % 12)
        return self

    def duplicate(self) -> MidiNote:
        return MidiNote(self.note, self.octave)

    def distance(self, note: MidiNote) -> int:
        """
        Returns distance in semitones
        """
        return abs(self.midi - note.midi)


@dataclass
class Scale:
    # Assume scale has 8 notes.
    notes: list[MidiNote]
    mode: Mode

    @property
    def root(self):
        return self.notes[0].note

    def get_note_by_distance(self, start: int, distance: int) -> MidiNote:
        """
        Retuns nth note from `start` index of self.notes where n=`distance`

        `start` is index of the starting note in self.notes
        """
        position = start + distance

        note = self.notes[position % 7]
        if position // 7 > 0:
            note = note.duplicate()
            note.octave += position // 7

        return note

    def get_note_by_degree(self, degree: int) -> MidiNote:
        # Assume scale has 8 notes.
        # Degree starts from 1

        position = degree - 1
        note = self.notes[position % 7]

        if position // 7 > 0:
            note = note.duplicate()
            note.octave += position // 7

        return note

    def get_diatonic_triad(self, degree: int):
        # degree starts at 1
        notes = [
            self.get_note_by_distance(degree - 1, 0),
            self.get_note_by_distance(degree - 1, 2),
            self.get_note_by_distance(degree - 1, 4),
        ]

        offset = self.mode.value
        _type = MAJOR_SCALE_CHORD_TYPES[(offset + degree - 1) % 7]
        return Chord(notes, self, degree, _type)


@dataclass
class Chord:
    notes: list[MidiNote]
    scale: Scale
    degree: int
    chord_type: ChordType

    def extend(self, degree: int, argumentation: str | None = None):
        """
        `argumentation` : Can be one of `sharp`, `flat` or None
        """

        note = self.scale.get_note_by_distance(self.degree - 1, degree - 1)
        if argumentation:
            note = note.duplicate()
            if argumentation == "flat":
                note.flatten()
            else:
                note.sharpen()

        self.notes.append(note)
        return self

    def extend_many(self, degrees: list[str]):
        """
        `degrees` : list of string containing scale degrees as follows `<b#><degree>`. e.g. : "#4", "b3" etc
        """
        _expr = re.compile(r"^([b#])?(\d{1,2})$")
        for d in degrees:
            match = re.match(_expr, d)
            if not match:
                continue

            arg = match.group(1)
            if arg:
                arg = "flat" if arg == "b" else "sharp"

            degree = int(match.group(2))
            self.extend(degree, argumentation=arg)

        return self
