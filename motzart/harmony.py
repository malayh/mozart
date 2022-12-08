from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from motzart.primitives import Chord, Mode, Note, Scale


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
    # TODO: MINOR_PLAGAL : Cannot encode this, because can't mention `minor 4th` as start from

    AUTHENTIC = Resolution(5, [5], [1])
    PLAGAL = Resolution(4, [4], [1])
    HALF = Resolution(2, [1, 2, 3, 4, 5, 6, 7], [5])
    DECEPTIVE = Resolution(1, ChordCategory.DOMINENT.value, ChordCategory.SUB_DOMINENT.value)

    # Not a cadence
    SUB_TO_DOM = Resolution(
        0,
        ChordCategory.SUB_DOMINENT.value,
        ChordCategory.DOMINENT.value,
    )

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
        choices = [i for i in Cadence.all_cadences if i.strenght == strength and chord.degree in i.starts_from]

        if not choices:
            return -1

        cadence: Resolution = random.choice(choices)
        return random.choice(cadence.resolves_to)

    @staticmethod
    def reverse_resolve(chord, strength: int) -> int:
        choices = [i for i in Cadence.all_cadences if i.strenght == strength and chord.degree in i.resolves_to]
        if not choices:
            return -1

        cadence: Resolution = random.choice(choices)
        return random.choice(cadence.starts_from)


@dataclass
class ChordProgression:
    key: Note
    chords: list[Chord]

    def add_spice(self, level: int = 1):
        spice = ["7"]
        if level == 2:
            spice.append("9")

        if level == 3:
            spice.append("11")

        if level > 3:
            spice.append("13")

        for chord in self.chords:
            chord.extend_many(spice)


class ChordProgressionGenerator:
    key: Note
    octave: int = 4
    scale: Scale
    mode: Mode
    lenght: int = 4

    def __init__(self, key: Note, mode: Mode, octave: int = 4, lenght: int = 4) -> None:
        self.key = key
        self.mode = mode
        self.octave = octave
        self.scale = self.mode.get_scale(self.key.get_midi(self.octave))
        self.lenght = lenght + (lenght % 2)

    def generate(self) -> ChordProgression:
        return self.generate_v2()

    def _resolve_forward(self, chord: Chord, strenght_choices: list[int]) -> Chord:
        strength = random.choice(strenght_choices)
        degree = Cadence.resolve(chord, strength)
        while degree == -1:
            strength = random.choice(strenght_choices)
            degree = Cadence.resolve(chord, strength)

        if degree == -1:
            raise ValueError("Can not resolve chord")

        return self.scale.get_diatonic_triad(degree)

    def generate_v2(
        self,
        start_with: ChordCategory = ChordCategory.TONIC,
        resolution_strenght: int = 5,
    ):
        """
        - v2 feats
            - minimum lenght of 2
            - renders 2 chord at a time, each pair resolves to some extent
            - * NOT doing this *: Progressions does not have to start or end at tonic
            - Progressions can end at 5th if there is a follow up section in the code
        """

        final_cadence = Cadence.AUTHENTIC
        if resolution_strenght == 4:
            final_cadence = Cadence.PLAGAL
        elif resolution_strenght == 2:
            final_cadence = Cadence.HALF
        elif resolution_strenght == 1:
            final_cadence = Cadence.DECEPTIVE

        chords: list[Chord] = [self.scale.get_diatonic_triad(random.choice([*start_with.value]))]
        strenght_choices = [0, 1, 2]

        for i in range(1, self.lenght - 2):
            chord = self._resolve_forward(chords[i - 1], strenght_choices)

            while chord == chords[i - 1]:
                chord = self._resolve_forward(chords[i - 1], strenght_choices)

            chords.append(chord)

        chords.append(self.scale.get_diatonic_triad(random.choice(final_cadence.starts_from)))
        chords.append(self.scale.get_diatonic_triad(random.choice(final_cadence.resolves_to)))

        return ChordProgression(self.key, chords)
