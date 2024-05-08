import contextlib
import time

from pretty_midi import note_number_to_name
import pygame.midi
import ChordsFSM as chords


def get_piano():
    pygame.midi.init()
    for n in range(pygame.midi.get_count()):
        with contextlib.suppress(Exception):
            return pygame.midi.Input(n)


def get_keys(device):
    while True:
        if device.poll():
            key = device.read(1)[0][0]
            if key != [248, 0, 0, 0] and key[1] != 0 and key[2] != 0:
                key = note_number_to_name(key[1])
                # print(key, time.time())
                chords.press(key)


if not (piano := get_piano()):
    print("No MIDI devices found")
else:
    get_keys(piano)
