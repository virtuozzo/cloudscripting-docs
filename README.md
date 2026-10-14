# Cloud Scripting Documentation

This repository contains the source files for the [Cloud Scripting documentation](https://docs.cloudscripting.com/). The site is built with [Hugo](https://gohugo.io/) and the shared Virtuozzo `compose-master` theme, which is included as the `themes` git submodule.

Each Cloud Scripting version lives on its own branch (for example `8.15.1`); the deploy workflow builds every version branch and publishes the newest one at the site root.

## Repository layout

| Path | Purpose |
|------|---------|
| `config.yaml` | Site configuration and version switcher list |
| `content/` | Pages as Hugo page bundles (`<section>/<slug>/index.md` plus images) |
| `themes/` | Shared theme submodule (`virtuozzo/docs-theme`) |
| `redirects.htaccess` | Redirects from the old MkDocs URLs to the Hugo slugs |
| `tools/mkdocs2hugo.py` | Converter used to migrate the MkDocs sources |
| `tools/import-basic-examples.py` | Generates the sample pages from the basic-examples GitHub repository |
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

Common shortcodes:

- `{{%note%}} … {{%/note%}}` for important information
- `{{%tip%}} … {{%/tip%}}` for optional context
- `{{%tabs%}}` with `{{%tabs-item title="YAML"%}}` for YAML/JSON manifest samples
- `{{%childrenList%}}` on section pages to list child pages

## Converting older version branches

`tools/mkdocs2hugo.py` converts a MkDocs checkout into Hugo page bundles:

```bash
python3 tools/mkdocs2hugo.py --src docs --img theme/readthedocs/img --out content
```

It maps the MkDocs navigation to sidebar sections, converts admonitions and tab blocks to shortcodes, co-locates images, rewrites internal links, and writes `redirects.htaccess`. The clean-up pass it ends with can also run on its own against existing pages (`python3 tools/mkdocs2hugo.py --polish content`): product rename, simple HTML to markdown, tight lists.

## Refreshing the sample pages

The pages under `content/samples/` that show manifests from the [basic-examples](https://github.com/jelastic-jps/basic-examples) repository are generated. To refresh them after the repository changes:

```bash
git clone --depth 1 https://github.com/jelastic-jps/basic-examples /tmp/basic-examples
python3 tools/import-basic-examples.py --repo /tmp/basic-examples --out content/samples
```

The explanatory text of each page lives in the `EXAMPLES` table of the script.
