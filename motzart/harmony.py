from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import random

from motzart.primitives import ChordType, Chord, Scale, Note, Mode


class ChordCategory(Enum):
    # Name : list of scale degrees
    TONIC = [1, 3]
    SUB_DOMINENT = [2, 4, 6]
    DOMINENT = [5, 7]

    @staticmethod
    def get_category(degree: int) -> ChordCategory:
        for category in ChordCategory:
            if degree % 8 in category.value:
                return category


@dataclass
class Resolution:
    """
    Encodes how chords of a diatonic scale resolves
    """

    # How strong the resoltion is. One of (0,1,2,3,4), 1 being weakest and 4 being strongest
    strenght: int

    # Which scale degrees to start from
    starts_from: list[int]

    # Which scale degrees to resolve to
    resolves_to: list[int]


class Cadence:
    AUTHENTIC = Resolution(5, [5], [1])
    PLAGAL = Resolution(4, [4], [1])
    HALF = Resolution(2, [1, 2, 3, 4, 5, 6, 7], [5])
    DECEPTIVE = Resolution(
        1, ChordCategory.DOMINENT.value, ChordCategory.SUB_DOMINENT.value
    )
    # MINOR_PLAGAL : TODO : Cannot encode this, because can't mention `minor 4th` as start from

    # Not a cadence
    TONIC_TO_OTHER = Resolution(
        0,
        ChordCategory.TONIC.value,
        [*ChordCategory.DOMINENT.value, *ChordCategory.SUB_DOMINENT.value],
    )
    # Not a cadence
    SUB_TO_SUB = Resolution(
        0,
        ChordCategory.SUB_DOMINENT.value,
        ChordCategory.SUB_DOMINENT.value,
    )

    # Not a cadence
    SUB_TO_DOM = Resolution(
        1,
        ChordCategory.SUB_DOMINENT.value,
        ChordCategory.DOMINENT.value,
    )

    all_cadences: list[Resolution] = [
        AUTHENTIC,
        PLAGAL,
        HALF,
        DECEPTIVE,
        TONIC_TO_OTHER,
        SUB_TO_SUB,
        SUB_TO_DOM,
    ]

    @staticmethod
    def resolve(chord: Chord, strength: int) -> int:
        choices = [
            i
            for i in Cadence.all_cadences
            if i.strenght == strength and chord.degree in i.starts_from
        ]

        if not choices:
            return -1

        cadence: Resolution = random.choice(choices)
        return random.choice(cadence.resolves_to)

    @staticmethod
    def reverse_resolve(chord, strength: int) -> int:
        choices = [
            i
            for i in Cadence.all_cadences
            if i.strenght == strength and chord.degree in i.resolves_to
        ]
        if not choices:
            return -1

        cadence: Resolution = random.choice(choices)
        return random.choice(cadence.starts_from)


@dataclass
class ChordProgression:
    key: Note
    mode: Mode
    chords: list[Chord]


class ChordProgressionGenerator:
    key: Note
    octave: int = 4
    scale: Scale
    mode: Mode

    lenght = 4
    chords: list[Chord] = []

    def __init__(self, key: Note, mode: Mode, octave: int = 4, lenght: int = 4) -> None:
        self.key = key
        self.mode = mode
        self.octave = octave
        self.scale = self.mode.get_scale(self.key.get_midi(self.octave))
        self.lenght = lenght

    def chooce_final_chords(self) -> tuple[Chord, Chord]:
        cadence = random.choice([Cadence.AUTHENTIC, Cadence.PLAGAL])
        if self.lenght >= 6:
            cadence = Cadence.AUTHENTIC

        final = self.scale.get_diatonic_triad(1)

        _rr = Cadence.reverse_resolve(final, cadence.strenght)
        pre_final = self.scale.get_diatonic_triad(_rr)

        return pre_final, final

    def spice_up(self, progession: ChordProgression) -> ChordProgression:
        spice = ["6", "9", "11"]

        add_7th = random.random() < 0.6
        if add_7th:
            for chord in progession.chords:
                if random.random() < 0.9:
                    chord.extend(7)

        #  20% chance of adding abit more spice to the chord
        add_more_spice = random.random() < 0.2
        if add_more_spice:
            for chord in progession.chords:
                if random.random() < 0.9:
                    chord.extend_many(random.choices(spice, k=1))

        return progession

    def generate(self) -> ChordProgression:
        """
        - v1 feats
            - always resolves to tonic
            - always starts with tonic
            - randomize adding 7ths
            - randomize adding other extensions
            - randomize replacing diminished
        """

        pre_final, final = self.chooce_final_chords()

        chords = [None] * (self.lenght - 2)
        chords.extend([pre_final, final])

        chords[0] = self.scale.get_diatonic_triad(1)

        for i in range(1, self.lenght - 2):
            chords[i] = self.scale.get_diatonic_triad(
                random.choice([1, 2, 3, 4, 5, 6, 7])
            )

            # If currently selected chord is dimiished, then there is 50% chance that it would be tried to be replaced 3 times
            if chords[i].chord_type == ChordType.diminished and random.random() < 0.5:
                for _ in range(2):
                    chords[i] = self.scale.get_diatonic_triad(
                        random.choice([1, 2, 3, 4, 5, 6, 7])
                    )
                    if chords[i].chord_type != ChordType.diminished:
                        break

            # Try 3 times to get a different chord than the previous one
            if i > 0 and chords[i] == chords[i - 1]:
                for _ in range(3):
                    chords[i] = self.scale.get_diatonic_triad(
                        random.choice([1, 2, 3, 4, 5, 6, 7])
                    )
                    if chords[i] != chords[i - 1]:
                        break

        progession = ChordProgression(self.key, self.mode, chords)
        return self.spice_up(progession)
