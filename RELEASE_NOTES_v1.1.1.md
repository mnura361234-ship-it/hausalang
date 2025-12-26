# Hausalang v1.1.1 Release Notes

**Release Date:** December 26, 2025
**Status:** Patch Release / Maintenance

## Overview

v1.1.1 is a minor patch release that adds proper licensing metadata and packaging housekeeping to v1.1.0.

All functionality from v1.1.0 is preserved. No breaking changes.

## Changes

### Licensing
- Added proper MIT License file (`LICENSE`) with copyright attribution to Nura Abdulkareem (2025)
- Updated `pyproject.toml` license metadata to explicitly include "MIT License" text
- Clarified project licensing in all distribution artifacts

### Packaging & Metadata
- Excluded debug helper module (`core/interpreter_debug.py`) from distribution to reduce package size and prevent accidental usage
- Updated `MANIFEST.in` to ensure only production code is shipped
- All distribution artifacts now include proper `LICENSE` file

## Installation

```bash
pip install hausalang==1.1.1
```

## Verification

- All 200 pytest tests pass (unchanged from v1.1.0)
- Build and distribution verified
- No functional changes from v1.1.0

## Migration

If you are using v1.1.0, upgrading to v1.1.1 is fully transparent and recommended:

```bash
pip install --upgrade hausalang
```

## Support

- Issues: https://github.com/mnura361234-ship-it/hausalang/issues
- Documentation: https://github.com/mnura361234-ship-it/hausalang#readme
