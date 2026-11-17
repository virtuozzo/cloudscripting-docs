# MkDocs to Hugo conversion

`mkdocs2hugo.py` is the script that converted the Cloud Scripting documentation from MkDocs to Hugo on the `8.15.1` branch. It is kept for history: the conversion is done, and pages are now edited directly under `content/`.

The script is not expected to run again. The navigated pages of the `8.8.1` and later branches are the same as in `8.15.1` (one heading differs in `samples.md`), so if one of those versions ever needs a Hugo build, copy the converted `8.15.1` branch instead of converting it.

## What was converted

Source: the MkDocs tree of `8.15.1` (`docs/`, `mkdocs.yml`, images in `theme/readthedocs/img/`), removed from the branch in the same change.

- One MkDocs page became one Hugo page bundle: `content/<section>/<slug>/index.md` with its images next to it.
- The sidebar follows the `pages:` block of `mkdocs.yml`. The *Getting Started* and *Creating Manifest* groups became sections with a generated index page; *Samples* uses `samples.md` as its index, with *Troubleshooting* as its child.
- URLs became flat (`/actions/` instead of `/creating-manifest/actions/`). Each moved page lists its old MkDocs URL in `aliases` after its own URL; the theme turns every alias but the first into a 301 redirect.

Pages that were not migrated:

- `examples/`, `reference/` and `releasenotes.md`: outdated drafts that never appeared in the navigation.
- `virtuozzo-cs-correspondence.md` (CS vs platform versions): there are no production versions below 6.0, where the two version lines started to match. Links to it were removed from the other pages.

The home page (`content/_index.md`) and the 404 page were written by hand.

## What the script changes in a page

Syntax that MkDocs (Python-Markdown) accepted and Hugo (goldmark) does not:

- `!!! note` admonitions become `{{%note%}} … {{%/note%}}`.
- `@@@ … @@!` tab blocks become `{{< tabs >}}` / `{{< tabs-item title="YAML" >}}`. The angle form is required: the `%` form renders the inner code twice.
- `#Heading` gets the space CommonMark requires; a page whose top heading is `##` gets it promoted to `#`.
- A blank line is added after a raw HTML block line, otherwise goldmark treats the markdown below it as HTML.
- Code fences are normalised (`` ``` json `` to `` ```json ``), and an outer fence is lengthened when the sample itself contains a fence indented by up to three spaces, which goldmark would take as the closing fence.

Links and images:

- Internal links are rewritten to the flat URLs.
- Referenced images are copied into the page bundle under lowercase names.

Clean-up pass, the only wording changes:

- *Virtuozzo Application Platform* becomes *Virtuozzo Application Management*, and the platform documentation, API, admin and partners URLs are updated.
- Simple HTML becomes markdown: `<a>`, `<b>`, `<em>`, `<p>`, headings, `<br>`, single-line `<ul>`, plain tables.
- Blank lines between list items are removed (tight lists).
- List items that link to a page that was not migrated are removed.

Front matter is generated: title from the first heading, SEO fields (description from the first paragraph), the sidebar menu entry, and `aliases`.

## Running it

From a checkout that still has the MkDocs sources:

```bash
python3 tools/mkdocs2hugo.py --src docs --img theme/readthedocs/img --out content --img-ref HEAD
```

`--img-ref` reads the images from that git revision instead of the working tree. It is required on macOS and Windows: the image folder holds names that differ only by letter case, two of those pairs are different pictures (`SettingsMain.jpg` / `settingsMain.jpg`, `SettingsCustom.jpg` / `settingsCustom.jpg`), and a case-insensitive file system keeps only one file of each pair.

`--polish <dir>` runs only the clean-up pass on already converted pages. It is idempotent.
