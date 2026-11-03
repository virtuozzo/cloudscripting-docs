"""Preserve rendered legacy destinations using prefix-independent page-relative URLs.

Only prose Markdown destinations and HTML src/href attribute values are edited.
Code, comments, front matter and the rest of every HTML tag retain their bytes.
"""
import html
from html.parser import HTMLParser
import posixpath
import re
from urllib.parse import urljoin, urlsplit, urlunsplit


def _protected(text):
    """Locate literal regions in document order, so examples cannot open comments."""
    spans = []
    if text.startswith('---\n') or text.startswith('---\r\n'):
        end = re.search(r'^---\s*$', text[4:], re.M)
        if end:
            spans.append((0, end.end() + 4))
    fence = None
    list_indent = None
    offset = 0
    for line in text.splitlines(keepends=True):
        end_of_line = offset + len(line)
        container = re.match(r'^[ \t]*(?:>[ \t]*)*', line)[0]
        quote_depth = container.count('>')
        content = line[len(container):]
        if fence and quote_depth < fence[1]:
            # A fenced block cannot lazily continue outside its blockquote.
            fence = None
        if fence:
            spans.append((offset, end_of_line))
            closing = re.match(r'(`{3,}|~{3,})(.*)', content)
            if closing and quote_depth == fence[1] and closing[1][0] == fence[0][0] and len(closing[1]) >= len(fence[0]) and not closing[2].strip():
                fence = None
            offset = end_of_line
            continue
        covered = next((end for start, end in spans if start <= offset < end), None)
        if covered is None:
            opening = re.match(r'(`{3,}|~{3,})(.*)', content)
            if opening:
                fence = (opening[1], quote_depth)
                spans.append((offset, end_of_line))
                offset = end_of_line
                continue
            item = re.match(r'^( *)(?:[-+*]|[0-9]+[.)]) +', line)
            indent = len(line) - len(line.lstrip(' '))
            if item:
                list_indent = item.end()
            elif line.strip() and list_indent is not None and indent < list_indent:
                list_indent = None
            if indent >= (list_indent + 4 if list_indent is not None else 4) or line.startswith('\t'):
                spans.append((offset, end_of_line))
                offset = end_of_line
                continue
        cursor = covered if covered is not None else offset
        while cursor < end_of_line:
            if text.startswith('<!--', cursor):
                closing = text.find('-->', cursor + 4)
                end = len(text) if closing < 0 else closing + 3
            elif text[cursor] == '`':
                delimiter = re.match(r'`+', text[cursor:])[0]
                closing = re.search(r'(?<!`)' + re.escape(delimiter) + r'(?!`)', text[cursor + len(delimiter):])
                if not closing:
                    cursor += len(delimiter)
                    continue
                end = cursor + len(delimiter) + closing.end()
            else:
                opening = re.match(r'<(pre|code|script|style)\b[^>]*>', text[cursor:], re.I)
                if not opening:
                    cursor += 1
                    continue
                closing = re.search(r'</' + opening[1] + r'\s*>', text[cursor + opening.end():], re.I)
                end = len(text) if closing is None else cursor + opening.end() + closing.end()
            spans.append((cursor, end))
            cursor = end
        offset = end_of_line
    return spans


def _destination(value, page, baseline, raw=False):
    decoded = html.unescape(value) if raw else value
    split = urlsplit(decoded)
    if split.scheme or split.netloc or not split.path:
        return value
    route = page['old_url']
    captured = baseline.get('pages', {}).get(route)
    if captured is None:
        raise ValueError('Missing rendered baseline page: ' + route)
    references = captured.get('links', []) + captured.get('images', [])
    if raw:
        matches = [r['resolved_url'] for r in references if r.get('href', r.get('src')) == decoded]
        target = matches[0] if matches else urljoin(route, decoded)
    elif split.path.lower().endswith('.md'):
        source = page.get('source_path', 'docs' + route.rstrip('/') + '.md')
        source_path = posixpath.normpath(posixpath.join(posixpath.dirname(source), split.path)) if not split.path.startswith('/') else 'docs/' + split.path.lstrip('/')
        targets = [url for url, record in baseline.get('pages', {}).items() if record.get('source_path') == source_path]
        target = urlunsplit(('', '', targets[0], split.query, split.fragment)) if targets else urljoin(route, decoded)
    else:
        # MkDocs rewrites Markdown media against the source directory; raw HTML
        # bypasses its treeprocessor. The rendered capture is authoritative.
        source = page.get('source_path') or captured.get('source_path') or ('docs' + route.rstrip('/') + '.md')
        source_dir = posixpath.dirname(source).removeprefix('docs') + '/'
        candidate = urljoin(source_dir, decoded)
        matches = [r['resolved_url'] for r in references if r.get('resolved_url') == candidate]
        target = matches[0] if matches else candidate
    result = urlsplit(target)
    if result.scheme or result.netloc:
        return value
    # urllib can return a relative path when a reference climbs above '/'.
    # Browser URL resolution clamps at the site root; filesystem cwd is irrelevant.
    rooted_path = '/' + result.path.lstrip('/')
    relative = posixpath.relpath(rooted_path, route)
    if result.path.endswith('/'):
        relative += '/'
    normalized = urlunsplit(('', '', relative, result.query, result.fragment))
    # Decoded quotes must never become attribute delimiters. Escape both quote
    # styles so named/numeric input entities retain their URL meaning in HTML.
    return html.escape(normalized, quote=True) if raw else normalized


class _Tags(HTMLParser):
    def __init__(self, text, visible, rewrite):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.visible = visible
        self.rewrite = rewrite
        self.edits = []
        self.offsets = [0]
        self.offsets.extend(m.end() for m in re.finditer('\n', text))

    def handle_starttag(self, tag, attrs):
        row, column = self.getpos()
        start = self.offsets[row - 1] + column
        original = self.get_starttag_text()
        if not self.visible[start:start + len(original)].strip():
            return
        # Attribute tokenizer edits values in-place; HTMLParser supplies tag
        # boundaries without reserializing case, spacing, entities or quotes.
        pattern = r'''([^\s=<>/]+)(\s*=\s*)(?:"([^"]*)"|'([^']*)'|([^\s>]+))'''
        for match in re.finditer(pattern, original):
            if match[1].lower() not in ('src', 'href'):
                continue
            group = next(g for g in (3, 4, 5) if match[g] is not None)
            self.edits.append((start + match.start(group), start + match.end(group), self.rewrite(match[group], True)))

    handle_startendtag = handle_starttag


def _markdown_destinations(text):
    # Reference definitions, including optional angle-delimited destinations.
    for match in re.finditer(r'^ {0,3}\[[^]\n]+\]:[ \t]*(?:<([^>\n]*)>|([^\s]+))', text, re.M):
        group = 1 if match[1] is not None else 2
        yield match.start(group), match.end(group)
    # Inline links/images: balance parentheses, preserve optional title text.
    for match in re.finditer(r'(?<!\\)\]\([ \t]*', text):
        start = match.end()
        if start >= len(text):
            continue
        if text[start] == '<':
            end = text.find('>', start + 1)
            if end != -1:
                yield start + 1, end
            continue
        level = 0
        end = start
        while end < len(text):
            char = text[end]
            if char == '\\':
                end += 2
                continue
            if char == '(':
                level += 1
            elif char == ')':
                if level == 0:
                    break
                level -= 1
            elif char.isspace() and level == 0:
                break
            end += 1
        if end > start:
            yield start, end


def normalize_document(markdown: bytes, page: dict, baseline: dict) -> bytes:
    text = markdown.decode('utf-8')
    visible = list(text)
    for start, end in _protected(text):
        visible[start:end] = [c if c in '\r\n' else ' ' for c in text[start:end]]
    visible = ''.join(visible)
    parser = _Tags(text, visible, lambda value, raw: _destination(value, page, baseline, raw))
    parser.feed(visible)
    edits = parser.edits
    # HTML attribute URLs cannot simultaneously be Markdown destinations.
    for start, end in _markdown_destinations(visible):
        if not any(a <= start < b for a, b, _ in edits):
            edits.append((start, end, _destination(text[start:end], page, baseline)))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text.encode('utf-8')


def bundle_markdown_images(markdown, resources):
    """Point supported prose images at collision-free local page resources."""
    text = markdown.decode('utf-8')
    visible = list(text)
    for start, end in _protected(text):
        visible[start:end] = [c if c in '\r\n' else ' ' for c in text[start:end]]
    visible = ''.join(visible)
    edits = []
    by_url = {r['relative_url']: r['name'] for r in resources}
    for start, end in _markdown_destinations(visible):
        # Only inline images; reference images can safely use static fallback.
        opening = visible.rfind('![', 0, start)
        closing = visible.rfind(']', 0, start)
        if opening >= 0 and visible.find(']', opening) == closing and visible[closing + 1:start].lstrip().startswith('('):
            value = text[start:end]
            split = urlsplit(value)
            if split.path in by_url:
                edits.append((start, end, urlunsplit(('', '', by_url[split.path], split.query, split.fragment))))
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text.encode('utf-8')
