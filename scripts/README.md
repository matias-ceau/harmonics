# Scripts

This directory contains modern, refactored versions of the command-line tools for harmonics.

## Scripts

### generate_music.py
Modern replacement for the root-level `generate_sequence.py`. 
- Uses the new `harmonics.ml.generation` module
- Proper argument parsing and error handling
- Configurable output options

```bash
python scripts/generate_music.py --model-path ./results --prompt "^" --temperature 0.7
```

### train_model.py  
Modern replacement for the root-level `trainer.py`.
- Uses the new `harmonics.ml.training` module
- Improved configuration and checkpointing
- Better error handling and logging

```bash
python scripts/train_model.py --tokens tokens.pt --output-dir ./results --epochs 10
```

### extract_midi.py
Modern replacement for the root-level `drum_extract.py`.
- Uses the new `harmonics.cli.analyze` module
- Batch processing capabilities
- Configurable output formats

```bash
python scripts/extract_midi.py --file-list midi_files.txt --output-dir ./extracted_data
```

## CLI Commands

You can also use the installed CLI commands after installing the package:

```bash
pip install -e .

# Generate music
harmonics-generate ml --model-path ./results --prompt "^"

# Train models  
harmonics-train --tokens tokens.pt --output-dir ./results

# Analyze MIDI files
harmonics-analyze batch midi_files.txt --output-dir ./extracted_data
```

## Migration from Old Scripts

The old scripts at the root level (`generate_sequence.py`, `trainer.py`, `drum_extract.py`) are deprecated and should be replaced with these new versions that use the reorganized codebase.