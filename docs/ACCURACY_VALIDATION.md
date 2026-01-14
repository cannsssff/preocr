# Accuracy Validation Status

## Current Status

⚠️ **Accuracy claims need validation with real datasets.**

The claimed accuracy of **92-95%** is based on:
- Design expectations
- Limited testing
- Theoretical analysis

**This needs to be validated with proper ground truth datasets.**

## Validation Tools Created

### 1. `validate_accuracy.py`
- Validates predictions against ground truth labels
- Calculates accuracy, precision, recall, F1-score
- Provides confusion matrix
- Shows breakdown by file type

### 2. `benchmark_accuracy.py`
- Combines performance benchmarking with accuracy validation
- Measures both speed and accuracy
- Comprehensive reporting

### 3. `docs/VALIDATION_GUIDE.md`
- Complete guide on how to validate accuracy
- Instructions for creating ground truth datasets
- Metrics explanation
- Best practices

## Next Steps

1. **Create validation dataset**
   - Collect diverse set of files (PDFs, images, office docs)
   - Manually label each file (needs OCR: true/false)
   - Aim for 500+ files minimum, 1000+ ideal

2. **Run validation**
   ```bash
   python scripts/validate_accuracy.py /path/to/dataset --ground-truth scripts/ground_truth.json
   ```

3. **Document results**
   - Record accuracy metrics
   - Analyze errors
   - Update README with validated numbers

4. **Iterate**
   - Fix issues found
   - Re-validate
   - Improve accuracy

## Recommended Dataset Composition

For reliable validation:
- **Digital PDFs**: 200+ files (should not need OCR)
- **Scanned PDFs**: 200+ files (should need OCR)
- **Mixed PDFs**: 50+ files (some pages need OCR)
- **Images**: 50+ files (should need OCR)
- **Office docs with text**: 50+ files (should not need OCR)
- **Office docs without text**: 50+ files (should need OCR)
- **Text files**: 50+ files (should not need OCR)

**Total**: 650+ files minimum

## Accuracy Targets

Based on design and testing:
- **Overall Accuracy**: > 90%
- **Precision**: > 85% (few false positives)
- **Recall**: > 90% (few false negatives)
- **F1-Score**: > 87%

## Contributing Validation Data

If you validate PreOCR on your dataset:
1. Document dataset size and composition
2. Share metrics (can be anonymized)
3. Report any issues
4. Help improve accuracy

See [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) for detailed instructions.

