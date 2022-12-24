from __future__ import annotations

import random

from mozart.player import Clip, PlayedNote
from mozart.primitives import Chord, MidiNote, TimeSignature


class BassArticulator:
    """
    Returns 1 bar long clip of articulated chord
    """

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

    def articulate_root(self, chord: Chord) -> Clip:
        """
        Articulates root note of chord
        """
        root = self.intensify([chord.notes[0]])[0]
        return Clip(played_notes=[PlayedNote(root, 0, self.time_signature.numerator)])
