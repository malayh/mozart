from __future__ import annotations

import copy
import time
from dataclasses import dataclass, field
from operator import attrgetter

import mido

import math
from mozart.primitives import MidiNote


@dataclass
class PlayedNote:
    """
    starts_at and ends_at is in beats
    """

    note: MidiNote

    # beat at which the note starts
    starts_at: int
    # beat at which the note ends
    ends_at: int
    # percentage by which to offset start_at.
    # -100% means start the note "one beat" earier
    starts_at_offset: float = 0
    ends_at_offset: float = 0

    midi_channel: int = 3

    def __post_init__(self):
        if self.starts_at_offset > 100 or self.starts_at_offset < -100:
            raise ValueError("start_at_offset is a percentage")

        if self.ends_at_offset > 100 or self.ends_at_offset < -100:
            raise ValueError("ends_at_offset is a percentage")

        if self.midi_channel < 1 or self.midi_channel > 16:
            raise ValueError("Midi channel has to be between 1 and 16")

    def copy(self) -> PlayedNote:
        return copy.deepcopy(self)

    @property
    def effective_start(self) -> float:
        return self.starts_at + (self.starts_at_offset / 100)

    @property
    def effective_end(self) -> float:
        return self.ends_at + (self.ends_at_offset / 100)


@dataclass
class Clip:
    """
    Issues
    - If ends_at is offsetted high, Clip.ends_at will not take the offset into account
    """

    _ends_at: int | None = None
    played_notes: list[PlayedNote] = field(default_factory=list)

    @property
    def starts_at(self) -> int:
        if not self.played_notes:
            return 0

        return min(self.played_notes, key=attrgetter("starts_at")).starts_at

    @property
    def ends_at(self) -> int:
        if not self.played_notes:
            return 0

        if self._ends_at:
            return self._ends_at

        return max(self.played_notes, key=attrgetter("ends_at")).ends_at

    def round_up_to_nearest_bar(self, beats_per_bar: int):
        """
        If the last note of the clip ends before the end of next bar, if you concat another clip to it, it would start right
        from where the last note was. Rounding it off makes the clip to have whole number of bars
        """
        if self.ends_at % beats_per_bar == 0:
            return

        self._ends_at = self.ends_at + (beats_per_bar - (self.ends_at % beats_per_bar))

    def concat(self, clip: Clip) -> Clip:
        ends_at = self.ends_at

        for note in clip.played_notes:
            _n = note.copy()
            _n.starts_at += ends_at
            _n.ends_at += ends_at
            self.played_notes.append(_n)

        self._ends_at = ends_at + clip.ends_at

        return self

    def cut(self, start_beat: int, end_beat: int) -> Clip:
        """
        Cuts the clip from start_beat to end_beat: [start_beat, end_beat)

        Notes can end at ends_beat, but not start at it
        """
        new_clip = Clip()

        for note in self.played_notes:

            # note ends before the start_beat or right at it
            if note.effective_end < start_beat or math.isclose(note.effective_end, start_beat):
                continue

            # note starts after the end_beat or right at it
            if note.effective_start > end_beat or math.isclose(note.effective_start, end_beat):
                continue

            _n = note.copy()

            if _n.effective_start < start_beat or math.isclose(_n.effective_start, start_beat):
                _n.starts_at = 0
                _n.starts_at_offset = 0
            else:
                start = _n.effective_start - start_beat
                start_offset = (start - int(start)) * 100
                _n.starts_at = int(start)
                _n.starts_at_offset = start_offset

            if _n.effective_end > end_beat or math.isclose(_n.effective_end, end_beat):
                _n.ends_at = end_beat - start_beat
                _n.ends_at_offset = 0
            else:
                end = _n.effective_end - start_beat
                end_offset = (end - int(end)) * 100
                _n.ends_at = int(end)
                _n.ends_at_offset = end_offset

            if math.isclose(_n.effective_start, _n.effective_end, abs_tol=0.01):
                continue

            new_clip.played_notes.append(_n)

        return new_clip


class Player:
    ticks_per_beat: int = 16
    bpm: int = 80
    lenght_of_tick = -1

    outport = None

    _rendered_notes: dict[int, list[mido.Message]] = {}

    def __init__(self, bpm: int = 80) -> None:
        self.bpm = bpm

        # 80 beats in 60 sec
        # 1 beat in 60/80 sec
        # 100 tick in 60/80 sec
        # 1 tick in 60/(80*100) sec
        self.lenght_of_tick = 60 / (self.bpm * self.ticks_per_beat)

        self.outport = mido.open_output("pyMidiPort 1")

    def __del__(self):
        if self.outport:
            self.outport.close()

    def render(self, notes: list[PlayedNote]):
        for note in notes:

            # Note start message
            start_at = note.starts_at * self.ticks_per_beat
            start_at_offset = round(self.ticks_per_beat * (note.starts_at_offset / 100))
            if start_at + start_at_offset >= 0:
                start_at = start_at + start_at_offset

            start_message = mido.Message(
                "note_on",
                note=note.note.midi,
                velocity=note.note.velocity,
                channel=note.midi_channel,
            )
            if start_at in self._rendered_notes:
                self._rendered_notes[start_at].append(start_message)
            else:
                self._rendered_notes[start_at] = [start_message]

            # note end message
            ends_at = note.ends_at * self.ticks_per_beat
            ends_at_offset = round(self.ticks_per_beat * (note.ends_at_offset / 100))
            if ends_at + ends_at_offset >= 0:
                ends_at = ends_at + ends_at_offset

            end_message = mido.Message("note_off", note=note.note.midi, velocity=0, channel=note.midi_channel)
            if ends_at in self._rendered_notes:
                self._rendered_notes[ends_at].append(end_message)
            else:
                self._rendered_notes[ends_at] = [end_message]

    def play(self):

        if not self._rendered_notes:
            return

        total_ticks = max(self._rendered_notes.keys()) + 1

        for i in range(0, total_ticks):
            _start = time.perf_counter()
            if i in self._rendered_notes:
                for note in self._rendered_notes[i]:
                    self.outport.send(note)
            _end = time.perf_counter()

            time.sleep(self.lenght_of_tick - (_end - _start))
