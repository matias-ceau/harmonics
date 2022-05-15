from ..data.chords import CHORDS
from ..data.general import DEFAULT_KEY
from .note import Note
from .interval import Interval

class Chord(Note):
    DEFAULT_ROOT = DEFAULT_KEY
    CHORDS = {k: [Interval(i) for i in v[0]]
              for k, v in CHORDS.items()}

    def __init__(self, chord='', notes=None, root='', key=''):
        self.key = key
        self.root = root
        if chord:
            self.chord = chord
            self.formula = self.CHORDS[chord]
            if not self.root:
                self.root = Chord.DEFAULT_ROOT
            self.notes = [Note(i) for i in [Note(
                self.root).midi + i.distance for i in self.formula]]
        elif notes:
            pass
        self.respell()
        if not self.root:
            pass

    def respell(self):
        if not self.key:
            def _respell(acc):
                for n in self.notes:
                    n.enharmonic(spelling=acc)
            if ('b' in self.root) or ('b' in ' '.join(
                    [i.name for i in self.formula])
                                      ):
                _respell('b')
            if ('#' in self.root) or ('#' in ' '.join(
                    [i.name for i in self.formula])
                                      ):
                _respell('#')
            _respell('natural')
        if self.key:
            pass  # right spelling depending on the key
