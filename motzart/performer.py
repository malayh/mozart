from __future__ import annotations
from dataclasses import dataclass
import time
import mido

from motzart.primitives import MidiNote


@dataclass
class PerformedNote:
    """
    A Note tells you
        - How long it is: in ticks
        - When does it start: in ticks
    """

    note: MidiNote

    # beat at which the note starts
    starts_at: int
    # beat at which the note ends
    ends_at: int
    # percentage by which to offset start_at.
    # -100% means start the note "one beat" earier
    starts_at_offset: int = 0
    ends_at_offset: int = 0

    midi_channel: int = 3

    def __post_init__(self):
        if self.starts_at_offset > 100 or self.starts_at_offset < -100:
            raise ValueError("start_at_offset is a percentage")

        if self.ends_at_offset > 100 or self.ends_at_offset < -100:
            raise ValueError("ends_at_offset is a percentage")

        if self.midi_channel < 1 or self.midi_channel > 16:
            raise ValueError("Midi channel has to be between 1 and 16")


class Performer:
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

    def render(self, notes: list[PerformedNote]):
        for note in notes:

            # Note start message
            start_at = note.starts_at * self.ticks_per_beat
            start_at_offset = int(self.ticks_per_beat * (note.starts_at_offset / 100))
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
            ends_at_offset = int(self.ticks_per_beat * (note.ends_at_offset / 100))
            if ends_at + ends_at_offset >= 0:
                ends_at = ends_at + ends_at_offset

            end_message = mido.Message(
                "note_off", note=note.note.midi, velocity=0, channel=note.midi_channel
            )
            if ends_at in self._rendered_notes:
                self._rendered_notes[ends_at].append(end_message)
            else:
                self._rendered_notes[ends_at] = [end_message]

    def play(self):
        
        total_ticks = max(self._rendered_notes.keys()) + 1

        for i in range(0, total_ticks):
            _start = time.perf_counter()
            if i in self._rendered_notes:
                for note in self._rendered_notes[i]:
                    self.outport.send(note)
            _end = time.perf_counter()

            time.sleep(self.lenght_of_tick - (_end - _start))
