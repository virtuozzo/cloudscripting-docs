# Repository guide

This is a Hugo documentation site. Edit articles in `content/`, layout overrides in `layouts/`, frontend assets in `assets/`, and public files in `static/`.

Read [README.md](README.md) for setup details and [docs/deployment.md](docs/deployment.md) for releases.

## Setup

```sh
git submodule update --init --recursive
devbox shell
uv sync --locked
```

On macOS, use case-sensitive build storage. Follow the README to set the build and test environment variables.

## Commands

- `task serve`: preview working content, including drafts.
- `task build`: build current content without drafts.
- `task hugo:verify`: check the Hugo setup.
- `uv run --locked python -m unittest discover -s tests/migration`: run tests.
- `task build-all`: build all published versions from frozen Git sources.
- `task validate`: check the complete release artifact.

Use Task instead of running Hugo directly. It prepares the required assets. Commit intended changes before building a complete release.

## Rules

- Work on a `feat/` branch. Do not work on `master` or use `codex/` branch names.
- Never push branches, tags, or commits without explicit user approval.
- Preserve existing working-tree changes.
- Keep the shared theme submodule pinned. Use local overrides for site changes.
- Use `uv run --locked` for Python scripts. Keep Python and uv versions aligned across project config, Devbox, and CI.
- Preserve published source pins, validation inputs, and exact code examples.
- Preserve filename casing. Export assets from frozen Git sources to case-sensitive storage.
- Keep generated files, plans, reports, and scratch work under ignored `build/` or outside the repository.
