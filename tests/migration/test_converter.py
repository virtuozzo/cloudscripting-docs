"""Behavioral regressions: loss, publication, example mutation and unsafe paths."""
import hashlib
import html5lib
from html.parser import HTMLParser
import os
import shutil
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
BASELINE_COMMIT = '76628f8aa01571fbc348211cb7df726cf408cd17'
FIXTURES = Path(__file__).parent / 'fixtures/conversion'
SPEC = importlib.util.find_spec('scripts.migration.markdown_converter')
if SPEC:
    from scripts.migration.markdown_converter import convert_document, ConversionError


def frozen_source(path):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(ROOT),
                                    'show', BASELINE_COMMIT + ':' + path])


def page(**changes):
    record = dict(source_path='docs/example.md', title='Example', nav_title='Navigation label',
                  published=True, menu_id='page-example', menu_parent='group', weight=10,
                  target_path='content/nested/example/index.md', old_url='/nested/example/')
    return dict(record, **changes)


def active_blocks(raw):
    """Independent test oracle: skip comments; extract fences without interpreting code."""
    result = []
    lines = raw.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if b'<!--' in lines[i]:
            while i < len(lines) and b'-->' not in lines[i]:
                i += 1
            i += 1
            continue
        match = re.match(rb'^([ \t]*)(`{3,}|~{3,})[ \t]*([^\r\n]*)', lines[i])
        if not match:
            i += 1
            continue
        indent, marker, language = match.groups()
        language = language.strip().split(b' ')[0].decode()
        i += 1
        body = []
        while i < len(lines) and not re.fullmatch(re.escape(indent) + marker[:1] + rb'{' + str(len(marker)).encode() + rb',}[ \t]*(?:\r?\n)?', lines[i]):
            body.append(lines[i][len(indent):] if lines[i].startswith(indent) else lines[i])
            i += 1
        result.append((language, b''.join(body)))
        i += 1
    return result


def legacy_blocks(route):
    """Independent captured-copy oracle; only the approved lost pair is added."""
    directory = ROOT/'tests/migration/fixtures/baseline'
    baseline = json.loads((directory/'legacy-root.json').read_text())
    if baseline['inputs']['source_commit'] != '76628f8aa01571fbc348211cb7df726cf408cd17':
        raise AssertionError('Unexpected captured-copy source pin')
    blocks = []
    for block in baseline['pages'][route]['code_blocks']:
        raw = (directory/block['text_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != block['sha256']:
            raise AssertionError('Captured code fixture hash mismatch: '+block['text_path'])
        blocks.append((block['language'] or '', raw))
    if route == '/creating-manifest/handling-custom-responses/':
        # Exact literals independently transcribed from source77–99 at the pin
        # above; this active pair was swallowed by the adjacent legacy note.
        if len(blocks) != 20:
            raise AssertionError('Unexpected legacy Custom Responses shape')
        blocks[4:4] = [
            ('yaml', b'type: update\nname: response handlers\n\nonInstall:\n  return:\n    result: warning\n    message: Warning!\n    email: string\n'),
            ('json', b'{\n    "type": "update",\n    "name": "response handlers",\n    "onInstall": {\n        "return": {\n          "result": "warning",\n          "message": "Warning!",\n          "email": "string"\n        }\n    }\n}\n')]
    return blocks


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(SPEC, 'converter implementation is missing')

    def convert(self, raw, **changes):
        record = page(**changes)
        if record['source_path'] == 'docs/virtuozzo-cs-correspondence.md':
            record['legacy_correspondence_template'] = (FIXTURES/'correspondence-template.html').read_bytes()
        result, issues = convert_document(raw, record)
        self.assertEqual(issues, [])
        return result

    def test_legacy_copy_tab_stops_blank_lines_and_significant_spaces(self):
        raw = (b'# Example\n\n```text\n \t \n'
               b'a\tb\nab\tc\nabc\td\nabcd\te\n\tindent\n'
               b'    \nvalue: ${token}  \n\n```\n')
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), [('text',
            b'\na   b\nab  c\nabc d\nabcd    e\n    indent\n\nvalue: ${token}  \n\n')])
        self.assertIn(b'cs_trailing_newlines=2', result)
        self.assertIn(b'\t', raw)  # The original input remains unchanged.

    def test_legacy_copy_normalizes_line_endings_without_touching_original(self):
        raw = b'# Example\r\n\r\n```yaml\r\na:\t1\r\n  \r\n```\r\n'
        original = bytes(raw)
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), [('yaml', b'a:  1\n\n')])
        self.assertEqual(raw, original)

    def test_legacy_copy_keeps_admonition_container_indent_out_of_tab_stops(self):
        raw = b'# Example\n\n!!! note\n    ```text\n    \tkey:\tvalue\n    ```\n'
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), [('text', b'    key:    value\n')])

    def test_actions_install_example_matches_legacy_copy_and_parses_as_yaml(self):
        record = next(p for p in json.loads((ROOT/'migration/page-map.json').read_text())['pages']
                      if p['source_path'] == 'docs/creating-manifest/actions.md')
        raw = frozen_source(record['source_path'])
        original_body = active_blocks(raw)[143][1]
        self.assertEqual(original_body.count(b'\t'), 18)
        with self.assertRaises(yaml.scanner.ScannerError):
            yaml.safe_load(original_body)
        converted, _ = convert_document(raw, record)
        copied = active_blocks(converted)[143][1]
        self.assertEqual(copied, legacy_blocks('/creating-manifest/actions/')[143][1])
        self.assertEqual(yaml.safe_load(copied)['onInstall'][0]['install']['type'], 'install')
        self.assertEqual(frozen_source(record['source_path']), raw)

    def test_ordered_tabs_preserve_code_bytes_and_literal_delimiters(self):
        raw = (FIXTURES / 'tabs.md').read_bytes()
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), active_blocks(raw))
        self.assertEqual([x[0] for x in active_blocks(result)], ['yaml', 'json', 'bash'])
        self.assertEqual(result.count(b'{{% tabs %}}'), 2)
        self.assertLess(result.index(b'title="YAML"'), result.index(b'title="JSON"'))
        self.assertIn(b'title="BASH"', result)
        self.assertIn(b'@@@\n@@!\n', result)

    def test_nested_literal_fences_do_not_end_an_example(self):
        raw = b'# Example\n\n@@@\n```yaml\ndescription: |\n  ```\n  # literal example\n  ```\n```\n@@!\n'
        result = self.convert(raw)
        self.assertIn(b'````yaml\n', result)
        self.assertEqual(active_blocks(result), [('yaml', b'description: |\n  ```\n  # literal example\n  ```\n')])

    def test_literal_shortcodes_preserve_rendered_and_clipboard_text(self):
        hugo = os.environ.get('HUGO_BIN') or shutil.which('hugo')
        if not hugo:
            self.skipTest('Pinned Hugo needed for rendering proof (set HUGO_BIN)')
        raw = (b'# Example\n\n<br>\n### After Break\n\n<!-- {{< ghost >}} -->\n\n@@@\n```text\n'
               b'<div>literal</div> https://example.test/?a=1&b=2 ${value}\n'
               b'{{< ghost >}}\n{{% ghost title="literal" %}}\n{{% /ghost %}}\n{{</* escaped */>}}\n'
               b'```\n@@!\n')
        result = self.convert(raw)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'content').mkdir()
            (root/'content/example.md').write_bytes(result)
            (root/'layouts/_default').mkdir(parents=True)
            (root/'layouts/shortcodes').mkdir()
            (root/'layouts/_default/single.html').write_text('{{ .Content }}')
            (root/'layouts/_default/_markup').mkdir()
            (root/'layouts/_default/_markup/render-codeblock.html').write_text('<pre><code>{{ .Inner }}{{ "\\n" }}</code></pre><textarea>{{ .Inner }}{{ "\\n" }}</textarea>')
            for name in ('tabs', 'tabs-item'):
                template = (ROOT/'themes/compose-master/layouts/shortcodes'/f'{name}.html').read_text()
                (root/'layouts/shortcodes'/f'{name}.html').write_text(template.replace('.Inner | markdownify', '.Inner'))
            (root/'hugo.yaml').write_text('markup:\n  goldmark:\n    parser:\n      attribute: true\n    renderer:\n      unsafe: true\n')
            run = subprocess.run([hugo, '--source', str(root), '--destination', str(root/'public')], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            class CodeText(HTMLParser):
                def __init__(self):
                    super().__init__(); self.code=[]; self.copied=[]; self.in_code=False; self.in_copy=False; self.ids=set()
                def handle_starttag(self, tag, attrs):
                    if 'id' in dict(attrs): self.ids.add(dict(attrs)['id'])
                    if tag == 'code': self.in_code=True
                    if tag == 'textarea': self.in_copy=True
                def handle_endtag(self, tag):
                    if tag == 'code': self.in_code=False
                    if tag == 'textarea': self.in_copy=False
                def handle_data(self, data):
                    if self.in_code: self.code.append(data)
                    if self.in_copy: self.copied.append(data)
            captured = CodeText()
            captured.feed((root/'public/example/index.html').read_text())
            expected = ('<div>literal</div> https://example.test/?a=1&b=2 ${value}\n'
                        '{{< ghost >}}\n{{% ghost title="literal" %}}\n{{% /ghost %}}\n{{</* escaped */>}}\n')
            self.assertEqual(''.join(captured.code), expected)
            self.assertEqual(''.join(captured.copied), expected)
            self.assertIn('after-break', captured.ids)

    def test_comment_looking_html_inside_code_is_literal(self):
        raw = b'# Example\n\n```html\n<!-- visible example text -->\n<div>content</div>\n```\n'
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), [('html', b'<!-- visible example text -->\n<div>content</div>\n')])

    def test_empty_fence_and_single_blank_line_have_distinct_metadata(self):
        empty = self.convert(b'# Example\n\n```text\n```\n')
        blank = self.convert(b'# Example\n\n```text\n\n```\n')
        self.assertIn(b'```text {cs_trailing_newlines=0}\n', empty)
        self.assertEqual(active_blocks(empty), [('text', b'')])
        self.assertNotIn(b'cs_trailing_newlines', blank)
        self.assertEqual(active_blocks(blank), [('text', b'\n')])

    def test_multiple_final_newlines_are_recorded_without_altering_body(self):
        raw = b'# Example\n\n```yaml\nvalue: 1\n\n```\n'
        result = self.convert(raw)
        self.assertIn(b'```yaml {cs_trailing_newlines=2}\n', result)
        self.assertEqual(active_blocks(result), [('yaml', b'value: 1\n\n')])
        ordinary = self.convert(b'# Example\n\n```yaml\nvalue: 1\n```\n')
        self.assertNotIn(b'cs_trailing_newlines', ordinary)

    def test_crlf_original_is_preserved_while_copy_uses_legacy_lf(self):
        raw = b'# Example\r\n\r\n@@@\r\n``` yaml\r\nx:  1\r\n\r\n```\r\n@@!\r\n'
        result = self.convert(raw)
        self.assertEqual(active_blocks(result), [('yaml', b'x:  1\n\n')])
        self.assertIn(b'\r\n', raw)

    def test_html_comments_keep_hidden_tabs_hidden(self):
        raw = b'# Example\n\n<!--\n@@@\n```yaml\nhidden: true\n```\n@@!\n-->\n\nVisible\n'
        result = self.convert(raw)
        self.assertIn(raw[raw.index(b'<!--'):raw.index(b'-->')+3], result)
        self.assertNotIn(b'{{% tabs %}}', result)
        self.assertEqual(active_blocks(result), [])

    def test_nested_admonition_retains_lists_images_and_code(self):
        raw = (FIXTURES / 'admonition.md').read_bytes()
        result = self.convert(raw)
        self.assertIn(b'{{% cs-admonition type="warning" title="Read carefully" %}}', result)
        self.assertIn(b'{{% cs-admonition type="note" title="Note" %}}', result)
        self.assertIn(b'- item\n  - nested\n', result)
        self.assertIn(b'![image](/img/exactCase.svg)', result)
        self.assertEqual(active_blocks(result), [('yaml', b'a: ${value}\n  nested: true\n')])
        self.assertIn(b'After the note.', result)

    def test_no_space_note_is_supported(self):
        result = self.convert(b'# Example\n\n!!!Note\n    Global scope survives.\n')
        self.assertIn(b'type="note" title="Note"', result)
        self.assertIn(b'Global scope survives.', result)

    def test_malformed_delimiters_fail_with_source_line(self):
        for raw, line in [(b'# Example\n@@!\n', 2), (b'# Example\n@@@\n', 2),
                          (b'# Example\n@@@\ntext lost?\n@@!\n', 3),
                          (b'# Example\n```yaml\nmissing close\n', 2),
                          (b'# Example\n!!!\n    body\n', 2),
                          (b'# Example\n<!-- unclosed\n', 2),
                          (b'# Example\n```text\n{{< unfinished\n```\n', 3),
                          (b'# Example\n```text\n{{< mismatched %}}\n```\n', 3)]:
            with self.subTest(raw=raw):
                with self.assertRaises(ConversionError) as caught:
                    self.convert(raw)
                issue = caught.exception.issues[0]
                self.assertEqual(issue['source_path'], 'docs/example.md')
                self.assertEqual(issue['line'], line)
                self.assertEqual(issue['severity'], 'error')

    def test_one_article_title_and_legacy_duplicate_heading_anchors(self):
        raw = b'## Example\n\n### loggerName\n### onBeforeInit\n### onBeforeInit\n\n```md\n# Example demonstration\n```\n'
        result = self.convert(raw)
        body = result.split(b'---', 2)[2]
        self.assertIn(b'# Example {#example}', body)
        self.assertIn(b'### loggerName {#loggername}', body)
        self.assertIn(b'### onBeforeInit {#onbeforeinit_1}', body)
        self.assertEqual(active_blocks(result), [('md', b'# Example demonstration\n')])

    def test_legacy_no_space_headings_and_escaped_placeholder_ids(self):
        result = self.convert(b'# Example\n\n###Skip Node Emails\n##Relative Links\n### ${\\*.toBase64()}\n')
        self.assertIn(b'### Skip Node Emails {#skip-node-emails}', result)
        self.assertIn(b'## Relative Links {#relative-links}', result)
        self.assertIn(b'{#42tobase64}', result)

    def test_current_heading_fragments_are_preserved(self):
        pages = json.loads((ROOT/'migration/page-map.json').read_text())['pages']
        baseline = json.loads((ROOT/'tests/migration/fixtures/baseline/legacy-root.json').read_text())
        for record in pages:
            if not record['published']:
                continue
            if record['source_path'] == 'docs/virtuozzo-cs-correspondence.md':
                record = dict(record, legacy_correspondence_template=(FIXTURES/'correspondence-template.html').read_bytes())
            result, _ = convert_document(frozen_source(record['source_path']), record)
            identifiers = set(re.findall(rb'\{#([^}]+)\}|\bid=["\']([^"\']+)', result))
            identifiers = {(a or b).decode() for a,b in identifiers}
            expected = {h['id'] for h in baseline['pages'][record['old_url']]['headings'] if h['id']}
            self.assertFalse(expected - identifiers, (record['source_path'], expected-identifiers))

    def test_frontmatter_separates_article_and_menu_title(self):
        result = self.convert(b'# Example\n')
        front = yaml.safe_load(result.split(b'---', 2)[1])
        self.assertEqual(front['title'], 'Example')
        self.assertEqual(front['menu']['docs']['title'], 'Navigation label')
        self.assertEqual(front['menu']['docs']['identifier'], 'page-example')
        self.assertFalse(front['draft'])
        self.assertNotIn('url', front)  # Hugo derives the nested path; version baseURL remains effective.

    def test_reconversion_is_stable(self):
        raw = (FIXTURES / 'tabs.md').read_bytes()
        first = self.convert(raw)
        self.assertEqual(first, self.convert(raw))
        self.assertEqual(first, self.convert(first))

    def test_correspondence_page_emits_generated_table_contract(self):
        result = self.convert(b'Versions intro\n', source_path='docs/virtuozzo-cs-correspondence.md', title='Versions')
        self.assertEqual(result.count(b'{{< cs-correspondence >}}'), 1)
        self.assertEqual(result, self.convert(result, source_path='docs/virtuozzo-cs-correspondence.md', title='Versions'))

    def test_correspondence_preserves_template_intro_and_link(self):
        result = self.convert(b'Original article body.\n', source_path='docs/virtuozzo-cs-correspondence.md')
        intro = (b'The table below displays dependencies between Cloud Scripting and the Virtuozzo Application Platform versions within the same '
                 b'<a href="https://www.virtuozzo.com/application-platform-partners/" target="_blank">hosting provider</a> platform.')
        self.assertIn(intro, result)
        self.assertLess(result.index(intro), result.index(b'{{< cs-correspondence >}}'))
        self.assertLess(result.index(b'{{< cs-correspondence >}}'), result.index(b'Original article body.'))
        self.assertIn(b'Original article body.', result)
        self.assertIn(b'{#virtuozzo-cs-correspondence}', result)

    def test_correspondence_requires_supported_pinned_template_context(self):
        for template in [None, b'<h1>Different historical title</h1>\nHistorical intro.',
                         (FIXTURES/'correspondence-template.html').read_bytes().replace(b'Virtuozzo', b'Other')]:
            with self.subTest(template=template):
                with self.assertRaises(ConversionError) as caught:
                    convert_document(b'Versions article\n', page(source_path='docs/virtuozzo-cs-correspondence.md', legacy_correspondence_template=template))
                self.assertEqual(caught.exception.issues[0]['id'], 'unsupported-correspondence-template')

    def test_jelastic_correspondence_preserves_source_branding_and_order(self):
        raw = (FIXTURES/'correspondence-jelastic-source.md').read_bytes()
        template = (FIXTURES/'correspondence-jelastic-template.html').read_bytes()
        record = page(source_path='docs/jelastic-cs-correspondence.md', old_url='/jelastic-cs-correspondence/',
                      target_path='content/jelastic-cs-correspondence/index.md', legacy_correspondence_template=template)
        result, issues = convert_document(raw, record)
        self.assertEqual(issues, [])
        front = yaml.safe_load(result.split(b'---', 2)[1])
        self.assertEqual(front['title'], 'Jelastic & CS Correspondence')
        self.assertIn(b'# Jelastic & CS Correspondence {#jelastic-cs-correspondence}', result)
        self.assertIn(b'<a href="https://jelastic.cloud/" target="_blank">hosting provider</a>', result)
        self.assertIn(b'{{< cs-correspondence platform="Jelastic" >}}', result)
        self.assertLess(result.index(b'{{< cs-correspondence platform="Jelastic" >}}'), result.index(next(line for line in raw.splitlines() if line.strip())))
        self.assertNotIn(b'Virtuozzo', result)
        self.assertEqual(result, convert_document(result, record)[0])

    def test_generated_correspondence_rejects_unknown_or_mismatched_context(self):
        for source, template in [
            ('docs/jelastic-cs-correspondence.md', None),
            ('docs/jelastic-cs-correspondence.md', (FIXTURES/'correspondence-template.html').read_bytes()),
            ('docs/other-cs-correspondence.md', (FIXTURES/'correspondence-jelastic-template.html').read_bytes())]:
            with self.subTest(source=source):
                with self.assertRaises(ConversionError) as caught:
                    convert_document(b'Original versions body.\n', page(source_path=source, legacy_correspondence_template=template))
                self.assertEqual(caught.exception.issues[0]['id'], 'unsupported-correspondence-template')

    def test_both_correspondence_variants_render_exact_rows_before_authored_prose(self):
        hugo = os.environ.get('HUGO_BIN') or shutil.which('hugo')
        if not hugo:
            self.skipTest('Pinned Hugo needed for correspondence rendering proof')
        variants = [
            ('virtuozzo', frozen_source('docs/virtuozzo-cs-correspondence.md'),
             (FIXTURES/'correspondence-template.html').read_bytes(),
             'Virtuozzo Application Platform & CS Correspondence', 'Virtuozzo PaaS',
             'https://www.virtuozzo.com/application-platform-partners/'),
            ('jelastic', (FIXTURES/'correspondence-jelastic-source.md').read_bytes(),
             (FIXTURES/'correspondence-jelastic-template.html').read_bytes(),
             'Jelastic & CS Correspondence', 'Jelastic', 'https://jelastic.cloud/')]
        expected_releases = ['8.15.1', '8.14.3', '8.14.2', '8.13.1', '8.12.1', '8.11.1', '8.10.2', '8.10.1',
                             '8.8.1', '8.6.2', '8.6.1', '8.4.1', '8.3.3', '8.3.2', '8.3.1', '8.2.5', '8.2.4',
                             '8.2.2', '8.1.1', '8.0.2', '7.3.1', '7.2.1', '7.0.2', '6.3.2']
        expected_platforms = ['8.15.1', '8.14.3', '8.14.2', '8.13.1', '8.12.1', '8.11.1', '8.10.2', '8.10.1',
                              '8.8.1', '8.6.2', '8.6.1', '8.4-1', '8.3-3', '8.3-2', '8.3-1', '8.2-5', '8.2-4',
                              '8.2-2', '8.1-1', '8.0-2', '7.3-1', '7.2-1', '7.0-2', '6.3-2']
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'layouts/_default').mkdir(parents=True)
            (root/'layouts/shortcodes').mkdir()
            (root/'layouts/_default/single.html').write_text('<title>{{ .Title }}</title><link rel="canonical" href="{{ .Permalink }}"><article>{{ .Content }}</article>')
            for shortcode in ['cs-correspondence', 'cs-admonition']:
                shutil.copyfile(ROOT/'layouts/shortcodes'/f'{shortcode}.html', root/'layouts/shortcodes'/f'{shortcode}.html')
            (root/'data').mkdir()
            shutil.copyfile(ROOT/'data/versions.yaml', root/'data/versions.yaml')
            (root/'hugo.yaml').write_text('markup:\n  goldmark:\n    parser:\n      attribute: true\n    renderer:\n      unsafe: true\n')
            for brand, raw, template, title, label, provider in variants:
                slug = brand+'-cs-correspondence'
                record = page(source_path='docs/'+slug+'.md', old_url='/'+slug+'/',
                              target_path='content/'+slug+'/index.md', legacy_correspondence_template=template)
                result, _ = convert_document(raw, record)
                target = root/record['target_path']
                target.parent.mkdir(parents=True)
                target.write_bytes(result)
            base = 'https://www.virtuozzo.com/cloudscripting-docs/6.3.2/'
            run = subprocess.run([hugo, '--source', str(root), '--baseURL', base], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
            for brand, raw, template, title, label, provider in variants:
                with self.subTest(brand=brand):
                    slug = brand+'-cs-correspondence'
                    text = (root/'public'/slug/'index.html').read_text()
                    document = html5lib.parse(text, namespaceHTMLElements=False)
                    headings = list(document.iter('h1'))
                    self.assertEqual([(''.join(h.itertext()), h.get('id')) for h in headings], [(title, slug)])
                    table = next(document.iter('table'))
                    rows = [[''.join(cell.itertext()) for cell in row if cell.tag in {'th','td'}] for row in table.iter('tr')]
                    self.assertEqual(rows, [['CS']+expected_releases, [label]+expected_platforms])
                    self.assertEqual(sum(node.get('id') == 'table-head' for node in document.iter()), 1)
                    self.assertIn(base+slug+'/', text)
                    self.assertTrue(any(a.get('href') == provider and ''.join(a.itertext()) == 'hosting provider' for a in document.iter('a')))
                    self.assertLess(text.index('The table below displays dependencies'), text.index('<table'))
                    self.assertLess(text.index('</table>'), text.index('Starting with the 6.0'))
                    self.assertIn('Cloud Union', text)

    def test_active_custom_responses_restored_and_actions_comment_preserved(self):
        pages = json.loads((ROOT / 'migration/page-map.json').read_text())['pages']
        counts = [0, 0]
        for record in pages:
            if not record['published']:
                continue
            raw = frozen_source(record['source_path'])
            if record['source_path'] == 'docs/virtuozzo-cs-correspondence.md':
                record = dict(record, legacy_correspondence_template=(FIXTURES/'correspondence-template.html').read_bytes())
            result, issues = convert_document(raw, record)
            self.assertEqual(issues, [], record['source_path'])
            self.assertEqual(active_blocks(result), legacy_blocks(record['old_url']), record['source_path'])
            counts[0] += result.count(b'{{% tabs %}}')
            counts[1] += len(active_blocks(result))
            if record['source_path'].endswith('/handling-custom-responses.md'):
                self.assertIn(b'result: warning\n', result)
                self.assertEqual(result.count(b'{{% tabs %}}'), 11)
            if record['source_path'].endswith('/actions.md'):
                self.assertEqual(result.count(b'{{% tabs %}}'), 86)
        self.assertEqual(counts, [269, 566])

    def run_cli(self, root, mapping, destination, report, *extra):
        map_path = root / 'map.json'
        map_path.write_text(json.dumps(mapping))
        return subprocess.run([sys.executable, '-m', 'scripts.migration.convert', '--source-root', str(root),
                               '--page-map', str(map_path), '--destination', str(destination), '--report', str(report),
                               *extra], cwd=ROOT, capture_output=True, text=True)

    def test_cli_preserves_source_bytes_and_excludes_unpublished(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'docs').mkdir()
            raw = b'# Example\n@@@\n```yaml\na: 1\n```\n@@!\n'
            (root/'docs/example.md').write_bytes(raw)
            record = page(source_sha256=hashlib.sha256(raw).hexdigest())
            mapping = dict(schema_version=1, source_kind='worktree', pages=[record, page(source_path='docs/private.md', published=False, target_path=None)])
            output, report = root/'out', root/'report.json'
            run = self.run_cli(root, mapping, output, report)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            converted = output/'content/nested/example/index.md'
            before = converted.read_bytes()
            self.assertEqual((root/'docs/example.md').read_bytes(), raw)
            self.assertEqual(list(output.rglob('*.md')), [converted])
            self.assertEqual(json.loads(report.read_text())['status'], 'pass')
            self.assertEqual(self.run_cli(root, mapping, output, report).returncode, 0)
            self.assertEqual(converted.read_bytes(), before)

    def test_pure_api_requires_explicit_boolean_publication(self):
        for published in [False, 'false', 'true', 1, 0, None, [], {}]:
            with self.subTest(published=published):
                with self.assertRaises(ConversionError):
                    convert_document(b'# Example\n', page(published=published))

    def test_cli_rejects_non_boolean_publication(self):
        for published in ['false', 'true', 1, 0, None, [], {}]:
            with self.subTest(published=published), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root/'docs').mkdir()
                raw = b'# Example\n'
                (root/'docs/example.md').write_bytes(raw)
                record = page(source_sha256=hashlib.sha256(raw).hexdigest(), published=published)
                run = self.run_cli(root, dict(schema_version=1, pages=[record]), root/'out', root/'report.json')
                self.assertNotEqual(run.returncode, 0)
                report = json.loads((root/'report.json').read_text())
                self.assertEqual(report['status'], 'fail')
                self.assertEqual(report['issues'][0]['source_path'], 'docs/example.md')
                self.assertFalse((root/'out').exists())
                self.assertEqual((root/'docs/example.md').read_bytes(), raw)

    def test_cli_report_overlap_rejection_preserves_every_input_and_output(self):
        for target in ['source', 'page_map', 'output', 'output_parent', 'template', 'old_template']:
            for symlink in [False, True]:
                with self.subTest(target=target, symlink=symlink), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    (root/'docs').mkdir()
                    source = root/'docs/example.md'
                    raw = b'# Example\n'
                    source.write_bytes(raw)
                    output = root/'out/content/nested/example/index.md'
                    output.parent.mkdir(parents=True)
                    old_output = b'# Existing converted output\n'
                    output.write_bytes(old_output)
                    template_path = root/'theme/readthedocs/virtuozzo-cs-correspondence.html'
                    template_path.parent.mkdir(parents=True)
                    template_path.write_bytes(b'Protected pinned template')
                    old_template_path = root/'theme/readthedocs/jelastic-cs-correspondence.html'
                    old_template_path.write_bytes(b'Protected old pinned template')
                    record = page(source_sha256=hashlib.sha256(raw).hexdigest())
                    mapping = dict(schema_version=1, pages=[record])
                    map_bytes = json.dumps(mapping).encode()
                    (root/'map.json').write_bytes(map_bytes)
                    report = dict(source=source, page_map=root/'map.json', output=output,
                                  output_parent=output.parent, template=template_path, old_template=old_template_path)[target]
                    if symlink:
                        alias = root/'report-alias'
                        alias.symlink_to(report)
                        report = alias
                    run = self.run_cli(root, mapping, root/'out', report)
                    self.assertNotEqual(run.returncode, 0, run.stdout+run.stderr)
                    self.assertEqual(source.read_bytes(), raw)
                    self.assertEqual((root/'map.json').read_bytes(), map_bytes)
                    self.assertEqual(output.read_bytes(), old_output)
                    self.assertEqual(template_path.read_bytes(), b'Protected pinned template')
                    self.assertEqual(old_template_path.read_bytes(), b'Protected old pinned template')
                    self.assertIn('report', run.stderr.lower())

    def test_cli_reports_invalid_page_map_types(self):
        for invalid in [[], None, {'schema_version': 1, 'pages': None}]:
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                run = self.run_cli(root, invalid, root/'out', root/'report.json')
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(json.loads((root/'report.json').read_text())['status'], 'fail')
                self.assertFalse((root/'out').exists())

    def test_cli_uses_pinned_correspondence_template_and_reports_its_hash(self):
        for brand, fixture in [('virtuozzo', 'correspondence-template.html'),
                               ('jelastic', 'correspondence-jelastic-template.html')]:
            for supplied in [True, False]:
                with self.subTest(brand=brand, supplied=supplied), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    (root/'docs').mkdir()
                    raw = b'Original versions article.\n'
                    slug = brand+'-cs-correspondence'
                    source = 'docs/'+slug+'.md'
                    (root/source).write_bytes(raw)
                    template = (FIXTURES/fixture).read_bytes()
                    template_path = 'theme/readthedocs/'+slug+'.html'
                    if supplied:
                        (root/template_path).parent.mkdir(parents=True)
                        (root/template_path).write_bytes(template)
                    record = page(source_path=source, source_sha256=hashlib.sha256(raw).hexdigest())
                    run = self.run_cli(root, dict(schema_version=1, pages=[record]), root/'out', root/'report.json')
                    report = json.loads((root/'report.json').read_text())
                    if supplied:
                        self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
                        self.assertEqual(report['checks'][0]['legacy_template_sha256'], hashlib.sha256(template).hexdigest())
                        self.assertEqual(report['checks'][0]['legacy_template_path'], template_path)
                        self.assertIn(b'The table below displays dependencies', (root/'out'/record['target_path']).read_bytes())
                    else:
                        self.assertNotEqual(run.returncode, 0)
                        self.assertEqual(report['status'], 'fail')
                        self.assertFalse((root/'out').exists())
                        self.assertIn(slug+'.html', report['issues'][0]['evidence'])
                    self.assertEqual((root/source).read_bytes(), raw)

    def test_cli_selected_source_does_not_convert_other_published_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'docs').mkdir()
            raw = b'# Example\n'
            (root/'docs/example.md').write_bytes(raw)
            record = page(source_sha256=hashlib.sha256(raw).hexdigest())
            other = page(source_path='docs/missing.md', target_path='content/other/index.md')
            run = self.run_cli(root, dict(schema_version=1, pages=[record, other]), root/'out', root/'report.json', '--source', record['source_path'])
            self.assertEqual(run.returncode, 0, run.stdout+run.stderr)
            self.assertEqual(len(list((root/'out').rglob('*.md'))), 1)

    def test_cli_reports_bad_markup_without_writing_other_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'docs').mkdir()
            good, bad = b'# Good\n', b'# Bad\n@@!\n'
            (root/'docs/example.md').write_bytes(good)
            (root/'docs/bad.md').write_bytes(bad)
            records = [page(source_sha256=hashlib.sha256(good).hexdigest()),
                       page(source_path='docs/bad.md', target_path='content/bad/index.md', source_sha256=hashlib.sha256(bad).hexdigest())]
            run = self.run_cli(root, dict(schema_version=1, pages=records), root/'out', root/'report.json')
            self.assertNotEqual(run.returncode, 0)
            report = json.loads((root/'report.json').read_text())
            self.assertEqual(report['issues'][0]['source_path'], 'docs/bad.md')
            self.assertEqual(report['issues'][0]['line'], 2)
            self.assertFalse((root/'out').exists())
            self.assertEqual((root/'docs/example.md').read_bytes(), good)
            self.assertEqual((root/'docs/bad.md').read_bytes(), bad)

    def test_cli_fails_before_writing_on_bad_hash_or_unsafe_path(self):
        for changes in [dict(source_sha256='0'*64), dict(target_path='../escape.md'),
                        dict(source_path='../outside.md'), dict(published=False)]:
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root/'docs').mkdir()
                raw = b'# Example\n'
                (root/'docs/example.md').write_bytes(raw)
                record = page(source_sha256=hashlib.sha256(raw).hexdigest(), **changes) if 'source_sha256' not in changes else page(**changes)
                run = self.run_cli(root, dict(schema_version=1, pages=[record]), root/'out', root/'report.json', '--source', record['source_path'])
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(json.loads((root/'report.json').read_text())['status'], 'fail')
                self.assertFalse((root/'out').exists())


if __name__ == '__main__':
    unittest.main()
