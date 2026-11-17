# Cloud Scripting Documentation

This repository contains the source files for the [Cloud Scripting documentation](https://docs.cloudscripting.com/). The site is built with [Hugo](https://gohugo.io/) and the shared Virtuozzo `compose-master` theme, which is included as the `themes` git submodule.

Each Cloud Scripting version lives on its own branch (for example `8.15.1`). `params.version` in `config.yaml` names the version a branch documents; the list of versions for the version switcher is kept on the `master` branch only.

## Repository layout

| Path | Purpose |
|------|---------|
| `config.yaml` | Site configuration, including the version this branch documents |
| `content/` | Pages as Hugo page bundles (`<section>/<slug>/index.md` plus images) |
| `themes/` | Shared theme submodule (`virtuozzo/docs-theme`) |
| `redirects.htaccess` | Redirects that page aliases cannot express, such as a redirect to another site |
| `tools/` | Script that migrated the site from MkDocs, kept for history (see `tools/README.md`) |
| `TECH-DOCS.md` | Repo-specific rules for the `tech-docs` authoring skill |

## Staging the docs locally

1. Clone the repository with the theme submodule:

   ```bash
   git clone --recurse-submodules git@github.com:virtuozzo/cloudscripting-docs.git
   cd cloudscripting-docs
   ```

   If the `themes/` folder is empty, run `git submodule update --init`.

2. Install [Devbox](https://www.jetify.com/devbox/docs/installing_devbox/). It pins the Hugo version used in production.

3. Start the dev server:

   ```bash
   devbox run serve
   ```

   or

   ```bash
   devbox shell
   task serve
   ```

4. Open [http://127.0.0.1:1313/](http://127.0.0.1:1313/). Hugo rebuilds the site on every file change.

To produce a production build, run `devbox run build`; the output lands in `public/`.

In VS Code, the `Start the Docs web server` task (`Terminal -> Run Task...`) runs the same command. The `.devcontainer` folder provides a Dev Container with Devbox inside for GitHub Codespaces or local Docker.

## Writing pages

Pages are page bundles: `content/<section>/<slug>/index.md` with images next to the markdown file. Front matter fields are described in `frontmatter.json`; the page template is in `.frontmatter/templates/index.md`. Sidebar order comes from `menu.docs.weight`, and the parent section from `menu.docs.parent`.

Redirects live in front matter: the first entry of `aliases` is the page's own URL, and every further entry is an old URL that the generated `.htaccess` redirects to the page. This is how the old MkDocs URLs (`/creating-manifest/actions/`) reach the Hugo pages (`/actions/`).

Common shortcodes:

- `{{%note%}} … {{%/note%}}` for important information
- `{{%tip%}} … {{%/tip%}}` for optional context
- `{{< tabs >}}` with `{{< tabs-item title="YAML" >}}` for YAML/JSON manifest samples (angle brackets, not `%`); tabs that hold a single code block each render as one code block with language tabs
- `{{%childrenList%}}` on section pages to list child pages

Two theme features are enabled in `config.yaml` and can be turned off per page in front matter: the "Suggest an improvement" link under every article (`params.feedback.url`, page override `feedback: false`) and the current page's headings in the sidebar (`params.sidebarHeadings`, `params.sidebarHeadingsDepth`, page override `sidebarHeadings: false`). `params.darkMode: true` enables the dark color scheme, which follows the system preference and can be switched from the header.
