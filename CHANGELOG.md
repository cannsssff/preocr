# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2024-12-31

### Added
- **Custom Exception Classes**: Added comprehensive exception hierarchy in `preocr/exceptions.py` for better error handling
- **Logging Framework**: Implemented configurable logging system with environment variable support (`PREOCR_LOG_LEVEL`)
- **Caching Support**: Added optional file-based caching for repeated analysis with automatic cache invalidation
- **Progress Callbacks**: Added progress callback support for batch processing operations
- **Type Safety Improvements**: Fixed all type hint inconsistencies (replaced `Dict[str, any]` with `Dict[str, Any]`)
- **CI/CD Pipeline**: Added GitHub Actions workflows for testing, linting, and automated PyPI publishing
- **Pre-commit Hooks**: Configured pre-commit hooks for code quality (Black, Ruff, mypy)
- **Project Documentation**: Added CONTRIBUTING.md, CODE_OF_CONDUCT.md, and py.typed marker file
- **Enhanced Documentation**: Added troubleshooting section and logging configuration to README

### Changed
- **Error Handling**: Replaced bare `except Exception:` with specific exception types throughout codebase
- **Version Management**: Updated `pyproject.toml` to dynamically read version from `preocr/version.py`
- **Type Checking**: Enhanced mypy configuration with stricter type checking settings
- **API Enhancement**: Added `use_cache` and `progress_callback` parameters to `needs_ocr()` function

### Fixed
- Fixed type hint inconsistencies across all modules (19 functions updated)
- Improved error messages with specific exception types and logging
- Enhanced code quality with better error handling patterns

## [0.3.2] - 2024-12-30

### Added
- **Dynamic Confidence Scoring**: Implemented formula-based confidence scores for PDFs (digital and scanned) and OpenCV refinement, providing more granular and accurate confidence levels based on text length, coverage, and ratios.

### Changed
- `preocr/decision.py`: Updated confidence calculation logic to use dynamic formulas instead of fixed thresholds for various PDF scenarios, improving accuracy and granularity of confidence scores.

## [0.3.1] - 2024-12-29

### Changed
- Updated `layout-refinement` dependency to use `opencv-python-headless` (lighter, better for server environments)
- Improved OpenCV layout detection algorithm with adaptive thresholding and better filtering
- Enhanced multi-page analysis: analyzes all pages for small PDFs, smart sampling for large ones
- Improved decision refinement using `layout_type` for more accurate decisions

### Added
- Documentation for libmagic system requirement with OS-specific installation instructions
- Better result structure with OpenCV analysis details in `layout["opencv"]`

### Fixed
- Better handling of missing OpenCV dependencies
- Improved layout display formatting in examples

## [0.3.0] - 2024-12-29

### Added
- **Hybrid pipeline with OpenCV refinement**: Adaptive pipeline that uses fast heuristics for clear cases and OpenCV layout analysis for edge cases
- **Layout-aware detection**: Analyze document layout to detect text regions, image regions, and mixed content
- **Automatic confidence-based refinement**: Low confidence decisions (< 0.9) automatically trigger OpenCV analysis for improved accuracy
- **OpenCV layout analysis module**: Detects text/image regions using computer vision techniques
- **Decision refinement**: Combines heuristics and OpenCV results for better accuracy (92-95% vs 85-90%)
- Optional `layout-refinement` extra dependency for OpenCV support
- New `layout_aware` parameter to `needs_ocr()` function for explicit layout analysis

### Changed
- Improved accuracy for edge cases through hybrid pipeline approach
- Most files stay fast (< 1 second) while edge cases get better analysis (1-2 seconds)
- Decision engine now supports OpenCV-based refinement for low-confidence cases

### Performance
- Clear cases (90%): < 1 second (heuristics only)
- Edge cases (10%): 1-2 seconds (heuristics + OpenCV)
- Overall accuracy: 92-95% (improved from 85-90%)

### Installation
```bash
# Basic installation
pip install preocr

# With OpenCV refinement (recommended)
pip install preocr[layout-refinement]
```

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

[Unreleased]: https://github.com/yuvaraj3855/preocr/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.3.0
[0.2.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.2.0
[0.1.1]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.1
[0.1.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.0

