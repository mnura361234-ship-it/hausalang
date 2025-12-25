# GitHub Release Instructions - Hausalang v1.1

## Using GitHub CLI (Recommended)

```bash
# Ensure you have GitHub CLI installed (brew install gh / winget install GitHub.CLI)
# Make sure you're logged in
gh auth status

# Create the release with RELEASE_NOTES_v1.1.md
gh release create v1.1 \
  --title "Hausalang v1.1 - Production Release" \
  --notes-file RELEASE_NOTES_v1.1.md \
  --draft=false
```

## Manual Web UI

1. Go to: https://github.com/mnura361234-ship-it/hausalang/releases
2. Click "Create a new release"
3. Select tag: `v1.1`
4. Title: `Hausalang v1.1 - Production Release`
5. Copy-paste contents of `RELEASE_NOTES_v1.1.md` into the description
6. Click "Publish release"

## Release Details

**Tag:** v1.1
**Commit:** 40cdd49 (main)
**Status:** Production Ready
**Test Results:** 180 tests passing ✅

---

See [RELEASE_NOTES_v1.1.md](RELEASE_NOTES_v1.1.md) for full details.
