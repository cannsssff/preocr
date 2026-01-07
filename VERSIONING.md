# Version Management

PreOCR uses **automated version bumping** based on [Conventional Commits](https://www.conventionalcommits.org/).

## How It Works

The version is automatically determined by analyzing git commit messages since the last tag:

- **`fix:`** → Patch bump (0.0.1)
- **`feat:`** → Minor bump (0.1.0)  
- **`feat!:`** or **`BREAKING CHANGE:`** → Major bump (1.0.0)

## Usage

### Automatic Version Bump (Recommended)

Simply run the script after making commits:

```bash
# Analyze commits since last tag and auto-bump
python bump_version.py

# With automatic git tag creation
python bump_version.py --tag

# Dry run (see what would happen)
python bump_version.py --dry-run
```

### Manual Version Bump

If you need to force a specific bump type:

```bash
# Force patch bump
python bump_version.py --bump patch

# Force minor bump
python bump_version.py --bump minor

# Force major bump
python bump_version.py --bump major
```

## Commit Message Format

Use conventional commits in your commit messages:

```bash
# Patch bump (bug fixes)
git commit -m "fix: resolve PDF parsing error"
git commit -m "fix: handle empty text extraction"

# Minor bump (new features)
git commit -m "feat: add batch processing support"
git commit -m "feat: implement page-level analysis"

# Major bump (breaking changes)
git commit -m "feat!: refactor API to use new detector class"
git commit -m "feat: add new layout analyzer

BREAKING CHANGE: removed deprecated analyze() method"
```

## Examples

### Example 1: Bug Fix (Patch Bump)

```bash
# Make a fix
git commit -m "fix: handle corrupted PDF files gracefully"

# Bump version (0.4.0 → 0.4.1)
python bump_version.py --tag
```

### Example 2: New Feature (Minor Bump)

```bash
# Add a feature
git commit -m "feat: add batch processing with parallel workers"

# Bump version (0.4.0 → 0.5.0)
python bump_version.py --tag
```

### Example 3: Breaking Change (Major Bump)

```bash
# Make breaking change
git commit -m "feat!: rename needs_ocr() to detect_ocr_need()

BREAKING CHANGE: API method renamed for clarity"

# Bump version (0.4.0 → 1.0.0)
python bump_version.py --tag
```

### Example 4: Multiple Commits

```bash
# Make several commits
git commit -m "fix: resolve memory leak in PDF processing"
git commit -m "feat: add caching support"
git commit -m "docs: update README with examples"

# Bump version (0.4.0 → 0.5.0)
# Minor bump because of the feat: commit
python bump_version.py --tag
```

## Workflow

### Recommended Workflow

1. **Make your changes and commit:**
   ```bash
   git commit -m "feat: add new feature"
   ```

2. **Bump version automatically:**
   ```bash
   python bump_version.py --tag
   ```

3. **Update CHANGELOG.md:**
   ```bash
   # Manually add entry for new version
   ```

4. **Push changes and tags:**
   ```bash
   git push && git push --tags
   ```

### CI/CD Integration

GitHub Actions workflows can automatically bump versions. There are two modes:

#### Option 1: Automatic Direct Commit (Default)

The workflow (`.github/workflows/version-bump.yml`) automatically:
- Detects version bumps needed from commits
- **Directly commits and pushes** the version bump to the branch
- Creates and pushes a git tag automatically
- No manual intervention needed

**How it works:**
1. You push commits with conventional commit messages
2. Workflow analyzes commits since last tag
3. Workflow automatically bumps version, commits, and pushes
4. Tag is created automatically

#### Option 2: Pull Request Mode (Review Required)

The alternative workflow (`.github/workflows/version-bump-pr.yml`) creates a PR:
- Detects version bumps needed
- Creates a Pull Request for review
- You review and merge manually
- More control, but requires manual step

**To use PR mode:**
1. Rename `version-bump-pr.yml` to `version-bump.yml`
2. Rename current `version-bump.yml` to `version-bump-direct.yml`
3. Or disable the direct commit workflow and enable PR mode

**Which to use?**
- **Direct commit**: Faster, fully automated, good for trusted workflows
- **PR mode**: Safer, allows review before version bump, good for production

## Version File

The version is stored in a single source of truth:

- **`preocr/version.py`**: Contains `__version__ = "0.4.0"`
- **`pyproject.toml`**: Dynamically reads from `preocr.version.__version__`

## Script Options

```bash
python bump_version.py [OPTIONS]

Options:
  --bump {major,minor,patch}  Force a specific bump type
  --dry-run                   Show what would happen without changes
  --tag                       Create git tag after bumping
  --no-commit                 Don't create git commit for version bump
```

## Legacy Method

If you prefer the old manual method, you can still use:

```bash
./update_version.sh 0.5.0
```

This updates the version manually without analyzing commits.

## Troubleshooting

### No commits found since last tag

If you see "No commits found since last tag", you can:
- Force a bump: `python bump_version.py --bump patch`
- Or make a commit first

### Version already bumped

The script skips version bump commits automatically. If you need to force it:
```bash
python bump_version.py --bump patch --no-commit
```

### Git tag already exists

If the tag already exists, you'll need to:
1. Delete the tag: `git tag -d v0.5.0`
2. Or use a different version

## Best Practices

1. **Always use conventional commits** - Makes versioning automatic
2. **Run `--dry-run` first** - See what will happen before committing
3. **Update CHANGELOG.md** - Document what changed in each version
4. **Tag releases** - Use `--tag` to create git tags automatically
5. **Push tags** - Don't forget `git push --tags`

## Conventional Commits Reference

| Type | Bump | Example |
|------|------|---------|
| `fix:` | Patch | `fix: resolve memory leak` |
| `feat:` | Minor | `feat: add batch processing` |
| `feat!:` | Major | `feat!: refactor API` |
| `BREAKING CHANGE:` | Major | Any commit with this footer |

Other types (`perf:`, `refactor:`, `docs:`, etc.) default to patch unless they have `!` or `BREAKING CHANGE`.

