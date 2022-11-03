from ..data.drums import quick_gm, dna_notation, codon_to_aa, aa_to_midi, aa_to_midi_2
from .._utils import _list
import mido
import rtmidi
import random
import time
import pandas as pd

# df : midinotes symbol description probability

class Sequencer:

    def __init__(self, name='', notation=None):
        self.name = name
        if notation:
            self.notation = notation
        else:
            self.notation = quick_gm
        self.df_cols = ['midi', 'symbol', 'probability', 'seq_pos', 'seq_len']
        self.df = pd.DataFrame({i : [] for i in self.df_cols})

    def read_text(self, path):
        dflines = []
        with open(path) as f:
            lines = f.readlines()
            lines = [i[:-1] for i in lines]
        for li in lines:
            if (li[0] in quick_gm.keys()) and (li[1] == ':'):
                line_name = li[0]
                notes = li.split('%')[0][2:].replace(' ','')
                try:
                    proba = li.split('%')[1]
                    proba = float(proba.strip())
                except:
                    proba = 1
                seq_len = len(notes)
                for n, note in enumerate(notes):
                    if note != '-':
                        try:
                            midi = [self.notation[line_name][note]]
                        except KeyError:
                            midi = list(self.notation[line_name].values())
                        dflines.append(pd.Series([midi, note, proba, n, seq_len], dtype='object'))
        cols = self.df.columns
        self.df = pd.DataFrame(dflines)
        self.df.columns = self.df_cols

    def loop(self):
        # to change
        midiout = rtmidi.MidiOut()
        midiout.open_port(0)
        # send midi
        counter = 0
        while True:
            counter += 1
            df = self.df.copy()
            df['index'] = counter % df['seq_len']
            df = df[df['seq_pos'] == df['index']]
            if len(df):
                for i in df.index:
                    if df.loc[i, 'probability'] >= random.random():
                        midiout.send_message(
                                mido.Message('note_on',
                                                channel=9,
                                                note=random.choice(df.loc[i, 'midi']),
                                                velocity=random.choice(range(70,90))).bin()
                            )
                    time.sleep(0.125)


def play_dna(path):
    midiout = rtmidi.MidiOut()
    midiout.open_port(0)
    with open(path) as f:
        content = f.read()
    for letter in content:
        if letter in ['A', 'T', 'G', 'C']:
            midiout.send_message(
                                mido.Message('note_on',
                                                channel=9,
                                                note=random.choice(dna_notation[letter]),
                                                velocity=random.choice(range(70,90))).bin()
                            )
            time.sleep(0.25)

def play_aa(path, length=0.125):
    midiout = rtmidi.MidiOut()
    midiout.open_port(0)
    with open(path) as f:
        content = ''.join(f.readlines()[1:])
    content1 = [content[i:i+3] for i in range(0, len(content)-3, 3)]
    content2 = [content[i:i+3] for i in range(1, len(content)-3, 3)]
    content3 = [content[i:i+3] for i in range(2, len(content)-3, 3)]
    for i,j,k in zip(content1, content2, content3):
        aa1, aa2, aa3 = codon_to_aa.get(i), codon_to_aa.get(j), codon_to_aa.get(k)
        def no_none(a):
            if a: return a
            else: return '#'
        print(no_none(aa1),
              no_none(aa2),
              no_none(aa3))
        midi1, midi2, midi3 = aa_to_midi.get(aa1), aa_to_midi.get(aa2), aa_to_midi.get(aa3)
        midia, midib, midic = aa_to_midi_2.get(aa1), aa_to_midi_2.get(aa2), aa_to_midi_2.get(aa3)
        def send(note, channel=0):
            if note:
                midiout.send_message(
                    mido.Message('note_on',
                                 channel=channel,
                                 note=note,
                                 velocity=random.choice(range(70,90))).bin()
                    )
        def unsend(note, channel=0):
            if note:
                midiout.send_message(
                    mido.Message('note_off',
                                 channel=channel,
                                 note=note,
                                 velocity=random.choice(range(70,90))).bin()
                    )
        send(midi1)
        send(midia,channel=9)
        time.sleep(length)
        send(midi2)
        send(midib,channel=9)
        time.sleep(length)
        send(midi3)
        send(midic,channel=9)
        time.sleep(length)
        unsend(midi1)
        unsend(midi2)
        unsend(midi3)


# def read_file(path):
#     with open(path) as f:
#         lines = f.readlines()
#         lines = [i[:-1] for i in lines]
#         instruments = {}
#     for li in lines:
#         if li[0] in quick_gm.keys():
#             line = li[2:].replace(' ','')
#             spec = [i for i in set(line) if i != '-']
#             dic = quick_gm[li[0]]
#             spec_midi = [dic.get(i) if i in dic.keys() else random.choice(list(dic.values())) for i in spec]
#             for sp,spm in zip(spec, spec_midi):
#                 instruments[spm] = []
#                 for n in line:
#                     if n == sp:
#                         instruments[spm].append(1)
#                     else:
#                         instruments[spm].append(0)
#     print(instruments)
#     # to change
#     midiout = rtmidi.MidiOut()
#     midiout.open_port(0)
#     # send midi
#     counter = 0
#     while True:
#         counter += 1
#         for k,v in instruments.items():
#             index = counter%len(v)
#             if v[index] == 1:
#                 midiout.send_message(
#                         mido.Message('note_on',
#                                         channel=9,
#                                         note=k,
#                                         velocity=random.choice(range(70,90))).bin()
#                         )
#
#         time.sleep(0.125)


