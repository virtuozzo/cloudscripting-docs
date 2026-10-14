#!/usr/bin/env python3
"""Convert the MkDocs sources of the Cloud Scripting docs into Hugo page bundles
for the compose-master theme.

Usage (from the repository root):

    python3 tools/mkdocs2hugo.py --src docs --img theme/readthedocs/img --out content

What it does:
  * one MkDocs page -> one Hugo page bundle (content/<section>/<slug>/index.md)
  * sidebar structure follows the `pages:` block of mkdocs.yml (hardcoded in NAV below)
  * `!!! note` admonitions   -> {{%note%}} ... {{%/note%}}
  * `@@@ ... @@!` tab blocks -> {{< tabs >}} / {{< tabs-item title="YAML" >}} (angle form: the inner code is rendered once)
  * `#Heading` (no space)    -> `# Heading` (CommonMark requires the space)
  * images from theme/readthedocs/img are co-located in the page bundle
  * internal links/hrefs are rewritten to the flat Hugo slugs (/slug/)
  * a blank line is inserted after raw HTML block lines so goldmark renders the markdown after them
  * writes redirects.htaccess with old-URL -> new-URL rules
"""
import argparse
import json
import os
import posixpath
import re
import shutil
import sys

# --------------------------------------------------------------------------- nav
# Mirrors the `pages:` block of mkdocs.yml. Pages outside that block are published
# as link-only pages (no sidebar entry), exactly like MkDocs did.
NAV = [
    {
        "slug": "getting-started", "title": "Getting Started", "weight": 1,
        "index": {"synthetic": True,
                  "intro": "Learn what Cloud Scripting is and deploy your first manifest."},
        "pages": [
            ("index.md", "Overview", "overview"),
            ("quick-start.md", "Quick Start", None),
        ],
    },
    {
        "slug": "creating-manifest", "title": "Creating Manifest", "weight": 2,
        "index": {"synthetic": True,
                  "intro": "A manifest is a JSON or YAML file that describes the environment "
                           "topology, the actions to run, and the events that trigger them. "
                           "The pages below cover every section of the manifest."},
        "pages": [
            ("creating-manifest/basic-configs.md", "Basic Configs", None),
            ("creating-manifest/selecting-containers.md", "Specifying Target Container", None),
            ("creating-manifest/actions.md", "Actions", None),
            ("creating-manifest/events.md", "Events", None),
            ("creating-manifest/placeholders.md", "Placeholders", None),
            ("creating-manifest/conditions-and-iterations.md", "Conditions and Iterations", None),
            ("creating-manifest/custom-scripts.md", "Custom Scripts", None),
            ("creating-manifest/mixins.md", "Mixins", None),
            ("creating-manifest/addons.md", "Add-Ons", None),
            ("creating-manifest/handling-custom-responses.md", "Custom Responses", None),
            ("creating-manifest/visual-settings.md", "Visual Settings", None),
        ],
    },
    {"slug": "samples", "title": "Samples", "weight": 3,
     "index": {"src": "samples.md"}, "pages": []},
    {"slug": "troubleshooting", "title": "Troubleshooting", "weight": 4,
     "index": {"src": "troubleshooting.md"}, "pages": []},
    {"slug": "virtuozzo-cs-correspondence", "title": "CS vs Virtuozzo PaaS Versions", "weight": 5,
     "index": {"src": "virtuozzo-cs-correspondence.md"}, "pages": []},
]

# Pages that MkDocs built but never listed in the sidebar: folder -> source files.
LINK_ONLY = {
    "examples": [
        "examples/add-ons.md", "examples/addon-inside-manifest.md",
        "examples/complex-ready-to-go-solutions.md", "examples/configs-adjustments.md",
        "examples/environment-migration-after-cloning.md", "examples/hello-world.md",
        "examples/horizontal-scaling.md", "examples/mount-data-storage.md",
        "examples/operation-examples.md", "examples/swap-domain.md",
        "examples/two-envs-in-diff-regions.md", "examples/using-docker.md",
        "examples/vertical-scaling.md", "examples/wordpress-cluster.md",
    ],
    "reference": [
        "reference/container-types.md", "reference/docker-actions.md",
        "reference/procedures.md", "releasenotes.md",
    ],
}

# Titles for pages whose source has no H1 (or where the MkDocs theme template supplied it).
TITLE_OVERRIDES = {
    "virtuozzo-cs-correspondence.md": "Virtuozzo Application Platform & CS Correspondence",
}

# Body that the MkDocs theme template (virtuozzo-cs-correspondence.html) used to prepend.
BODY_PREFIX = {
    "virtuozzo-cs-correspondence.md": (
        "# Virtuozzo Application Platform & CS Correspondence\n\n"
        "The table below displays dependencies between Cloud Scripting and the Virtuozzo "
        "Application Platform versions within the same "
        '<a href="https://www.virtuozzo.com/application-platform-partners/" target="_blank">'
        "hosting provider</a> platform.\n\n"
        "{{< cs-versions >}}\n\n"
    ),
}

SITE_KEYWORD = "cloud scripting"

warnings = []


def warn(msg):
    warnings.append(msg)


# --------------------------------------------------------------------------- helpers
def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def split_code(text):
    """Split text into [(is_code, chunk)] on fenced code blocks (``` or ~~~)."""
    out, buf, in_code, fence = [], [], False, None
    for line in text.split("\n"):
        m = re.match(r"^(```+|~~~+)", line)
        if not in_code and m:
            if buf:
                out.append((False, "\n".join(buf)))
            buf, in_code, fence = [line], True, m.group(1)[0]
            continue
        if in_code and m and m.group(1)[0] == fence and not line.strip()[len(m.group(1)):].strip():
            buf.append(line)
            out.append((True, "\n".join(buf)))
            buf, in_code = [], False
            continue
        buf.append(line)
    if buf:
        out.append((in_code, "\n".join(buf)))
    return out


def map_prose(text, fn):
    """Apply fn to the non-code chunks only."""
    return "\n".join(fn(chunk) if not is_code else chunk for is_code, chunk in split_code(text))


def fix_nested_fences(chunk):
    """Python-Markdown only closes a fence at column 0; CommonMark also accepts up to
    3 spaces of indentation. Lengthen the outer fence when the block embeds one."""
    lines = chunk.split("\n")
    inner = [len(m.group(1)) for l in lines[1:-1] for m in [re.match(r"^ {0,3}(`{3,})", l)] if m]
    if not inner:
        return chunk
    n = max(inner) + 1
    lines[0] = re.sub(r"^`{3,}", "`" * n, lines[0])
    lines[-1] = re.sub(r"^`{3,}", "`" * n, lines[-1])
    return "\n".join(lines)


BLOCK_TAGS = ("address|article|aside|blockquote|br|center|dd|details|dialog|div|dl|dt|fieldset|figcaption|"
              "figure|footer|form|h[1-6]|header|hr|iframe|img|legend|li|main|menu|nav|ol|optgroup|option|p|"
              "section|summary|table|tbody|td|tfoot|th|thead|tr|ul")
CONTAINER_TAGS = "table|div|ul|ol|dl|center|details|blockquote|figure|section|nav|aside|form|fieldset"


def fix_html_blocks(chunk):
    """Goldmark treats a line that starts with a block-level HTML tag as raw HTML up to the
    next blank line, so markdown right after `<h3>..</h3>` or `<p>..</p>` is swallowed.
    Python-Markdown did not. Insert a blank line after a closed HTML block line when the
    next line is markdown."""
    lines = chunk.split("\n")
    out, depth = [], 0
    for i, line in enumerate(lines):
        out.append(line)
        is_html = re.match(r"^<(%s)(\s|>|/)" % BLOCK_TAGS, line, re.I) or re.match(r"^</?[A-Za-z][^<>]*>\s*$", line)
        depth += len(re.findall(r"<(%s)(\s[^>]*)?>" % CONTAINER_TAGS, line, re.I))
        depth -= len(re.findall(r"</(%s)>" % CONTAINER_TAGS, line, re.I))
        if depth < 0:
            depth = 0
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if (is_html or (depth == 0 and re.match(r"^\s*</(%s)>" % CONTAINER_TAGS, line, re.I))) \
                and depth == 0 and nxt.strip() and not nxt.lstrip().startswith("<"):
            out.append("")
    return "\n".join(out)


def map_code(text, fn):
    return "\n".join(fn(chunk) if is_code else chunk for is_code, chunk in split_code(text))


def fix_headings(chunk):
    chunk = re.sub(r"^(#{1,6})([^#\s])", r"\1 \2", chunk, flags=re.M)
    return re.sub(r"^(#{1,6} .*?)[ \t]+$", r"\1", chunk, flags=re.M)


def promote_h2(text):
    """Pages whose top heading is `## Title` (MkDocs did not care): make it the H1."""
    if re.search(r"^# ", text, re.M):
        return text
    return re.sub(r"^## ", "# ", text, count=1, flags=re.M)


def convert_admonitions(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^!!! ?(\w+)\s*(\"[^\"]*\")?\s*$", lines[i], re.I)
        if not m:
            out.append(lines[i])
            i += 1
            continue
        kind = m.group(1).lower()
        if kind != "note":
            warn(f"admonition type '{kind}' mapped to note")
        i += 1
        body = []
        while i < len(lines) and (lines[i].strip() == "" or lines[i].startswith("    ") or lines[i].startswith("\t")):
            body.append(lines[i][4:] if lines[i].startswith("    ") else lines[i].lstrip("\t"))
            i += 1
        while body and body[-1].strip() == "":
            body.pop()
        while body and body[0].strip() == "":
            body.pop(0)
        out.append("{{%note%}}")
        out.extend(body)
        out.append("{{%/note%}}")
        out.append("")
    return "\n".join(out)


LANG_TITLES = {"yaml": "YAML", "yml": "YAML", "json": "JSON", "javascript": "JavaScript", "js": "JavaScript",
               "bash": "Bash", "example": "Example", "": "Text"}


def convert_tabs(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if not re.match(r"^@@@\s*$", lines[i]):
            out.append(lines[i])
            i += 1
            continue
        i += 1
        items, cur, lang = [], None, None
        while i < len(lines) and not re.match(r"^@@!\s*$", lines[i]):
            line = lines[i]
            m = re.match(r"^```\s*([\w-]*)\s*$", line)
            if cur is None:
                if m:
                    lang = m.group(1).lower()
                    cur = ["```" + lang]
                elif line.strip():
                    warn(f"stray text inside tabs block: {line.strip()[:60]!r}")
            else:
                cur.append(line)
                if m and not m.group(1):
                    items.append((lang, cur))
                    cur = None
            i += 1
        i += 1  # skip @@!
        if cur:
            warn("unterminated code fence inside tabs block")
            items.append((lang, cur))
        out.append("{{< tabs >}}")
        for lang, body in items:
            title = LANG_TITLES.get(lang, lang.upper())
            out.append('{{< tabs-item title="' + title + '" >}}')
            out.extend(body)
            out.append("{{< /tabs-item >}}")
        out.append("{{< /tabs >}}")
    return "\n".join(out)


def normalize_fences(text):
    # "``` json " -> "```json"; keep content untouched
    return re.sub(r"^(`{3,})[ \t]*([\w-]*)[ \t]*$", r"\1\2", text, flags=re.M)


def strip_markup(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`]+", "", s)
    s = re.sub(r"&[a-z]+;", "", s)
    return re.sub(r"\s+", " ", s).strip()


def first_paragraph(body):
    lines = body.split("\n")
    i = 0
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith("#") or lines[i].startswith("{{")):
        i += 1
    para = []
    while i < len(lines) and lines[i].strip() and not lines[i].startswith("{{"):
        para.append(lines[i])
        i += 1
    return strip_markup(" ".join(para))


def seodesc(body, title):
    text = first_paragraph(body) or title
    if len(text) > 155:
        text = text[:155].rsplit(" ", 1)[0].rstrip(",.;:")
    return text


# --------------------------------------------------------------------------- pages
class Page:
    def __init__(self, src, slug, section, menu_title=None, weight=None, parent=None, is_section_index=False):
        self.src = src                    # path relative to docs/, or None for synthetic pages
        self.slug = slug
        self.section = section
        self.menu_title = menu_title
        self.weight = weight
        self.parent = parent              # None = link-only, "" = top level
        self.is_section_index = is_section_index

    @property
    def key(self):
        return re.sub(r"\.md$", "", self.src) if self.src else None

    @property
    def mk_url(self):
        """URL MkDocs served this page at (directory style)."""
        if self.key in ("index", None):
            return "/"
        return "/" + self.key + "/"

    @property
    def src_dir_url(self):
        return "/" + posixpath.dirname(self.src) + "/" if self.src and "/" in self.src else "/"

    @property
    def out_dir(self):
        d = self.slug if not self.is_section_index else self.slug
        return os.path.join(self.section, d)

    @property
    def url(self):
        return "/" + self.slug + "/"


def build_pages():
    pages = []
    for sec in NAV:
        idx = sec["index"]
        pages.append(Page(idx.get("src"), sec["slug"], sec["slug"], sec["title"], sec["weight"], "",
                          is_section_index=True))
        for w, (src, title, slug) in enumerate(sec["pages"], start=1):
            slug = slug or re.sub(r"\.md$", "", posixpath.basename(src))
            pages.append(Page(src, slug, sec["slug"], title, w, sec["slug"]))
    for folder, srcs in LINK_ONLY.items():
        for src in srcs:
            slug = re.sub(r"\.md$", "", posixpath.basename(src))
            pages.append(Page(src, slug, folder))
    return pages


# --------------------------------------------------------------------------- links & images
class Converter:
    def __init__(self, src_root, img_root, out_root, pages):
        self.src_root, self.img_root, self.out_root = src_root, img_root, out_root
        self.pages = pages
        self.by_key = {p.key: p for p in pages if p.key}
        self.by_key[""] = self.by_key["index"]
        self.redirects = []

    def lookup(self, path):
        key = path.strip("/")
        key = re.sub(r"\.md$", "", key)
        if key.endswith("/index"):
            key = key[:-6]
        return self.by_key.get(key)

    def resolve_link(self, url, page):
        raw = url
        url = url.strip()
        if not url or re.match(r"^(https?:|mailto:|javascript:|#|//|\{)", url, re.I):
            return raw
        path, _, frag = url.partition("#")
        frag = ("#" + frag) if frag else ""
        if re.match(r"^(\.\./)*/?img/", path):
            return self.copy_image(path, page) + frag
        cands = []
        if path.startswith("/"):
            cands.append(path)
        else:
            cands.append(posixpath.normpath(posixpath.join(page.mk_url, path)))
            cands.append(posixpath.normpath(posixpath.join(page.src_dir_url, path)))
            cands.append(posixpath.normpath(posixpath.join(page.mk_url, "..", path)))
        for c in cands:
            target = self.lookup(c)
            if target:
                return target.url + frag
        base = posixpath.basename(path.rstrip("/"))
        hits = [p for p in self.pages if p.key and posixpath.basename(p.key) == re.sub(r"\.md$", "", base)]
        if len(hits) == 1:
            return hits[0].url + frag
        warn(f"{page.src}: unresolved internal link {raw!r}")
        return raw

    def copy_image(self, path, page):
        name = re.sub(r"^(\.\./)*/?img/", "", path)
        src = os.path.join(self.img_root, name)
        if not os.path.isfile(src):
            warn(f"{page.src}: missing image {name}")
            return path
        new = name.lower()
        dest_dir = os.path.join(self.out_root, page.out_dir)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, new)
        if not os.path.exists(dest):
            shutil.copy2(src, dest)
        return new

    def rewrite_links(self, chunk, page):
        def md(m):
            bang, text, url, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
            return f"{bang}[{text}]({self.resolve_link(url, page)}{title})"

        chunk = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)", md, chunk)

        def attr(m):
            return f'{m.group(1)}={m.group(2)}{self.resolve_link(m.group(3), page)}{m.group(2)}'

        chunk = re.sub(r"\b(href|src)\s*=\s*([\"'])([^\"']*)\2", attr, chunk)
        # <center>![alt](img)</center>: raw HTML blocks are not markdown-processed by goldmark
        chunk = re.sub(r"<center>\s*!\[([^\]]*)\]\(([^)\s]+)\)\s*</center>",
                       r'<center><img src="\2" alt="\1"></center>', chunk)
        return chunk

    # ----------------------------------------------------------------------- page conversion
    def body_for(self, page):
        if page.src is None:
            sec = next(s for s in NAV if s["slug"] == page.slug)
            return f"# {sec['title']}\n\n{sec['index']['intro']}\n\nIn this section:\n\n{{{{%childrenList%}}}}\n", sec["title"]
        with open(os.path.join(self.src_root, page.src), encoding="utf-8") as fh:
            text = fh.read().replace("\r\n", "\n")
        text = re.sub(r"^<h1[^>]*>(.*?)</h1>\s*$", r"# \1", text, count=1, flags=re.M)
        text = map_prose(text, fix_headings)
        text = promote_h2(text)
        text = map_prose(text, convert_admonitions)
        text = convert_tabs(text)
        text = map_code(text, fix_nested_fences)
        text = normalize_fences(text)
        text = map_prose(text, lambda c: self.rewrite_links(c, page))
        text = map_prose(text, fix_html_blocks)
        if page.src in BODY_PREFIX:
            text = BODY_PREFIX[page.src] + text
        m = re.search(r"^# (.+?)\s*$", text, re.M)
        title = TITLE_OVERRIDES.get(page.src) or (strip_markup(m.group(1)) if m else None)
        if not title:
            title = page.menu_title or page.slug.replace("-", " ").title()
            warn(f"{page.src}: no H1 found, using {title!r}")
            text = f"# {title}\n\n" + text
        if page.is_section_index and page.src and NAV_HAS_CHILDREN.get(page.slug):
            text = text.rstrip("\n") + "\n\nIn this section:\n\n{{%childrenList%}}\n"
        return text.rstrip() + "\n", title

    def front_matter(self, page, title, body):
        menu_title = page.menu_title or title
        fm = [
            "---",
            "draft: false",
            f"title: {yaml_str(title)}",
            f"aliases: {yaml_str(page.url)}",
            'seoindex: "index, follow"',
            f"seotitle: {yaml_str(title)}",
            f"seokeywords: {yaml_str(SITE_KEYWORD + ', ' + strip_markup(title).lower())}",
            f"seodesc: {yaml_str(seodesc(body, title))}",
            "menu:",
            "    docs:",
            f"        title: {yaml_str(menu_title)}",
            f"        url: {yaml_str(page.url)}",
        ]
        if page.parent is not None:
            fm.append(f"        weight: {page.weight}")
            fm.append(f"        parent: {yaml_str(page.parent)}")
        fm.append(f"        identifier: {yaml_str(page.slug)}")
        fm.append("---")
        return "\n".join(fm) + "\n\n"

    def run(self):
        for page in self.pages:
            body, title = self.body_for(page)
            dest_dir = os.path.join(self.out_root, page.out_dir)
            os.makedirs(dest_dir, exist_ok=True)
            with open(os.path.join(dest_dir, "index.md"), "w", encoding="utf-8") as fh:
                fh.write(self.front_matter(page, title, body) + body)
            if page.src and page.mk_url not in ("/", page.url):
                self.redirects.append((page.mk_url, page.url))
        return self.redirects


NAV_HAS_CHILDREN = {s["slug"]: bool(s["pages"]) for s in NAV}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="docs")
    ap.add_argument("--img", default="theme/readthedocs/img")
    ap.add_argument("--out", default="content")
    ap.add_argument("--redirects", default="redirects.htaccess")
    args = ap.parse_args()

    pages = build_pages()
    conv = Converter(args.src, args.img, args.out, pages)
    redirects = conv.run()

    with open(args.redirects, "w", encoding="utf-8") as fh:
        fh.write("# Old MkDocs URLs -> Hugo slugs (generated by tools/mkdocs2hugo.py)\n")
        for old, new in redirects:
            fh.write(f"RewriteRule ^{old.strip('/')}/?$ {new} [L,R=301]\n")

    print(f"converted {len(pages)} pages into {args.out}/, {len(redirects)} redirects")
    seen = set()
    for w in warnings:
        if w not in seen:
            seen.add(w)
            print("WARN:", w, file=sys.stderr)


if __name__ == "__main__":
    main()
