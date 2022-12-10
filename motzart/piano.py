from __future__ import annotations

import random

from motzart.player import PlayedNote
from motzart.primitives import Chord, MidiNote, TimeSignature


class PianoChordArticulator:
    time_signature: TimeSignature
    intensity: int

    def __init__(self, time_signature: TimeSignature, intensity: int) -> None:
        self.time_signature = time_signature
        self.intensity = intensity

        if self.intensity < 1 or self.intensity > 5:
            raise ValueError("intensity needs to be between 1-5")

    def intensify(self, notes: list[MidiNote]) -> list[MidiNote]:
        """
        Randomizes velocities based on intensity
        """

        _notes = []
        max_velocity = self.intensity * 25

        for note in notes:
            _n = note.copy()
            _n.velocity = random.randint(max_velocity - 20, max_velocity)
            _notes.append(_n)

        return _notes

    def arpegiate(self, beat_offset: int, notes: list[MidiNote], sustain_notes_at: list[int] = []) -> list[PlayedNote]:
        """
        sustains notes at indexes `sustain_notes_at` a little bit more
        """
        played_notes = []

        for i, note in enumerate(notes):

            ends_at = (
                beat_offset + random.randint(2, self.time_signature.numerator)
                if i in sustain_notes_at
                else beat_offset + 1
            )

            played_notes.append(
                PlayedNote(
                    note=note,
                    starts_at=beat_offset,
                    ends_at=ends_at,
                    starts_at_offset=i * random.randint(10, 20),
                )
            )

        return played_notes

    def articulate_slow_arp_with_bass(self, bar: int, chord: Chord, sloppyness: int = 0) -> list[PlayedNote]:
        """
        Arpiggiating chord articulator

        count of `bar` start from 0
        """

        # v1 cannout articulate chrods shorted than 3 notes
        if len(chord.notes) < 3:
            return []

        beat_offset = bar * self.time_signature.numerator

        # randomize velocity
        notes: list[MidiNote] = self.intensify(chord.notes)

        played_notes = []
        for beat in range(0, self.time_signature.numerator):
            absolute_beat = beat + beat_offset
            slopy_offset = random.randint(0, sloppyness)

            # play 1 and the 5  of the chord on beat 1, with a lowerd ocatave left hand
            if beat == 0:
                _1, _5 = notes[0].copy(), notes[2].copy()
                _1.octave -= 1
                _5.octave -= 1

                played_notes.append(
                    PlayedNote(
                        note=_1,
                        starts_at=absolute_beat,
                        ends_at=absolute_beat + self.time_signature.numerator,
                    )
                )

                played_notes.append(
                    PlayedNote(
                        note=_5,
                        starts_at=absolute_beat,
                        starts_at_offset=slopy_offset,
                        ends_at=absolute_beat + self.time_signature.numerator,  # notes lasts the duration of the bar
                    )
                )

            else:
                played_notes.append(
                    PlayedNote(
                        note=notes[beat % len(notes)],
                        starts_at=absolute_beat,
                        starts_at_offset=slopy_offset,
                        ends_at=absolute_beat + 1,
                    )
                )

        return played_notes

    def articulate_quick_arp(self, bar: int, chord: Chord, sloppyness: int = 0) -> list[PlayedNote]:
        # v1 cannout articulate chrods shorted than 3 notes
        if len(chord.notes) < 3:
            return []

        beat_offset = bar * self.time_signature.numerator

        # randomize velocity
        notes: list[MidiNote] = self.intensify(chord.notes)

        # sustain 1st, and 5th scale degrees
        sustain_notes = set([0, 2])

        played_notes = self.arpegiate(beat_offset, notes, sustain_notes_at=sustain_notes)

        return played_notes

    def articulate_arp_with_bass(self, bar: int, chord: Chord, sloppyness: int = 0) -> list[PlayedNote]:
        # v1 cannout articulate chrods shorted than 3 notes
        if len(chord.notes) < 3:
            return []

        beat_offset = bar * self.time_signature.numerator

        # randomize velocity
        notes: list[MidiNote] = self.intensify(chord.notes)

        played_notes = []

        lower_octave = set([0, 2])  # 1st and 5th
        sustain_notes = set([3, 4])  # sustain 7th and 9th

        for i, note in enumerate(notes):
            if i in lower_octave:
                _n = note.copy()
                _n.octave -= 1
                played_notes.append(
                    PlayedNote(
                        note=_n,
                        starts_at=beat_offset,
                        ends_at=beat_offset + random.randint(1, 2),
                    )
                )

                continue

        remaining_notes = [note for i, note in enumerate(notes) if i not in lower_octave]
        played_notes.extend(self.arpegiate(beat_offset + 1, remaining_notes, sustain_notes_at=sustain_notes))

        return played_notes
