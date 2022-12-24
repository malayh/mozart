from __future__ import annotations

import script_include  # noqa F401

from mozart.bass import BassArticulator
from mozart.harmony import ChordProgressionGenerator
from mozart.midifile import parse_midfile
from mozart.piano import PianoChordArticulator
from mozart.player import Clip, Player, Track
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


def try_track():
    path = r"midi_clips\drums\fpc_affection_lofi.mid"

    drum_clip = parse_midfile(path).clip
    drum_clip.round_up_to_nearest_bar(4)

    drum_track = Track(midi_channel=3)
    drum_track.append(drum_clip)

    chord_clip = generate_chord_progession()
    chord_track = Track(midi_channel=0)
    chord_track.put(chord_clip, 4)

    player = Player(bpm=100)
    player.render(drum_track.render())
    player.render(chord_track.render())
    player.play()


def trY_track_with_bass():

    path = r"midi_clips\drums\fpc_affection_lofi.mid"
    drum_clip = parse_midfile(path).clip
    drum_clip.round_up_to_nearest_bar(4)
    drum_track = Track(midi_channel=1)
    drum_track.append(drum_clip)

    generator = ChordProgressionGenerator(Note.C, Mode.mixolydian, lenght=4, octave=4)
    progression = generator.generate_v2(resolution_strenght=5)

    chord_track = Track(midi_channel=0)
    bass_track = Track(midi_channel=2)

    chord_art = PianoChordArticulator(time_signature=TimeSignature(8, 4), intensity=3)
    bass_art = BassArticulator(time_signature=TimeSignature(8, 4), intensity=3)
    for chord in progression.chords:
        chord.extend_many(["9"])
        chord_track.append(chord_art.articulate_quick_arp(chord, sloppyness=0))
        bass_track.append(bass_art.articulate_root(chord))

    # print(bass_track.clips)
    player = Player(bpm=140)
    player.render(drum_track.render())
    player.render(chord_track.render())
    player.render(bass_track.render())
    player.play()


trY_track_with_bass()

# try_track()
