# Developer guide

This file documents how to set up a development environment, run linters/typecheckers, and run tests locally for the `cbz-merger` project.

Development environment

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Upgrade pip and install editable package with dev dependencies:

```bash
python -m pip install --upgrade pip
pip install -e .[dev]
```

Taskfile

This repository includes a `Taskfile.yml` to standardize common developer commands. If you have the `task` CLI installed, use the following shortcuts:

- `task install` — create `.venv` and install development dependencies
- `task lint` — run `ruff check .`
- `task lint-fix` — run `ruff format .` (apply formatting)
- `task typecheck` — run `mypy .`
- `task test` — run `pytest -q`
- `task checks` — runs `install`, `lint`, `typecheck`, and `test` (CI-like)

Linters and formatters

- Ruff is used for linting and formatting. To auto-fix formatting issues run:

```bash
ruff format .
```

- To check linting without modifying files:

```bash
ruff check .
```

Type checking

```bash
mypy .
```

Testing

Run tests with coverage:

```bash
pytest -q
```

Continuous integration

The [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) workflow runs the same steps (lint, format-check, mypy, pytest) across supported Python versions on push and pull requests.

Notes and tips

- If you modify `pyproject.toml` or add dependencies, re-run `task install` (or `pip install -e .[dev]`) inside the activated virtualenv.
- If you see lint warnings that are deliberate for tests (e.g., prints in test helpers), prefer adding a scoped per-file `# ruff: noqa` or fine-grained rule ignores in `pyproject.toml` rather than disabling rules globally.
- Before opening a PR, run `task checks` locally to catch issues early.

License

See [LICENSE](./LICENSE).
