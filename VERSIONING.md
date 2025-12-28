# Versioning Guide for PreOCR

## Overview

PreOCR uses **Semantic Versioning (SemVer)** with the format: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

## Version Storage

The version is stored in **two places** (must be kept in sync):

1. **`preocr/version.py`** - Single source of truth: `__version__ = "0.1.0"`
2. **`pyproject.toml`** - Required for setuptools: `version = "0.1.0"`

> **Important**: Always update both files with the same version!

## Semantic Versioning Rules

### MAJOR version (X.0.0)
Increment when you make **breaking API changes**:
- Changing function signatures
- Removing public APIs
- Changing return value structures in incompatible ways
- Example: `0.1.0` → `1.0.0` (breaking change to `needs_ocr()` signature)

### MINOR version (0.X.0)
Increment when you add **new features** (backward-compatible):
- Adding new file type support
- Adding new optional parameters
- Adding new functions/classes
- Example: `0.1.0` → `0.2.0` (added support for ODT files)

### PATCH version (0.0.X)
Increment when you make **bug fixes** (backward-compatible):
- Fixing PDF text extraction bugs
- Improving decision engine accuracy
- Performance improvements
- Example: `0.1.0` → `0.1.1` (fixed MIME detection bug)

## Version Update Workflow

### Step 1: Update Version Files

Update both files with the new version:

**`preocr/version.py`:**
```python
__version__ = "0.2.0"  # Update this
```

**`pyproject.toml`:**
```toml
[project]
version = "0.2.0"  # Update this to match
```

### Step 2: Update CHANGELOG.md

Add a new section for the version:

```markdown
## [0.2.0] - 2024-12-28

### Added
- Support for ODT file format
- New `batch_needs_ocr()` function

### Changed
- Improved PDF text extraction accuracy

### Fixed
- Fixed MIME detection for edge cases

[0.2.0]: https://github.com/yourusername/preocr/releases/tag/v0.2.0
```

### Step 3: Commit Version Bump

```bash
git add preocr/version.py pyproject.toml CHANGELOG.md
git commit -m "Bump version to 0.2.0"
```

### Step 4: Create Git Tag

Create an **annotated tag** matching the version:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
```

Tag format: `v{MAJOR}.{MINOR}.{PATCH}` (e.g., `v0.2.0`)

### Step 5: Push Commits and Tags

```bash
git push
git push --tags
```

Pushing the tag will trigger the CI workflow to:
- Validate version consistency
- Build the package
- Run tests
- Publish to PyPI (if configured)

## Release Checklist

Before every release, verify:

- [ ] **Version in `preocr/version.py`** - Updated
- [ ] **Version in `pyproject.toml`** - Updated (matches version.py)
- [ ] **Version in `__init__.py`** - Exported (auto-imported from version.py)
- [ ] **Git tag matches version** - Tag format `vX.Y.Z` matches `__version__`
- [ ] **CHANGELOG.md updated** - All changes documented
- [ ] **CI triggers on tag** - GitHub Actions workflow runs on tag push

## Quick Version Update Script

You can use this helper script to update versions:

```bash
#!/bin/bash
# update_version.sh

NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./update_version.sh 0.2.0"
    exit 1
fi

# Update version.py
sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" preocr/version.py

# Update pyproject.toml
sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "Version updated to $NEW_VERSION in:"
echo "  - preocr/version.py"
echo "  - pyproject.toml"
echo ""
echo "Next steps:"
echo "  1. Update CHANGELOG.md"
echo "  2. git commit -m 'Bump version to $NEW_VERSION'"
echo "  3. git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "  4. git push && git push --tags"
```

## Version Validation

The CI workflow automatically validates:
- Version in `version.py` matches git tag
- Version in `pyproject.toml` matches `version.py`
- Version format is valid SemVer

## Examples

### Example 1: Bug Fix Release
```bash
# Current: 0.1.0
# New: 0.1.1 (bug fix)

# 1. Update files
echo '__version__ = "0.1.1"' > preocr/version.py
# Update pyproject.toml version = "0.1.1"

# 2. Update CHANGELOG.md
# Add [0.1.1] section with bug fixes

# 3. Commit and tag
git commit -m "Bump version to 0.1.1"
git tag -a v0.1.1 -m "Release v0.1.1"
git push && git push --tags
```

### Example 2: Feature Release
```bash
# Current: 0.1.0
# New: 0.2.0 (new feature)

# Same process, but increment MINOR version
```

### Example 3: Breaking Change
```bash
# Current: 0.5.2
# New: 1.0.0 (breaking API change)

# Increment MAJOR version, reset MINOR and PATCH
```

## Common Mistakes to Avoid

❌ **Auto-incrementing versions** - Always manually review and decide version bumps
❌ **Changing API without bumping MAJOR** - Breaking changes require MAJOR version bump
❌ **Forgetting to tag releases** - Always create git tags for releases
❌ **Multiple version sources** - Keep `version.py` and `pyproject.toml` in sync
❌ **Tag format mismatch** - Tags must be `vX.Y.Z` (with 'v' prefix)

## Verifying Version Consistency

You can verify versions are in sync:

```bash
# Check version.py
python -c "from preocr.version import __version__; print(__version__)"

# Check pyproject.toml (requires tomli or similar)
python -c "import tomllib; f=open('pyproject.toml','rb'); print(tomllib.load(f)['project']['version'])"

# Check __init__.py (should match version.py)
python -c "from preocr import __version__; print(__version__)"
```

All three should output the same version!

