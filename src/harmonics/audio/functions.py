import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from ..symbols import Note
from .plot import audio_plot


def get_enveloppe(s, data, length=0.02, plot=True):
    x = np.array([i for i in range(0, len(data), int(0.02*s))])
    y = np.array([0]+[np.max(data[x[i]:x[i+1]]) for i in range(len(x)-1)])
    x1 = x/s
    x2 = x/x.max()
    y = y/y.max()
    if plot:
        audio_plot(x1, y, 'time', 'amplitude')
    return np.vstack((x1, x2, y))


def get_sine(duration,
             F,
             A=4096,
             aR=1,
             fR=1,
             phase=0,
             sample_rate=44100,
             plot=True):
    t = np.arange(duration*int(sample_rate))  # Time axis
    wave = aR*A*np.sin(2*np.pi*(fR*F/sample_rate)*t-phase)
    if plot:
        audio_plot(np.arange(0, len(wave)), wave, 'time (s)', 'amplitude')
    return wave


def get_harmonics(s, data, plot=True):
    t = np.arange(data.shape[0])
    freq = np.fft.rfftfreq(t.shape[-1])*s
    sp = np.fft.rfft(data)
    amplitude = np.abs(sp)
    phase = np.angle(sp)
    df = pd.DataFrame(np.vstack((freq, amplitude, phase)).T,
                      columns=['frequency', 'amplitude', 'phase'])
    max_freq = df[df.amplitude == df.amplitude.max()].frequency
    a, _ = find_peaks(df.amplitude,
                      threshold=df.amplitude.max()*0.01,
                      distance=int(max_freq/900*100))
    f = df.loc[a, :]
    f.sort_values('frequency', inplace=True)
    harmonics = [(round(a, 3), round(b, 3), round(c, 3))
                 for a, b, c in zip(f.frequency,
                                    f.amplitude,
                                    f.phase)]
    fundamental = f[f.amplitude ==
                    f.amplitude.max()].frequency.to_numpy().max()
    rel_h = [(round(a/fundamental, 3),
              round(b/f.amplitude.max(), 3),
              round(c, 3)) for a, b, c in harmonics]
    note = Note(str(fundamental)+'Hz')
    if plot:
        freq = freq[freq < 10*fundamental]
        ampl = amplitude[:len(freq)]
        audio_plot(freq, ampl, 'Frequency (Hz)', 'Amplitude', scatter=(
            [a for a, b, c in harmonics], [b for a, b, c in harmonics]))
    return rel_h, note

