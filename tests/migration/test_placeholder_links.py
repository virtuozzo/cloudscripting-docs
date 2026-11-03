"""Source-intended navigation regression; literal destinations are independently specified."""
import copy
import hashlib
import html
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.migration.markdown_converter import convert_document
from scripts.migration.check_site import _expected_blocks, report_shell, check_site

ROOT = Path(__file__).resolve().parents[2]
ROUTE = '/creating-manifest/placeholders/'
SOURCE = 'docs/creating-manifest/placeholders.md'
TARGETS = [('#42tobase64', '${*.toBase64()}'), ('#42frombase64', '${*.fromBase64()}'),
           ('#42md5', '${*.md5()}'), ('#42join', '${*.join()}'),
           ('#42tojson', '${*.toJSON()}'), ('#42contains', '${*.contains()}'), ('#42print', '${*.print()}')]


def snapshots():
    return json.loads((ROOT/'migration/releases/baselines/index.json').read_text())['snapshots']


def load(entry):
    mapping = json.loads((ROOT/entry['page_map']).read_text())
    page = next(p for p in mapping['pages'] if p['source_path'] == SOURCE)
    raw = subprocess.check_output(['git', '--no-replace-objects', 'show', entry['source_commit']+':'+SOURCE], cwd=ROOT)
    baseline_path = ROOT/entry['baseline']
    return mapping, page, raw, json.loads(baseline_path.read_text()), baseline_path


class PlaceholderConverterTests(unittest.TestCase):
    def test_all_frozen_sources_emit_seven_literal_destinations_without_changing_source(self):
        for entry in snapshots():
            with self.subTest(source=entry['source_commit']):
                _, page, raw, _, _ = load(entry)
                before = hashlib.sha256(raw).hexdigest()
                converted, _ = convert_document(raw, page)
                for href, label in TARGETS:
                    self.assertTrue(('['+'`'+label+'`'+']('+href+')').encode() in converted, (entry['source_commit'], href))
                self.assertEqual(hashlib.sha256(raw).hexdigest(), before)
                self.assertEqual(convert_document(converted, page)[0], converted)

    def test_unrelated_routes_unknown_functions_and_changed_list_structure_are_not_repaired(self):
        _, page, raw, _, _ = load(snapshots()[0])
        for mutation in ('route', 'function', 'description', 'order', 'missing_heading'):
            with self.subTest(mutation=mutation):
                changed, metadata = raw, dict(page)
                if mutation == 'route': metadata['source_path'] = 'docs/other.md'
                if mutation == 'function': changed = raw.replace(b'[`' + b'${*.join()}`]', b'[`${*.other()}`]', 1)
                if mutation == 'description': changed = raw.replace(b'- *md5* hash generator', b'- changed description', 1)
                if mutation == 'order':
                    lines = changed.splitlines(keepends=True); start = next(i for i,l in enumerate(lines) if l.startswith(b'- [`${*.toBase64()}'))
                    lines[start], lines[start+1] = lines[start+1], lines[start]; changed = b''.join(lines)
                if mutation == 'missing_heading': changed = raw.replace(b'### ${\\*.join()}', b'### Other heading', 1)
                converted, _ = convert_document(changed, metadata)
                self.assertNotIn(b'](#42tobase64)', converted)

    def test_changed_adjacent_list_boundaries_are_not_partially_repaired(self):
        for entry in snapshots():
            _, page, raw, _, _ = load(entry)
            start = raw.index(b'- [`${*.toBase64()}')
            end = raw.index(b'\n\n', start) + 1
            unknown = b'- [`${*.unknown()}`](#${\\*.unknown()}) - unknown function  \n'
            cases = {
                'appended_item': raw[:end] + unknown + raw[end:],
                'preceding_adjacent_item': raw[:start] + unknown + raw[start:],
                'appended_loose_item': raw[:end] + b'\n' + unknown + raw[end:],
                'appended_item_continuation': raw[:end] + b'    additional list content\n' + raw[end:],
            }
            for mutation, changed in cases.items():
                with self.subTest(source=entry['source_commit'], mutation=mutation):
                    converted, _ = convert_document(changed, page)
                    self.assertFalse(any((']('+href+')').encode() in converted for href, _ in TARGETS),
                                     'Changed complete list boundary must leave all seven authored hrefs unrepaired')

    def test_fenced_inline_and_commented_literals_keep_original_destinations(self):
        _, page, raw, _, _ = load(snapshots()[0])
        start = raw.index(b'- [`${*.toBase64()}')
        listing = raw[start:raw.index(b'\n\n',start)]
        extra = b'\n```text\n'+listing+b'\n```\n\n<!--\n'+listing+b'\n-->\n\n`'+listing.splitlines()[0]+b'`\n'
        converted, _ = convert_document(raw+extra, page)
        self.assertIn(b'```text\n'+listing+b'\n```', converted)
        self.assertIn(b'<!--\n'+listing+b'\n-->', converted)
        self.assertIn(b'`'+listing.splitlines()[0]+b'`', converted)


class PlaceholderExpectationTests(unittest.TestCase):
    def test_all_captures_replace_only_four_corrupt_references_with_seven_literal_links(self):
        for entry in snapshots():
            with self.subTest(source=entry['source_commit']):
                mapping, _, _, baseline, path = load(entry)
                original = copy.deepcopy(baseline)
                report = report_shell({})
                expected = _expected_blocks(baseline, path.parent, report, mapping, path.name)
                links = expected[ROUTE]['links']
                repaired = [(r['href'], r['text']) for r in links if r['text'] in {label for _, label in TARGETS}]
                self.assertEqual(repaired, TARGETS)
                self.assertEqual(len(links), len(baseline['pages'][ROUTE]['links'])+3)
                self.assertEqual(baseline, original)
                self.assertEqual(report['status'], 'pass', report)

    def test_unknown_source_file_list_or_reference_identity_fails_closed(self):
        for mutation in ('commit', 'hash', 'source_path', 'baseline_href', 'baseline_label', 'extra_ref', 'lost_id'):
            with self.subTest(mutation=mutation):
                mapping, page, _, baseline, path = load(snapshots()[0])
                if mutation == 'commit': mapping['source_commit'] = baseline['inputs']['source_commit'] = '0'*40
                if mutation == 'hash': page['source_sha256'] = '0'*64
                if mutation == 'source_path': baseline['pages'][ROUTE]['source_path'] = 'docs/other.md'
                if mutation == 'baseline_href': baseline['pages'][ROUTE]['links'][42]['href'] = '#unknown'
                if mutation == 'baseline_label': baseline['pages'][ROUTE]['links'][42]['text'] = 'other'
                if mutation == 'extra_ref': baseline['pages'][ROUTE]['links'].append({'href':'#other','text':'other'})
                if mutation == 'lost_id': baseline['pages'][ROUTE]['ids'].remove('42join')
                report = report_shell({})
                expected = _expected_blocks(baseline, path.parent, report, mapping, path.name)
                self.assertEqual(report['status'], 'fail', report)
                self.assertIn('placeholder-navigation-baseline', [i['id'] for i in report['issues']])
                self.assertEqual(expected[ROUTE]['links'], baseline['pages'][ROUTE]['links'])


    def test_source_catalog_binds_every_file_and_exact_seven_line_list(self):
        catalog = json.loads((ROOT/'scripts/migration/placeholder_navigation_identities.json').read_text())
        self.assertEqual(set(catalog['snapshots']), {e['source_commit'] for e in snapshots()})
        for entry in snapshots():
            _, page, raw, _, _ = load(entry)
            identity = catalog['snapshots'][entry['source_commit']]
            self.assertEqual(hashlib.sha256(raw).hexdigest(), identity['source_sha256'])
            start, end = identity['list_lines']
            listing = b''.join(raw.splitlines(keepends=True)[start-1:end])
            self.assertEqual(hashlib.sha256(listing).hexdigest(), identity['list_sha256'])
            self.assertEqual(end-start, 6)
            self.assertEqual(page['source_sha256'], identity['source_sha256'])

    def test_check_site_rejects_rendered_navigation_mutations_independently(self):
        mapping, page, raw, baseline, path = load(snapshots()[0])
        mapping['pages'] = [page]; mapping['navigation'] = []; mapping['scope'] = 'selected'
        base = 'https://example.test/docs/oldest/'
        descriptions = ['does data encoding into Base64 format', 'decodes data from Base64 format',
                        'md5 hash generator', 'concatenates data provided as array of words or objects',
                        'converts array of of words or objects into JSON format',
                        'allows to find a word or object in the array of words or objects respectively',
                        'outputs an array of words or objects to the console']
        def render(items, missing_target=False, changed_description=False, plain_label=False):
            body = '<main><h2 id="data-processing-placeholders">Data Processing Placeholders</h2><ul>'
            for i, (href, label) in enumerate(items):
                caption = html.escape(label) if plain_label else '<code>'+html.escape(label)+'</code>'
                description = 'changed' if changed_description and i == 2 else descriptions[min(i,6)]
                body += '<li><a href="'+base+ROUTE.lstrip('/')+href+'">'+caption+'</a> - '+description+'</li>'
            body += '</ul>'
            for href, _ in TARGETS:
                if missing_target and href == '#42join': continue
                body += '<h3 id="'+href[1:]+'">function</h3>'
            return body+'</main>'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); site = root/'site'; target = site/ROUTE.strip('/')/'index.html'
            target.parent.mkdir(parents=True)
            pm = root/'map.json'; pm.write_text(json.dumps(mapping))
            ex = root/'exceptions.json'; ex.write_text('{"exceptions":[]}')
            def checks(text):
                target.write_text(text)
                report = check_site(path, pm, site, base, ex)
                return [i['id'] for i in report['issues'] if i['id'].startswith('placeholder-navigation')]
            self.assertEqual(checks(render(TARGETS)), [])
            for mutation in ('missing', 'extra', 'wrong_label', 'wrong_target', 'reordered', 'duplicate', 'target_lost', 'description', 'plain_label'):
                with self.subTest(mutation=mutation):
                    links = list(TARGETS)
                    if mutation == 'missing': links.pop(1)
                    if mutation == 'extra': links.append(('#42join','${*.unknown()}'))
                    if mutation == 'wrong_label': links[2] = ('#42md5','${*.other()}')
                    if mutation == 'wrong_target': links[2] = ('#42join','${*.md5()}')
                    if mutation == 'reordered': links[2],links[3] = links[3],links[2]
                    if mutation == 'duplicate': links.insert(2,links[2])
                    self.assertIn('placeholder-navigation', checks(render(links, mutation=='target_lost', mutation=='description', mutation=='plain_label')))


if __name__ == '__main__': unittest.main()
