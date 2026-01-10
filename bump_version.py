#!/usr/bin/env python3
"""
Automated version bumping based on conventional commits.

Analyzes git commit messages since the last tag and automatically bumps version:
- fix: → patch (0.0.1)
- feat: → minor (0.1.0)
- feat!: or BREAKING CHANGE → major (1.0.0)
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


def get_current_version() -> str:
    """Get current version from version.py."""
    version_file = Path("preocr/version.py")
    if not version_file.exists():
        raise FileNotFoundError("preocr/version.py not found")
    
    content = version_file.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in version.py")
    
    return match.group(1)


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string into (major, minor, patch)."""
    parts = version.split(".")
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple into string."""
    return f"{major}.{minor}.{patch}"


def get_last_tag() -> Optional[str]:
    """Get the last git tag."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_commits_since_tag(tag: Optional[str] = None) -> list[str]:
    """Get commit messages since the last tag (or all commits if no tag)."""
    if tag:
        try:
            result = subprocess.run(
                ["git", "log", f"{tag}..HEAD", "--pretty=format:%s"],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n") if result.stdout.strip() else []
            return [c for c in commits if c]  # Filter empty strings
        except subprocess.CalledProcessError:
            return []
    else:
        # No tag found, get all commits
        try:
            result = subprocess.run(
                ["git", "log", "--pretty=format:%s"],
                capture_output=True,
                text=True,
                check=True,
            )
            commits = result.stdout.strip().split("\n") if result.stdout.strip() else []
            return [c for c in commits if c]
        except subprocess.CalledProcessError:
            return []


def analyze_commits(commits: list[str]) -> Tuple[str, list[str]]:
    """
    Analyze commits to determine version bump type.
    
    Returns:
        Tuple of (bump_type, list of relevant commits)
    """
    bump_type = "patch"  # Default to patch
    relevant_commits = []
    
    # Patterns for conventional commits
    breaking_pattern = re.compile(r"^(feat|fix|perf|refactor|docs|style|test|chore)!:", re.IGNORECASE)
    breaking_change_pattern = re.compile(r"BREAKING CHANGE:", re.IGNORECASE)
    feat_pattern = re.compile(r"^feat:", re.IGNORECASE)
    fix_pattern = re.compile(r"^fix:", re.IGNORECASE)
    
    for commit in commits:
        # Skip merge commits, version bumps, and commits marked to skip version bump
        if (commit.startswith("Merge ") or 
            "version" in commit.lower() or 
            "bump" in commit.lower() or
            "[no bump]" in commit.lower() or
            "[skip version]" in commit.lower() or
            "[no version]" in commit.lower()):
            continue
        
        relevant_commits.append(commit)
        
        # Check for breaking changes (major bump)
        if breaking_pattern.match(commit) or breaking_change_pattern.search(commit):
            bump_type = "major"
            # Don't break, continue to check all commits
        
        # Check for features (minor bump, unless already major)
        elif bump_type != "major" and feat_pattern.match(commit):
            bump_type = "minor"
        
        # Fixes are patch (default), so no need to check
    
    return bump_type, relevant_commits


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump version based on type."""
    major, minor, patch = parse_version(current_version)
    
    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    elif bump_type == "patch":
        return format_version(major, minor, patch + 1)
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def update_version_file(new_version: str) -> None:
    """Update version in preocr/version.py."""
    version_file = Path("preocr/version.py")
    content = version_file.read_text()
    
    # Replace version
    new_content = re.sub(
        r'__version__ = ["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content,
    )
    
    version_file.write_text(new_content)
    print(f"✓ Updated preocr/version.py to {new_version}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automatically bump version based on conventional commits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect version bump from commits since last tag
  python bump_version.py

  # Force a specific bump type
  python bump_version.py --bump major
  python bump_version.py --bump minor
  python bump_version.py --bump patch

  # Dry run (show what would happen without making changes)
  python bump_version.py --dry-run

  # Create git tag after bumping
  python bump_version.py --tag

Conventional Commits:
  - fix: → patch bump (0.0.1)
  - feat: → minor bump (0.1.0)
  - feat!: or BREAKING CHANGE → major bump (1.0.0)
        """,
    )
    
    parser.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        default=None,
        help="Force a specific bump type (overrides commit analysis)",
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without making changes",
    )
    
    parser.add_argument(
        "--tag",
        action="store_true",
        help="Create git tag after bumping version",
    )
    
    parser.add_argument(
        "--no-commit",
        action="store_true",
        help="Don't create a git commit for the version bump",
    )
    
    args = parser.parse_args()
    
    # Get current version
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Determine bump type
    if args.bump:
        bump_type = args.bump
        commits = []
        print(f"Forcing {bump_type} bump")
    else:
        # Analyze commits
        last_tag = get_last_tag()
        if last_tag:
            print(f"Last tag: {last_tag}")
            commits = get_commits_since_tag(last_tag)
        else:
            print("No tags found, analyzing all commits")
            commits = get_commits_since_tag()
        
        if not commits:
            print("No commits found since last tag. Use --bump to force a version bump.")
            sys.exit(0)
        
        bump_type, relevant_commits = analyze_commits(commits)
        print(f"\nAnalyzed {len(commits)} commit(s) since last tag")
        print(f"Detected bump type: {bump_type}")
        
        if relevant_commits:
            print("\nRelevant commits:")
            for commit in relevant_commits[:10]:  # Show first 10
                print(f"  - {commit}")
            if len(relevant_commits) > 10:
                print(f"  ... and {len(relevant_commits) - 10} more")
    
    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"\nNew version: {new_version}")
    
    if args.dry_run:
        print("\n[DRY RUN] Would update version to:", new_version)
        if args.tag:
            print(f"[DRY RUN] Would create tag: v{new_version}")
        sys.exit(0)
    
    # Update version file
    try:
        update_version_file(new_version)
    except Exception as e:
        print(f"Error updating version: {e}")
        sys.exit(1)
    
    # Create git commit
    if not args.no_commit:
        try:
            subprocess.run(
                ["git", "add", "preocr/version.py"],
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"chore: bump version to {new_version}"],
                check=True,
            )
            print(f"✓ Created git commit for version {new_version}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not create git commit: {e}")
            print("You may need to commit manually:")
            print(f"  git add preocr/version.py")
            print(f"  git commit -m 'chore: bump version to {new_version}'")
    
    # Create git tag
    if args.tag:
        try:
            subprocess.run(
                ["git", "tag", "-a", f"v{new_version}", "-m", f"Release v{new_version}"],
                check=True,
            )
            print(f"✓ Created git tag v{new_version}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not create git tag: {e}")
            print(f"You may need to create the tag manually:")
            print(f"  git tag -a v{new_version} -m 'Release v{new_version}'")
    
    print(f"\n✓ Version bumped from {current_version} to {new_version}")
    print("\nNext steps:")
    print(f"  1. Review CHANGELOG.md and update it for version {new_version}")
    if not args.tag:
        print(f"  2. Create tag: git tag -a v{new_version} -m 'Release v{new_version}'")
    print(f"  3. Push changes: git push && git push --tags")


if __name__ == "__main__":
    main()

