from __future__ import annotations

import random
from dataclasses import dataclass

from motzart.player import PlayedNote
from motzart.primitives import Chord, MidiNote, TimeSignature


@dataclass
class PianoChordArticulator:
    time_signature: TimeSignature
    intensity: int

    def __post_init__(self):
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

    def articulate(
        self, bar: int, chord: Chord, sloppyness: int = 0
    ) -> list[PlayedNote]:
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
                        ends_at=absolute_beat + self.time_signature.numerator - 1,
                    )
                )

                played_notes.append(
                    PlayedNote(
                        note=_5,
                        starts_at=absolute_beat,
                        starts_at_offset=slopy_offset,
                        ends_at=absolute_beat
                        + self.time_signature.numerator
                        - 1,  # notes lasts the duration of the bar
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
