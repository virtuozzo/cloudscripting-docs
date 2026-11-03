"""Focused real-Hugo current/oldest proof; never captures or rewrites legacy baselines."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tests/migration'))
from scripts.migration.markdown_converter import convert_document
from scripts.migration.check_site import semantic
from scripts.migration.placeholder_navigation import check_rendered
from scripts.migration.inventory import _git
from test_theme_compatibility import Capture

SOURCE = 'docs/creating-manifest/placeholders.md'
ROUTE = '/creating-manifest/placeholders/'
BASE = 'https://www.virtuozzo.com/cloudscripting-docs/'
EXPECTED = [('#42tobase64', '${*.toBase64()}'), ('#42frombase64', '${*.fromBase64()}'),
            ('#42md5', '${*.md5()}'), ('#42join', '${*.join()}'), ('#42tojson', '${*.toJSON()}'),
            ('#42contains', '${*.contains()}'), ('#42print', '${*.print()}')]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    hugo = os.environ.get('HUGO_BIN') or str(ROOT/'.devbox/nix/profile/default/bin/hugo')
    index_path = ROOT/'migration/releases/baselines/index.json'
    entries = json.loads(index_path.read_text())['snapshots']
    page_map = json.loads((ROOT/'migration/page-map.json').read_text())
    def source_hashes():
        return {p['source_path']: hashlib.sha256(_git(ROOT, 'show', page_map['source_commit'] + ':' + p['source_path'])).hexdigest()
                for p in page_map['pages']}
    sources_before = source_hashes()
    assert all(sources_before[p['source_path']] == p['source_sha256'] for p in page_map['pages'])
    protected = [index_path, ROOT/'migration/page-map.json', *(ROOT/e['baseline'] for e in entries), *(ROOT/e['page_map'] for e in entries)]
    before = {str(p.relative_to(ROOT)): digest(p) for p in protected}
    report = dict(schema_version=1, status='pass', inputs=dict(
        scope='Focused current/oldest Placeholders real Hugo navigation and exact legacy code proof; no complete site acceptance',
        hugo=subprocess.check_output([hugo,'version'],text=True).strip(), base_url=BASE,
        theme_commit=subprocess.check_output(['git','-C',str(ROOT/'themes'),'rev-parse','HEAD'],text=True).strip(),
        tooling_sha256={p:digest(ROOT/p) for p in ('scripts/migration/markdown_converter.py','scripts/migration/check_site.py','scripts/migration/placeholder_navigation.py','scripts/migration/placeholder_navigation_identities.json')},
        preserved_inputs_sha256=before, preserved_source_commit=page_map['source_commit'],
        preserved_sources_sha256=sources_before), checks=[], issues=[])
    for label, entry in [('oldest',entries[0]),('current',entries[-1])]:
        revision = entry['source_commit']
        mapping = json.loads((ROOT/entry['page_map']).read_text())
        page = next(p for p in mapping['pages'] if p['source_path']==SOURCE)
        raw = subprocess.check_output(['git','--no-replace-objects','show',revision+':'+SOURCE],cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest()==page['source_sha256']
        baseline_path = ROOT/entry['baseline']
        captured = json.loads(baseline_path.read_text())['pages'][ROUTE]
        expected = []
        for block in captured['code_blocks']:
            path = baseline_path.parent/block['text_path']
            assert digest(path)==block['sha256']
            expected.append(path.read_bytes().decode())
        converted,_ = convert_document(raw,page)
        with tempfile.TemporaryDirectory(prefix='placeholder-links-hugo-') as directory:
            work = Path(directory)
            output = work/page['target_path']; output.parent.mkdir(parents=True); output.write_bytes(converted)
            (work/'themes').symlink_to(ROOT/'themes')
            for name in ('layouts','data','assets'):
                shutil.copytree(ROOT/name,work/name)
            for name in ('config.yaml','redirects.htaccess'):
                shutil.copy(ROOT/name,work/name)
            shutil.copy(ROOT/'content/search.md',work/'content/search.md')
            result = subprocess.run([hugo,'--source',str(work),'--baseURL',BASE],text=True,capture_output=True)
            assert result.returncode==0, result.stdout+result.stderr
            rendered=(work/'public'/ROUTE.strip('/')/'index.html').read_text()
            tree=semantic(rendered); copies=Capture(rendered)
            links=[(r['href'],r['text']) for r in tree['link_records'] if r['text'] in {label for _,label in EXPECTED}]
            navigation_error=check_rendered(tree,BASE)
            actual=dict(label=label,source_commit=revision,source_sha256=page['source_sha256'],baseline_sha256=digest(baseline_path),
                        converted_sha256=hashlib.sha256(converted).hexdigest(),html_sha256=hashlib.sha256(rendered.encode()).hexdigest(),
                        function_links=links,all_seven_targets_exist=all(href[1:] in tree['ids'] for href,_ in EXPECTED),
                        exact_ordered_function_links=links==EXPECTED,exact_visible_code=copies.pre==expected,
                        exact_html5_clipboard_code=copies.copies==expected,code_blocks=len(expected),
                        tab_groups=len(tree['tabs']),expected_tab_groups=len(captured['tab_panels']),
                        navigation_error=navigation_error)
            report['checks'].append(actual)
            if (links!=EXPECTED or navigation_error is not None or copies.pre!=expected or copies.copies!=expected
                    or len(tree['tabs'])!=len(captured['tab_panels']) or not actual['all_seven_targets_exist']):
                report['status']='fail'; report['issues'].append(dict(id='focused-placeholder-proof',severity='error',evidence=actual))
    after={str(p.relative_to(ROOT)):digest(p) for p in protected}
    sources_after=source_hashes()
    report['preserved_inputs_unchanged']=before==after and sources_before==sources_after
    if not report['preserved_inputs_unchanged']:
        report['status']='fail'; report['issues'].append(dict(id='input-mutation',severity='error',evidence=[p for p in before if before[p]!=after[p]] + [p for p in sources_before if sources_before[p]!=sources_after[p]]))
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],checks=[{k:c[k] for k in ('label','code_blocks','tab_groups','exact_ordered_function_links','navigation_error')} for c in report['checks']],issues=report['issues'])))
    return 0 if report['status']=='pass' else 1


if __name__=='__main__': raise SystemExit(main())
