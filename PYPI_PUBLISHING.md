# PyPI Publishing Guide - Hausalang v1.1

## Prerequisites

```bash
# Ensure build tools are installed
pip install build twine wheel
```

## Building the Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build sdist (source) and wheel (binary)
python -m build

# Verify the distribution
twine check dist/*
```

## Local Testing

```bash
# Test installation in a fresh venv
python -m venv test_venv
source test_venv/bin/activate  # or `test_venv\Scripts\activate` on Windows

pip install dist/hausalang-1.1.0-py3-none-any.whl
python -c "from hausalang.core.interpreter import interpret_program; print('Import successful!')"

# Try a simple program
python -c "
from hausalang.core.interpreter import interpret_program
code = '''
x = 5 + 3
rubuta x
'''
interpret_program(code)
"

deactivate
rm -rf test_venv
```

## Publishing to PyPI (Test & Production)

### Option 1: Using GitHub Actions (Recommended)

The automated workflow in `.github/workflows/publish.yml` will:
1. Build distribution on tag push
2. Check with `twine check`
3. Publish to PyPI using trusted OIDC publishing

**Steps:**
```bash
# After merge to main and all tests pass:
git tag v1.1.0
git push origin main v1.1.0

# Workflow triggers automatically
# Monitor at: https://github.com/mnura361234-ship-it/hausalang/actions
```

### Option 2: Manual Publishing (Local)

#### Test PyPI First:

```bash
# Create account at https://test.pypi.org/
# Generate token: https://test.pypi.org/manage/account/#api-tokens

# Store credentials in ~/.pypirc:
# [distutils]
# index-servers =
#     testpypi
#     pypi
#
# [testpypi]
# repository: https://test.pypi.org/legacy/
# username: __token__
# password: pypi-AgEIcHlwaS5vcmcvXXXX

twine upload -r testpypi dist/*

# Verify at: https://test.pypi.org/project/hausalang/
```

#### Production PyPI:

```bash
# Create account at https://pypi.org/
# Generate token: https://pypi.org/manage/account/#api-tokens

# Update ~/.pypirc with [pypi] section

# Upload to production
twine upload dist/*

# Verify at: https://pypi.org/project/hausalang/
```

## Post-Release Verification

```bash
# Verify on PyPI
curl -s https://pypi.org/pypi/hausalang/json | jq '.info.version'
# Should output: "1.1.0"

# Test installation from PyPI
pip install hausalang==1.1.0

# Quick smoke test
python -c "from hausalang.core.interpreter import interpret_program; print('✓ PyPI install works!')"
```

## Release Checklist

- [ ] All tests pass locally (196 tests)
- [ ] Git commit history is clean
- [ ] RELEASE_NOTES_v1.1.md is complete
- [ ] Version bumped in pyproject.toml (version = "1.1.0")
- [ ] Git tagged with v1.1.0
- [ ] CHANGELOG.md updated (if exists)
- [ ] Distribution built: `python -m build`
- [ ] Distribution verified: `twine check dist/*`
- [ ] Test PyPI upload successful
- [ ] Documentation updated (README, INSTALLATION.md)
- [ ] GitHub Release created
- [ ] Production PyPI upload successful
- [ ] Installation verified: `pip install hausalang==1.1.0`

## Troubleshooting

### "twine check" Fails

**Issue:** Long description rendering problem
**Fix:** Ensure README.md is valid reStructuredText or Markdown (PyPI auto-converts)

```bash
python -m readme_render --strict README.md
```

### Upload Fails with 401

**Issue:** Token expired or invalid credentials
**Fix:** Check ~/.pypirc and regenerate token from PyPI account settings

### Version Already Exists

**Issue:** 1.1.0 already uploaded to PyPI
**Fix:** PyPI doesn't allow overwriting. Use 1.1.1 or delete old version from PyPI web UI (not recommended)

### Build System Error

**Issue:** `ModuleNotFoundError: setuptools` or `wheel`
**Fix:**
```bash
pip install --upgrade setuptools wheel build
```

## Distribution Contents

After building, check what's included:

```bash
# List sdist contents
tar -tzf dist/hausalang-1.1.0.tar.gz | head -20

# List wheel contents
unzip -l dist/hausalang-1.1.0-py3-none-any.whl | head -20
```

Should include:
- `hausalang/` (package code)
- `hausalang-1.1.0.dist-info/` (metadata)
- `README.md`
- `RELEASE_NOTES_v1.1.md`

## Long-Term Maintenance

### Future Releases (v1.2, v1.3, ...):

1. Update version in pyproject.toml
2. Run the same build & publish workflow
3. Tag with semantic version (v1.2.0, v1.3.1, etc.)
4. Automated GitHub Actions will handle PyPI upload

### Yanking (Removing) a Bad Release:

If a release needs to be withdrawn:

```bash
# Via PyPI web UI:
# Go to https://pypi.org/project/hausalang/
# Click version → "Yank this release"

# Or via API (deprecated, not recommended)
```

---

**Questions?** See official guides:
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Help](https://pypi.org/help/)
