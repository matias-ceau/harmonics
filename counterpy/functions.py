import numpy as np
import random

from cantus import Sequence
from cantus import max_leap,max_range
# GENERAL UTILITIES===============================================================================================================
#================================================================================================================================

# def full_pitch_gen(key,mode):
#     '''return array of midi notes relative to a key center and intervals specified in mode (given as a list of intervals)'''
#     return np.array([a + sum(mode[:n]) for a in list(range(key%12,127,12)) for n in range(len(mode))])

# def climax_choser(key,full_pitches,maxr,direction=0):
#     '''chooses a climax (at least 3 st up or down)  based on a note (key) and a maximum range up or down (maxr)'''
#     while True:
#         climax = random.choices(full_pitches)[0]
#         if direction == 0:
#             if 3 < abs(key - climax) <= maxr:
#                 return climax
#         else:
#             if 3 < climax - key <= maxr:
#                 return climax

# def restricted_pitch_gen(key,climax, full_pitches):
#     '''generate a shortened list of available pitches based on climax'''
#     if climax - key > 0:
#         return full_pitches[(full_pitches >= climax-12) & (full_pitches <= climax)]
#     if climax - key < 0:
#         return full_pitches[(full_pitches >= climax) & (full_pitches <= climax+12)]

# def sequence_gen(start,end,lenght,cantus_pitches):
#     '''generate a random sequence based on elements of a pitch collection'''
#     return np.asarray([start] + list(np.random.choice(cantus_pitches,lenght-2)) + [end])
    
# CONDITIONS======================================================================================================================
#================================================================================================================================

# common-------------------------------------------------------------------------------
#========================================


# voice specific-----------------------------------------------------------------------
#========================================
def ante_differ(cantus,voice):
    '''checks that antepenultian note is different between two sequences'''
    return cantus[-2]%12 != voice[-2]%12

def contrary_when_perfect(cantus,voice):
    '''checks that there is contrary motion when intervals are perfect'''
    return

def voice_start(cantus,position):
    '''selects starting note to a voice'''
    if position == "above": # note 1, 3, 5, 8
        return cantus[0] + random.choice([0,5,7,12])
    if position == "below": # note 1, 8
        return cantus[0] + random.choice([0,-12])

def voice_end(cantus,position):
    '''selects ending note to a voice'''
    if position == 'above':
        return cantus[0] + random.choice([0,12])
    if position == 'below':
        return cantus[0] + random.choice([0,-12])

def select_note(note,consonance,key_mod):
    '''selects consonant note for harmony'''
    return random.choice([i for i in np.array(consonance)+note if i%12 in key_mod])

def harmonize(cantus,position,consonance,key_mod):
    '''creates candidate voice using functions voice_end/start and select_note'''
    ca = [i for i in consonance if i >= 0]
    cb = [i for i in consonance if i <= 0]
    start = [voice_start(cantus,position)]
    if position == "above":
        middle = np.array([select_note(n,ca,key_mod) for n in cantus[1:-1]])
    if position == "below":
        middle = np.array([select_note(n,cb,key_mod) for n in cantus[1:-1]])
    end = [voice_end(cantus,position)]
    return np.concatenate((start,middle,end))

