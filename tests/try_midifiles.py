from __future__ import annotations

import script_include  # noqa F401

from motzart.harmony import ChordCategory, ChordProgressionGenerator
from motzart.midifile import parse_midfile
from motzart.piano import PianoChordArticulator
from motzart.player import Clip, Player
from motzart.primitives import Mode, Note, TimeSignature


def generate_chord_progession() -> Clip:
    generator = ChordProgressionGenerator(Note.E, Mode.ionian, lenght=4, octave=4)
    progression = generator.generate_v2(resolution_strenght=5, start_with=ChordCategory.TONIC)

    clip = Clip()
    art = PianoChordArticulator(time_signature=TimeSignature(8, 4), intensity=3)
    for i in range(len(progression.chords)):
        chord = progression.chords[i]
        chord.extend_many(["9", "13"])
        clip.concat(art.articulate_arp_with_bass(chord, sloppyness=0))

    for n in clip.played_notes:
        n.midi_channel = 2

    return clip


def try_midi_file_read():
    path = r"midi_clips\drums\fpc_affection_lofi.mid"

    midi_clip = parse_midfile(path)
    midi_clip.clip.round_up_to_nearest_bar(4)

    chord_clip = generate_chord_progession()

    player = Player(bpm=120)
    player.render(midi_clip.clip.played_notes)
    player.render(chord_clip.played_notes)

    player.play()


try_midi_file_read()
