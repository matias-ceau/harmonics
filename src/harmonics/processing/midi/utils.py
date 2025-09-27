import numpy as np
import rtmidi
import time

from ...core.midi import MIDI_CC, DRUM_PROG, MIDI_GM1, DRUM_KEYMAP, MIDIMESSAGE
from ...core.notes import NDICT


def play_bytes(bytes_data,
               tick_durations=None,
               ticks_per_beat=192,
               bpm=120,
               durations=None,
               create_port=True,
               port_name='CH345:CH345 MIDI 1 32:0',
               choose_port=False,
               speed=1):
    midiout = rtmidi.MidiOut()
    ports = midiout.get_ports()
    choice = '\n'.join([f"{n} : {p}" for n, p in enumerate(ports)])
    if choose_port:
        print(choice)
        midiout.open_port(int(input('\nChoose a port!')))
    elif create_port:
        midiout.open_virtual_port('RTMIDI_SPECIAL37')
    else:
        try:
            port = ports.index(port_name)
            midiout.open_port(port)
        except ValueError:
            print('\nDefault port does not exist!\n', choice)
            midiout.open_port(int(input('\nChoose a port!')))
    if durations:
        pass
    elif tick_durations:
        durations = [_*60/(ticks_per_beat*bpm) for _ in tick_durations]
    else:
        durations = [0.5]*len(bytes_data)
    durations = [speed*i for i in durations]
    for n, d in zip(bytes_data, durations):
        midiout.send_message(n)
        time.sleep(d)
    #midiout.close_port()
    midiout.delete()


class MidiUtils:

    @classmethod
    def quantitize(cls, n):
        bins = np.array([0, 0.125, 0.29, 0.4, 0.58, 0.7, 0.875])
        vals = np.array([0, 0.25,  0.33, 0.5, 0.66, 0.75, 0])
        return vals[np.digitize(n, bins)-1]

    @classmethod
    def midi_cc(cls, data1):
        return MIDI_CC.get(data1)

    @classmethod
    def midi_program(cls, channel, data1):
        if channel == 9:
            return DRUM_PROG.get(data1)
        else:
            return MIDI_GM1.get(data1)

    @classmethod
    def midi_drum(cls, midi):
        return DRUM_KEYMAP.get(midi)

    @classmethod
    def midi_to_note(cls, midi):
        return [a for a, b in NDICT.items() if midi % 12 == b][0]

    @classmethod
    def midi_octave(cls, midi):
        return (midi//12)-1

    @classmethod
    def midi_to_name(cls, midi):
        return ''.join([cls.midi_to_note(midi), str(cls.midi_octave(midi))])
