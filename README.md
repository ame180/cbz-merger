# cbz-merger

Merge multiple CBZ chapter archives into a single CBZ "volume". Files from input archives are flattened to the top level and prefixed with a sanitized source archive name (for example: `Archive1_Img1.jpg`).

Use case

If you have a folder full of CBZ chapters for a comic/manga, this tool merges them into a single "Volume" CBZ that can be uploaded to a reader as one file instead of many chapters.

Features

- Packaging via `pyproject.toml` (hatchling)
- Linting and formatting with Ruff
- Type checking with mypy
- Testing with pytest and coverage
- GitHub Actions CI to run all checks

Quick start

For a quick user install (no dev dependencies):

```bash
python -m pip install .
```

Examples

```bash
# Merge all .cbz in a directory (auto will also detect this):
cbz-merger Volume01.cbz path/to/chapters_folder

# Explicit archives list:
cbz-merger --mode archives Volume01.cbz Chap01.cbz Chap02.cbz

# Build a CBZ from individual image files:
cbz-merger --mode files Volume01.cbz page001.jpg page002.jpg page003.jpg
```

Notes

- Nested paths in input archives are flattened; only the final filename is used and prefixed.
- Archive name prefixes are sanitized: non-alphanumeric chars become underscores, repeated underscores collapse.

Developer docs

See [DEVELOPER.md](./DEVELOPER.md) for development setup, tests, linting, and CI instructions.

## CI

The repository includes a GitHub Actions workflow that runs linting, formatting checks, type checking, and tests on push/PR for supported Python versions.

## License

See [LICENSE](./LICENSE).
