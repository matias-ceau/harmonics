import numpy as np
from ..data.general import DEF_OCTAVE
from ..data.notes import NDICT
from ..midi.utils import MidiUtils

class Pitch:

    @classmethod
    def freq2pitch(cls, freq): return round(np.log2(freq/440)*12+69)
    @classmethod
    def pitch2freq(cls, pitch): return 440*np.power(2, (pitch-69)/12)

    def __init__(self, n):
        if type(n) in [int, float]:
            self.midi = n
        elif type(n) == str:
            if n[-1] == 'z':
                self.frequency = float(n[:-2])
                self.midi = Pitch.freq2pitch(self.frequency)
            else:
                if n[-1].isnumeric():
                    self.octave = int(n[-1])
                    self.name = n[:-1]
                else:
                    self.name = n
                    self.octave = DEF_OCTAVE
                self.midi = NDICT[self.name] + (self.octave+1)*12
        else:
            print('wut?')
        if 'name' not in self.__dict__:
            self.name = MidiUtils.midi_to_note(self.midi)
        if 'octave' not in self.__dict__:
            self.octave = MidiUtils.midi_octave(self.midi)
        # computed
        self.equivalents = [
            a for a, b in NDICT.items() if self.midi % 12 == b]
        self.pitch_class = NDICT[self.name]
        if 'frequency' not in self.__dict__:
            self.frequency = Pitch.pitch2freq(self.midi)
        self.offpitch\
            = f'{1200*np.log2(self.frequency/Pitch.pitch2freq(self.midi))}\
                cents'

    def __repr__(self): return self.name
