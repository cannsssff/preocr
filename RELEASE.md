# PyPI Release Guide - PreOCR v0.4.0

## Pre-Release Checklist

✅ **Completed:**
- [x] Version updated to 0.4.0 in `preocr/version.py`
- [x] CHANGELOG.md updated with all improvements
- [x] Package built successfully (`dist/preocr-0.4.0-py3-none-any.whl` and `preocr-0.4.0.tar.gz`)
- [x] All new modules included (exceptions.py, logger.py, cache.py)
- [x] pyproject.toml configured correctly with dynamic version

## Uploading to PyPI

### Option 1: Using twine (Recommended)

1. **Install twine** (if not already installed):
   ```bash
   pip install twine
   ```

2. **Check the package** (optional but recommended):
   ```bash
   twine check dist/*
   ```

3. **Upload to TestPyPI first** (recommended for testing):
   ```bash
   twine upload --repository testpypi dist/*
   ```
   - You'll need TestPyPI credentials: https://test.pypi.org/account/register/

4. **Test installation from TestPyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ preocr
   ```

5. **Upload to PyPI** (production):
   ```bash
   twine upload dist/*
   ```
   - You'll need PyPI credentials: https://pypi.org/account/register/
   - Or use API token: https://pypi.org/manage/account/token/

### Option 2: Using GitHub Actions (Automated)

The repository already has a GitHub Actions workflow (`.github/workflows/publish.yml`) that will automatically publish when you:

1. **Create a git tag**:
   ```bash
   git tag v0.4.0
   git push origin v0.4.0
   ```

2. **Create a GitHub Release**:
   - Go to GitHub → Releases → Create a new release
   - Tag: `v0.4.0`
   - Title: `PreOCR v0.4.0`
   - Description: Copy from CHANGELOG.md
   - Publish release

The workflow will automatically:
- Build the package
- Run tests
- Upload to PyPI (if PYPI_API_TOKEN secret is configured)

### Option 3: Using build and upload directly

```bash
# Build
python -m build

# Upload
python -m twine upload dist/*
```

## Post-Release

After successful upload:

1. **Verify on PyPI**: https://pypi.org/project/preocr/
2. **Test installation**:
   ```bash
   pip install --upgrade preocr
   python -c "from preocr import needs_ocr, __version__; print(__version__)"
   ```
3. **Update GitHub release notes** (if using manual upload)
4. **Announce the release** (if applicable)

## Version Information

- **Current Version**: 0.4.0
- **Package Name**: preocr
- **Python Requirements**: >=3.9
- **Build Files**:
  - `dist/preocr-0.4.0-py3-none-any.whl` (37K)
  - `dist/preocr-0.4.0.tar.gz` (43K)

## What's New in v0.4.0

- Custom exception classes for better error handling
- Logging framework with environment variable support
- Optional caching for repeated analysis
- Progress callbacks for batch processing
- Type safety improvements (all type hints fixed)
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks for code quality
- Enhanced documentation and project files

See CHANGELOG.md for complete details.

