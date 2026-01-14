# Accuracy Validation Guide

## Overview

This guide explains how to validate PreOCR accuracy claims and run comprehensive benchmarks.

## Accuracy Claims

PreOCR claims **92-95% accuracy** with the hybrid pipeline (heuristics + OpenCV refinement). This needs to be validated with real data.

## Validation Process

### Step 1: Prepare Ground Truth Dataset

Create a ground truth file with known labels for your test files:

```bash
# Create a template from your test directory
python scripts/validate_accuracy.py --create-template /path/to/test/files

# This creates scripts/ground_truth.json - edit it to set needs_ocr: true/false for each file
# Or use auto-labeling helper:
python scripts/auto_label_ground_truth.py scripts/scripts/ground_truth.json
```

**Ground Truth File Format:**

```json
[
  {
    "file": "/path/to/document.pdf",
    "needs_ocr": false,
    "notes": "Digital PDF with extractable text"
  },
  {
    "file": "/path/to/scanned.pdf",
    "needs_ocr": true,
    "notes": "Scanned PDF, no extractable text"
  }
]
```

### Step 2: Run Validation

```bash
# Basic validation
python scripts/validate_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json

# With layout-aware analysis
python scripts/validate_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json --layout-aware

# With page-level analysis
python scripts/validate_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json --page-level

# Save results to file
python scripts/validate_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json --output results.json
```

### Step 3: Run Comprehensive Benchmark

Benchmark both performance AND accuracy:

```bash
python scripts/benchmark_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json
```

## Metrics Explained

### Accuracy
- **Overall Accuracy**: Percentage of correct predictions
- **Formula**: (TP + TN) / Total × 100%

### Precision
- **Definition**: Of all files predicted as "needs OCR", how many actually need OCR?
- **Formula**: TP / (TP + FP) × 100%
- **High precision** = Few false positives (not flagging digital docs as needing OCR)

### Recall
- **Definition**: Of all files that actually need OCR, how many did we catch?
- **Formula**: TP / (TP + FN) × 100%
- **High recall** = Few false negatives (not missing files that need OCR)

### F1-Score
- **Definition**: Harmonic mean of precision and recall
- **Formula**: 2 × (Precision × Recall) / (Precision + Recall)
- **Balanced metric** that considers both precision and recall

### Confusion Matrix

```
                Predicted
              Needs OCR  No OCR
Actual Needs OCR   TP      FN
      No OCR        FP      TN
```

- **TP (True Positive)**: Correctly identified as needing OCR
- **FP (False Positive)**: Incorrectly flagged as needing OCR (Type I error)
- **TN (True Negative)**: Correctly identified as not needing OCR
- **FN (False Negative)**: Missed files that need OCR (Type II error)

## Recommended Dataset Size

For reliable accuracy estimates:
- **Minimum**: 100 files per category (digital PDFs, scanned PDFs, images, etc.)
- **Recommended**: 500+ files total
- **Ideal**: 1000+ files with diverse document types

## Validation Checklist

- [ ] Create ground truth dataset with known labels
- [ ] Run validation on test dataset
- [ ] Calculate accuracy metrics
- [ ] Review confusion matrix
- [ ] Analyze errors (false positives/negatives)
- [ ] Test with different configurations (layout-aware, page-level)
- [ ] Document results

## Interpreting Results

### Good Results
- **Accuracy > 90%**: Good overall performance
- **Precision > 85%**: Few false positives
- **Recall > 90%**: Few false negatives
- **F1-Score > 87%**: Good balance

### Areas for Improvement
- **Low Precision**: Too many false positives → Adjust thresholds
- **Low Recall**: Too many false negatives → Improve detection logic
- **Low Accuracy**: Overall issues → Review decision logic

## Example Output

```
📊 ACCURACY VALIDATION RESULTS
================================================================================

📁 Files:
   Total: 500
   Validated: 485
   Skipped: 15

📊 Confusion Matrix:
   True Positive (TP):  245 - Correctly identified as needing OCR
   False Positive (FP):  18 - Incorrectly flagged as needing OCR
   True Negative (TN):  210 - Correctly identified as not needing OCR
   False Negative (FN):  12 - Missed files that need OCR

🎯 Overall Metrics:
   Accuracy:  93.81%
   Precision: 93.16%
   Recall:    95.33%
   F1-Score:  94.23%

📋 Accuracy by File Type:
   pdf         94.2% (245/260 files)
                  Precision: 93.1%, Recall: 95.3%
   image      100.0% (50/50 files)
                  Precision: 100.0%, Recall: 100.0%
   office      88.5% (115/130 files)
                  Precision: 87.2%, Recall: 90.1%
```

## Best Practices

1. **Use diverse dataset**: Include various document types, sizes, and qualities
2. **Label carefully**: Ensure ground truth labels are accurate
3. **Test edge cases**: Include difficult cases (mixed PDFs, low-quality scans)
4. **Run multiple times**: Validate consistency
5. **Document methodology**: Keep records of how ground truth was created
6. **Update regularly**: Re-validate as code changes

## Current Status

⚠️ **Note**: The 92-95% accuracy claim needs validation with a real dataset. Use this guide to:
1. Create your own validation dataset
2. Run validation
3. Report results
4. Update accuracy claims based on actual measurements

## Contributing Validation Data

If you have validation results, please:
1. Document your dataset (size, composition)
2. Share metrics (anonymized if needed)
3. Report any issues found
4. Help improve the validation tools

