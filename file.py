import time

import pretty_midi

import ChordsFSM as chords


def print_notes():
    midi_data = pretty_midi.PrettyMIDI('song.mid')
    ptime = 0
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            key = pretty_midi.note_number_to_name(note.pitch)
            lapsed = note.start
            if lapsed - ptime > 0:
                time.sleep(lapsed - ptime)
            chords.press(key)
            ptime = lapsed


print_notes()
