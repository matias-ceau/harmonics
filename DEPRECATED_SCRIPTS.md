# Deprecated Scripts

The following scripts at the root level are deprecated and should not be used:

## generate_sequence.py
**DEPRECATED** - Use `scripts/generate_music.py` or `harmonics-generate` CLI command instead.

Issues with the old script:
- Hardcoded model path `/home/matias/git/harmonics/results`
- No proper error handling
- Limited configuration options

## trainer.py
**DEPRECATED** - Use `scripts/train_model.py` or `harmonics-train` CLI command instead.

Issues with the old script:
- Hardcoded paths
- No proper configuration management
- Poor error handling
- Unclear resumption logic

## drum_extract.py
**DEPRECATED** - Use `scripts/extract_midi.py` or `harmonics-analyze` CLI command instead.

Issues with the old script:
- Hardcoded file paths
- No command-line interface
- Limited error handling
- Not modular

## Migration Guide

### Old: generate_sequence.py
```bash
python generate_sequence.py "prompt"
```

### New: Using scripts
```bash
python scripts/generate_music.py --model-path ./results --prompt "prompt"
```

### New: Using CLI
```bash
harmonics-generate ml --model-path ./results --prompt "prompt"
```

### Old: trainer.py  
```bash
python trainer.py
```

### New: Using scripts
```bash
python scripts/train_model.py --tokens tokens.pt --output-dir ./results
```

### New: Using CLI
```bash
harmonics-train --tokens tokens.pt --output-dir ./results
```

### Old: drum_extract.py
```bash
python drum_extract.py  # No CLI interface
```

### New: Using scripts
```bash
python scripts/extract_midi.py --file-list files.txt --output-dir ./data
```

### New: Using CLI
```bash
harmonics-analyze batch files.txt --output-dir ./data
```

These old scripts will be removed in a future version. Please migrate to the new structure.