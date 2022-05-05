from scipy.signal import find_peaks
import harmonics as h
import pandas as pd
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

def get_enveloppe(s,data,length=0.02,plot=True):
    x = np.array([i for i in range(0,len(data),int(0.02*s))])
    y = np.array([0]+[np.max(data[x[i]:x[i+1]]) for i in range(len(x)-1)])
    x = x/x.max()
    y = y/y.max()
    if plot: audio_plot(x,y,'time','amplitude')
    return np.vstack((x,y))

def get_sine(duration,F,A=4096,aR=1,fR=1,sample_rate=44100,plot=True):
    t = np.arange(duration*int(sample_rate)) # Time axis
    wave = (aR*A)*np.sin(2*np.pi*(fR*F/sample_rate)*t)
    if plot: audio_plot(np.arange(0,len(wave)),wave,'time (s)','amplitude')
    return wave

def get_harmonics(s,data,plot=True):
      t    = np.arange(data.shape[0])
      freq = np.fft.rfftfreq(t.shape[-1])*s
      sp   = np.fft.rfft(data) 
      df = pd.DataFrame(np.vstack((freq,abs(sp.real))).T,
                        columns=['frequency','amplitude'])#.sort_values('amplitude',ascending=False)
      max_freq = df[df.amplitude == df.amplitude.max()].frequency
      a, _ = find_peaks(df.amplitude,
                        threshold=df.amplitude.max()*0.01, 
                          distance=int(max_freq/900*100))
      f = df.loc[a,:]
      f.sort_values('frequency',inplace=True)
      harmonics = [(round(a,2),round(b,2)) for a,b in zip(f.frequency,f.amplitude)]
      fundamental = f[f.amplitude == f.amplitude.max()].frequency.to_numpy().max()
      rel_h = [(round(a/fundamental,2), round(b/f.amplitude.max(),2)) for a,b in harmonics]
      note = h.Note(str(fundamental)+'Hz')
      if plot:
          freq = freq[freq<10*fundamental]
          ampl = abs(sp.real)[:len(freq)]
          audio_plot(freq,ampl,'Frequency (Hz)','Amplitude',scatter=([a for a,b in harmonics],[b for a,b in harmonics]))
      return rel_h, note
      
def audio_plot(x,y,xlabel='',ylabel='',title='',show='all',figsize=(10,4),scatter=False):
    if show != 'all': x = x[:show] ; y = y[:show]
    plt.figure(figsize=figsize)
    plt.plot(x,y)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    if scatter: plt.scatter(*scatter,c='r')
    plt.title(title)
    plt.grid()

class Sampler:
    """Generates sound waves, can base overtones and enveloppe on extracted sample."""
    def __init__(self,frequency=440,sample_rate=44100,amplitude=4096,file=None):
        self.frequency      = frequency
        self.sample_rate    = sample_rate
        self.amplitude      = amplitude
        self.file           = file
        self._analyzed      = {'file':[],'data':[],'rel_harmonics':[],'note':[],'offpitch':[],'enveloppe':[],
                               'frequency':[],'duration':[]}
        self.overtones      = False
        self.enveloppe      = False
        
    @property
    def analyzed(self):
        return pd.DataFrame({k:pd.Series(v) for k,v in self._analyzed.items()})
    
    def set_overtones(self,i):
        if type(i) == int: self.overtones = self.analyzed.loc[i,'rel_harmonics']
        elif i == False: self.overtones = False
        return self.overtones
    
    def set_enveloppe(self,i):
        if type(i) == int: self.enveloppe = self.analyzed.loc[i,'enveloppe']
        elif i == False: self.enveloppe = False
        return self.enveloppe
            
        
    def get_wave(self,duration,
                 freq=None,
                 plot=True,
                 wav=True,
                 overtones='def',
                 enveloppe='def',
                 filename='name.wav',
                 show='all',
                 s=44100):
        if freq: self.frequency = freq
        if overtones == 'def': overtones = self.overtones
        if enveloppe == 'def': enveloppe = self.enveloppe
        if type(overtones) == int: overtones = self.set_overtones(overtones)
        if type(enveloppe) == int: enveloppe = self.set_enveloppe(enveloppe)
        if not overtones:
            wave = get_sine(duration,self.frequency,self.amplitude, sample_rate=s)
        else:
            print('added overtones')
            wave = np.sum([get_sine(duration,A=self.amplitude,F=self.frequency,aR=a,fR=f,sample_rate=s,plot=False) for f,a in overtones],axis=0)
        #def get_sine(duration,F,A=4096,aR=1,fR=1,sample_rate=44100,plot=True)
        if type(enveloppe) == np.ndarray:
            print('WELL HELLP')
            scaled_env = np.interp(np.arange(0,len(wave)),
                                    enveloppe[0,:]*len(wave),
                                    enveloppe[1,:])
            print(len(wave),len(scaled_env))
            wave *= scaled_env
        if plot:audio_plot(np.arange(len(wave))/self.sample_rate,wave,'time','amplitude',show=show)
        
        if wav: wavfile.write(filename, rate=self.sample_rate, data=wave.astype(np.int16))
        return wave
    
    def extract(self,filepath,plot=True,dist=10,cutoff=0.01,figsize=(10,4)):
        sample_rate, data = wavfile.read(filepath)
        i,j = 0,0
        while j < 0.01*data.max():
            j = data[i] ; i += 1
        data = data[i:]
        duration = len(data)/sample_rate
        self._analyzed['file'].append(filepath)
        if plot:  audio_plot(np.linspace(0,duration,len(data)), data,'Time','Amplitude',filepath,figsize=figsize)
        relh,note = get_harmonics(sample_rate, data, plot=plot)
        self._analyzed['duration'].append(duration)
        self._analyzed['data'].append((sample_rate,data))
        self._analyzed['rel_harmonics'].append(relh)
        self._analyzed['note'].append(note)
        self._analyzed['offpitch'].append(note.pitch.offpitch)
        self._analyzed['frequency'].append(note.pitch.frequency)
        self._analyzed['enveloppe'].append(get_enveloppe(sample_rate,data, plot=plot))
        