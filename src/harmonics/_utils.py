import os
import yaml
import numpy as np
import time


def timer(string, t):
    print(f"{string} took {time.time() - t} seconds")
    return time.time()


class Harmonics:
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    DEFINITIONS_PATH = os.path.join(ROOT_DIR, 'harmonics', 'definitions.yaml')
    with open(DEFINITIONS_PATH, "r") as f:
        DEF = yaml.safe_load(f)
    IDICT: dict = {k: v for k, v in zip(DEF['INAMES'], DEF['IDIST'])}
    EDICT: dict = {k: v for k, v in zip(DEF['INAMES'], DEF['EXTENSION'])}
    NDICT: dict = {k: v for k, v in zip(DEF['NOTES'], DEF['NDIST'])}
    INAMES: dict = DEF['INAMES']
    INTERVALS: dict = DEF['INTERVALS']
    SCALES: dict = DEF['SCALES']
    CHORDS: dict = DEF['CHORDS']
    PATTERNS: dict = DEF['PATTERNS']
    FORMULAS = {**SCALES, **CHORDS, **PATTERNS}
    TUNING: dict = DEF['TUNING']
    INSTRUMENTS: dict = DEF["INSTRUMENTS"]
    MIDI_CHANNELS: dict = DEF['MIDI_CHANNELS']
    MIDI_GM1: dict = DEF['MIDI_GM1']
    MIDI_GM2: dict = DEF['MIDI_GM2']
    MIDI_CC: dict = DEF['MIDI_CC']
    DRUM_PROG: dict = DEF['DRUM_PROG']
    DRUM_KEYMAP: dict = DEF['DRUM_KEYMAP']
    DEF_OCTAVE = 4
    DEFAULT_KEY = 'C'
    MIDIMESSAGE = DEF['MIDIMESSAGE']

    @classmethod
    def _list(cls, thing):
        if type(thing) in (tuple, list, np.ndarray):
            return thing
        if type(thing) in (str, float, str):
            return [thing]
