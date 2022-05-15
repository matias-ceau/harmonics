import numpy as np
import pandas as pd
from .note import Note
from ..data.general import DEFAULT_KEY


class Vessel():
    """Melody, bassline or drum part."""

    DEFAULT_REF = DEFAULT_KEY

    def __init__(self, notes=None, key=None):
        super().__init__()
        self.notes = notes
        self.key = key
        if not self.key:
            self.key = self.DEFAULT_REF
        self.part_type = None
        self.respell()

    def __getitem__(self, index):
        if type(index) == int:
            return self.notes[index]
        return Vessel(notes=self.notes[index],
                      key=self.key,
                      part_type=self.part_type)

    def __add__(self, obj):
        if isinstance(obj, Vessel):
            return Vessel(notes=self.notes+obj.notes,
                          part_type=self.part_type,
                          key=self.key)
        if isinstance(obj, Note):
            print(self.notes)
            print(obj)
            return Vessel(notes=self.notes+[obj],
                          part_type=self.part_type,
                          key=self.key)

    def __contains__(self, note):
        return [note == n for n in self.notes]

    def __repr__(self):
        return str(self.notes)

    @property
    def df(self):
        df = pd.DataFrame([i.to_data() for i in self.notes])
        df['beat_time'] = 0  # ""
        df['_miditime'] = [0]+df._duration.to_list()[:-1]

    def respell(self, names=[]):
        if names:
            for name in names:
                for note in self.notes:
                    note.enharmonic(name=name)
        else:
            def _respell(acc):
                for n in self.notes:
                    n.enharmonic(spelling=acc)
            if 'b' in str(self.key):
                _respell('b')
            if '#' in str(self.key):
                _respell('#')
            _respell('natural')
