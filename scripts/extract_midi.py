#!/usr/bin/env python3
"""
Modern replacement for drum_extract.py

Usage:
    python scripts/extract_midi.py --file-list midi_files.txt --output-dir ./extracted_data
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path so we can import harmonics
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from harmonics.cli.analyze import batch_analyze_midi

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Extract drum data from MIDI files"
    )
    parser.add_argument(
        "--file-list", 
        required=True,
        help="Text file containing list of MIDI file paths"
    )
    parser.add_argument(
        "--output-dir", 
        required=True,
        help="Output directory for extracted data"
    )
    parser.add_argument(
        "--batch-size", 
        type=int, 
        default=1000,
        help="Batch size for processing (default: 1000)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Use the batch analysis function from CLI module
    batch_analyze_midi(args)


if __name__ == "__main__":
    main()