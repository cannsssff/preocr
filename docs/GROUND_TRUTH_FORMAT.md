# Ground Truth File Format

## What is `scripts/ground_truth.json`?

The `scripts/ground_truth.json` file contains the **known correct answers** (labels) for your test files. It tells the validation script which files actually need OCR and which don't, so it can compare PreOCR's predictions against the truth.

## File Format

The ground truth file is a JSON file with one of two formats:

### Format 1: Array of Objects (Recommended)

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
  },
  {
    "file": "/path/to/image.png",
    "needs_ocr": true,
    "notes": "Image file, always needs OCR"
  }
]
```

### Format 2: Simple Dictionary

```json
{
  "/path/to/document.pdf": false,
  "/path/to/scanned.pdf": true,
  "/path/to/image.png": true
}
```

## Creating a Ground Truth File

### Method 1: Use Template Generator (Easiest)

```bash
# Create template from your test directory
python scripts/validate_accuracy.py --create-template /path/to/test/files

# This creates scripts/ground_truth.json with all files, but needs_ocr is set to null
# Edit the file and set needs_ocr: true or false for each file
```

**Example output:**
```json
[
  {
    "file": "/path/to/test/files/document1.pdf",
    "needs_ocr": null,
    "notes": ""
  },
  {
    "file": "/path/to/test/files/document2.pdf",
    "needs_ocr": null,
    "notes": ""
  }
]
```

Then edit it to:
```json
[
  {
    "file": "/path/to/test/files/document1.pdf",
    "needs_ocr": false,
    "notes": "Digital PDF"
  },
  {
    "file": "/path/to/test/files/document2.pdf",
    "needs_ocr": true,
    "notes": "Scanned PDF"
  }
]
```

### Method 2: Create Manually

Create a JSON file with your labels:

```json
[
  {
    "file": "document.pdf",
    "needs_ocr": false
  },
  {
    "file": "scanned.pdf",
    "needs_ocr": true
  }
]
```

## Field Descriptions

- **`file`**: Path to the file (can be full path or just filename)
- **`needs_ocr`**: Boolean (`true` or `false`)
  - `true`: File actually needs OCR (scanned PDF, image, etc.)
  - `false`: File does NOT need OCR (digital PDF, text file, etc.)
- **`notes`**: (Optional) Any notes about the file

## Example Ground Truth File

Here's a complete example:

```json
[
  {
    "file": "digital_document.pdf",
    "needs_ocr": false,
    "notes": "Digital PDF created from Word, has extractable text"
  },
  {
    "file": "scanned_letter.pdf",
    "needs_ocr": true,
    "notes": "Scanned PDF, appears to be scanned document"
  },
  {
    "file": "photo.png",
    "needs_ocr": true,
    "notes": "Image file, always needs OCR"
  },
  {
    "file": "report.docx",
    "needs_ocr": false,
    "notes": "Office document with text content"
  },
  {
    "file": "empty_slide.pptx",
    "needs_ocr": true,
    "notes": "PowerPoint with only images, no text"
  },
  {
    "file": "data.txt",
    "needs_ocr": false,
    "notes": "Plain text file"
  }
]
```

## How to Determine Ground Truth

### Files that DON'T need OCR (`needs_ocr: false`):
- ✅ Digital PDFs with extractable text
- ✅ Text files (.txt, .csv)
- ✅ Office documents with text content (.docx, .pptx, .xlsx)
- ✅ Structured data (JSON, XML)
- ✅ HTML files with text

### Files that DO need OCR (`needs_ocr: true`):
- ✅ Scanned PDFs (no extractable text)
- ✅ Image files (.png, .jpg, .tiff, etc.)
- ✅ Office documents that are mostly images
- ✅ PDFs with scanned pages

### How to Check:

**For PDFs:**
```python
# Try extracting text - if you get meaningful text, needs_ocr = false
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
    if text and len(text.strip()) > 50:
        needs_ocr = False  # Has extractable text
    else:
        needs_ocr = True   # No extractable text (scanned)
```

**For Images:**
- Always `needs_ocr: true` (images always need OCR)

**For Office Docs:**
- Check if document has text content
- If mostly images/graphics → `needs_ocr: true`
- If has text → `needs_ocr: false`

## Using the Ground Truth File

Once you have `scripts/ground_truth.json`:

```bash
# Run validation
python scripts/validate_accuracy.py /path/to/test/files --ground-truth scripts/ground_truth.json

# The script will:
# 1. Read ground truth labels
# 2. Run PreOCR on each file
# 3. Compare predictions vs ground truth
# 4. Calculate accuracy metrics
```

## Tips

1. **Use absolute paths** for more reliable matching
2. **Be consistent** with your labeling
3. **Include edge cases** (mixed PDFs, low-quality scans)
4. **Document your decisions** in the `notes` field
5. **Start small** - validate on 50-100 files first, then expand

## File Matching

The validation script matches files by:
1. Full path match
2. Filename match (if full path doesn't match)

So you can use either:
- Full paths: `"/home/user/documents/file.pdf"`
- Just filenames: `"file.pdf"` (if files are in the test directory)

## Example Workflow

```bash
# 1. Create template
python scripts/validate_accuracy.py --create-template ./test_files

# 2. Edit scripts/ground_truth.json (set needs_ocr for each file)

# 3. Run validation
python scripts/validate_accuracy.py ./test_files --ground-truth scripts/ground_truth.json

# 4. Review results and accuracy metrics
```

## Troubleshooting

**Q: File not found in ground truth?**
- Check file paths match
- Use absolute paths if relative paths don't work
- Check filename spelling

**Q: How many files do I need?**
- Minimum: 50-100 files
- Recommended: 500+ files
- Ideal: 1000+ files with diverse types

**Q: Can I use relative paths?**
- Yes, but absolute paths are more reliable
- The script tries to match by filename if full path doesn't match

