from mido import MidiFile
import mido
import time
import numpy as np
import pandas as pd

from ...core.midi import MIDI_CC, DRUM_PROG, MIDI_GM1, DRUM_KEYMAP, MIDIMESSAGE
from ...core.notes import NDICT
from ..._utils import timer, _list
from .utils import MidiUtils, play_bytes



class MidiReader():
    def __init__(self, path=None, bpm=None, key='', time_signature=(4, 4)):
        super().__init__()
        self.info = []
        self.path = path
        self.bpm = bpm
        self.tempo = self._midi_get('tempo', bpm=self.bpm)
        self.time_signature = time_signature
        if self.path:
            self.MIDI = MidiFile(path, clip=True)
            start = time.time()
            self._extract_midi()
            timer('extraction', start)
        else:
            self.MIDI = None
            self.__dict__.update({i: None for i in ['key_signature',
                                                    'channel_list',
                                                    'df',
                                                    'tracks',
                                                    'parts']})

    def __repr__(self):
        return f"""\
path:     {self.path}
bpm:      {self._bpm}
key:      {self.key_signature}
time_sig: {self.time_signature}
channels: {self.channel_list}
"""

    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, val):
        self._bpm = val
        self._tempo = self._midi_get('tempo', bpm=self._bpm)

    @property
    def tempo(self):
        return self._tempo

    @tempo.setter
    def tempo(self, val):
        self._tempo = val
        self._bpm = self._midi_get('bpm', tempo=self._tempo)

    @property
    def ticks_per_beat(self):
        return self.MIDI.ticks_per_beat

    @property
    def df(self):
        return self._df[[i for i in self._df.columns if i[0] != '_']]

    @property
    def instr(self):
        return {i: [a for a in set(self._df[self._df.channel == i].instr)
                    if type(a) != float] for i in self.channel_list}

    def notes(self, channel='all'):
        if channel == 'all':
            return self.df[self._df.type == 'note_on']
        else:
            return self.df[(self._df.type == 'note_on') &
                           (self._df.channel == channel)]

    def channel(self, channel, meta=False):
        df = self.df[self.df.channel == channel]
        if not meta:
            return df[(df.type == 'note_on') | (df.type == 'note_off')]
        else:
            return df

    def cc(self, channel=None):
        df = self.df[self.df.type == 'CC']
        if channel:
            return df[df.channel == channel]
        else:
            return df

    def prog(self, channel=None):
        df = self.df[self.df.type == 'program']
        if channel:
            return df[df.channel == channel]
        else:
            return df

    def get(self, c=None, t=None):
        if len(self._df):
            if c and t:
                return self._df[(self._df.channel == c) & (self._df.type == t)]
            if c:
                return self._df[(self._df.channel == c)]
            if t:
                return self._df[(self._df.type == t)]

    def send_midi(self, channel='all', **kwargs):
        data = self._df[self._df.type != 'sysex']
        if channel != 'all':
            ch = _list(channel)
            data = data[data.isin(ch)]
        note_bytes = data._bytes.tolist()
        durations = data._duration.tolist()
        play_bytes(note_bytes,
                   tick_durations=durations,
                   ticks_per_beat=self.ticks_per_beat,
                   bpm=self.bpm,
                   **kwargs)

    def __getitem__(self, number):
        if type(number) == int:
            return None

    def _midi_get(self,
                  string,
                  tempo=None,
                  bpm=None,
                  beats=None,
                  ticks_per_beat=None,
                  ticks=None,
                  ceil=False,
                  time_signature=None):
        if string == 'bpm' and tempo:
            return int(mido.tempo2bpm(tempo))
        if string == 'tempo' and bpm:
            return mido.bpm2tempo(bpm)
        if string == 'beats' and ticks_per_beat and ticks:
            if ceil:
                return np.ceil(ticks/ticks_per_beat)
            else:
                return ticks/ticks_per_beat
        if string == 'ticks' and beats and ticks_per_beat:
            return beats*ticks_per_beat
        if string == 'bar' and time_signature and beats:
            if ceil:
                return np.ceil(beats/int(time_signature.split(':')[0]))
            else:
                return beats/int(time_signature.split(':')[0])
        else:
            return None

    def _extract_midi(self):
        tracks = []
        for n, track in enumerate(self.MIDI.tracks):
            _miditime = np.array([i.time for i in track]).astype(np.int32)
            time_to_next = np.hstack((_miditime[1:], [0])).astype(np.int32)
            tick_time = np.cumsum(_miditime).astype(np.int32)
            msg = np.array([i.hex() for i in track])
            msgtranslate = MIDIMESSAGE
            df = pd.DataFrame({
             'track':   [n]*len(time_to_next),
             'type':    np.array([msgtranslate[i[0]] for i in msg]),
             'channel': np.array([int(i[1], 16) for i in msg],
                                 dtype=np.int32),
             'data1':   np.array([int(i[3:5], 16) for i in msg],
                                 dtype=np.int32),
             'data2':   np.array([int(i[6:], 16)
                                  if len(i[6:]) == 2
                                  else 999 for i in msg],
                                 dtype=np.int32),
             '_miditime':     _miditime,
             '_duration':     time_to_next,
             'tick_time':    tick_time,
             '_hex_msg':      msg,
             '_bytes':    [i.bytes() for i in track]
            })
            off = df[(df.type == 'note_on') & (df.data2 == 0)].index.values
            df.loc[off, 'type'] = 'note_off'
            tracks.append(df)
        if len(tracks) == 1:
            self._df = tracks[0]
        else:
            self._df = pd.concat(tracks)
        self._df.reset_index(inplace=True, drop=True)

        # EXTRACT METAMESSAGES
        self.channel_list = list(set(self._df.channel))
        self.metamessages = {a.type: a for a in [
            i for a in self.MIDI.tracks for i in a if i.is_meta]}
        if 'time_signature' in self.metamessages:
            ts = self.metamessages['time_signature']
            self.time_signature = (ts.numerator, ts.denominator)
        else:
            self.time_signature = (4, 4)
            self.info.append(
                'No time signature in MIDI file, default selected.')
        if 'set_tempo' in self.metamessages:
            self.tempo = self.metamessages['set_tempo'].tempo
        else:
            self.info.append('No tempo in MIDI file.')
        if 'key_signature' in self.metamessages:
            self.key_signature = self.metamessages['key_signature'].key
        else:
            self.key_signature = ''
            self.info.append('No key signature in MIDI file')

        # COMPUTING RELEVANT INFO

        self._df['beat_time'] = np.round(
            self._df.tick_time/self.MIDI.ticks_per_beat, 2)
        self._df['_beat_pos'] = np.round(self._df.beat_time.to_numpy() % 1, 2)
        f = MidiUtils.quantitize
        self._df['q_beat_p'] = f(self._df._beat_pos.to_numpy())
        self._df['_curr_beat'] = np.floor(
            self._df.beat_time.to_numpy()).astype(np.int32)+1
        self._df['rel_beat'] = (
            (self._df._curr_beat.to_numpy() - 1) % self.time_signature[0])+1
        self._df['_bar_time'] = np.round(
            self._df.beat_time.to_numpy()/self.time_signature[0], 2)
        self._df['curr_bar'] = np.array(
            ((self._df._curr_beat - 1)
             / self.time_signature[0])+1, dtype=np.int32)
        self._df['bar_pos'] = np.round(self._df._bar_time.to_numpy() % 1, 2)

        # TRANSLATE NOTES
        vm = np.vectorize(MidiUtils.midi_to_note)
        vd = np.vectorize(MidiUtils.midi_drum)
        midx = self._df[self._df.channel != 9].index
        didx = self._df[self._df.channel == 9].index
        self._df.loc[:, 'note'] = ''
        if len(midx):
            self._df.loc[midx, 'note'] = vm(self._df.loc[midx, 'data1'])
        if len(didx):
            self._df.loc[didx, 'note'] = vd(self._df.loc[didx, 'data1'])

        # GET NOTE DURATION
        for c in self.channel_list:
            df = self.channel(c)
            for n in set(df.data1):
                d = df[df.data1 == n]
                idx_on = d[d.type == 'note_on'].index
                idx = list(zip(idx_on, d[d.type == 'note_off'].index))
                _ntdur = np.array(
                    [(d.loc[b, 'tick_time']-d.loc[a, 'tick_time'])
                     for a, b in idx], dtype=np.int32)
                for n, i in enumerate(idx_on):
                    self._df.loc[i, '_ntdur'] = int(_ntdur[n])

        # TRANSLATE PROGRAM CHANGES AND CCS
        vcc = np.vectorize(MidiUtils.midi_cc)
        cc_idx = self._df[self._df.type == 'CC'].index
        self._df.loc[:, 'cc'] = ''
        if len(cc_idx):
            self._df.loc[cc_idx, 'cc'] = vcc(
                self._df.loc[cc_idx, 'data1'].to_numpy())
        vpr = np.vectorize(MidiUtils.midi_program)

        pr_idx = self._df[self._df.type == 'program'].index
        self._df.loc[:, 'instr'] = ''
        if len(pr_idx):
            self._df.loc[pr_idx, 'instr'] = vpr(
                self._df.loc[pr_idx, 'channel'].to_numpy(),
                self._df.loc[pr_idx, 'data1'].to_numpy()
                )
        # TODO expand instrument on all channel ?

