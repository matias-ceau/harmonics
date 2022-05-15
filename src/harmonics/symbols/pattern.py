from .interval import Interval
from ..data.patterns import PATTERNS
from ..data.general import FORMULAS

import numpy as np


class Pattern():

    """A sequence of intervals."""

    @classmethod
    def find_pattern(cls, arr, seq):
        Na, Nseq = arr.size, seq.size
        r_seq = np.arange(Nseq)
        M = (arr[np.arange(Na-Nseq+1)[:, None] + r_seq] == seq).all(1)
        if M.any() > 0:
            return np.where(np.convolve(M, np.ones((Nseq), dtype=int)) > 0)[0]
        else:
            return []

    def __init__(self, name='', notes=None, intervals=None):
        self.name = name
        self.notes = notes
        self.intervals = intervals
        if notes:
            try:
                self.intervals = [a//b for a, b in zip(notes, notes[1:])]
                self.distance = np.array([i.distance for i in self.intervals])
            except TypeError:
                pass
        elif name:
            try:
                intervals_from_start = {
                    Interval(i) for i in FORMULAS[self.name]}
                self.distance = np.array(
                    [(b-a).distance for a, b in zip(intervals_from_start,
                                                    intervals_from_start[1:])])
                self.intervals = [Interval(i) for i in self.distance]
            except KeyError:
                pass
        else:
            return

    def __repr__(self): return '--' + \
        '--'.join([str(i) for i in self.distance])+'--'

    def __str__(self): return '--' + \
        '--'.join([str(i) for i in self.intervals])+'--'
