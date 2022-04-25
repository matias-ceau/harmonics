import yaml

class Music():
    with open("config.yaml", "r") as f:
        CFG = yaml.safe_load(f)
    IDICT = {k:v for k,v in zip(CFG['INAMES'],CFG['IDIST'])}
    NDICT = {k:v for k,v in zip(CFG['NOTES'],CFG['NDIST'])}
    INAMES =  CFG['INAMES']
    INTERVALS =  CFG['INTERVALS']
    SCALES    =  CFG['SCALES']
    
class Interval(Music):
    
    
    def __init__(self,name):
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
                self.name      = candidates[0]
            self.other_names   = [a for a,b in self.IDICT.items() if b == self.distance%12]
            for a in self.INTERVALS.keys():
                self._detect(a)
            if self.extension: self.octave = 1
    
    def _detect(self,class_attribute):
        if type(self.INTERVALS[class_attribute][0]) == str:
            attribute = self.name
        else:
            attribute = self.distance
        if attribute in self.INTERVALS[class_attribute]:
            self.__dict__[class_attribute.lower()] = True
        else:
            self.__dict__[class_attribute.lower()] = False
    
    def __repr__(self):
        return self.name
        
    def __add__(self,interval):
        if type(interval)  == Interval: return Interval(self.distance + interval.distance)
        elif type(interval) == int: return Interval(self.distance + interval)
    
    def __radd__(self,interval):
        return self.__add__(interval)
    
    def __sub__(self,interval):
        if type(interval) == Interval: return Interval((self.distance - interval.distance)%12)
        elif type(interval) == int: return Interval((self.distance - interval)%12)
    
    def __rsub__(self,interval):
        return self.__sub__(interval)
    
    def invert(self):
        if self.distance <  0: return Interval(abs(self.distance-12)%12)
        if self.distance >  0: return Interval(abs(self.distance+12)%12)
        if self.distance == 0: return Interval(0) 


class Note(Music):
    DEF_OCTAVE = 4
    
    def __init__(self,n,octave=None,duration=1,rest=0,volume=90):
        if isinstance(n,Note): self.__dict__.update(vars(n))
        else:
            self.duration = duration
            self.rest = rest
            self.volume   = volume
            if type(n) == str:
                self.name = n
                if not octave: self.octave = Note.DEF_OCTAVE
                self.midi = self.NDICT[n] + (self.octave+1)*12
            else:
                self.midi   = n
                self.name   = [a for a,b in self.NDICT.items() if n%12 == b][0]
                self.octave = (self.midi//12)-1
            self.equivalents = [a for a,b in self.NDICT.items() if self.midi%12 == b]
    
    def enharmonic(self,spelling='b'):
        if spelling == 'natural': selection = [i for i in self.equivalents if ('b' not in i) & ('#' not in i)]
        else: selection = [i for i in self.equivalents if spelling in i]
        if len(selection):
            self.name = selection[0]
    
    def __str__(self): return self.name
    
    def __repr__(self): return self.name
    
    def __len__(self): return self.midi
    
    def __add__(self,note):
        if type(note) == Interval: return Note(n=self.midi+note.distance,
                                               octave=self.octave,
                                               duration=self.duration,
                                               volume=self.volume) 
        if type(note) == Note: return Chord(notes=[self,note])
    
    def __radd__(self,note): self.__add__(note)
        
    def append(self,note):
        if type(note) == Note: return Melody(notes=[self,note])
        
class Melody(Music):
    
    DEFAULT_REF = 'C'
    PATTERNS = {'arp_M7'  : [Interval(i) for i in ['1', '3' , '5' , '7' ]],
                'arp_7'   : [Interval(i) for i in ['1', '3' , '5' , 'b7']],
                'arp_m7'  : [Interval(i) for i in ['1', 'b3', '5' , 'b7']],
                'arp_m7b5': [Interval(i) for i in ['1', 'b3', 'b5', 'b7']],
                'penta_m' : [Interval(i) for i in ['1', 'b3', '4' , '5', 'b7']],
                'penta_M' : [Interval(i) for i in ['1', '2' , '3' , '5', '6']],
                'coltr_m' : [Interval(i) for i in ['1', 'b3', '4' , '5']],
                'coltr_M' : [Interval(i) for i in ['1', '2' , '3' , '5']]}
    
    def __init__(self,name=False,notes=False,ref_note=None):
        self.name     = name
        self.notes    = notes
        if not ref_note: self.ref_note = Note(Melody.DEFAULT_REF)
        else: self.ref_note = Note(ref_note)
        if self.name:
            self.pattern = Melody.PATTERNS[name]
            self.notes   = [self.ref_note + i for i in self.pattern]  
        if self.notes:
            self
        if not ref_note: self.ref_note = sorted(self.notes,key=len)
        self.respell()
    
    def respell(self):
        def _respell(acc):
            for n in self.notes: n.enharmonic(spelling=acc)
        if 'b' in str(self.ref_note): _respell('b')
        if '#' in str(self.ref_note): _respell('#')
        _respell('natural')

    def __repr__(self):
        return str(self.notes)
        
class Chord(Music):
    DEFAULT_ROOT = 'C'
    FORMULAS  = {'I'  : [Interval(i) for i in ['1', '3' , '5' , '7' , '9' , '11' ,'13' ]],
                 'ii' : [Interval(i) for i in ['1', 'b3', '5' , 'b7', '9' , '11' ,'13' ]],
                 'iii': [Interval(i) for i in ['1', 'b3', '5' , 'b7', 'b9', '11' ,'b13']],
                 'IV' : [Interval(i) for i in ['1', '3' , '5' , '7' , '9' , '#11','13' ]],
                 'V'  : [Interval(i) for i in ['1', '3' , '5' , 'b7', '9' , '11' ,'13' ]],
                 'vi' : [Interval(i) for i in ['1', 'b3', '5' , 'b7', '9' , '11' ,'b13']],
                 'vii': [Interval(i) for i in ['1', 'b3', 'b5', 'b7', 'b9', '11' ,'b13']]}
    
    def __init__(self,chord='',notes=None,root='',key=''):
        self.key  = key
        self.root = root
        if chord:
            self.chord = chord
            self.formula = Chord.FORMULAS[chord]
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
