---
description: Sync all auto-generated documentation (changelog, API reference) and verify the Zensical build
---

# /sync_docs — Documentation Sync Workflow

Regenerates all auto-generated documentation files and verifies the Zensical build.
Run this before committing doc-related changes or before a release.

// turbo-all

1. Sync the changelog from git-cliff into docs/changelog.md:
```
uv run python scripts/sync_changelog.py
```

2. Generate the API reference from Python docstrings:
```
uv run python scripts/gen_api_reference.py
```

3. Verify the Zensical build passes without errors:
```
uv run zensical build
```

4. (Optional) Preview locally:
```
uv run zensical serve
```

If step 3 fails, check the output for broken links or malformed markdown.
The most common cause is a new public symbol added without a docstring.
