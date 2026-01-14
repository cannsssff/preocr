# PreOCR Library - Improvement Suggestions

This document contains comprehensive suggestions to improve the PreOCR library based on code review.

## 🔴 Critical Issues

### 1. Unused Imports
**Location**: `preocr/batch.py:3`, `preocr/cache.py:5`
- `import os` is present but never used
- **Fix**: Remove unused imports

### 2. Missing Error Handling for Custom Exceptions
**Location**: Throughout codebase
- Custom exceptions are defined but rarely used
- Many places catch generic `Exception` instead of specific exceptions
- **Fix**: Use custom exceptions (`PDFProcessingError`, `TextExtractionError`, etc.) consistently

### 3. Logger Handler Duplication Risk
**Location**: `preocr/logger.py:27-41`
- Potential for duplicate handlers if logger is configured multiple times
- **Fix**: Check `logger.handlers` before adding, or use `logging.getLogger()` singleton pattern

## 🟡 Important Improvements

### 4. Type Safety Enhancements

#### 4.1 Missing Type Hints
- Some functions return `Dict[str, Any]` but could use TypedDict for better type safety
- **Suggestion**: Create TypedDict classes for return types (e.g., `OCRResult`, `PageAnalysis`, `LayoutResult`)

#### 4.2 Optional Dependencies Type Checking
**Location**: `preocr/opencv_layout.py:12-13`
- Using `Optional[Any]` loses type information
- **Suggestion**: Use `TYPE_CHECKING` guard with proper types:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import cv2
    import numpy as np
```

### 5. Input Validation

#### 5.1 File Path Validation
- No validation for path traversal attacks (`../../../etc/passwd`)
- No validation for extremely long paths
- **Suggestion**: Add path validation utility:
```python
def validate_file_path(path: Union[str, Path]) -> Path:
    """Validate and normalize file path."""
    path = Path(path).resolve()
    # Check for path traversal
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path
```

#### 5.2 File Size Limits
- No maximum file size validation before processing
- Large files could cause memory issues
- **Suggestion**: Add configurable file size limits

### 6. Error Handling Improvements

#### 6.1 Better Error Messages
- Some errors don't include file path context
- **Suggestion**: Always include file path in error messages

#### 6.2 Graceful Degradation
- When optional dependencies fail, return informative errors
- **Suggestion**: Check dependencies upfront and provide clear error messages

### 7. Performance Optimizations

#### 7.1 Cache Key Generation
**Location**: `preocr/cache.py:19-39`
- Using MD5 for cache keys (deprecated, though still secure)
- **Suggestion**: Consider SHA256 or use `hashlib.blake2b` for better performance

#### 7.2 PDF Page Sampling
**Location**: `preocr/opencv_layout.py:69-79`
- Random sampling uses `random` module without seed
- **Suggestion**: Use deterministic sampling or make seed configurable

#### 7.3 Memory Management
- Large PDFs loaded entirely into memory
- **Suggestion**: Stream processing for very large files

### 8. Code Quality

#### 8.1 Magic Numbers
- Hard-coded thresholds scattered throughout code
- **Suggestion**: Move all thresholds to `constants.py` with documentation

#### 8.2 Code Duplication
- Similar error handling patterns repeated
- **Suggestion**: Create error handling utilities

#### 8.3 Assert Statements
**Location**: `preocr/batch.py:301, 359`
- Using `assert` for type narrowing (could fail in optimized mode)
- **Suggestion**: Use explicit type guards or type narrowing with `if` statements

### 9. API Improvements

#### 9.1 Batch Results Export
- No method to export results to JSON/CSV
- **Suggestion**: Add `BatchResults.to_json()`, `BatchResults.to_csv()` methods

#### 9.2 Progress Callback Enhancement
- Progress callback only provides stage name and progress
- **Suggestion**: Include more context (file name, current operation details)

#### 9.3 Configuration Object
- Many parameters passed individually
- **Suggestion**: Create `PreOCRConfig` dataclass for configuration

### 10. Documentation

#### 10.1 API Documentation
- Some functions lack comprehensive docstrings
- **Suggestion**: Add examples to all public API docstrings

#### 10.2 Type Documentation
- Return type dictionaries not fully documented
- **Suggestion**: Use TypedDict with field descriptions

#### 10.3 Performance Documentation
- No guidance on when to use which features
- **Suggestion**: Add performance tuning guide

## 🟢 Nice-to-Have Enhancements

### 11. Testing Improvements

#### 11.1 Test Coverage
- Add tests for edge cases (corrupted files, very large files, etc.)
- **Suggestion**: Aim for >90% coverage

#### 11.2 Integration Tests
- More end-to-end integration tests
- **Suggestion**: Test full pipeline with various file types

#### 11.3 Performance Tests
- No performance regression tests
- **Suggestion**: Add benchmark tests to CI/CD

### 12. Features

#### 12.1 Result Serialization
- No way to save/load results
- **Suggestion**: Add `save_results()` and `load_results()` methods

#### 12.2 Batch Processing Resume
- Resume functionality exists but could be improved
- **Suggestion**: Add checkpointing during processing (not just at end)

#### 12.3 Metrics and Monitoring
- No built-in metrics collection
- **Suggestion**: Add metrics export (Prometheus, StatsD compatible)

#### 12.4 Async Support
- Batch processing uses multiprocessing, not async
- **Suggestion**: Consider async/await API for I/O-bound operations

### 13. Security

#### 13.1 Cache Security
- Cache files stored in user home directory without permission checks
- **Suggestion**: Set appropriate file permissions (0600) for cache files

#### 13.2 Input Sanitization
- File paths not sanitized before use
- **Suggestion**: Add path sanitization utility

### 14. Developer Experience

#### 14.1 Debug Mode
- No comprehensive debug mode
- **Suggestion**: Add `--debug` flag that enables verbose logging and saves intermediate results

#### 14.2 CLI Tool
- No command-line interface
- **Suggestion**: Add `preocr` CLI command for batch processing

#### 14.3 Configuration File
- No support for configuration files
- **Suggestion**: Support YAML/TOML config files

### 15. Dependencies

#### 15.1 Optional Dependency Checks
- No upfront check for optional dependencies
- **Suggestion**: Add `check_dependencies()` function

#### 15.2 Version Pinning
- Dependencies use `>=` which could cause breaking changes
- **Suggestion**: Consider upper bounds or test against latest versions in CI

## 📊 Priority Summary

### High Priority (Do First)
1. Remove unused imports
2. Fix logger handler duplication
3. Add input validation
4. Use custom exceptions consistently
5. Add TypedDict for return types

### Medium Priority (Do Soon)
6. Improve error messages
7. Move magic numbers to constants
8. Add file size limits
9. Improve cache security
10. Add result export methods

### Low Priority (Future)
11. Add CLI tool
12. Add async support
13. Add configuration files
14. Add metrics export
15. Add comprehensive debug mode

## 🔧 Quick Wins

These can be implemented quickly with high impact:

1. **Remove unused imports** (5 minutes)
2. **Add file size validation** (30 minutes)
3. **Create TypedDict classes** (1-2 hours)
4. **Add result export methods** (1 hour)
5. **Fix logger handler duplication** (30 minutes)
6. **Move magic numbers to constants** (1 hour)

## 📝 Code Examples

### Example: TypedDict for Results
```python
from typing import TypedDict, List, Optional

class OCRResult(TypedDict):
    needs_ocr: bool
    file_type: str
    category: str
    confidence: float
    reason: str
    reason_code: str
    signals: Dict[str, Any]
    pages: Optional[List[Dict[str, Any]]]
    layout: Optional[Dict[str, Any]]]
```

### Example: Input Validation
```python
def validate_file_path(path: Union[str, Path], max_size: Optional[int] = None) -> Path:
    """Validate file path and size."""
    path = Path(path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    if max_size:
        size = path.stat().st_size
        if size > max_size:
            raise ValueError(f"File too large: {size} bytes (max: {max_size})")
    
    return path
```

### Example: Configuration Class
```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PreOCRConfig:
    page_level: bool = False
    layout_aware: bool = False
    use_cache: bool = False
    max_file_size: Optional[int] = None
    cache_dir: Optional[Path] = None
    log_level: str = "WARNING"
```

## 🎯 Conclusion

The PreOCR library is well-structured and functional. The suggestions above focus on:
- **Code quality**: Type safety, error handling, documentation
- **Security**: Input validation, path sanitization
- **Performance**: Optimizations, memory management
- **Developer experience**: Better APIs, debugging tools
- **Maintainability**: Reducing duplication, improving organization

Most improvements are incremental and can be implemented gradually without breaking changes.

