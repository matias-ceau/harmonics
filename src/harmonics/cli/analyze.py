"""
Command line interface for music analysis.

This module provides CLI access to music analysis tools.
"""

import sys
import argparse
import logging
from pathlib import Path
import numpy as np

from ..processing.midi.drum_extraction import extract_midi_data

logger = logging.getLogger(__name__)


def analyze_midi_file(args: argparse.Namespace) -> None:
    """Analyze a MIDI file and extract drum data."""
    try:
        file_path = Path(args.input_file)
        if not file_path.exists():
            logger.error(f"MIDI file not found: {file_path}")
            sys.exit(1)
        
        logger.info(f"Analyzing MIDI file: {file_path}")
        
        # Extract MIDI data
        midi_data, last_time_tick = extract_midi_data(str(file_path))
        
        if midi_data is None:
            logger.error("Failed to extract MIDI data")
            sys.exit(1)
        
        # Print analysis results
        print(f"MIDI Analysis Results for: {file_path.name}")
        print(f"Shape: {midi_data.shape}")
        print(f"Last time tick: {last_time_tick}")
        print(f"Total notes: {np.sum(midi_data)}")
        print(f"Active drum tracks: {np.sum(np.any(midi_data, axis=1))}")
        
        # If output file specified, save the data
        if args.output_file:
            output_path = Path(args.output_file)
            np.save(output_path, midi_data)
            logger.info(f"MIDI data saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"MIDI analysis failed: {e}")
        sys.exit(1)


def batch_analyze_midi(args: argparse.Namespace) -> None:
    """Analyze multiple MIDI files in batch."""
    try:
        file_list_path = Path(args.file_list)
        if not file_list_path.exists():
            logger.error(f"File list not found: {file_list_path}")
            sys.exit(1)
        
        # Read file paths
        with open(file_list_path, 'r') as f:
            file_paths = [line.strip() for line in f.readlines()]
        
        logger.info(f"Processing {len(file_paths)} MIDI files")
        
        # Initialize accumulation arrays
        notes = 47
        time_ticks = 30_000
        counts = np.zeros((notes, time_ticks), dtype=np.int64)
        files_count_per_tick = np.zeros(time_ticks, dtype=np.int64)
        
        successful_files = 0
        
        for file_path in file_paths:
            midi_data, last_time_tick = extract_midi_data(file_path)
            if midi_data is not None:
                counts += midi_data
                slice_index = min(last_time_tick, 29_999)
                files_count_per_tick[:slice_index] += 1
                successful_files += 1
                logger.info(f"Processed: {file_path}")
        
        # Calculate probabilities
        probabilities = counts / np.maximum(files_count_per_tick, 1)
        
        print(f"Batch Analysis Results:")
        print(f"Successfully processed: {successful_files}/{len(file_paths)} files")
        print(f"Output shape: {probabilities.shape}")
        
        # Save results
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(exist_ok=True)
            
            np.save(output_dir / 'note_probabilities.npy', probabilities)
            np.save(output_dir / 'counts.npy', counts)
            np.save(output_dir / 'files_count_per_tick.npy', files_count_per_tick)
            
            logger.info(f"Results saved to: {output_dir}")
        
    except Exception as e:
        logger.error(f"Batch analysis failed: {e}")
        sys.exit(1)


def main() -> None:
    """Main CLI entry point for analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze music files"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Analysis commands')
    
    # Single file analysis
    single_parser = subparsers.add_parser('single', help='Analyze single MIDI file')
    single_parser.add_argument('input_file', help='Input MIDI file')
    single_parser.add_argument('--output-file', 
                              help='Output file for extracted data (.npy)')
    single_parser.set_defaults(func=analyze_midi_file)
    
    # Batch analysis
    batch_parser = subparsers.add_parser('batch', help='Batch analyze MIDI files')
    batch_parser.add_argument('file_list', 
                             help='Text file containing list of MIDI file paths')
    batch_parser.add_argument('--output-dir', required=True,
                             help='Output directory for results')
    batch_parser.set_defaults(func=batch_analyze_midi)
    
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Call appropriate function
    args.func(args)


if __name__ == '__main__':
    main()