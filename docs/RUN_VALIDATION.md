# How to Run Validation

## Quick Start

### Step 1: Prepare Your Test Files

Create a directory with test files:
```bash
mkdir -p test_files
# Copy your PDFs, images, etc. to test_files/
```

### Step 2: Create Ground Truth Template

```bash
python scripts/validate_accuracy.py --create-template test_files
```

This creates `scripts/ground_truth.json` with all files found, but `needs_ocr` is set to `null`.

### Step 3: Edit Ground Truth File

Open `scripts/ground_truth.json` and set `needs_ocr` to `true` or `false` for each file:

```json
[
  {
    "file": "test_files/document.pdf",
    "needs_ocr": false,
    "notes": "Digital PDF"
  },
  {
    "file": "test_files/scanned.pdf",
    "needs_ocr": true,
    "notes": "Scanned PDF"
  }
]
```

### Step 4: Run Validation

```bash
# Basic validation
python scripts/validate_accuracy.py test_files --ground-truth scripts/ground_truth.json

# With layout-aware analysis
python scripts/validate_accuracy.py test_files --ground-truth scripts/ground_truth.json --layout-aware

# With page-level analysis
python scripts/validate_accuracy.py test_files --ground-truth scripts/ground_truth.json --page-level

# Save results to JSON
python scripts/validate_accuracy.py test_files --ground-truth scripts/ground_truth.json --output results.json
```

## Example Commands

```bash
# Create template from your files
python scripts/validate_accuracy.py --create-template /path/to/my/files

# Run validation (scripts/ground_truth.json is default)
python scripts/validate_accuracy.py /path/to/my/files

# Use custom ground truth file
python scripts/validate_accuracy.py /path/to/my/files --ground-truth my_labels.json

# Full example with all options
python scripts/validate_accuracy.py /path/to/my/files \
  --ground-truth scripts/ground_truth.json \
  --layout-aware \
  --output validation_results.json
```

## What You'll See

The script will:
1. Process each file in the directory
2. Compare PreOCR predictions vs ground truth
3. Calculate accuracy metrics:
   - Overall Accuracy
   - Precision
   - Recall
   - F1-Score
   - Confusion Matrix (TP, FP, TN, FN)
4. Show breakdown by file type
5. List incorrect predictions

## Output Example

```
Validating 100 files...
[1/100] document1.pdf... ✅ Correct
[2/100] scanned1.pdf... ✅ Correct
[3/100] image1.png... ❌ Wrong (GT: True, Pred: False)

================================================================================
📊 ACCURACY VALIDATION RESULTS
================================================================================

📁 Files:
   Total: 100
   Validated: 98
   Skipped: 2

📊 Confusion Matrix:
   True Positive (TP):   45 - Correctly identified as needing OCR
   False Positive (FP):   3 - Incorrectly flagged as needing OCR
   True Negative (TN):  48 - Correctly identified as not needing OCR
   False Negative (FN):   2 - Missed files that need OCR

🎯 Overall Metrics:
   Accuracy:  94.90%
   Precision: 93.75%
   Recall:    95.74%
   F1-Score:  94.74%
```

## Need Help?

- See `docs/GROUND_TRUTH_FORMAT.md` for detailed format explanation
- See `docs/VALIDATION_GUIDE.md` for complete validation guide

