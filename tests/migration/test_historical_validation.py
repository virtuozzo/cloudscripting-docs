"""Historical acceptance mutations use frozen captures, never converter output."""
import copy
import hashlib
import html
import json
from pathlib import Path
import tempfile
import unittest

from scripts.migration.check_site import _expected_blocks, check_site, report_shell

ROOT = Path(__file__).resolve().parents[2]
ROUTE = '/creating-manifest/handling-custom-responses/'
SOURCE = 'docs/creating-manifest/handling-custom-responses.md'
YAML = 'type: update\nname: response handlers\n\nonInstall:\n  return:\n    result: warning\n    message: Warning!\n    email: string\n'
JSON = '{\n    "type": "update",\n    "name": "response handlers",\n    "onInstall": {\n        "return": {\n          "result": "warning",\n          "message": "Warning!",\n          "email": "string"\n        }\n    }\n}\n'


def snapshots():
    return [x for x in json.loads((ROOT/'migration/releases/baselines/index.json').read_text())['snapshots'] if x['source_commit'] != '76628f8aa01571fbc348211cb7df726cf408cd17']


class HistoricalRestorationTests(unittest.TestCase):
    def load(self, entry):
        path = ROOT/entry['baseline']
        return json.loads(path.read_text()), json.loads((ROOT/entry['page_map']).read_text()), path.parent

    def test_all_19_reviewed_captures_restore_only_literal_pair_at_four_five(self):
        for entry in snapshots():
            with self.subTest(source=entry['source_commit']):
                baseline, page_map, base = self.load(entry)
                report = report_shell({})
                expected = _expected_blocks(baseline, base, report, page_map)
                self.assertEqual(report['status'], 'pass', report)
                page = expected[ROUTE]
                self.assertEqual(len(page['code_blocks']), 22)
                self.assertEqual(len(page['tab_panels']), 11)
                self.assertEqual([(x['language'],x['text']) for x in page['code_blocks'][4:6]], [('yaml',YAML),('json',JSON)])
                self.assertEqual(page['tab_panels'][2], {'code_blocks':[4,5], 'languages':['yaml','json']})
                self.assertEqual(sum(len(x['code_blocks']) for x in expected.values()), sum(len(x['code_blocks']) for x in baseline['pages'].values())+2)
                # The baseline object and commented Actions example remain untouched.
                self.assertEqual(len(baseline['pages'][ROUTE]['code_blocks']),20)
                self.assertEqual(expected['/creating-manifest/actions/']['tab_panels'],baseline['pages']['/creating-manifest/actions/']['tab_panels'])

    def test_unknown_source_does_not_restore_pair(self):
        baseline, page_map, base = self.load(snapshots()[0])
        baseline['inputs']['source_commit'] = '0'*40
        page_map['source_commit'] = '0'*40
        report = report_shell({})
        self.assertEqual(len(_expected_blocks(baseline,base,report,page_map)[ROUTE]['code_blocks']),20)

    def test_changed_source_identity_or_ordered_baseline_fails_closed(self):
        for mutation in ('file_hash','source_path','map_commit','count','language','body','position','tab_order'):
            with self.subTest(mutation=mutation):
                baseline, page_map, base = self.load(snapshots()[0])
                page = baseline['pages'][ROUTE]
                mapped = next(x for x in page_map['pages'] if x['source_path']==SOURCE)
                if mutation=='file_hash': mapped['source_sha256']='0'*64
                if mutation=='source_path': page['source_path']='docs/other.md'
                if mutation=='map_commit': page_map['source_commit']='0'*40
                if mutation=='count': page['code_blocks'].pop()
                if mutation=='language': page['code_blocks'][4]['language']='javascript'
                if mutation=='body': page['code_blocks'][4]['sha256']='0'*64
                if mutation=='position': page['code_blocks'][0],page['code_blocks'][2]=page['code_blocks'][2],page['code_blocks'][0]
                if mutation=='tab_order': page['tab_panels'][2]['code_blocks']=[5,4]
                report=report_shell({})
                expected=_expected_blocks(baseline,base,report,page_map)
                self.assertEqual(report['status'],'fail',report)
                self.assertIn('restoration-baseline',[x['id'] for x in report['issues']])
                self.assertLess(len(expected[ROUTE]['code_blocks']),22)

    def test_rendered_pair_changed_language_byte_position_or_extra_example_fails(self):
        baseline, page_map, base = self.load(snapshots()[0])
        baseline['pages']={ROUTE:baseline['pages'][ROUTE]}
        page=baseline['pages'][ROUTE];page['links']=[];page['images']=[]
        page_map['pages']=[p for p in page_map['pages'] if p['source_path']==SOURCE]
        page_map['navigation']=[];page_map['scope']='selected'
        page_map['pages'][0]['title']='Handling Custom Responses'
        blocks=[(b['language'],(base/b['text_path']).read_text()) for b in page['code_blocks']]
        blocks[4:4]=[('yaml',YAML),('json',JSON)]
        with tempfile.TemporaryDirectory() as d:
            temp=Path(d);site=temp/'site';site.mkdir()
            # Keep code paths relative to immutable original capture location.
            for b in page['code_blocks']: b['text_path']=(base/b['text_path']).resolve().relative_to(ROOT).as_posix()
            # Store fixture under repository root so safe relative paths resolve.
            bf=ROOT/('.historical-test-'+temp.name+'.json')
            self.addCleanup(bf.unlink,missing_ok=True)
            bf.write_text(json.dumps(baseline))
            pm=temp/'map.json';pm.write_text(json.dumps(page_map))
            ex=temp/'exceptions.json';ex.write_text('{"exceptions":[]}')
            (site/'index.json').write_text(json.dumps([{'title':'Handling Custom Responses','contents':'Examples','permalink':'https://example.test/'+ROUTE.lstrip('/')}]))
            (site/'sitemap.xml').write_text('<urlset><url><loc>https://example.test/'+ROUTE.lstrip('/')+'</loc></url></urlset>')
            (site/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://example.test/sitemap.xml\n')
            (site/'search').mkdir();(site/'search/index.html').write_text('search');(site/'search.html').write_text('legacy search')
            target=site/ROUTE.strip('/')/'index.html';target.parent.mkdir(parents=True)
            def render(items):
                body='<aside><a href="'+ROUTE+'">'+page_map['pages'][0]['nav_title']+'</a></aside><main><h1 id="handling-custom-responses">Handling Custom Responses</h1>'
                for i in range(0,len(items),2):
                    body+='<div class="tabs-container">'
                    for lang,text in items[i:i+2]:
                        body+='<div role="tabpanel" data-tab-title="'+lang+'"><div class="code-block"><textarea class="code-block-source">'+html.escape(text)+'</textarea><pre><code class="language-'+lang+'">'+html.escape(text)+'</code></pre></div></div>'
                    body+='</div>'
                return '<html><head><meta name="robots" content="noindex"><link rel="canonical" href="https://example.test/'+ROUTE.lstrip('/')+'"></head>'+body+'</main></html>'
            target.write_text(render(blocks))
            report=check_site(bf,pm,site,'https://example.test/',ex,archived=True)
            self.assertEqual(report['status'],'pass',report)
            for mutation,issue in [('byte','code-bytes'),('language','code-language'),('position','code-bytes'),('extra','code-count'),('missing','code-count')]:
                changed=copy.deepcopy(blocks)
                if mutation=='byte': changed[4]=('yaml',YAML.replace('Warning!','warning!'))
                if mutation=='language': changed[4]=('json',YAML)
                if mutation=='position': changed[2:6]=changed[4:6]+changed[2:4]
                if mutation=='extra': changed += [('yaml','commented Actions\n'),('json','{}\n')]
                if mutation=='missing': del changed[4:6]
                target.write_text(render(changed))
                report=check_site(bf,pm,site,'https://example.test/',ex,archived=True)
                self.assertIn(issue,[x['id'] for x in report['issues']],report)


class HistoricalCodeStoreTests(unittest.TestCase):
    def test_only_canonical_hashed_store_paths_are_accepted_without_symlinks(self):
        from unittest.mock import patch
        from scripts.migration import check_site as validator
        entry=snapshots()[0]
        original=json.loads((ROOT/entry['baseline']).read_text())
        original['pages']={ROUTE:original['pages'][ROUTE]}
        for mutation in ('none','source','filename','hash','traversal','baseline_name','parent_symlink','file_symlink','baseline_symlink','missing'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=ROOT) as d:
                temp=Path(d);base=temp/'migration/releases/baselines'/entry['source_commit'];base.mkdir(parents=True)
                code=temp/'migration/releases/code';code.mkdir()
                baseline=copy.deepcopy(original)
                for block in baseline['pages'][ROUTE]['code_blocks']:
                    (code/Path(block['text_path']).name).write_bytes((ROOT/entry['baseline']).parent.joinpath(block['text_path']).read_bytes())
                bf=base/'baseline.json';bf.write_text(json.dumps(baseline))
                block=baseline['pages'][ROUTE]['code_blocks'][0]
                path=base/block['text_path']
                name='baseline.json'
                if mutation=='source': baseline['inputs']['source_commit']='0'*40
                if mutation=='filename': block['text_path']='../../code/'+'0'*64+'.txt'
                if mutation=='hash': block['sha256']='0'*64
                if mutation=='traversal': block['text_path']='../../code/../code/'+path.name
                if mutation=='baseline_name': name='alternate.json'
                if mutation=='parent_symlink':
                    code.rename(code.with_name('moved'));code.symlink_to(code.with_name('moved'),target_is_directory=True)
                if mutation=='file_symlink':
                    body=path.read_bytes();path.unlink();other=temp/'other.txt';other.write_bytes(body);path.symlink_to(other)
                if mutation=='baseline_symlink':
                    bf.rename(base/'moved.json');bf.symlink_to(base/'moved.json')
                if mutation=='missing': path.unlink()
                report=report_shell({})
                # Isolate the tooling repository root; the actual path resolver and
                # filesystem integrity checks run unchanged in this cloned layout.
                with patch.object(validator,'__file__',str(temp/'scripts/migration/check_site.py')):
                    validator._expected_blocks(baseline,base,report,json.loads((ROOT/entry['page_map']).read_text()),baseline_name=name)
                self.assertEqual(report['status'],'pass' if mutation=='none' else 'fail',report['issues'][:2])


class ExactInheritedFragmentTests(unittest.TestCase):
    def setUp(self):
        import shutil
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'fixture'
        shutil.copytree(ROOT/'tests/migration/fixtures/validation',self.root)
        self.baseline=json.loads((self.root/'baseline.json').read_text())
        self.exceptions=json.loads((self.root/'exceptions.json').read_text())
        self.target='/guide/?view=old#inherited-absent'
        self.baseline['pages']['/']['links'].append({'href':self.target,'resolved_url':self.target,'text':'Old fragment'})
        self.entry={'id':'inherited-fragment','check':'missing-fragment','url':'/','target':self.target,'source_commit':'1111111111111111111111111111111111111111','reason':'Captured missing fragment, exact origin/query/fragment and one occurrence'}
        self.exceptions['exceptions'].append(self.entry)
        self.path=self.root/'site/index.html'
        self.original=self.path.read_text()
        self.path.write_text(self.original.replace('</main>','<a href="'+self.target+'">Old fragment</a></main>'))

    def check(self):
        (self.root/'baseline.json').write_text(json.dumps(self.baseline))
        (self.root/'exceptions.json').write_text(json.dumps(self.exceptions))
        return check_site(self.root/'baseline.json',self.root/'page-map.json',self.root/'site','https://docs.cloudscripting.com/',self.root/'exceptions.json')

    def test_accepts_exact_inherited_fragment_with_query_identity(self):
        report=self.check()
        self.assertEqual(report['status'],'pass',report)

    def test_new_changed_query_fragment_origin_source_or_occurrence_fails(self):
        for mutation in ('fragment','query','origin','source','extra'):
            with self.subTest(mutation=mutation):
                self.setUp()
                if mutation in {'fragment','query'}:
                    self.path.write_text(self.path.read_text().replace(self.target,self.target.replace('absent','new') if mutation=='fragment' else self.target.replace('old','new')))
                if mutation=='origin': self.entry['url']='/guide/'
                if mutation=='source': self.entry['source_commit']='2'*40
                if mutation=='extra': self.path.write_text(self.path.read_text().replace('</main>','<a href="'+self.target+'">extra</a></main>'))
                report=self.check()
                self.assertEqual(report['status'],'fail',report)
                self.assertTrue(any(x['id'] in {'missing-fragment','exception-provenance'} for x in report['issues']),report)

    def test_exception_cannot_hide_deletion_of_formerly_valid_fragment_or_image(self):
        self.entry['target']='/guide/#run'
        p=self.root/'site/guide/index.html';p.write_text(p.read_text().replace('id="run"','id="removed"'))
        report=self.check()
        self.assertIn('exception-provenance',[x['id'] for x in report['issues']],report)
        self.assertIn('missing-fragment',[x['id'] for x in report['issues']],report)
        self.entry['target']=self.target
        self.path.write_text(self.path.read_text().replace('src="/img/Icon.svg"','src="'+self.target+'"'))
        report=self.check()
        self.assertTrue(any(x['id']=='missing-fragment' and x['evidence'].get('href')==self.target for x in report['issues']),report)


class HistoricalCatalogTests(unittest.TestCase):
    def verify(self, catalog=None):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory(dir=ROOT) as d:
            temp=Path(d);report=temp/'report.json'
            args=[sys.executable,'-m','scripts.migration.check_acceptance','--report',str(report)]
            if catalog is not None:
                path=temp/'catalog.json';path.write_text(json.dumps(catalog));args+=['--catalog',str(path)]
            result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
            return result,json.loads(report.read_text()) if report.exists() else {}

    def test_reviewed_inputs_cover_24_frozen_releases_without_claiming_full_acceptance(self):
        result,report=self.verify()
        self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertEqual(report['status'],'pass')
        self.assertEqual(report['summary']['historical_releases'],24)
        self.assertEqual(report['summary']['historical_sources'],19)
        self.assertEqual(report['summary']['full_task_10'],'incomplete')

    def test_catalog_source_missing_duplicate_and_unsafe_paths_fail(self):
        catalog=json.loads((ROOT/'migration/releases/acceptance.json').read_text())
        for mutation in ('source','validation_source','missing','duplicate','traversal'):
            with self.subTest(mutation=mutation):
                changed=copy.deepcopy(catalog)
                historical=next(build for build in changed['builds'] if build['id']!='root')
                if mutation=='source': historical['source_commit']='0'*40
                if mutation=='validation_source': historical['validation_source_commit']='0'*40
                if mutation=='missing': changed['builds']=[build for build in changed['builds'] if build['id']!=historical['id']]
                if mutation=='duplicate': changed['builds'].append(copy.deepcopy(historical))
                if mutation=='traversal': historical['page_map']='../outside.json'
                result,report=self.verify(changed)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(report['status'],'fail',result.stderr)

    def test_changed_source_map_publication_or_exception_provenance_fails(self):
        catalog=json.loads((ROOT/'migration/releases/acceptance.json').read_text())
        for mutation in ('source_hash','publish_unlisted','pending','title','exception_target','exception_occurrence'):
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory(dir=ROOT) as d:
                changed=copy.deepcopy(catalog);entry=next(build for build in changed['builds'] if build['id']!='root');temp=Path(d)
                field='exceptions' if mutation.startswith('exception') else 'page_map'
                data=json.loads((ROOT/entry[field]).read_text())
                if mutation=='source_hash': data['pages'][0]['source_sha256']='0'*64
                if mutation=='publish_unlisted': next(p for p in data['pages'] if not p['published'])['published']=True
                if mutation=='pending': next(p for p in data['pages'] if not p['published'])['disposition']='pending'
                if mutation=='title': next(p for p in data['pages'] if p['source_path']=='docs/jelastic-cs-correspondence.md')['title']='Virtuozzo Application Platform & CS Correspondence'
                if mutation=='exception_target': data['exceptions'][0]['target']='/new-unobserved-defect/'
                if mutation=='exception_occurrence': data['exceptions'][0]['evidence']['occurrences'][0]['href']='unobserved'
                path=temp/(field+'.json');path.write_text(json.dumps(data));entry[field]=path.relative_to(ROOT).as_posix()
                result,report=self.verify(changed)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(report['status'],'fail',result.stderr)


if __name__ == '__main__': unittest.main()
