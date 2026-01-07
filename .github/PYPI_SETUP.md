# PyPI Publishing Setup Guide

## Why Publishing Wasn't Working

The release workflow was using the old API token method which requires a `PYPI_API_TOKEN` secret. We've now updated it to use **trusted publishing**, which is more secure and doesn't require secrets.

## Setup Trusted Publishing (Recommended)

### Step 1: Go to PyPI Project Settings

1. Go to https://pypi.org/manage/projects/
2. Click on your project (e.g., `preocr`)
3. Go to **"Publishing"** tab
4. Scroll to **"Trusted publishers"** section

### Step 2: Add GitHub as Trusted Publisher

1. Click **"Add"** under Trusted publishers
2. Fill in the details:
   - **PyPI project name:** `preocr`
   - **Owner:** `yuvaraj3855` (your GitHub username/organization)
   - **Repository name:** `preocr`
   - **Workflow filename:** `.github/workflows/release.yml`
   - **Environment name:** (leave empty, or specify if using environments)
3. Click **"Add trusted publisher"**

### Step 3: Verify Setup

After setup, the workflow will automatically:
- Use GitHub's OIDC tokens (no secrets needed)
- Authenticate to PyPI securely
- Publish packages automatically when tags are pushed

## Alternative: Using API Token (Not Recommended)

If you prefer to use an API token instead:

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token with scope: **"Entire account"** or **"Project: preocr"**
3. Copy the token (starts with `pypi-`)
4. In GitHub repository:
   - Go to **Settings → Secrets and variables → Actions**
   - Click **"New repository secret"**
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI API token
   - Click **"Add secret"**

Then revert the release.yml workflow to use the token method (but trusted publishing is better).

## How It Works Now

```
Tag pushed (v0.5.1)
    ↓
release.yml workflow triggers
    ↓
Validates version
    ↓
Runs tests
    ↓
Builds package
    ↓
Publishes to PyPI using trusted publishing ✅
```

## Troubleshooting

### Workflow not running on tag push

- Check that tag format is `v*` (e.g., `v0.5.1`)
- Verify workflow file is in `.github/workflows/release.yml`
- Check Actions tab to see if workflow is triggered

### Publishing fails

- Verify trusted publisher is configured correctly on PyPI
- Check workflow logs for specific error messages
- Ensure project name matches exactly: `preocr`
- Verify repository name matches: `yuvaraj3855/preocr`

### Version mismatch errors

- Ensure `preocr/version.py` matches tag version
- Check that `pyproject.toml` uses dynamic version
- Verify tag was created from the correct commit

## Testing

To test the publishing:

1. Create a test tag: `git tag v0.5.1-test && git push origin v0.5.1-test`
2. Check Actions tab for workflow run
3. Verify package appears on PyPI (or test PyPI: https://test.pypi.org)

## Current Status

✅ Workflow updated to use trusted publishing  
✅ No secrets required  
✅ Automatic publishing on tag push  

**Next step:** Set up trusted publisher on PyPI (see Step 1-2 above)

