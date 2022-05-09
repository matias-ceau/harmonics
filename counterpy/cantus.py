import numpy as np
import random
from typing import List, Callable, Tuple
import time
import pandas as pd

Sequence    = np.ndarray
Population  = List[Sequence]
FitnessList = List[Callable] 
FitnessFunc = Callable
MAX_RANGE = 12
MAX_LEAP  = 8
NOTES = np.hstack([np.arange(i+36,80,12) for i in [0,2,4,5,7,9,11]])


### COMMON
def no_repeted_notes(sequence: Sequence,*args) -> bool:
    '''True if there isn't any repeted notes'''
    return (np.diff(sequence) != 0).all()

def all_notes(sequence: Sequence,*args) -> bool:
    '''if sequence is longer than 10, it should contain all (ie 7) the notes'''
    if sequence.shape[0] >=10:
        return np.unique(sequence%12).shape[0] == 7
    else:
        return True

def mostly_stepwise(sequence: Sequence,*args) -> bool:
    '''True if 50% of intervals are less or equal to 2 semitones'''
    test = np.abs(np.diff(sequence))
    return (test[test <= 2].shape[0] >= sequence.shape[0]/2)
    
def single_climax(sequence: Sequence,*args) -> bool:
    '''True if climax appears only once'''
    idx = np.where(np.abs(sequence) == np.abs(sequence).max())[0]
    return (sequence[sequence == sequence[idx]].shape[0] == 1)

def leap_range_ok(sequence: Sequence,*args) -> bool:
    '''True if no leap above 8 semitones'''
    test = np.abs(np.diff(sequence))
    return test[test > MAX_LEAP].shape[0] == 0
                 
def leap_frequency_ok(sequence: Sequence,*args) -> bool:
    '''True if there isn't more than 3 consecutive leaps (more than 3 semitones)'''
    return (0 not in np.diff(np.diff(np.where( np.abs(np.diff(sequence)) >= 3)[0])))

def range_is_ok(sequence: Sequence,*args) -> bool:
    '''True if range is less than specified interval (in semitones)'''
    return sequence.max()-sequence.min() <= MAX_RANGE

def leap_balance_ok(sequence: Sequence,*args) -> bool:
     '''True if eventual leaps greater than p4 are counterbalanced by leaps in opposite directions (first tests the presence of such leaps, then identify if they are counterbalanced (half of sum of differences is still under p4)'''
     if np.abs(np.diff(sequence).max()) <= 5: return True
     else:
         idx = np.where(np.abs(np.diff(sequence)) >= 5)[0]
         test = [np.diff(sequence[i:i+3]) for i in idx]
         return np.sum([np.sign(np.prod(i)) == -1 for i in test]) + \
                 np.sum([np.abs(i[-1])>=5 for i in test])             == len(test)
   
### CANTUS SPECIFIC

def ante_is_leading(sequence: Sequence, *args) -> bool:
    '''True if antepenultian note is the leading tone above or below (based on assumption that all notes are diatonic'''
    return  0 < np.abs(sequence[-1]-sequence[-2]) <= 2

#### CANTUS FIRMUS
'''
single climax (ascending if cantus firmus)
generate a restrictive list of pitches for the random sequence based on climax (to limlit permutations)
antepenultian note is leading tone
range is less than 12 semitones
notes repeat
every note is present (if lenght > 10)
mostly stepwise (50% movement)
no leap greater than 8 semitones 
there is only 1 climax
no more than 2 consecutive leaps
leaps are in contrary motion if 2 consecutive
'''

cantus_list = [(ante_is_leading,   100),
               (range_is_ok,       100),
               (no_repeted_notes,  200),
               (all_notes,         50),
               (mostly_stepwise,   100),
               (single_climax,     50),
               (leap_range_ok,     40),
               (leap_frequency_ok, 30),
               (leap_balance_ok,   20)]

cantus_func   = [a for a,b in cantus_list]
cantus_scores = [b for a,b in cantus_list]
max_fit = len(cantus_list)


def generate_sequence(length: int, key_center: int, restricted_notes) -> Sequence:
    #start = 60
    #end   = random.choice([60,67])
    return np.concatenate(([key_center],np.random.choice(restricted_notes,size=length-2),[key_center]))

def generate_population(size: int, length: int, key_center: int, restricted_notes) -> Population:
    return [generate_sequence(length=length, key_center=key_center, restricted_notes=restricted_notes) for _ in range(size)]

def fitness(sequence: Sequence, functions: FitnessList, key: int) -> int:
    if key not in range(128): raise ValueError("Key should be a valid midi note (0-127")
    score = np.sum(np.array([f(sequence,key) for f in functions]))
    return score

def pair_selection(population,
                   weights) -> Population:
    return random.choices(
           population = population,
           weights    = [i*max_fit/3 for i in weights],
           k=2
           )

def single_point_crossover(a: Sequence, b: Sequence) -> Tuple[Sequence, Sequence]:
    if len(a) != len(b):
        raise ValueError('Sequence length must match!')
    if len(a) == 2: return a,b
    p = random.randint(1, len(a)-1)
    return np.hstack((a[0:p],b[p:])),np.hstack((b[0:p],a[p:]))

def mutation(sequence: Sequence, restricted_notes, num: int = 1, probability: float = 0.5) -> Sequence:
    for _ in range(num):
        index = random.randrange(1,sequence.shape[0]-1)
        note  = random.choice(restricted_notes)
        sequence[index] = sequence[index] if random.random() > probability else note
    return sequence


def run_evolution(
        sequence_length: int = 10,
        key_center:      int = 60,
        fitness_limit  = max_fit,
        population_size: int = 100,
        fitness_list   = cantus_func,
        #fitness_weight = cantus_scores,
        fitness_func   = fitness,
        sequence_gen   = generate_sequence,
        population_gen = generate_population,
        pair           = pair_selection,
        crossover      = single_point_crossover,
        mut            = mutation,
        mut_proba: float = 0.5,
        mut_nb:    int   = 3,
        generation_limit = 1000) -> Tuple[Population, int]: 
    
    start = time.time()
    if key_center not in [60,62,64,65,67,69,71]: raise ValueError('Wrong octave for generation!')
    climax = random.choice([i for i in NOTES if MAX_LEAP < np.abs(key_center - i) <= MAX_RANGE])
    restricted_notes = [i for i in NOTES if (np.abs(climax-i) <= MAX_RANGE) and (np.abs(key_center-i) <= MAX_RANGE)]
    population = generate_population(size=population_size,
                                     length=sequence_length,
                                     key_center=key_center,
                                     restricted_notes=restricted_notes)
    
    max_scores = []
    for i in range(generation_limit):
        popD = pd.DataFrame({"sequence":population,
                          "score"    :[fitness_func(sequence=seq,
                                                   functions=fitness_list,
                                                   key=key_center) for seq in population]})
        popD.sort_values("score",inplace=True,ascending=False)
        
        max_scores.append(np.max(popD.score))
        
        pp = '\n'.join([f"""{str(popD.loc[i,"sequence"])} {popD.loc[i,"score"]}""" for i in popD.index])
        print(f"""Generation {i}\n{pp}""")
        if popD.score.max() >= fitness_limit:
            end = time.time()
            print(f'Found a cantus in {round((end -start)*1000,2)} ms!')
            print(popD[popD.score == popD.score.max()].sequence)
            break
        
        next_generation = popD.sequence.tolist()[:2]
        
        print('Generating crossover mutation...')
        if np.sum(popD.score) == 0: popD.score += 0.01
        bad_pop  = popD[(popD.score <0.5*max_fit)].sequence.tolist()
        good_pop = popD[(popD.score >=0.5*max_fit) & (popD.score < 0.8*max_fit)].sequence.tolist()
        for j in range(int(len(bad_pop) / 2) - 1 - int(len(bad_pop)*0.1)):
            parent_a,parent_b = pair(popD.sequence,popD.score)
            offspring_a,offspring_b = crossover(parent_a,parent_b)
            offspring_a = mut(offspring_a,restricted_notes,mut_nb,mut_proba)
            offspring_b = mut(offspring_b,restricted_notes,mut_nb,mut_proba)
            next_generation += [offspring_a,offspring_b]
        for g in good_pop:
            next_generation += [mut(g,restricted_notes,mut_nb*2,mut_proba*2)]
            
        n = np.abs(population_size - len(next_generation))
        population = next_generation + generate_population(n, sequence_length, key_center, restricted_notes=restricted_notes)
        
    # population = sorted(
    #     population,
    #     key=lambda seq: fitness_func(sequence=seq,functions=fitness_list,key=key_center),
    #     reverse=True)
    
    winners = popD[popD.score == popD.score.max()].sequence
    return [i for i in winners],np.max(max_scores)
    
# def cantus_gen(key,mode,lenght):
#     '''generates random sequences of n notes (lenght), chooses a climax and decides of a restrictive pitch collection based on it, then tests all conditions and repeats first 3 steps if condition fails'''
#     #create array of all pitches in given key + mode 
#     full_pitches = full_pitch_gen(key,mode)
#     # chose a climax (ascending if cantus firmus)
#     climax = climax_choser(key,full_pitches,12,direction=1)
#     # generate a restrictive list of pitches for the random sequence based on climax (to limlit permutations)
#     cantus_pitches = restricted_pitch_gen(key,climax,full_pitches)
#     while True:
#         # random sequence
#         sequence = sequence_gen(key,key,lenght,cantus_pitches)
#         print(sequence)
#         if ante_is_leading(sequence,key):
#             #print("antepenultian note is leading tone")
#             if range_is_ok(sequence,12):
#                 #print("range is less than 12 semitones")
#                 if no_repeted_notes(sequence):
#                     #print("notes repeat")
#                     if all_notes(sequence):
#                         #print("every note is present (if lenght > 10)")
#                         if mostly_stepwise(sequence):
#                             #print("50% movement is stepwise")
#                             if leap_range_ok(sequence,8):
#                                 #print("no leap greater than 8 semitones ")
#                                 if single_climax(climax,sequence):
#                                     #print("there is only 1 climax")
#                                     if leap_frequency_ok(sequence):
#                                         #print("no more than 2 consecutive leaps")
#                                         if leap_balance_ok(sequence):
#                                             #print("leaps are in contrary motion if 2 consecutive")
#                                             return sequence


# dissonant outline TT,7
# tonic or dominant outlined triad
# leap bask to same note
# leap more than a third to penultimate note

