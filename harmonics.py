import yaml
import numpy as np
import pandas as pd
from mido import MidiFile
import mido


class Music():
    with open("config.yaml", "r") as f:
        CFG = yaml.safe_load(f)
    IDICT = {k:v for k,v in zip(CFG['INAMES'],CFG['IDIST'])}
    EDICT = {k:v for k,v in zip(CFG['INAMES'],CFG['EXTENSION'])}
    NDICT = {k:v for k,v in zip(CFG['NOTES'],CFG['NDIST'])}
    INAMES    =  CFG['INAMES']
    INTERVALS =  CFG['INTERVALS']
    SCALES    =  CFG['SCALES']
    CHORDS    =  CFG['CHORDS']
    PATTERNS  =  CFG['PATTERNS']
    TUNING    =  CFG['TUNING']
    
    def __init__(self):
        pass
    
    def _list(self,thing):
        if type(thing) in (tuple,list,np.ndarray): return thing
        if type(thing) in (str,float,str): return [thing]
    
class Interval(Music):
    
    """Encapsulates the concept of an interval."""
    
    def __init__(self,name):
        super().__init__()
        if isinstance(name,Interval):
            self.__dict__.update(vars(name))
            return
        else:
            if name in self.INAMES: 
                self.name     = name
                self.distance  = self.IDICT[name]
                if int(self.name.split('b')[-1].split('#')[-1]) > 7: self.distance += 12
            else: 
                if type(name) in [tuple,list]:
                    if len(name) == 2 and type(name[0]) == Note:
                        self.distance = name[1].midi - name[0].midi  
                else: self.distance  = name
                candidates     = [a for a,b in self.IDICT.items() if b == self.distance%12]
                if self.distance >12:
                    candidates = [c for c in candidates if self.EDICT[c] in (1,2)]
                elif self.distance <12:
                    candidates = [c for c in candidates if self.EDICT[c] in (0,2)]
                self.name      = candidates[0]
            self.other_names   = [a for a,b in self.IDICT.items() if b == self.distance%12]
            for a in self.INTERVALS.keys():
                self._detect(a)
            self.octave = (self.distance//12)
    
    def _detect(self,class_attribute):
        if type(self.INTERVALS[class_attribute][0]) == str:
            attribute = self.name
        else:
            attribute = self.distance
        if attribute in self.INTERVALS[class_attribute]:
            self.__dict__[class_attribute.lower()] = True
        else:
            self.__dict__[class_attribute.lower()] = False
    
    def __repr__(self): return self.name
    def __str__(self): return self.name
    
    def __eq__(self,interval):
        if isinstance(interval, Interval):
            return self.distance == interval.distance
        elif type(interval) == str:
            return self.distance == Interval(str)
        else:
            return self.distance == interval
        
    def __add__(self,interval):
        if type(interval)  == Interval: return Interval(self.distance + interval.distance)
        elif type(interval) == int: return Interval(self.distance + interval)
    
    
    def __sub__(self,interval):
        if type(interval) == Interval: return Interval((self.distance - interval.distance)%12)
        elif type(interval) == int: return Interval((self.distance - interval)%12)
    

    def __invert__(self):
        if self.distance <  0: return Interval(abs(self.distance-12)%12)
        if self.distance >  0: return Interval(abs(self.distance+12)%12)
        if self.distance == 0: return Interval(0) 


class Pattern(Music):
    
    """A sequence of intervals."""
    CHORDS   = {k : [Interval(i) for i in v[0]] for k,v in Music.CHORDS.items()}
    SCALES   = {k : [Interval(i) for i in v+['1']] for k,v in Music.SCALES.items()}
    PATTERNS = {k : [Interval(i) for i in v] for k,v in Music.PATTERNS.items()}
    FORMULAS      = {**CHORDS,**SCALES,**PATTERNS}
    
    def __init__(self,name='',notes=None,intervals=None):
        self.name = name ; self.notes = notes ; self.intervals = intervals
        if notes:
            try:
                self.intervals = [a//b for a,b in zip(notes,notes[1:])]
                self.distance = np.array([i.distance for i in self.intervals])
            except TypeError: pass
        elif name:
            try:
                intervals_from_start = self.FORMULAS[self.name]              
                self.distance  = np.array([(b-a).distance for a,b in zip(intervals_from_start,intervals_from_start[1:])])
                self.intervals = [Interval(i) for i in self.distance] 
            except KeyError: pass
        else:
            return
     
    def __repr__(self) : return '--'+'--'.join([str(i) for i in self.distance])+'--'
    def __str__(self):   return '--'+'--'.join([str(i) for i in self.intervals])+'--'          

class Note(Music):
    DEF_OCTAVE = 4
    
    def __init__(self,n,
                 rest     = 0,
                 duration = 1, #unit?
                 volume   = 100, #units
                 mod      = None,
                 context  = None,
                 instrument=None):
        super().__init__()
        if isinstance(n,Note): self.__dict__.update(vars(n))
        else:
            self.duration = duration
            self.rest = rest
            self.volume      = volume
            self.mod         = mod
            self._set_instrument(instrument)
            self._set_context(context)
            if type(n) == str:
                if n[-1].isnumeric():
                    self.octave = int(n[-1])
                    self.name = n[:-1]
                else:
                    self.name = n
                    self.octave = Note.DEF_OCTAVE
                self.midi = self.NDICT[n] + (self.octave+1)*12
            else:
                self.midi   = n
                self.name   = [a for a,b in self.NDICT.items() if n%12 == b][0]
                self.octave = (self.midi//12)-1
            # computed
            self.equivalents = [a for a,b in self.NDICT.items() if self.midi%12 == b]
            self.pitch = self.NDICT[self.name]
            self.MIDI = self.to_midi()
    
    def __eq__(self,note):
        if type(note) == str:
            return note in self.equivalents
        if type(note) == int:
            return self.midi%12 == note%12
        if isinstance(note, Note):
            return self.pitch == note.pitch
        
    def __floordiv__(self,note):
        if isinstance(note, Note):
            return Interval([self,note])  
    
    def __truediv__(self,note):
        if isinstance(note, Note):
            distance = Interval([self,note]).distance
            octaves  = distance // 12 ; semis = distance % 12
            return f"{octaves} octaves and {semis} semitones"                    
    
    def __str__(self): return self.name
    
    def __repr__(self): return self.name
    
    def __len__(self): return self.midi
    
    def __add__(self,note):
        if type(note) == Interval: return Note(n          = self.midi+note.distance,
                                               rest       = self.rest,
                                               duration   = self.duration,
                                               volume     = self.volume,
                                               instrument = self.instrument)
        if type(note) == Note:
            return Part(notes=[self,note])
        
    def _set_context(self,context):
        if isinstance(context, Context):  self.context = context
        else: self.context = Context()
    
    def _set_instrument(self,instrument):    
        if isinstance(instrument, Instrument): self.instrument = instrument
        else: self.instrument = Instrument()
            
    def enharmonic(self,spelling='b',name=''):
        if (name != '') and name in self.equivalents:
            self.name = name
        if spelling == 'natural': selection = [i for i in self.equivalents if ('b' not in i) & ('#' not in i)]
        else: selection = [i for i in self.equivalents if spelling in i]
        if len(selection):
            self.name = selection[0]
    
    def to_midi(self):
        """Probabably need to auto-convert units"""
        channel = 0#f(self.instrument
        velocity = 100 #f(self.volume)
        time = 0 #f(self.rest)
        time2 = 10 #f(self.duration)
        on  = mido.Message('note_on', channel=channel, note=self.midi, velocity=velocity,  time=time)
        off = mido.Message('note_off',channel=channel,note=self.midi, velocity=velocity, time=time2)
        if True:
            pass # add info about midi CC if necessary
        return mido.MidiTrack([on,off])
    
    def append(self,note):
        if type(note) == Note: return Part(notes=[self,note])

class Context(Music):
    "Harmonic, rhytmic context for a note, used in Part and Song."
    def __init__(self,key='C',mode=1,time_signature='4:4',chord=None):
        self.key            = key
        self.mode           = mode
        self.time_signature = time_signature
        self.chord          = chord
    
    def __eq__(self, context):
        if isinstance(context, Context):
            return (self.key == context.key) & (self.mode == context.mode) & (self.time_signature == context.time_signature) & (self.chord == context.chord)
     
class Part(Music):
    """Melody, bassline or drum part."""
    
    DEFAULT_REF = 'C'
    
    def __init__(self,#init pattern
                 notes=False,     #
                 key=None,
                 part_type=None):
        super().__init__()
        self.notes    = notes
        self.key = key 
        if not self.key: self.key = self.DEFAULT_REF
        self.part_type = None
        self.respell()
    
    def _detect_key(self):
        try:
            self.key = self.notes[0].key
        except FileExistsError:
            print('erooor')
            self.key = self.DEFAULT_REF 
    
    def __getitem__(self,index):
        if type(index) == int: return self.notes[index]
        return Part(notes=self.notes[index],key=self.key,part_type=self.part_type)
    
    # def setkey(self,key):
    #     if not key:
    #         self.key = Note(Part.DEFAULT_REF)
    #     else:
    #         self.key = Note(key)
    #     self.key = key
    #     self.relative_to_key
    
    def __add__(self,obj):
        if isinstance(obj, Part):
            return Part(notes=self.notes+obj.notes,part_type=self.part_type,key=self.key)
        if isinstance(obj, Note):
            print(self.notes)
            print(obj)
            return Part(notes=self.notes+[obj],part_type=self.part_type,key=self.key)
            
    def __contains__(self,note):
        return [note==n for n in self.notes]                

    def __repr__(self):
        return str(self.notes)
    
    def respell(self,names=[]):
        if names:
            for name in names:
                for note in self.notes:
                    note.enharmonic(name=name)
        else:
            def _respell(acc):
                for n in self.notes: n.enharmonic(spelling=acc)
            if 'b' in str(self.key): _respell('b')
            if '#' in str(self.key): _respell('#')
            _respell('natural')
        
class Chord(Music):
    DEFAULT_ROOT = 'C'
    # FORMULAS  = {'I'  : [Interval(i) for i in ['1', '3' , '5' , '7' , '9' , '11' ,'13' ]],
    #              'ii' : [Interval(i) for i in ['1', 'b3', '5' , 'b7', '9' , '11' ,'13' ]],
    #              'iii': [Interval(i) for i in ['1', 'b3', '5' , 'b7', 'b9', '11' ,'b13']],
    #              'IV' : [Interval(i) for i in ['1', '3' , '5' , '7' , '9' , '#11','13' ]],
    #              'V'  : [Interval(i) for i in ['1', '3' , '5' , 'b7', '9' , '11' ,'13' ]],
    #              'vi' : [Interval(i) for i in ['1', 'b3', '5' , 'b7', '9' , '11' ,'b13']],
    #              'vii': [Interval(i) for i in ['1', 'b3', 'b5', 'b7', 'b9', '11' ,'b13']]}
    CHORDS   = {k : [Interval(i) for i in v[0]] for k,v in Music.CHORDS.items()}
    
    def __init__(self,chord='',notes=None,root='',key=''):
        super().__init__()
        self.key  = key
        self.root = root
        if chord:
            self.chord = chord
            self.formula = Chord.CHORDS[chord]
            if not self.root: self.root = Chord.DEFAULT_ROOT
            self.notes   = [Note(i) for i in [Note(self.root).midi + i.distance for i in self.formula]]
        elif notes:
            pass
        self.respell()
        if not self.root:
            pass
        
    def respell(self):
        if not self.key:
            def _respell(acc):
                for n in self.notes: n.enharmonic(spelling=acc)
            if ('b' in self.root) or ('b' in ' '.join([i.name for i in self.formula])): _respell('b')
            if ('#' in self.root) or ('#' in ' '.join([i.name for i in self.formula])): _respell('#')
            _respell('natural')
        if self.key:
            pass #right spelling depending on the key
            
class Song:
    def __init__(self,path=None,bpm=120,clip=True):
        if path:
            self.MIDI = MidiFile(path,clip=clip)
            self.df   = self._tracks_to_df()
            tempo = self.df.tempo.dropna().values
            if len(tempo)== 1:
                self.tempo = round(tempo[0])
                self.bpm = mido.tempo2bpm(self.tempo)
            elif not len(tempo) == 0:
                self.tempo, self.bpm = None,None
            else:
                self.tempo = tempo
                self.bpm = self.tempo.apply(mido.tempo2bpm)
        else:
            self.MIDI = None
            self.df = None
            self.bpm = bpm
            self.tempo = mido.bpm2tempo(self.bpm)
   
    def _tracks_to_df(self):
        full_df = pd.DataFrame([])
        for n,track in enumerate(self.MIDI.tracks): 
            df = pd.concat([pd.DataFrame({k: pd.Series([v]) for k,v in a.__dict__.items()}) for a in track],ignore_index=True)
            df['track'] = pd.Series([n]*len(df))
            df['meta'] = pd.Series([m.is_meta for m in track])
            if self.MIDI.type == 2:
                df['ticks'] = np.cumsum(df.time.values)
            full_df = pd.concat([full_df,df])
        if self.MIDI.type == 1:
            full_df['ticks'] = np.cumsum(full_df.time.values)
        return full_df
    
    def export(self,path):
        """wrapper for mido object"""
        pass
    
    def get(self,what):
        pass
    
    def add_Part(self,Part):
        pass

class Instrument(Music):
    INSTRUMENTS   = Music.CFG["INSTRUMENTS"] 
    MIDI_CHANNELS = Music.CFG['MIDI_CHANNELS']
    MIDI_GM1      = Music.CFG['MIDI_GM1']
    MIDI_GM2      = Music.CFG['MIDI_GM2']
    def __init__(self,name=None,channel=None,bank=None,instrument_type=None):
        super().__init__()
        self.name = name
        self.channel = channel
        self.bank = bank
        self.instrument_type = instrument_type
        