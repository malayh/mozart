import script_include  # noqa F401

from motzart.harmony import ChordCategory, ChordProgressionGenerator
from motzart.piano import PianoChordArticulator
from motzart.player import Player
from motzart.primitives import Mode, Note, TimeSignature


def dummy_play_progession():
    # random.seed(100)

    generator = ChordProgressionGenerator(Note.C, Mode.lydian, lenght=4, octave=4)
    progression = generator.generate_v2(resolution_strenght=5, start_with=ChordCategory.TONIC)
    player = Player(bpm=120)
    art = PianoChordArticulator(time_signature=TimeSignature(4, 4), intensity=2)

    for i in range(len(progression.chords)):
        # if i == 1:
        #     break
        chord = progression.chords[i]
        chord.extend_many(["7", "9"])
        notes = art.articulate_arp_with_bass(i, chord, sloppyness=0)
        player.render(notes)

    player.play()


dummy_play_progession()
