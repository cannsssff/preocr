# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-12-28

### Added
- **Page-level detection**: Analyze PDFs page-by-page to identify which pages need OCR
- **Reason codes**: Structured reason codes (e.g., `PDF_DIGITAL`, `IMAGE_FILE`) for programmatic decision handling
- **Enhanced confidence scoring**: Improved confidence calculation with page-level analysis support
- New `page_level` parameter to `needs_ocr()` function for PDF page-level analysis
- `reason_code` field in API response for structured decision tracking
- Support for mixed PDFs (some pages digital, some scanned)

### Changed
- Decision engine now returns reason codes in addition to human-readable reasons
- Confidence scores are more nuanced based on page-level analysis
- API response structure enhanced with `reason_code` field

### Example Usage
```python
# Page-level analysis
result = needs_ocr("document.pdf", page_level=True)
for page in result["pages"]:
    if page["needs_ocr"]:
        print(f"Page {page['page_number']} needs OCR: {page['reason']}")

# Reason codes
if result["reason_code"] == "PDF_MIXED":
    # Handle mixed PDF (some pages need OCR, some don't)
    pass
```

## [0.1.1] - 2024-12-28

### Changed
- Updated GitHub URLs in package metadata to point to correct repository
- Fixed license format in pyproject.toml (use string instead of table)
- Removed deprecated license classifier

## [0.1.0] - 2024-12-28

### Added
- Initial release
- File type detection using python-magic with fallback to mimetypes
- Text extraction probes for PDF, Office documents (DOCX, PPTX, XLSX), and plain text files
- Image analysis with entropy calculation
- Decision engine to determine if OCR is needed
- Main API: `needs_ocr()` function
- Comprehensive test suite
- Documentation and examples

[Unreleased]: https://github.com/yuvaraj3855/preocr/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.2.0
[0.1.1]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.1
[0.1.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.0

