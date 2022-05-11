import numpy as np
from midiutil.MidiFile import MIDIFile as MD
import random
import time
import sys

from data import *
from functions import *

#---------------------------------------------------------------------------------------------
### VOICE 2 (while loop and iteration until ok)
''' step by step procedure
rules:
- start not u, p5 or octave
- end not u or octave
- all notes included in 10 notes intervalls
- only consonant intervals between voices (p4, p5, M3, m3, m6, M6) but watch out and calculate the opposite to (modulo 12)
- no more than two perfect intervals in a row
- >50% stepwise motion
- parallel motion only 3 times in a row
- if perfect interval, check that there is contrary motion
- largest interval = p12 ie 16 semitones
'''
def voice_gen(cantus,key=None,mode=None,position="random",consonance="standard"):
    if consonance == "standard": consonance = [-5,5,-7,7,-4,4,-3,3,-8,8,-9,9]#p4, p5, M3, m3, m6, M6
    if position == "random": position = random.choice(["above","below"])
    key_mod = read_key(key,mode,cantus)
    # start u, p5 or octave, end not u or octave, only consonant intervals between voices (p4, p5, M3, m3, m6, M6)
    while True:
        voice = harmonize(cantus,position,consonance,key_mod)
        print(voice)
        if all_notes(voice):
            if mostly_stepwise(voice):
                if no_repeted_notes(voice):
                    if leap_range_ok(voice,8):
                        if single_climax(voice.max(),voice):
                            if ante_is_leading(voice,cantus[0]):
                                if ante_differ(cantus,voice):
                                    if range_is_ok(voice,16):
                                        if position == "above":
                                            voice = voice+12
                                        if position == "below":
                                            voice = voice-12
                                        return voice

    # if perfect interval, check that there is contrary motion
    # largest interval = p12 ie 16 semitones
    # all notes included in 10 notes intervalls
    
if __name__ == "__main__":
    cantus = np.array(sys.argv[1].split(" "),dtype="int")
    voice_gen(cantus)
