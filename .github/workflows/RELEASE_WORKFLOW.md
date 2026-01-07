# Release and PyPI Publishing Workflow

This document explains how the automated release and PyPI publishing process works.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Developer pushes commits with conventional commits           │
│    (feat:, fix:, feat!:, etc.)                                  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. version-bump.yml workflow triggers                           │
│    - Analyzes commits since last tag                            │
│    - Determines version bump (patch/minor/major)                 │
│    - Creates PR with version bump                               │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. PR Review & Merge                                             │
│    - Review version bump PR                                      │
│    - Merge to main branch                                        │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. create-tag-on-version-bump.yml workflow triggers             │
│    - Detects merged version bump PR                              │
│    - Extracts version from version.py                            │
│    - Creates git tag (vX.Y.Z)                                   │
│    - Pushes tag to repository                                    │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. release.yml workflow triggers (on tag push)                  │
│    - Validates version consistency                               │
│    - Runs tests                                                  │
│    - Builds package                                              │
│    - Publishes to PyPI                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Steps

### Step 1: Version Bump Detection

**Workflow:** `.github/workflows/version-bump.yml`

**Triggers:** Push to `main` or `develop` branches

**What it does:**
- Analyzes commit messages since last tag
- Detects version bump type:
  - `fix:` → Patch (0.0.1)
  - `feat:` → Minor (0.1.0)
  - `feat!:` or `BREAKING CHANGE:` → Major (1.0.0)
- Creates PR with version bump commit

### Step 2: PR Review

**Manual step:** Review and merge the version bump PR

**What to check:**
- Version number is correct
- CHANGELOG.md is updated (if needed)
- All tests pass

### Step 3: Tag Creation

**Workflow:** `.github/workflows/create-tag-on-version-bump.yml`

**Triggers:** When version bump PR is merged to `main`

**What it does:**
- Extracts version from `preocr/version.py`
- Creates annotated git tag: `vX.Y.Z`
- Pushes tag to repository

### Step 4: PyPI Publishing

**Workflow:** `.github/workflows/release.yml`

**Triggers:** Push of tag matching pattern `v*`

**What it does:**
1. **Version Validation:**
   - Validates version in `version.py` matches tag
   - Validates `pyproject.toml` uses dynamic version
   - Validates `__init__.py` exports correct version

2. **Build & Test:**
   - Runs test suite
   - Builds wheel and source distribution
   - Verifies built package version

3. **Publish:**
   - Uploads to PyPI using `PYPI_API_TOKEN` secret
   - Uses trusted publishing (no password needed if configured)

## Configuration

### Required Secrets

1. **PYPI_API_TOKEN** (in GitHub repository secrets)
   - PyPI API token for publishing
   - Get from: https://pypi.org/manage/account/token/
   - Or use trusted publishing (recommended)

### Trusted Publishing (Recommended)

Instead of using an API token, you can use PyPI's trusted publishing:

1. Go to PyPI project settings
2. Enable "GitHub" as a trusted publisher
3. Configure repository and workflow
4. Remove `PYPI_API_TOKEN` secret (not needed)

## Manual Release Process

If you need to manually create a release:

```bash
# 1. Bump version manually
python bump_version.py --bump minor

# 2. Commit and push
git add preocr/version.py CHANGELOG.md
git commit -m "chore: bump version to 0.5.0"
git push

# 3. Create and push tag
git tag -a v0.5.0 -m "Release v0.5.0"
git push origin v0.5.0

# 4. Release workflow will automatically:
#    - Validate version
#    - Run tests
#    - Build package
#    - Publish to PyPI
```

## Troubleshooting

### Tag not created after PR merge

- Check if workflow ran: Actions tab → "Create Tag on Version Bump Merge"
- Verify PR title contains "bump version"
- Check workflow logs for errors

### PyPI publish fails

- Verify `PYPI_API_TOKEN` secret is set
- Check PyPI project name matches `pyproject.toml`
- Verify version doesn't already exist on PyPI
- Check workflow logs for specific error

### Version mismatch errors

- Ensure `preocr/version.py` has correct version
- Verify `pyproject.toml` uses dynamic version
- Check that tag version matches code version

## Workflow Files

- **version-bump.yml**: Creates PR with version bump
- **create-tag-on-version-bump.yml**: Creates tag when PR merged
- **release.yml**: Validates, builds, and publishes to PyPI
- **publish.yml**: Alternative publish workflow (triggers on GitHub release)

