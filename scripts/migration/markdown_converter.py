"""Lossless legacy-block conversion; URL and asset handling belongs to prepare_content.

Code bodies are never parsed as YAML/JSON. Their presentation reproduces legacy
Markdown whitespace handling; immutable source bytes are never written. Hugo
literal-shortcode escaping preserves the resulting displayed/copied text.
Unsupported legacy structure raises ConversionError with actionable issue records.
"""
import html
import hashlib
import json
import re
import unicodedata

import yaml


class ConversionError(ValueError):
    def __init__(self, issues):
        self.issues = issues
        super().__init__('; '.join(f"{i['source_path']}:{i['line']}: {i['evidence']}" for i in issues))


_FENCE = re.compile(r'^( {0,3})(`{3,}|~{3,})[ \t]*([^\r\n]*)')
_HEADING = re.compile(r'^(#{1,6})(?!#)[ \t]*(.+?)[ \t]*#*[ \t]*$')
_ADMONITION = re.compile(r'^!!!\s*([\w-]+)(?:[ \t]+"(.*)")?[ \t]*$', re.I)
_LITERAL_SHORTCODE = re.compile(r'\{\{(?:<[\s\S]*?>|%[\s\S]*?%)\}\}')
_MARKER = 'cloudscripting_migration'
LEGACY_CORRESPONDENCE_TEMPLATE = 'theme/readthedocs/virtuozzo-cs-correspondence.html'
LEGACY_CORRESPONDENCE_TEMPLATES = {
    'docs/virtuozzo-cs-correspondence.md': LEGACY_CORRESPONDENCE_TEMPLATE,
    'docs/jelastic-cs-correspondence.md': 'theme/readthedocs/jelastic-cs-correspondence.html',
}
_SUPPORTED_CORRESPONDENCE_TEMPLATES = {
    'docs/virtuozzo-cs-correspondence.md': '064581ed50f9a811b86627a56cab9537e50ab5802484fec1fc322d505210852e',
    'docs/jelastic-cs-correspondence.md': '6137f5f71614614134ef981389a9ba351cd1fa5cdb4ef1d143a5434d543cfbb1',
}

# Exact source-authored navigation list, outside examples/comments only.
_PLACEHOLDER_INTRO = (
    'There are data conversion routines in Cloud Scripting which can be performed with '
    'specially developed *Data Processing Placeholders*:  \n'
)
_PLACEHOLDER_LIST = (
    '- [`${*.toBase64()}`](#${\\*.tobase64()}) - does data encoding into *Base64* format  \n'
    '- [`${*.fromBase64()}`](#${\\*.frombase64()}) - decodes data from *Base64* format  \n'
    '- [`${*.md5()}`](#${\\*.md5()}) - *md5* hash generator  \n'
    '- [`${*.join()}`](#${\\*.join()}) - concatenates data provided as array of words or objects  \n'
    '- [`${*.toJSON()}`](#${\\*.tojson()}) - converts array of of words or objects into JSON format  \n'
    '- [`${*.contains()}`](#${\\*.contains()}) - allows to find a word or object in the array of words or objects respectively   \n'
    '- [`${*.print()}`](#${\\*.print()}) - outputs an array of words or objects to the [console](http://docs.cloudscripting.com/troubleshooting/#troubleshooting)  \n'
)
_PLACEHOLDER_TARGETS = (
    "42tobase64", "42frombase64", "42md5", "42join", "42tojson", "42contains", "42print",
)


def _escape_shortcodes(text):
    # Hugo expands shortcodes even in fenced code and HTML comments. Escaped
    # shortcodes are rendered literally by Hugo, including their original spaces.
    return _LITERAL_SHORTCODE.sub(lambda m: m[0][:3] + '/*' + m[0][3:-3] + '*/' + m[0][-3:], text)


def _quote(value):
    return json.dumps(value, ensure_ascii=False)


class _Converter:
    def __init__(self, source, page):
        self.page = page
        self.newline = '\r\n' if '\r\n' in source else '\n'
        self.ids = set()
        self.has_title = False
        self.placeholder_lists = []

    def fail(self, line, evidence, issue_id='unsupported-markup'):
        raise ConversionError([dict(id=issue_id, source_path=self.page['source_path'],
                                    line=line, severity='error', evidence=evidence)])

    def escape(self, text, number):
        covered = _LITERAL_SHORTCODE.sub(lambda m: ' ' * len(m[0]), text)
        incomplete = re.search(r'\{\{[<%]', covered)
        if incomplete:
            self.fail(number + text[:incomplete.start()].count('\n'),
                      'Incomplete literal shortcode syntax requires review', 'unsupported-shortcode-literal')
        return _escape_shortcodes(text)

    def correspondence(self):
        source = self.page['source_path']
        template_path = LEGACY_CORRESPONDENCE_TEMPLATES.get(source)
        if template_path is None:
            self.fail(1, 'Unsupported generated correspondence source: ' + source,
                      'unsupported-correspondence-template')
        template = self.page.get('legacy_correspondence_template')
        if not isinstance(template, bytes):
            self.fail(1, 'Exact legacy template bytes are required: ' + template_path,
                      'unsupported-correspondence-template')
        digest = hashlib.sha256(template).hexdigest()
        if digest != _SUPPORTED_CORRESPONDENCE_TEMPLATES[source]:
            self.fail(1, 'Unsupported legacy correspondence template ' + template_path
                      + ' (sha256=' + digest + '); review the pinned release template',
                      'unsupported-correspondence-template')
        # Recognize complete template bytes for this route before extracting its
        # literal content. Never apply modern branding to an older source.
        text = template.decode('utf-8')
        prefix = text.split('{%', 1)[0]
        heading = re.fullmatch(r'<h1 id="([^"]+)">([^<]+)</h1>\s+([\s\S]+?)\s*', prefix)
        platform = re.findall(r'<th[^>]*>([^<]+)</th>', text)[1]
        return dict(anchor=heading[1], title=html.unescape(heading[2]), intro=heading[3], platform=platform)

    def anchor(self, text):
        # Matches vendored Python-Markdown toc.slugify and duplicate-ID suffixes.
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'!?\[([^]]*)\]\([^)]*\)', r'\1', text)
        # Legacy inline escape placeholders survived into toc.slugify as their
        # decimal character codes (notably \\* -> 42 in placeholder headings).
        text = re.sub(r'\\([!\"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', lambda m: str(ord(m[1])), text)
        text = html.unescape(text)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
        identifier = re.sub(r'[^\w\s-]', '', text).strip().lower()
        identifier = re.sub(r'[-\s]+', '-', identifier)
        while not identifier or identifier in self.ids:
            match = re.match(r'^(.*)_([0-9]+)$', identifier)
            identifier = f'{match[1]}_{int(match[2])+1}' if match else identifier + '_1'
        self.ids.add(identifier)
        return identifier

    def fence(self, lines, start):
        opening, number = lines[start]
        match = _FENCE.match(opening)
        marker, info = match[2], match[3].strip()
        if marker[0] == '`' and '`' in info:
            self.fail(number, 'Backticks in fence info are unsupported')
        if not re.fullmatch(r'[\w+.#-]*', info):
            self.fail(number, 'Unsupported fenced-code info: ' + info)
        close = re.compile('^' + re.escape(match[1]) + re.escape(marker[0]) + '{' + str(len(marker)) + r',}[ \t]*(?:\r?\n)?$')
        end = start + 1
        while end < len(lines) and not close.fullmatch(lines[end][0]):
            end += 1
        if end == len(lines):
            self.fail(number, 'Unclosed fenced code block', 'unclosed-fence')
        # Legacy fences close at the opening indentation. CommonMark also closes
        # on indented markers; lengthen the wrapper to protect literal nested
        # fences, without changing the legacy presentation tokens.
        body = ''.join(t for t, _ in lines[start+1:end])
        # Vendored Markdown NormalizeWhitespace runs before fenced extraction:
        # tab_length is four, line endings become LF, and spaces-only lines are
        # emptied. Apply that behavior only to this generated presentation body;
        # preserve significant trailing spaces, blank-line count and all tokens.
        # Admonition containers remove multiples of four columns, so tab stops
        # remain aligned with the original document before container removal.
        body = body.replace('\r\n', '\n').replace('\r', '\n').expandtabs(4)
        body = re.sub(r'(?m)^ +(?=\n)', '', body)
        inner = [len(m[1]) for m in re.finditer(r'^ {0,3}(' + re.escape(marker[0]) + r'{3,})[ \t]*$', body, re.M)]
        width = max([len(marker)] + [length + 1 for length in inner])
        if width > len(marker):
            opening = opening.replace(marker, marker[0] * width, 1)
            closing = lines[end][0].replace(marker[0] * len(marker), marker[0] * width, 1)
        else:
            closing = lines[end][0]
        # Goldmark discards terminal blank lines before invoking its code hook.
        # Keep terminal blank lines in the presentation; annotate exceptional counts.
        final_newlines = body[len(body.rstrip('\r\n')):].count('\n')
        if final_newlines != 1:
            ending = opening[len(opening.rstrip('\r\n')):]
            opening = opening.rstrip('\r\n') + ' {cs_trailing_newlines=' + str(final_newlines) + '}' + ending
        return self.escape(opening + body + closing, number), end + 1, info

    def tabs(self, lines, start):
        out = ['{{% tabs %}}' + self.newline + self.newline]
        i = start + 1
        items = 0
        while i < len(lines):
            text, number = lines[i]
            if text.strip() == '@@!':
                if not items:
                    self.fail(number, 'Tab group has no fenced examples')
                out.append('{{% /tabs %}}' + self.newline + self.newline)
                return ''.join(out), i + 1
            if not text.strip():
                i += 1
                continue
            if not _FENCE.match(text):
                self.fail(number, 'Tab groups may contain only fenced examples and blank lines')
            block, i, language = self.fence(lines, i)
            title = language.upper() or 'TEXT'
            out.extend(['{{% tabs-item title=' + _quote(title) + ' %}}' + self.newline + self.newline,
                        block, self.newline, '{{% /tabs-item %}}' + self.newline + self.newline])
            items += 1
        self.fail(lines[start][1], 'Unclosed tab group', 'unclosed-tabs')

    def blocks(self, lines):
        out = []
        i = 0
        while i < len(lines):
            text, number = lines[i]
            # A fence takes precedence over comment-looking example content.
            if _FENCE.match(text):
                block, i, _ = self.fence(lines, i)
                out.append(block)
                continue
            if '<!--' in text:
                # Preserve the complete comment, including its legacy delimiters.
                comment = [text]
                while '<!--' in ''.join(comment) and ''.join(comment).rfind('<!--') > ''.join(comment).rfind('-->'):
                    i += 1
                    if i == len(lines):
                        self.fail(number, 'Unclosed HTML comment', 'unclosed-comment')
                    comment.append(lines[i][0])
                out.append(self.escape(''.join(comment), number))
                i += 1
                continue
            if (self.page['source_path'] == 'docs/creating-manifest/placeholders.md'
                    and 'data-processing-placeholders' in self.ids
                    and i > 0 and lines[i-1][0] == _PLACEHOLDER_INTRO
                    and ''.join(t for t, _ in lines[i:i+7]) == _PLACEHOLDER_LIST
                    # Match the complete reviewed list boundary, not a prefix
                    # of a longer/loose list or an item with extra content.
                    and ''.join(t for t, _ in lines[i+7:i+9]) == '\n### ${\\*.toBase64()}\n'):
                replacement = _PLACEHOLDER_LIST
                for target in _PLACEHOLDER_TARGETS:
                    name = target.removeprefix('42')
                    replacement = replacement.replace('#${\\*.' + name + '()}', '#' + target)
                self.placeholder_lists.append((out, len(out), replacement))
                out.append(_PLACEHOLDER_LIST)
                i += 7
                continue
            stripped = text.strip()
            if stripped == '@@@':
                block, i = self.tabs(lines, i)
                out.append(block)
                continue
            if stripped.startswith(('@@@', '@@!')):
                self.fail(number, 'Unexpected or malformed tab delimiter')
            if text.startswith('!!!'):
                match = _ADMONITION.fullmatch(text.rstrip('\r\n'))
                if not match:
                    self.fail(number, 'Malformed admonition marker or title')
                kind, title = match[1].lower(), match[2]
                if kind not in {'note', 'tip', 'warning', 'danger', 'important', 'attention', 'caution', 'hint', 'error', 'info', 'success', 'question', 'example', 'quote', 'abstract', 'todo', 'seealso'}:
                    self.fail(number, 'Unsupported admonition type: ' + kind)
                body = []
                i += 1
                while i < len(lines):
                    inner, inner_number = lines[i]
                    if not inner.strip():
                        body.append((inner, inner_number))
                    elif inner.startswith('    '):
                        body.append((inner[4:], inner_number))
                    elif inner.startswith('\t'):
                        body.append((inner[1:], inner_number))
                    else:
                        break
                    i += 1
                if not any(t.strip() for t, _ in body):
                    self.fail(number, 'Admonition has no indented body')
                out.extend([self.newline, '{{% cs-admonition type=' + _quote(kind) + ' title=' + _quote(title if title is not None else kind.title()) + ' %}}' + self.newline + self.newline,
                            self.blocks(body), self.newline, '{{% /cs-admonition %}}' + self.newline + self.newline])
                continue
            line = text.rstrip('\r\n')
            heading = _HEADING.fullmatch(line)
            if heading:
                # End a preceding raw-HTML block (for example <br>) so Goldmark
                # parses the heading and its explicit compatibility fragment.
                out.append(self.newline)
                level, label = heading.groups()
                explicit = re.search(r'\s+\{#([\w.-]+)\}$', label)
                if explicit:
                    self.ids.add(explicit[1])
                else:
                    label += ' {#' + self.anchor(label) + '}'
                if not self.has_title:
                    level = '#'
                    self.has_title = True
                text = level + ' ' + label + text[len(line):]
            elif re.match(r'^<h1(?:\s|>)', text, re.I):
                self.has_title = True
            # Markdown images embedded in center wrappers remain raw text in
            # Goldmark. Give the Markdown a standalone block within the wrapper.
            text = re.sub(r'(<center>)\s*(!\[[^\n]*?\]\([^\n]*?\))\s*(</center>)',
                          lambda m: m[1] + self.newline*2 + m[2] + self.newline*2 + m[3], text)
            out.append(self.escape(text, number))
            i += 1
        if set(_PLACEHOLDER_TARGETS) <= self.ids:
            for container, index, replacement in self.placeholder_lists:
                if container is out:
                    out[index] = replacement
        return ''.join(out)


def convert_document(source: bytes, page: dict) -> tuple[bytes, list[dict]]:
    """Convert one explicitly published page or raise ConversionError; never write.

    The generated front matter marks schema 1. Passing that result again is a
    no-op; repeated directory conversion also derives output solely from source.
    All emitted wrappers use the source document's newline convention.
    """
    converter = _Converter('', page)
    if page.get('published') is not True:
        converter.fail(1, 'Unpublished sources cannot enter the content tree', 'unpublished-source')
    try:
        text = source.decode('utf-8-sig')
    except UnicodeDecodeError as error:
        converter.fail(1, 'Source is not UTF-8: ' + str(error), 'invalid-encoding')
    converter = _Converter(text, page)
    if text.startswith('---\n') or text.startswith('---\r\n'):
        front = re.match(r'^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)', text)
        if front:
            try:
                metadata = yaml.safe_load(front[1])
            except yaml.YAMLError:
                metadata = None
            if isinstance(metadata, dict) and metadata.get(_MARKER) == 1:
                return source, []
        converter.fail(1, 'Existing unrecognized front matter requires review')
    correspondence = None
    if page['source_path'].endswith('-cs-correspondence.md'):
        correspondence = converter.correspondence()
        page = dict(page, title=correspondence['title'])
        converter.page = page
        converter.has_title = True
    lines = [(line, number) for number, line in enumerate(text.splitlines(keepends=True), 1)]
    body = converter.blocks(lines)
    newline = converter.newline
    if correspondence:
        shortcode = '{{< cs-correspondence >}}'
        if correspondence['platform'] == 'Jelastic':
            # Narrow source-defined table restoration approved after the legacy
            # all_jel_versions alias counterfactual; retain its historical label.
            shortcode = '{{< cs-correspondence platform="Jelastic" >}}'
        body = ('# ' + page['title'] + ' {#' + correspondence['anchor'] + '}' + newline*2
                + correspondence['intro'] + newline*2 + shortcode + newline*2 + body)
    elif not converter.has_title:
        body = '# ' + page['title'] + ' {#' + converter.anchor(page['title']) + '}' + newline*2 + body
    if not isinstance(page.get('weight'), int) or page['weight'] == 0:
        converter.fail(1, 'Published navigation requires a nonzero integer weight', 'invalid-metadata')
    menu = dict(identifier=page['menu_id'], name=page['nav_title'], title=page['nav_title'], weight=page['weight'])
    if page.get('menu_parent'):
        menu['parent'] = page['menu_parent']
    metadata = dict(title=page['title'], draft=False, menu=dict(docs=menu), **{_MARKER: 1})
    front = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, line_break=newline)
    return ('---' + newline + front + '---' + newline + newline + body).encode('utf-8'), []
