from .volume import Volume
from .pitch import Pitch
from .duration import Duration
from .effect import Effect
from .interval import Interval
from .instrument import Instrument
from dataclasses import dataclass

@dataclass
class NoteData:
    message_type: str
    instrument:      int
    pitch:        int
    volume:        int
    duration:     float


class Note:
    is_note = True

    @classmethod
    def fromData(cls, obj):
        if obj.message_type == 'note_on':
            # need to convert duration and maybe change channel to instrument
            return cls(obj.pitch,
                       volume=obj.volume,
                       duration=obj.duration,
                       instrument=obj.instrument)

    def __init__(self, n,
                 duration=1,  # unit?
                 volume=100,  # units
                 effect=None,
                 kind=None,
                 instrument=0):
        self.pitch = Pitch(n)
        self.duration = Duration(duration)
        self.volume = Volume(volume)
        self.effect = Effect(effect)
        self.type = kind
        self.instrument = Instrument(instrument)

    def __eq__(self, note):
        return self.pitch == note

    def __floordiv__(self, note):
        if isinstance(note, Note):
            return Interval([self.pitch, note.pitch])

    def __truediv__(self, note):
        if isinstance(note, Note):
            distance = Interval([self.pitch, note.pitch]).distance
            octaves = distance // 12
            semis = distance % 12
            return f"{octaves} octaves and {semis} semitones"

    def __str__(self): return repr(self.pitch)
    def __repr__(self): return repr(self.pitch)
    def __len__(self): return self.pitch.midi

    def __add__(self, note):
        if type(note) == Interval:
            return Note(n=self.pitch.midi+note.distance,
                        duration=self.duration,
                        volume=self.volume,
                        mod=self.effect)

    def enharmonic(self, spelling='b', name=''):
        if (name != '') and name in self.pitch.equivalents:
            self.name = name
        if spelling == 'natural':
            selection = [i for i in self.pitch.equivalents if (
                'b' not in i) & ('#' not in i)]
        else:
            selection = [i for i in self.pitch.equivalents if spelling in i]
        if len(selection):
            self.name = selection[0]

    def to_data(self):
        # if mod also return CC message
        return NoteData('note_on',
                        self.instrument.name,
                        self.pitch.midi,
                        self.volume.velocity,
                        self.duration.duration)
