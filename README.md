# Cloud Scripting documentation

This repository contains the source for the [Cloud Scripting documentation](https://www.virtuozzo.com/cloudscripting-docs/). The site is built with Hugo.

You can edit and preview the docs in the cloud or on your own machine.

## Contributor setup

Fork the repository if you do not have write access. Make changes on a `feat/` branch and submit a pull request when ready.

### Developing in the cloud

#### GitHub Codespaces

1. Open the repository or your fork on GitHub. Select **Code > Codespaces** and create a Codespace.
2. Wait for the Dev Container to finish setup. It includes the project tools and VS Code extensions.
3. Run `uv sync --locked`, then `task serve` in the terminal.
4. Open the forwarded port **8000** in your browser. The preview updates as you edit.

See the [Codespaces guide](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository) for more details.

#### github.dev

For quick edits, press `.` while viewing the repository on GitHub. This opens [github.dev](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor). It supports Markdown previews but has no terminal to run the site.

### Developing locally

Clone the repository with its theme submodule. Use your fork's URL if needed.

```sh
git clone --recurse-submodules https://github.com/virtuozzo/cloudscripting-docs.git
cd cloudscripting-docs
```

For an existing clone, run `git submodule update --init --recursive`. Keep the theme at the recorded revision; do not use `--remote`.

#### Devbox

[Install Devbox](https://www.jetify.com/docs/devbox/installing-devbox), then run:

```sh
devbox shell
uv sync --locked
```

Devbox supplies the Hugo, Task, Python and uv versions in [devbox.json](devbox.json). uv installs the locked Python dependencies into `.venv`. You do not need to activate it.

On macOS, complete the [storage setup](#macos-build-storage) before starting the preview.

#### Dev Container

1. Install Docker and the **Dev Containers** extension for VS Code.
2. Open the repository in VS Code and run **Dev Containers: Reopen in Container** from the command palette.
3. Once setup finishes, run `uv sync --locked` in the terminal.

The container uses the same Devbox tools and includes Markdown, spelling and Hugo extensions.

## Editing and previewing

- Edit articles in `content/`.
- Add public files, such as images, to `static/`.
- Put site styles and scripts in `assets/` and template overrides in `layouts/`.
- Edit site settings and menu groups in `config.yaml`.

Start the preview:

```sh
task serve
```

Open <http://127.0.0.1:8000/>. The preview includes drafts and updates when files change. Use `task serve -- --port 9000` to choose another port.

In VS Code, you can also select **Terminal > Run Task > Start the Hugo preview**. Use Task for builds and previews so the required assets are prepared.

Keep filenames and links in their original case. Use local overrides for theme changes.

### Sidebar settings

Set `params.docsMenu` in `config.yaml`:

```yaml
params:
  docsMenu:
    showPageHeadings: true
    alwaysOpen:
      - creating-manifest
```

`showPageHeadings` adds section links beneath the current page. Set it to `false` to hide them. `alwaysOpen` keeps listed menu groups and their parents expanded. Use menu identifiers, not labels. Set it to `[]` to allow all groups to collapse.

## macOS build storage

Builds need case-sensitive storage because some image names differ only by letter case. On Linux, the default `build/` directory usually works. On macOS, create a case-sensitive disk image once:

```sh
CS_IMAGE_DIR="$HOME/Library/Caches/cloudscripting-docs-hugo"
mkdir -p "$CS_IMAGE_DIR"
hdiutil create -size 8g -type SPARSE -fs 'Case-sensitive APFS' -volname CloudScriptingHugo "$CS_IMAGE_DIR/build.sparseimage"
```

Mount it when needed, then set these variables in each shell used for builds or tests:

```sh
CS_IMAGE_DIR="$HOME/Library/Caches/cloudscripting-docs-hugo"
hdiutil attach "$CS_IMAGE_DIR/build.sparseimage" -mountpoint "$CS_IMAGE_DIR/volume" -nobrowse
export CS_BUILD_ROOT="$CS_IMAGE_DIR/volume/work"
export CS_DELIVERY_TMPDIR="$CS_IMAGE_DIR/volume"
export CS_DELIVERY_TEST_TMPDIR="$CS_IMAGE_DIR/volume"
export MIGRATION_TEST_ROOT="$CS_IMAGE_DIR/volume"
export MIGRATION_CASE_SENSITIVE_TMP="$CS_IMAGE_DIR/volume"
```

Skip the attach command if the image is already mounted. Stop servers and builds before unmounting it:

```sh
hdiutil detach "$CS_IMAGE_DIR/volume"
```

## Building and testing

Build the current content without drafts:

```sh
task build
```

Output goes to `build/current-site`, or `$CS_BUILD_ROOT/current-site` when set.

Run the Hugo checks and test suite:

```sh
task hugo:verify
uv run --locked python -m unittest discover -s tests/migration
```

The full test suite also needs Node.js. It is not required for previews or builds.

Use `uv add` or `uv remove` to change Python dependencies. Commit both `pyproject.toml` and `uv.lock`.

### Building all published versions

The full build uses fixed Git commits from the [release manifest](migration/release-sources.yaml). Keep the full Git history and pinned theme available. Commit intended content and tooling changes before building.

```sh
task build-all
task validate
```

Output goes to `build/artifact`, or `$CS_BUILD_ROOT/artifact` when set. Serve only its `site/` directory. Set `CS_BUILD_JOBS` to run builds in parallel; the default is `1`.

These commands use the production base URL. See the [deployment guide](docs/deployment.md) for packaging, staging, production and rollback steps.
