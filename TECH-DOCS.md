<!--
This repository uses the universal `tech-docs` skill from the `documentation`
plugin (virtuozzo-skills marketplace: bitbucket.org/virtuozzocore/skills).
Install that plugin for your agent of choice before working on the docs.

The skill adapts to this repo automatically. The instructions below are
repo-specific; they override the skill where the two conflict.
-->

# Repo overlay for the tech-docs skill

## Repo facts

- Single-language site: the content root is `content/`. Top-level sections are `getting-started`, `creating-manifest`, and `samples` (which also holds the troubleshooting page).
- One branch per Cloud Scripting version. `params.version` in `config.yaml` is the version the branch documents; the list of versions for the version switcher is kept on the `master` branch only, so do not add `params.versions` to a version branch.
- Serve with `devbox run serve` (runs `task serve`) or `task serve` inside `devbox shell`.
- `config.yaml` sets `goldmark.renderer.unsafe: true`, so HTML comments ship in the page source. Use the theme's `comment` shortcode for notes.
- Redirects are front matter `aliases`: the first entry is the page's own URL, every further entry is an old URL that the theme's `.htaccess` redirects to the page. When a page moves, keep its existing aliases and add the old URL. `redirects.htaccess` is only for redirects that aliases cannot express, such as a redirect to another site.
- Theme features switched on in `config.yaml`: `params.feedback.url` adds the "Suggest an improvement" link (a prefilled GitHub issue) under every article; `params.sidebarHeadings: true` lists the current page's h2 and h3 headings under its sidebar item (`sidebarHeadingsDepth` sets the deepest level; a page with child pages shows those instead). A page opts out with `feedback: false` or `sidebarHeadings: false` in its front matter (the search and 404 pages are skipped automatically). `params.darkMode: true` adds the dark color scheme (system preference plus a switch in the header); colors in the theme are CSS custom properties defined in the theme's `_theme.sass` and `_theme-dark.sass`, so never hardcode a color in a repo override.
- `tools/` holds the script that migrated the site from MkDocs, kept for history. It is not part of the authoring workflow: edit the pages under `content/` directly.

## Content conventions

- Manifest samples are shown in YAML and JSON side by side with `{{< tabs >}}` / `{{< tabs-item title="YAML" >}}` (angle form only: the theme renders the markdown inside each tab). A tab group whose tabs hold one code block each is shown by the theme as a single code block with language tabs and one Copy button, so keep nothing but the fence inside such tabs.
- Leaf pages end with `## What's next?` and a tight list of related links (Basic Configs and Mixins do not have one yet).
- Product name in prose: *Virtuozzo Application Management*, not *Virtuozzo Application Platform*.
- Image files are co-located in the page bundle, with lowercase names and no spaces.
