from __future__ import annotations

import script_include  # noqa F401

from mozart.harmony import ChordProgressionGenerator
from mozart.midifile import parse_midfile
from mozart.piano import PianoChordArticulator
from mozart.player import Clip, Player
from mozart.primitives import Mode, Note, TimeSignature


def generate_chord_progession() -> Clip:
    generator = ChordProgressionGenerator(Note.C, Mode.ionian, lenght=4, octave=4)
    progression = generator.generate_v2(resolution_strenght=5)

    for c in progression.chords:
        print(c.chord_type, c.degree, c.notes)

    clip = Clip()
    art = PianoChordArticulator(time_signature=TimeSignature(8, 4), intensity=3)
    for i in range(len(progression.chords)):
        chord = progression.chords[i]
        chord.extend_many(["9"])
        clip.concat(art.articulate_quick_arp(chord, sloppyness=0))

    for n in clip.played_notes:
        n.midi_channel = 0

    return clip


def try_midi_file_read_with_chords():
    path = r"midi_clips\drums\fpc_affection_lofi.mid"

    midi_clip = parse_midfile(path)
    midi_clip.clip.round_up_to_nearest_bar(4)

    chord_clip = generate_chord_progession()

    player = Player(bpm=120)
    player.render(midi_clip.clip.played_notes)
    player.render(chord_clip.played_notes)

    player.play()


def try_midi_file_read():
    path = r"tests\test_files\test_midi.mid"

    midi_clip = parse_midfile(path)
    for n in midi_clip.clip.played_notes:
        n.midi_channel = 0

    player = Player(bpm=120)
    player.render(midi_clip.clip.played_notes)

    player.play()


try_midi_file_read_with_chords()
# try_midi_file_read()
