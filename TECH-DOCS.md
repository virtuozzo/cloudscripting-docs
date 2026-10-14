<!--
This repository uses the universal `tech-docs` skill from the `documentation`
plugin (virtuozzo-skills marketplace: bitbucket.org/virtuozzocore/skills).
Install that plugin for your agent of choice before working on the docs.

The skill adapts to this repo automatically. The instructions below are
repo-specific; they override the skill where the two conflict.
-->

# Repo overlay for the tech-docs skill

## Repo facts

- Single-language site: the content root is `content/`. Top-level sections are `getting-started`, `creating-manifest`, `samples`, `troubleshooting`, and `virtuozzo-cs-correspondence`.
- `examples/` and `reference/` hold link-only pages (no sidebar entry), which is how MkDocs published them. Promote a page into the sidebar by adding `parent` and `weight` to its menu block.
- One branch per Cloud Scripting version (`8.15.1`, `8.14.3`, …). `params.version` and `params.versions` in `config.yaml` drive the version switcher; `params.csPlatformVersions` drives the table on the *CS vs Virtuozzo PaaS Versions* page through the repo-local `cs-versions` shortcode.
- Serve with `devbox run serve` (runs `task serve`) or `task serve` inside `devbox shell`.
- `config.yaml` sets `goldmark.renderer.unsafe: true`, so HTML comments ship in the page source. Use the theme's `comment` shortcode for notes.
- `tools/mkdocs2hugo.py` is the one-off converter used for the MkDocs migration. It stays in the repo so older version branches can be converted the same way.

## Content conventions

- Manifest samples are shown in YAML and JSON side by side with `{{%tabs%}}` / `{{%tabs-item title="YAML"%}}`.
- Pages inherited from MkDocs end with an HTML `<h2>What's next?</h2>` block; keep that heading text when editing, or convert it to `## What's next?`.
