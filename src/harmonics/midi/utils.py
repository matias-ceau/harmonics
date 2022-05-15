import numpy as np

from ..data.midi import MIDI_CC, DRUM_PROG, MIDI_GM1, DRUM_KEYMAP, MIDIMESSAGE
from ..data.notes import NDICT

class MidiUtils:

    @classmethod
    def quantitize(cls, n):
        bins = np.array([0, 0.125, 0.29, 0.4, 0.58, 0.7, 0.875])
        vals = np.array([0, 0.25,  0.33, 0.5, 0.66, 0.75, 0])
        return vals[np.digitize(n, bins)-1]

    @classmethod
    def midi_cc(cls, data1):
        return MIDI_CC.get(data1)

    @classmethod
    def midi_program(cls, channel, data1):
        if channel == 9:
            return DRUM_PROG.get(data1)
        else:
            return MIDI_GM1.get(data1)

    @classmethod
    def midi_drum(cls, midi):
        return DRUM_KEYMAP.get(midi)

    @classmethod
    def midi_to_note(cls, midi):
        return [a for a, b in NDICT.items() if midi % 12 == b][0]

    @classmethod
    def midi_octave(cls, midi):
        return (midi//12)-1

    @classmethod
    def midi_to_name(cls, midi):
        return ''.join([cls.midi_to_note(midi), str(cls.midi_octave(midi))])
