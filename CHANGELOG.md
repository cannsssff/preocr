# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2024-12-28

### Changed
- Updated GitHub URLs in package metadata to point to correct repository

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

[Unreleased]: https://github.com/yuvaraj3855/preocr/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.1
[0.1.0]: https://github.com/yuvaraj3855/preocr/releases/tag/v0.1.0

