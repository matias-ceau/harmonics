import pandas as pd
import numpy as np
import mido

def extract_midi_data(file_path):
    '''Extract data of a midi file, outputs a numpy array of shape (47, 30000) and the last drum note time tick'''
    
    def get_drum_notes_with_absolute_time(track, k):
        '''helper function that gets the notes from each midi track'''
        track_drum_notes = []
        absolute_time = 0
    
        for msg in track:
            absolute_time += int(msg.time * k / 10)
            if msg.type == 'note_on' and msg.channel == 9 and msg.velocity != 0:
                track_drum_notes.append((msg.note, absolute_time))
    
        return track_drum_notes
    
    try: 
        # GET ALL DRUM NOTES
        mid = mido.MidiFile(file_path)
        k = int(480 / mid.ticks_per_beat)   
        drum_notes = []
        for track in mid.tracks:
            drum_notes.extend(get_drum_notes_with_absolute_time(track, k))
        df = pd.DataFrame(drum_notes, columns=['note', 'time'])
        
        # Ensure time does not exceed 30,000
        df = df[df['time'] < 30_000]
        
        if df.empty:
            return None, 0
        
        # CONVERT MIDI NOTES TO ARRAY INDEX
        df['note_as_index'] = df['note'].apply(lambda x: x - 35)
        df = df[(df['note'] > 35) & (df['note'] <= 81)][['time', 'note_as_index']]
    
        # CREATE EMPTY NUMPY ARRAY
        array = np.zeros((47, 30_000), dtype=bool)
    
        # CHANGE TO TRUE WHERE NOTES ARE PRESENT
        for note in df['note_as_index'].unique():
            timetick = df[df['note_as_index'] == note]['time'].to_numpy()
            array[note, timetick] = True
        
        last_time_tick = df['time'].max()
        
        return array, last_time_tick
    except Exception as e:
        print(e)
        return None, 0

def process_files_in_batches(file_paths, batch_size=1000):
    notes = 47
    time_ticks = 30_000
    counts = np.zeros((notes, time_ticks), dtype=np.int64)
    files_count_per_tick = np.zeros(time_ticks, dtype=np.int64)

    for i in range(0, len(file_paths), batch_size):
        batch_files = file_paths[i:i+batch_size]
        for file_path in batch_files:
            midi_data, last_time_tick = extract_midi_data(file_path)
            if midi_data is not None:
                counts += midi_data
                slice_index = last_time_tick if (last_time_tick < 29_999) else 29_999
                files_count_per_tick[:slice_index] += 1
                print(f"SUCCESS: extracted {file_path}!")

    probabilities = counts / files_count_per_tick
    print(f"Extracted {files_count_per_tick[0]} files.")
    return probabilities, counts, files_count_per_tick 

# Read file paths from the text file
with open('/home/matias/FAST_DATA/harmonics/lahk_full_paths.txt', 'r') as f:
    file_paths = [line.strip() for line in f.readlines()]

# Process files and compute probabilities
probabilities, counts, files_count_per_tick = process_files_in_batches(file_paths, batch_size=1000)

# Save the probabilities array to a file if needed
np.save('FAST_DATA/note_probabilities.npy', probabilities)
np.save('FAST_DATA/counts.npy', counts)
np.save('FAST_DATA/files_count_per_tick.npy', files_count_per_tick)

print(probabilities.shape)  # Should be (47, 30_000)

