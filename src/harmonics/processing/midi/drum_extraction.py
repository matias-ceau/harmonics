"""
MIDI drum extraction utilities.

This module provides functions for extracting drum patterns from MIDI files.
"""

import pandas as pd
import numpy as np
import mido
from typing import Optional, Tuple


def extract_midi_data(file_path: str) -> Tuple[Optional[np.ndarray], int]:
    """
    Extract data of a midi file, outputs a numpy array of shape (47, 30000) and the last drum note time tick.
    
    Args:
        file_path: Path to the MIDI file
        
    Returns:
        Tuple of (midi_data, last_time_tick) where:
        - midi_data: Boolean array of shape (47, 30000) or None if extraction failed
        - last_time_tick: Time tick of the last drum note
    """
    
    def get_drum_notes_with_absolute_time(track, k):
        """Helper function that gets the notes from each midi track."""
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
        print(f"Error processing {file_path}: {e}")
        return None, 0


def process_files_in_batches(file_paths: list, batch_size: int = 1000) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Process multiple MIDI files in batches to compute probabilities.
    
    Args:
        file_paths: List of file paths to process
        batch_size: Number of files to process in each batch
        
    Returns:
        Tuple of (probabilities, counts, files_count_per_tick)
    """
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

    probabilities = counts / np.maximum(files_count_per_tick, 1)
    print(f"Extracted {files_count_per_tick[0]} files.")
    return probabilities, counts, files_count_per_tick