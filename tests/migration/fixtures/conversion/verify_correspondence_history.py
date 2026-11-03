"""Check generated correspondence conversion against every pinned release Git object."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from scripts.migration.convert import convert_tree
from scripts.migration.inventory import _git, build_inventory


EXPECTED = {
    'docs/jelastic-cs-correspondence.md': ('Jelastic & CS Correspondence',
        '6137f5f71614614134ef981389a9ba351cd1fa5cdb4ef1d143a5434d543cfbb1',
        'theme/readthedocs/jelastic-cs-correspondence.html',
        b'{{< cs-correspondence platform="Jelastic" >}}'),
    'docs/virtuozzo-cs-correspondence.md': ('Virtuozzo Application Platform & CS Correspondence',
        '064581ed50f9a811b86627a56cab9537e50ab5802484fec1fc322d505210852e',
        'theme/readthedocs/virtuozzo-cs-correspondence.html', b'{{< cs-correspondence >}}'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    manifest_path = ROOT / 'migration/release-sources.yaml'
    manifest = yaml.safe_load(manifest_path.read_bytes())
    snapshots = {}
    for release in manifest['releases']:
        snapshots.setdefault(release['source_commit'], []).append(release['id'])
    report = dict(schema_version=1, status='pass',
                  inputs=dict(manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                              correspondence_inputs_sha256={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                  for name in ['scripts/migration/convert.py', 'scripts/migration/markdown_converter.py',
                                               'layouts/shortcodes/cs-correspondence.html']},
                              git_reads='--no-replace-objects; GIT_NO_LAZY_FETCH=1; GIT_OPTIONAL_LOCKS=0',
                              generated_metadata_restoration=dict(route='/jelastic-cs-correspondence/',
                                  template_sha256=EXPECTED['docs/jelastic-cs-correspondence.md'][1],
                                  scope='Only source-defined CS/Jelastic version table; canonical baseline unchanged')),
                  checks=[], issues=[])
    for revision, releases in snapshots.items():
        inventory = build_inventory(ROOT, revision)
        pages = [page for page in inventory['pages'] if page['source_path'] in EXPECTED]
        assert len(pages) == 1 and pages[0]['published'] is True, (revision, pages)
        page = pages[0]
        title, digest, template_path, shortcode = EXPECTED[page['source_path']]
        source = _git(ROOT, 'show', revision + ':' + page['source_path'])
        template = _git(ROOT, 'show', revision + ':' + template_path)
        wrapper = _git(ROOT, 'show', revision + ':theme/readthedocs/content.html')
        include = ('{% include "' + Path(template_path).name + '" %}').encode()
        assert wrapper.index(include) < wrapper.index(b'{{ page.content }}')
        assert hashlib.sha256(template).hexdigest() == digest
        with tempfile.TemporaryDirectory(prefix='cs-correspondence-history-') as temporary:
            root = Path(temporary)
            for name, raw in [(page['source_path'], source), (template_path, template)]:
                path = root / 'source' / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            result = convert_tree(root / 'source', dict(inventory, pages=pages), root / 'converted')
            assert result['status'] == 'pass', result
            output = (root / 'converted' / page['target_path']).read_bytes()
            metadata = yaml.safe_load(output.split(b'---', 2)[1])
            authored = next(line for line in source.splitlines() if line.strip())
            assert metadata['title'] == title
            assert output.index(b'# ' + title.encode()) < output.index(b'The table below displays dependencies')
            assert output.index(b'The table below displays dependencies') < output.index(shortcode) < output.index(authored)
            assert (root / 'source' / page['source_path']).read_bytes() == source
            report['checks'].append(dict(source_commit=revision, release_ids=releases, source_path=page['source_path'],
                source_sha256=hashlib.sha256(source).hexdigest(), template_path=template_path,
                template_sha256=digest, source_wrapper_sha256=hashlib.sha256(wrapper).hexdigest(),
                route=page['old_url'], target_path=page['target_path'], title=title,
                output_sha256=hashlib.sha256(output).hexdigest(), status='pass',
                order=['generated H1', 'generated intro', 'generated table', 'authored source prose/note']))
    report['distinct_snapshots'] = len(report['checks'])
    report['release_ids'] = sum(len(c['release_ids']) for c in report['checks'])
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(f"PASS: {report['distinct_snapshots']} pinned snapshots / {report['release_ids']} releases")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
