from __future__ import annotations

from dataclasses import dataclass

from mido import Message, MetaMessage, MidiFile, merge_tracks, tempo2bpm

import math
from mozart.player import Clip, PlayedNote
from mozart.primitives import Note, TimeSignature


@dataclass
class MidiClip:
    clip: Clip
    bpm: int
    time_signature: TimeSignature
    name: str = ""


def print_midi_file_tracks(mid: MidiFile):
    for i, track in enumerate(mid.tracks):
        print("Track {}: {}".format(i, track.name))
        for msg in track:
            print(f"\t{msg}")
        print()


def parse_meta(mid: MidiFile) -> tuple[int, int, TimeSignature]:
    """
    Return (bpm,clocks_per_click,TimeSignature)
    """

    bpm = 0
    time_sig = None
    clocks_per_click = 0

    for msg in merge_tracks(mid.tracks):
        if msg.type == "set_tempo":
            bpm = math.ceil(tempo2bpm(msg.tempo))
            continue

        if msg.type == "time_signature":
            time_sig = TimeSignature(msg.numerator, msg.denominator)
            clocks_per_click = msg.clocks_per_click

    return bpm, clocks_per_click, time_sig


def make_played_note(note_value: int, velocity: int, starts_at: int, lenght: int, ticks_per_beat: int) -> PlayedNote:
    note = Note(note_value % 12).get_midi(note_value // 12)

    end_tick = starts_at + lenght

    start_beat = starts_at // ticks_per_beat
    start_offset = (starts_at % ticks_per_beat) / ticks_per_beat * 100

    end_beat = end_tick // ticks_per_beat
    end_offset = (end_tick % ticks_per_beat) / ticks_per_beat * 100

    return PlayedNote(
        note=note, starts_at=start_beat, starts_at_offset=start_offset, ends_at=end_beat, ends_at_offset=end_offset
    )


def parse_midfile(filepath: str) -> MidiClip:
    """

    Note: If the last note of the track ends at the middle of the bar, the _ends_at won't be set to round off the bar
    """

    mid = MidiFile(filepath)
    bpm, clocks_per_click, time_sig = parse_meta(mid)

    played_notes = []

    # note : (msg,start_at)
    note_stack: dict[int, tuple[Message, int]] = {}

    total_time_passed = 0

    for msg in merge_tracks(mid.tracks):

        if isinstance(msg, MetaMessage) or msg.type not in ("note_on", "note_off"):
            continue

        total_time_passed += msg.time

        if msg.note not in note_stack:
            note_stack[msg.note] = (msg, total_time_passed)
            continue

        # encountered two note_on for the same midi value, while expecting a note_off
        if msg.type == "note_on":
            raise ValueError("Encountered two note_on for the same midi value, while expecting a note_off")

        start_msg, start_at = note_stack.pop(msg.note)
        length = total_time_passed - start_at

        # IDK why 4, but seems like it
        # ticks_per_beat = 4 * clocks_per_click

        # Skipping the above calculation and hardcoding it to 96
        ticks_per_beat = 96

        played_notes.append(make_played_note(start_msg.note, start_msg.velocity, start_at, length, ticks_per_beat))

    return MidiClip(clip=Clip(played_notes=played_notes), bpm=bpm, time_signature=time_sig)
