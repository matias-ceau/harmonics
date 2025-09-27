import pandas as pd
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from .functions import get_sine, get_enveloppe, get_harmonics
from .plot import audio_plot

class Sampler:
    """Generates sound waves,
    can base harmonics and enveloppe on extracted sample."""

    def __init__(self,
                 frequency=440,
                 sample_rate=44100,
                 amplitude=4096,
                 file=None):
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.file = file
        self._analyzed = {'file': [],
                          'data': [],
                          'rel_harmonics': [],
                          'note': [], 'offpitch': [],
                          'enveloppe': [],
                          'frequency': [],
                          'duration': []}
        self._harmonics = False
        self._enveloppe = False

    @property
    def df(self):
        return pd.DataFrame({k: pd.Series(v)
                             for k, v in self._analyzed.items()})

    @property
    def harmonics(self):
        return self._harmonics

    @harmonics.setter
    def harmonics(self, i):
        if type(i) == int:
            self._harmonics = self.df.loc[i, 'rel_harmonics']
        elif not i:
            self._harmonics = False

    @property
    def enveloppe(self):
        return self._enveloppe

    @enveloppe.setter
    def enveloppe(self, i):
        if type(i) == int:
            self._enveloppe = self.df.loc[i, 'enveloppe']
        elif not i:
            self._enveloppe = False

    def get_wave(self, duration,
                 freq=None,
                 plot=True,
                 wav=True,
                 harmonics='def',
                 enveloppe='def',
                 env_stretch=False,
                 filename='name.wav',
                 autodecay=20,
                 show='all',
                 s=44100):
        if freq:
            self.frequency = freq
        if harmonics == 'def':
            harmonics = self.harmonics
        if enveloppe == 'def':
            enveloppe = self.enveloppe
        if type(harmonics) == int:
            self.harmonics = harmonics
            harmonics = self.harmonics
        if type(enveloppe) == int:
            self.enveloppe = enveloppe
            enveloppe = self.enveloppe
        if not harmonics:
            wave = get_sine(duration, self.frequency,
                            self.amplitude, sample_rate=s)
        else:
            print('added harmonics')
            wave = np.sum(
                [get_sine(duration, A=self.amplitude, F=self.frequency,
                          aR=a, fR=f, phase=p, sample_rate=s, plot=False)
                 for f, a, p in harmonics],
                axis=0)

        if type(enveloppe) == np.ndarray:
            t = np.arange(0, len(wave))
            if env_stretch:
                scaled_env = np.interp(
                    t, enveloppe[1, :]*len(wave), enveloppe[2, :])
            else:
                scaled_env = np.interp(t, enveloppe[0, :]*s, enveloppe[2, :])
                plt.plot(scaled_env[:int(s*0.02)-100])
                if autodecay:
                    idx = int(s*autodecay/1000)
                    scaled_env = np.concatenate((
                        scaled_env[:-idx], np.linspace(
                                          scaled_env[-idx], 0, idx)
                        ))
                plt.plot(scaled_env[:int(s*0.02)-100])
            wave *= scaled_env
        if plot:
            audio_plot(np.arange(len(wave))/self.sample_rate,
                       wave, 'time', 'amplitude', show=show)

        if wav:
            wavfile.write(filename, rate=self.sample_rate,
                          data=wave.astype(np.int16))
        return wave

    def extract(self,
                filepath,
                plot=True,
                dist=10,
                cutoff=0.01,
                figsize=(10, 4)):
        sample_rate, data = wavfile.read(filepath)
        i, j = 0, 0
        while j < 0.01*data.max():
            j = data[i]
            i += 1
        data = data[i:]
        duration = len(data)/sample_rate
        self._analyzed['file'].append(filepath)
        if plot:
            audio_plot(np.linspace(0, duration, len(data)), data,
                       'Time', 'Amplitude', filepath, figsize=figsize)
        relh, note = get_harmonics(sample_rate, data, plot=plot)
        self._analyzed['duration'].append(duration)
        self._analyzed['data'].append((sample_rate, data))
        self._analyzed['rel_harmonics'].append(relh)
        self._analyzed['note'].append(note)
        self._analyzed['offpitch'].append(note.pitch.offpitch)
        self._analyzed['frequency'].append(note.pitch.frequency)
        self._analyzed['enveloppe'].append(
            get_enveloppe(sample_rate, data, plot=plot))
