import time
import mido
from theory import Note, MidiNote, Scale, Mode, Chord

"""
- 12 tone equal temperament. Note 0 = C0, Note 12 = C1, Note 24 = C2

- Each beat is a quater note. Each beat has X number of ticks.
- Default tempto is 500_000 micro seconds per beat = 120 bpm


- 500_000 mico sec = 1 beat = 120 bpm

- 120 bpm = 500_000 mico sec
- 1 bpm = 500_000 / 120 micro sec
- X bmp = X * (500_000/120) micro sec

"""


def test_midi_file_out():
    midi_file = mido.MidiFile()
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    c_on =  mido.Message('note_on', note=48, velocity=100,time=0)
    c_off =  mido.Message('note_off', note=48, velocity=0,time=480*4)


    e_on =  mido.Message('note_on', note=51, velocity=100,time=0)
    e_off =  mido.Message('note_off', note=51, velocity=0,time=480*4)

    g_on =  mido.Message('note_on', note=55, velocity=100,time=0)
    g_off =  mido.Message('note_off', note=55, velocity=0,time=480*4)

    track.append(c_on)
    track.append(c_off)
    track.append(e_on)
    track.append(e_off)
    track.append(g_on)
    track.append(g_off)

    midi_file.save('new_song.mid')


def play_notes(notes: list[MidiNote]):
    print(notes)
    outport = mido.open_output('pyMidiPort 1')
    for note in notes:
        note_on = mido.Message('note_on', note=note.midi, velocity=100,channel=3)
        note_off = mido.Message('note_off', note=note.midi, velocity=0,channel=3)

        outport.send(note_on)
        time.sleep(0.3)

        outport.send(note_off)

    outport.close()

def play_chord(chord: Chord):
    print(chord.notes)

    outport = mido.open_output('pyMidiPort 1')
    for note in chord.notes:
       outport.send(mido.Message('note_on', note=note.midi, velocity=100,channel=3))
       time.sleep(0.1)
    
    time.sleep(2)

    for note in chord.notes:
       outport.send(mido.Message('note_off', note=note.midi, velocity=0,channel=3))

    outport.close()


def test_scale():
    
    note = Note.A.get_midi(3)

    for mode in Mode:
        scale = Scale.get_mode_scale(note, mode)
        play_notes(scale)
        
def test_chords():
    root = Note.C.get_midi(4)

    for mode in Mode:
        scale = mode.get_scale(root)
        for i in range(7):
            play_chord(scale.get_diatonic_chord(i))




    

# test_midout()
# test_midi_file_out()
# test_scale()
test_chords()