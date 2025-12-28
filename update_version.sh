#!/bin/bash
# Helper script to update version in both version.py and pyproject.toml

set -e

NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./update_version.sh <VERSION>"
    echo "Example: ./update_version.sh 0.2.0"
    exit 1
fi

# Validate version format (basic SemVer check)
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format MAJOR.MINOR.PATCH (e.g., 0.2.0)"
    exit 1
fi

# Get current version for reference
CURRENT_VERSION=$(python3 -c "import sys; sys.path.insert(0, '.'); from preocr.version import __version__; print(__version__)" 2>/dev/null || echo "unknown")

echo "Current version: $CURRENT_VERSION"
echo "New version: $NEW_VERSION"
echo ""

# Update version.py
if [ -f "preocr/version.py" ]; then
    sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" preocr/version.py
    echo "✓ Updated preocr/version.py"
else
    echo "✗ Error: preocr/version.py not found"
    exit 1
fi

# Update pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml
    echo "✓ Updated pyproject.toml"
else
    echo "✗ Error: pyproject.toml not found"
    exit 1
fi

echo ""
echo "Version updated successfully!"
echo ""
echo "Next steps:"
echo "  1. Review the changes:"
echo "     git diff preocr/version.py pyproject.toml"
echo ""
echo "  2. Update CHANGELOG.md with changes for version $NEW_VERSION"
echo ""
echo "  3. Commit the version bump:"
echo "     git add preocr/version.py pyproject.toml CHANGELOG.md"
echo "     git commit -m 'Bump version to $NEW_VERSION'"
echo ""
echo "  4. Create and push the tag:"
echo "     git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "     git push && git push --tags"
echo ""

