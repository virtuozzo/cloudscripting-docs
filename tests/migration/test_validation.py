"""Independent, literal HTML mutation fixtures for migration acceptance."""
import copy
import hashlib
import html
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).parent / 'fixtures' / 'validation'
PYTHON = sys.executable


class SiteValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(FIXTURE, self.root / 'fixture')
        self.fixture = self.root / 'fixture'
        self.site = self.fixture / 'site'
        self.base = 'https://docs.cloudscripting.com/'
        self.archived = False

    def run_check(self):
        report = self.root / 'report.json'
        report.unlink(missing_ok=True)
        result = subprocess.run([PYTHON, '-m', 'scripts.migration.check_site', '--baseline', str(self.fixture/'baseline.json'), '--page-map', str(self.fixture/'page-map.json'), '--site-dir', str(self.site), '--base-url', self.base, '--exceptions', str(self.fixture/'exceptions.json'), '--report', str(report)]+(['--asset-map',str(self.asset_map)] if hasattr(self,'asset_map') else [])+(['--archived'] if self.archived else []), cwd=ROOT, capture_output=True, text=True)
        return result, json.loads(report.read_text()) if report.exists() else {}

    def replace(self, path, old, new):
        p = self.site / path
        text = p.read_text()
        self.assertIn(old, text)
        p.write_text(text.replace(old, new))

    def reject(self, issue, location):
        result, report = self.run_check()
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        issues = report.get('issues', [])
        self.assertTrue(any(x['id'] == issue and location in json.dumps(x) for x in issues), (report, result.stderr))

    def test_accepts_exact_code_through_highlight_wrappers_and_precise_inherited_defect(self):
        result, report = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr+str(report))
        self.assertEqual(report['status'], 'pass')
        for name in ('browser', 'http', 'hosting'):
            self.assertEqual(report['checks'][name]['status'], 'not_run')

    def test_retired_correspondence_menu_keeps_route_required_and_archives_unchanged(self):
        # Reuse literal page content under the retired route; only its sidebar
        # membership may change. Content, search, links and publication still count.
        retired = '/virtuozzo-cs-correspondence/'
        for path in self.fixture.rglob('*'):
            if path.is_file() and path.suffix in {'.json', '.html', '.xml', '.txt'}:
                path.write_text(path.read_text().replace('/guide/', retired))
        (self.site / 'guide').rename(self.site / retired.strip('/'))
        item = '<a href="' + retired + '">Guide</a>'
        for path in self.site.rglob('*.html'):
            path.write_text(path.read_text().replace(item, ''))
        result, report = self.run_check()
        self.assertEqual(result.returncode, 0, report)
        self.archived = True
        self.reject('menu-label', retired)
        self.archived = False
        self.replace('index.html', '</aside>', item + '</aside>')
        self.reject('menu-order', retired)
        self.replace('index.html', item, '')
        (self.site / retired.strip('/') / 'index.html').unlink()
        self.reject('missing-page', retired)

    def test_mutations_are_rejected_for_the_intended_reason(self):
        mutations = [
            ('guide/index.html', 'value: ${token}', 'value: ${Token}', 'code-bytes', '/guide/'),
            ('guide/index.html', '<span class="nt">value</span>: ${token}', '<span class="nt">value</span>: ${Token}', 'code-bytes', '/guide/'),
            ('guide/index.html', 'role="tabpanel"', 'role="deleted-panel"', 'tab-panels', '/guide/'),
            ('guide/index.html', 'data-tab-title="YAML"', 'data-tab-title="JSON"', 'tab-panels', '/guide/'),
            ('guide/index.html', 'id="run"', 'id="run-new"', 'missing-fragment', '/guide/'),
            ('index.html', '/img/Icon.svg', '/img/icon.svg', 'asset-case', '/'),
            ('index.html', '>Guide</a>', '>Wrong label</a>', 'menu-label', '/'),
            ('index.json', 'https://docs.cloudscripting.com/guide/', 'https://docs.cloudscripting.com/missing/', 'search-entry', '/guide/'),
            ('index.html', 'rel="canonical" href="https://docs.cloudscripting.com/"', 'rel="canonical" href="https://wrong.invalid/"', 'canonical', '/'),
            ('robots.txt', 'Allow: /', 'Disallow: /', 'robots-rule', 'robots.txt'),
            ('sitemap.xml', '<url><loc>https://docs.cloudscripting.com/guide/</loc></url>', '', 'sitemap-entry', '/guide/'),
            ('guide/index.html', '/missing/', '/new-missing/', 'broken-link', '/new-missing/'),
        ]
        for path, old, new, issue, location in mutations:
            with self.subTest(issue=issue, path=path, old=old):
                original = (self.site/path).read_bytes()
                self.replace(path, old, new)
                self.reject(issue, location)
                (self.site/path).write_bytes(original)

    def test_changed_heading_and_search_title_are_detected(self):
        self.replace('index.html','>Overview</h1>','>Different technical topic</h1>')
        self.reject('heading-text','/')
        self.replace('index.html','>Different technical topic</h1>','>Overview</h1>')
        self.replace('index.json','"title":"Guide"','"title":"Wrong result"')
        self.reject('search-entry','/guide/')

    def test_missing_copy_surface_is_detected(self):
        self.replace('guide/index.html','class="code-block-source"','class="removed-copy-source"')
        self.reject('copy-source','/guide/')

    def test_external_reference_changes_and_duplicate_image_loss_fail(self):
        p=self.fixture/'baseline.json'; baseline=json.loads(p.read_text())
        baseline['pages']['/']['links'].append({'href':'https://example.test/frozen','resolved_url':'https://example.test/frozen','text':'Reference'})
        baseline['pages']['/']['images'].append(copy.deepcopy(baseline['pages']['/']['images'][0]))
        p.write_text(json.dumps(baseline))
        self.reject('link-reference','/')
        self.reject('image-reference','/')

    def test_directory_endpoint_without_slash_has_offline_target(self):
        p=self.fixture/'baseline.json';baseline=json.loads(p.read_text())
        baseline['pages']['/']['links'][0]['href']='/guide#run';baseline['pages']['/']['links'][0]['resolved_url']='/guide#run'
        p.write_text(json.dumps(baseline));self.replace('index.html','/guide/#run','/guide#run')
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertEqual(report['checks']['http']['status'],'not_run')

    def test_inherited_exception_has_no_unlimited_occurrence_budget(self):
        self.replace('guide/index.html','</main>','<a href="/missing/">New occurrence</a></main>')
        self.reject('broken-link','/missing/')

    def test_group_menu_label_is_checked(self):
        p=self.fixture/'page-map.json';data=json.loads(p.read_text())
        data['navigation']=[{'title':'Getting Started','menu_id':'getting-started','menu_parent':None,'weight':1,'children':[]}]
        p.write_text(json.dumps(data))
        self.reject('menu-group','Getting Started')

    def test_site_digest_uses_literal_posix_lexical_inventory(self):
        inventory=''.join(hashlib.sha256((self.site/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in ['guide/index.html','img/Icon.svg','index.html','index.json','robots.txt','search.html','search/index.html','sitemap.xml'])
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertEqual(report['inputs']['site_sha256'],hashlib.sha256(inventory.encode('utf-8')).hexdigest())

    def test_malformed_baseline_shape_still_emits_a_failed_report(self):
        (self.fixture/'baseline.json').write_text('[]')
        self.reject('invalid-input','/')

    def test_missing_source_identity_or_build_mode_is_incomplete(self):
        pm=self.fixture/'page-map.json'; baseline_path=self.fixture/'baseline.json'
        mapdata=json.loads(pm.read_text()); baseline=json.loads(baseline_path.read_text())
        baseline['build_provenance'].pop('mode');baseline_path.write_text(json.dumps(baseline))
        result,report=self.run_check();self.assertNotEqual(result.returncode,0,result.stderr)
        self.assertEqual(report.get('status'),'incomplete',report)
        (self.fixture/'exceptions.json').write_text('{"schema_version":1,"exceptions":[]}')
        baseline['pages']['/guide/']['links']=[]
        self.replace('guide/index.html','<a href="/missing/">Inherited defect</a>','')
        mapdata['source_commit']=None;baseline['inputs']['source_commit']=None;baseline['build_provenance']['source_commit']=None
        pm.write_text(json.dumps(mapdata));baseline_path.write_text(json.dumps(baseline))
        result,report=self.run_check();self.assertNotEqual(result.returncode,0,result.stderr)
        self.assertEqual(report.get('status'),'incomplete',report)

    def rebase(self, base):
        old_base=self.base
        prefix=base.split('://',1)[1].partition('/')[2]
        for p in self.site.rglob('*'):
            if p.is_file() and p.suffix in {'.html','.json','.xml','.txt'}:
                text=p.read_text().replace(old_base,base)
                text=text.replace('href="/','href="/'+prefix).replace('src="/','src="/'+prefix)
                p.write_text(text)
        self.base=base

    def test_production_root_profile_does_not_infer_archive_from_base_path(self):
        self.rebase('https://www.virtuozzo.com/cloudscripting-docs/')
        result,report=self.run_check()
        self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertIs(report['inputs'].get('archived'),False)
        self.replace('index.html','</head>','<meta name="robots" content="noindex, follow"></head>')
        self.reject('robots-rule','/')

    def test_archive_profile_requires_noindex_for_every_article(self):
        self.rebase('https://www.virtuozzo.com/cloudscripting-docs/8.15.1/')
        for path in ('index.html','guide/index.html'):
            self.replace(path,'</head>','<meta name="robots" content="noindex, follow"></head>')
        self.archived=True
        result,report=self.run_check()
        self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertIs(report['inputs'].get('archived'),True)
        self.replace('guide/index.html','<meta name="robots" content="noindex, follow">','')
        self.reject('robots-rule','/guide/')

    def test_authored_same_page_link_cannot_disappear_with_heading_glyph(self):
        p=self.fixture/'baseline.json';baseline=json.loads(p.read_text())
        baseline['pages']['/']['headings'][0]['text']='Overview¶'
        baseline['pages']['/']['links'].extend([
            {'href':'#overview','resolved_url':'/#overview','text':'¶'},
            {'href':'#overview','resolved_url':'/#overview','text':'Read Overview'},
        ])
        p.write_text(json.dumps(baseline))
        self.replace('index.html','<p>Welcome.</p>','<p>Welcome.</p><a href="#overview">Read Overview</a>')
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.replace('index.html','<a href="#overview">Read Overview</a>','')
        self.reject('link-reference','Read Overview')
        self.replace('index.html','<p>Welcome.</p>','<p>Welcome.</p><a href="#overview">¶</a>')
        self.reject('link-reference','Read Overview')

    def test_textarea_extraction_matches_literal_html5_value_cases(self):
        from scripts.migration.check_site import semantic
        for case in json.loads((FIXTURE/'textarea-cases.json').read_text()):
            with self.subTest(case=case['name']):
                output='<main><div class="code-block"><textarea class="code-block-source">'+case['body_html']+'</textarea><pre><code>visible</code></pre></div></main>'
                self.assertEqual(semantic(output)['codes'][0]['copy'],case['value'])

    def set_yaml_example(self, body, textarea_html):
        baseline_path=self.fixture/'baseline.json'
        baseline=json.loads(baseline_path.read_text())
        block=baseline['pages']['/guide/']['code_blocks'][0]
        (self.fixture/block['text_path']).write_bytes(body.encode('utf-8'))
        block['sha256']=hashlib.sha256(body.encode('utf-8')).hexdigest()
        block['byte_length']=len(body.encode('utf-8'))
        baseline_path.write_text(json.dumps(baseline))
        p=self.site/'guide/index.html'; output=p.read_text()
        output=re.sub(r'(<textarea class="code-block-source" hidden>).*?(</textarea>)',lambda m:m[1]+textarea_html+m[2],output,count=1,flags=re.S)
        output=re.sub(r'<pre><code class="language-yaml">.*?</code></pre>',lambda m:'<pre><code class="language-yaml">'+html.escape(body)+'</code></pre>',output,count=1,flags=re.S)
        p.write_text(output)

    def test_sacrificial_encoded_lf_preserves_exact_clipboard_body(self):
        cases=[('normal','value: test\n'),('empty',''),('lf-only','\n'),('leading-lf','\nvalue: test\n'),('multiple-lfs','\n\nvalue: test\n\n')]
        for name,body in cases:
            with self.subTest(case=name):
                self.set_yaml_example(body,'&#10;'+html.escape(body).replace('\n','&#10;'))
                result,report=self.run_check()
                self.assertEqual(result.returncode,0,result.stderr+str(report))

    def test_missing_sentinel_cannot_hide_loss_of_real_leading_lf(self):
        body='\nvalue: test\n'
        self.set_yaml_example(body,html.escape(body).replace('\n','&#10;'))
        self.reject('code-bytes','/guide/')
        result,report=self.run_check()
        self.assertTrue(any(x['id']=='code-bytes' and x['evidence']['surface']=='copy' and x['evidence']['first_changed_byte']==0 for x in report['issues']))

    def test_unlabeled_code_accepts_only_plaintext_aliases(self):
        p=self.fixture/'baseline.json';original=p.read_bytes()
        data=json.loads(original);data['pages']['/guide/']['code_blocks'][0]['language']=None
        p.write_text(json.dumps(data))
        guide=self.site/'guide/index.html';guide_original=guide.read_bytes()
        for language in ('text','plaintext'):
            guide.write_bytes(guide_original)
            with self.subTest(language=language):
                self.replace('guide/index.html','language-yaml','language-'+language)
                result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        guide.write_bytes(guide_original)
        self.replace('guide/index.html','language-yaml','language-json');self.reject('code-language','/guide/')
        p.write_bytes(original)
        for language,index in [('yaml',0),('json',1)]:
            with self.subTest(named_language=language):
                guide.write_bytes(guide_original)
                self.replace('guide/index.html','language-'+language,'language-text')
                result,report=self.run_check();self.assertNotEqual(result.returncode,0,result.stderr)
                self.assertTrue(any(x['id']=='code-language' and x['evidence']['block_index']==index for x in report['issues']))

    def test_group_labels_can_be_visible_spans_and_divs_but_keep_order(self):
        p=self.fixture/'page-map.json';data=json.loads(p.read_text())
        data['navigation']=[{'title':name,'menu_id':name,'menu_parent':None,'weight':i+1,'children':[]} for i,name in enumerate(['Getting Started','Creating Manifest'])]
        p.write_text(json.dumps(data))
        groups='<span class="aside-menu-item"><span>Getting Started</span></span><div>Creating Manifest</div>'
        for f in ('index.html','guide/index.html'):
            self.replace(f,'<aside>','<aside>'+groups)
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.replace('index.html','<span>Getting Started</span>','<span hidden>Getting Started</span>')
        self.reject('menu-group','Getting Started')
        self.replace('index.html','<span hidden>Getting Started</span>','<span>Getting Started</span>')
        self.replace('index.html',groups,'<div>Creating Manifest</div><span>Getting Started</span>')
        self.reject('menu-group-order','/')
        self.replace('index.html','<span>Getting Started</span>','<span hidden>Getting Started</span>')
        self.reject('menu-group','Getting Started')

    def test_captured_absolute_cross_product_link_is_external_on_new_host(self):
        self.rebase('https://www.virtuozzo.com/cloudscripting-docs/')
        p=self.fixture/'baseline.json';data=json.loads(p.read_text())
        cross='https://www.virtuozzo.com/application-platform-docs/ssh-gate/'
        data['pages']['/']['links'].append({'href':cross,'resolved_url':cross,'text':'SSH gate'})
        p.write_text(json.dumps(data));self.replace('index.html','<p>Welcome.</p>','<p>Welcome.</p><a href="'+cross+'">SSH gate</a>')
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.replace('index.html',cross,'https://www.virtuozzo.com/application-platform-docs/new-target/')
        self.reject('release-prefix','new-target')
        self.replace('index.html','https://www.virtuozzo.com/application-platform-docs/new-target/','https://www.virtuozzo.com/guide/')
        self.reject('release-prefix','/guide/')
        self.replace('index.html','https://www.virtuozzo.com/guide/','https://www.virtuozzo.com/img/Icon.svg')
        self.reject('release-prefix','/img/Icon.svg')

    def test_legacy_copy_bytes_remain_exact_over_raw_source_whitespace(self):
        case=json.loads((FIXTURE/'legacy-whitespace-case.json').read_text())
        self.set_yaml_example(case['legacy_body'],'&#10;'+html.escape(case['legacy_body']).replace('\n','&#10;'))
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        baseline=self.fixture/'baseline.json';legacy_baseline=baseline.read_bytes()
        code=self.fixture/'code/yaml.txt';legacy_code=code.read_bytes()
        self.set_yaml_example(case['source_body'],'&#10;'+html.escape(case['source_body']).replace('\n','&#10;'))
        baseline.write_bytes(legacy_baseline);code.write_bytes(legacy_code)
        result,report=self.run_check();self.assertNotEqual(result.returncode,0,result.stderr)
        self.assertEqual({x['evidence']['surface'] for x in report['issues'] if x['id']=='code-bytes'}, {'text','copy'})
        self.assertEqual(hashlib.sha256(case['legacy_body'].encode()).hexdigest(),report['issues'][0]['evidence']['expected_sha256'])

    def test_one_extra_code_block_is_not_waived(self):
        self.replace('guide/index.html', '</main>', '<pre><code>hidden example\n</code></pre></main>')
        self.reject('code-count', '/guide/')

    def test_draft_and_undeclared_pages_cannot_publish(self):
        for route, issue in [('draft', 'draft-publication'), ('surprise', 'undeclared-publication')]:
            with self.subTest(route=route):
                p = self.site/route/'index.html'
                p.parent.mkdir()
                p.write_text('<main><h1>Leak</h1></main>')
                self.reject(issue, route)
                shutil.rmtree(p.parent)

    def test_homepage_must_be_in_search(self):
        p = self.site/'index.json'
        p.write_text(json.dumps(json.loads(p.read_text())[1:]))
        self.reject('search-entry', '/')

    def test_exact_exception_does_not_allow_different_page_or_source(self):
        self.replace('index.html', '<p>Welcome.</p>', '<p>Welcome.</p><a href="/missing/">new link</a>')
        self.reject('broken-link', '/')
        self.replace('index.html', '<a href="/missing/">new link</a>', '')
        ex = self.fixture/'exceptions.json'
        data = json.loads(ex.read_text())
        data['exceptions'][0]['source_commit'] = '2'*40
        ex.write_text(json.dumps(data))
        self.reject('exception-provenance', 'fixture-inherited-link')

    def test_prefix_is_enforced_for_markdown_and_raw_html_links(self):
        self.base += '8.15.1/'
        for p in self.site.rglob('*'):
            if p.is_file() and p.suffix in {'.html', '.json', '.xml', '.txt'}:
                t = p.read_text().replace('https://docs.cloudscripting.com/', self.base)
                t = t.replace('href="/', 'href="/8.15.1/').replace('src="/', 'src="/8.15.1/')
                p.write_text(t)
        result, report = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr+str(report))
        for attribute in ('href', 'src'):
            with self.subTest(attribute=attribute):
                path = 'index.html'
                old = f'{attribute}="/8.15.1/'
                self.replace(path, old, f'{attribute}="/')
                self.reject('release-prefix', '/')
                self.replace(path, f'{attribute}="/', old)

    def test_unsafe_route_is_rejected_without_reading_outside_site(self):
        p = self.fixture/'page-map.json'
        data = json.loads(p.read_text())
        data['pages'][1]['old_url'] = '/../escape/'
        p.write_text(json.dumps(data))
        self.reject('unsafe-path', 'escape')

    def test_baseline_code_hash_and_provenance_are_verified(self):
        p = self.fixture/'code/yaml.txt'
        p.write_text('changed baseline\n')
        self.reject('baseline-code-integrity', 'yaml.txt')

    def test_selected_pilot_map_passes_and_records_its_limited_scope(self):
        p=self.fixture/'page-map.json'; data=json.loads(p.read_text())
        data['scope']='selected'; data['pages']=data['pages'][:2]
        p.write_text(json.dumps(data))
        result, report=self.run_check()
        self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertEqual(report['inputs']['publication_scope'],'selected')

    def test_map_metadata_and_pending_dispositions_cannot_silently_pass(self):
        p = self.fixture/'page-map.json'
        original=p.read_bytes()
        for field, value, issue in [('source_sha256','', 'page-metadata'),('title','', 'page-metadata'),('disposition','pending','pending-disposition'),('weight',0,'page-metadata'),('nav_title',None,'page-metadata'),('menu_id',None,'page-metadata'),('target_path','../../outside.md','page-metadata')]:
            with self.subTest(field=field):
                data=json.loads(original); data['pages'][0][field]=value; p.write_text(json.dumps(data))
                self.reject(issue, 'docs/index.md')
        p.write_bytes(original)

    def test_resource_image_maps_to_a_derivative_but_compatibility_bytes_are_required(self):
        # Literal independent map uses Task5's public schema, with a recognisable
        # collision-safe resource name and an independently authored derivative.
        image=b'PNG fixture bytes'
        static=self.site/'img/Photo.png'; static.write_bytes(image)
        original=self.site/'guide/0123456789abcdef-Photo.png'; original.write_bytes(image)
        derivative=self.site/'guide/0123456789abcdef-Photo_hu123_20_480x0_resize.png'; derivative.write_bytes(b'resized')
        p=self.fixture/'baseline.json'; baseline=json.loads(p.read_text())
        baseline['pages']['/guide/']['images']=[{'src':'/img/Photo.png','resolved_url':'/img/Photo.png','alt':'Photo'}]
        p.write_text(json.dumps(baseline))
        self.replace('guide/index.html','</main>','<img src="/guide/0123456789abcdef-Photo_hu123_20_480x0_resize.png" srcset="/guide/0123456789abcdef-Photo.png 600w" alt="Photo"></main>')
        amap=self.fixture/'asset-map.json'
        amap.write_text(json.dumps({'schema_version':1,'source_commit':'1'*40,'source_kind':'git','assets':[{'git_path':'theme/readthedocs/img/Photo.png','git_blob':'4'*40,'public_url':'/img/Photo.png','sha256':hashlib.sha256(image).hexdigest(),'byte_length':len(image),'casefold_collision_group':None,'overlay_decision':'exact-git-no-intentional-overlay','bundle_resources':[{'page_url':'/guide/','target_path':'content/guide/0123456789abcdef-Photo.png','name':'0123456789abcdef-Photo.png','relative_url':'../img/Photo.png'}]}]}))
        self.asset_map=amap
        result,report=self.run_check(); self.assertEqual(result.returncode,0,result.stderr+str(report))
        static.write_bytes(b'wrong compatibility bytes'); self.reject('asset-integrity','/img/Photo.png')
        static.write_bytes(image); original.unlink(); self.reject('asset-integrity','Photo.png')

    def test_current_source_restores_only_the_exact_custom_responses_pair(self):
        legacy=ROOT/'tests/migration/fixtures/baseline'
        baseline=json.loads((legacy/'legacy-root.json').read_text())
        self.assertEqual(sum(len(p['code_blocks']) for p in baseline['pages'].values()),564)
        self.assertEqual(sum(len(p['tab_panels']) for p in baseline['pages'].values()),268)
        route='/creating-manifest/handling-custom-responses/'
        page=copy.deepcopy(baseline['pages'][route])
        page['links']=[]; page['images']=[]
        baseline['pages']={route:page}
        baseline['inputs']['source_commit']='76628f8aa01571fbc348211cb7df726cf408cd17'
        (self.fixture/'baseline.json').write_text(json.dumps(baseline))
        for b in page['code_blocks']:
            path=self.fixture/b['text_path']; path.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(legacy/b['text_path'],path)
        pm=json.loads((self.fixture/'page-map.json').read_text())
        pm['source_commit']=baseline['inputs']['source_commit']; pm['pages']=pm['pages'][1:2]
        pm['pages'][0].update(old_url=route,source_path='docs/creating-manifest/handling-custom-responses.md',title='Custom Responses',nav_title='Custom Responses')
        (self.fixture/'page-map.json').write_text(json.dumps(pm)); (self.fixture/'exceptions.json').write_text('{"schema_version":1,"exceptions":[]}')
        restored_yaml='type: update\nname: response handlers\n\nonInstall:\n  return:\n    result: warning\n    message: Warning!\n    email: string\n'
        restored_json='{\n    "type": "update",\n    "name": "response handlers",\n    "onInstall": {\n        "return": {\n          "result": "warning",\n          "message": "Warning!",\n          "email": "string"\n        }\n    }\n}\n'
        blocks=[(b['language'],(legacy/b['text_path']).read_text()) for b in page['code_blocks']]
        blocks[4:4]=[('yaml',restored_yaml),('json',restored_json)]
        def render(items):
            out='<aside><a href="'+route+'">Custom Responses</a></aside><main><h1 id="handling-custom-responses">Handling Custom Responses</h1>'
            for i in range(0,len(items),2):
                out+='<div class="tabs-container">'
                for lang,text in items[i:i+2]:
                    out+='<div role="tabpanel" data-tab-title="'+lang.upper()+'"><div class="code-block"><textarea class="code-block-source">'+html.escape(text)+'</textarea><pre><code class="language-'+lang+'">'+html.escape(text)+'</code></pre></div></div>'
                out+='</div>'
            return '<html><head><link rel="canonical" href="'+self.base+route.lstrip('/')+'"></head><body>'+out+'</main></body></html>'
        shutil.rmtree(self.site); self.site.mkdir()
        p=self.site/route.strip('/')/'index.html';p.parent.mkdir(parents=True);p.write_text(render(blocks))
        (self.site/'index.json').write_text(json.dumps([{'title':'Custom Responses','contents':'Example responses','permalink':self.base+route.lstrip('/')}]))
        (self.site/'sitemap.xml').write_text('<urlset><url><loc>'+self.base+route.lstrip('/')+'</loc></url></urlset>')
        (self.site/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+self.base+'sitemap.xml\n')
        (self.site/'search').mkdir();(self.site/'search/index.html').write_text('search');(self.site/'search.html').write_text('legacy search')
        result,report=self.run_check();self.assertEqual(result.returncode,0,result.stderr+str(report))
        p.write_text(render(blocks[:4]+blocks[6:]));self.reject('code-count',route)
        altered=copy.deepcopy(blocks);altered[4]=('yaml',restored_yaml.replace('Warning!','warning!'))
        p.write_text(render(altered));self.reject('code-bytes',route)
        p.write_text(render(blocks+[('yaml','commented actions must stay hidden\n'),('json','{}\n')]))
        self.reject('code-count',route)

    def test_real_pinned_hugo_final_lf_loss_is_detected(self):
        hugo=ROOT/'.devbox/nix/profile/default/bin/hugo'
        if not hugo.is_file():
            self.skipTest('Pinned Hugo unavailable; see task11 evidence for real build')
        version=subprocess.run([str(hugo),'version'],capture_output=True,text=True,check=True).stdout
        self.assertIn('v0.124.1+extended',version)
        source=self.root/'hugo';source.mkdir()
        (source/'config.yaml').write_text('baseURL: https://docs.cloudscripting.com/\ntheme: compose-master\nmarkup:\n  highlight:\n    noClasses: false\n')
        (source/'themes').symlink_to(ROOT/'themes')
        (source/'content').mkdir()
        (source/'content/_index.md').write_text('---\ntitle: Test\n---\n{{< tabs >}}\n{{< tabs-item title="YAML" >}}\n```yaml\nvalue: ${token}\n```\n{{< /tabs-item >}}\n{{< /tabs >}}\n')
        build=subprocess.run([str(hugo),'--source',str(source),'--destination',str(source/'public')],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(build.returncode,0,build.stderr)
        # Exercise the parser's public observable surface using the real theme
        # output, then feed a byte mutation through the CLI fixture too.
        from scripts.migration.check_site import semantic
        page=semantic((source/'public/index.html').read_text())
        self.assertEqual([(x['text'],x['copy']) for x in page['codes']],[('value: ${token}','value: ${token}')])
        self.assertEqual(page['tabs'],[{'code_blocks':[0],'languages':['yaml']}])
        self.replace('guide/index.html','value: ${token}\n','value: ${token}')
        self.reject('code-bytes','/guide/')


class ArtifactValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.artifact = self.root/'artifact'
        self.artifact.mkdir()
        self.manifest = self.root/'manifest.yaml'
        self.data = {'schema_version':1, 'production_base_url':'https://www.virtuozzo.com/cloudscripting-docs/', 'default_version':'8.15.1', 'root':{'source_commit':'1'*40,'source_format':'mkdocs','output_prefix':''}, 'releases':[{'id':'8.15.1','source_commit':'2'*40,'source_format':'mkdocs','publication':'retained','output_prefix':'8.15.1/'}]}
        self.manifest.write_text(yaml.safe_dump(self.data))
        self.metadata = {'schema_version':1,'kind':'production','base_url':self.data['production_base_url'], 'manifest_sha256':hashlib.sha256(self.manifest.read_bytes()).hexdigest(),'content_commit':'1'*40,'tooling_commit':'3'*40,'theme_commit':'91b3863e863981905ba45566832022270a56085f','tools':{'hugo':'0.124.1','hugo_extended':True,'task':'3.44.1'},'prefixes':['','8.15.1/'],'builds':[]}
        for name, prefix, commit in [('root','','1'*40),('8.15.1','8.15.1/','2'*40)]:
            site = self.artifact/'site'/prefix
            site.mkdir(parents=True, exist_ok=True)
            for f in ('index.html','index.json','sitemap.xml','robots.txt','search/index.html','search.html'):
                p = site/f; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('fixture\n')
            report_path = f'validation/{name}.json'
            rp = self.artifact/report_path; rp.parent.mkdir(exist_ok=True)
            rp.write_text(json.dumps({'schema_version':1,'status':'pass','inputs':{'source_commit':commit,'base_url':self.data['production_base_url']+prefix,'site_dir':'site/'+prefix,'archived':name!='root'},'checks':{'offline':{'status':'pass'},'browser':{'status':'not_run'},'http':{'status':'not_run'},'hosting':{'status':'not_run'}},'issues':[]}))
            self.metadata['builds'].append({'id':name,'output_prefix':prefix,'source_commit':commit,'source_format':'mkdocs','site_report':report_path,'validation_source_commit':commit})
        for build in self.metadata['builds']:
            prefix=build['output_prefix']; site=self.artifact/'site'/prefix
            files=sorted((p for p in site.rglob('*') if p.is_file() and (prefix or not p.relative_to(site).as_posix().startswith('8.15.1/'))),key=lambda p:p.relative_to(site).as_posix())
            inventory=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(site).as_posix()+'\n' for p in files)
            rp=self.artifact/build['site_report']; report=json.loads(rp.read_text())
            report['scope']='offline'; report['inputs']['baseline_sha256']='a'*64; report['inputs']['page_map_sha256']='b'*64; report['inputs']['publication_scope']='complete'; report['inputs']['site_sha256']=hashlib.sha256(inventory.encode()).hexdigest()
            rp.write_text(json.dumps(report))
        self.seal()

    def seal(self):
        (self.artifact/'artifact.json').write_text(json.dumps(self.metadata))
        files = sorted(p for p in self.artifact.rglob('*') if p.is_file() and p.name!='checksums.sha256')
        (self.artifact/'checksums.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(self.artifact).as_posix()+'\n' for p in files))

    def run_check(self):
        rp = self.root/'report.json'
        result = subprocess.run([PYTHON,'-m','scripts.migration.check_artifact','--artifact-dir',str(self.artifact),'--manifest',str(self.manifest),'--report',str(rp)],cwd=ROOT,capture_output=True,text=True)
        return result, json.loads(rp.read_text()) if rp.exists() else {}

    def reject(self, issue):
        result, report = self.run_check()
        self.assertNotEqual(result.returncode,0,result.stderr)
        self.assertIn(issue,[x['id'] for x in report.get('issues',[])],(report,result.stderr))

    def test_complete_artifact_passes_offline_without_claiming_hosting(self):
        result, report = self.run_check()
        self.assertEqual(result.returncode,0,result.stderr+str(report))
        self.assertEqual(report['checks']['hosting']['status'],'not_run')

    def test_missing_retained_prefix_fails_even_when_resealed(self):
        shutil.rmtree(self.artifact/'site/8.15.1')
        self.seal()
        self.reject('missing-release-output')

    def test_changed_release_prefix_fails(self):
        self.metadata['builds'][1]['output_prefix']='8.15.2/'
        self.metadata['prefixes'][1]='8.15.2/'
        self.seal()
        self.reject('release-prefix')

    def test_provenance_mutations_fail(self):
        for field, value, issue in [('content_commit','2'*40,'root-provenance'),('theme_commit','4'*40,'theme-provenance'),('manifest_sha256','a'*64,'manifest-integrity'),('tooling_commit','HEAD','tooling-provenance')]:
            with self.subTest(field=field):
                original=self.metadata[field]; self.metadata[field]=value; self.seal(); self.reject(issue); self.metadata[field]=original
        self.metadata['builds'][1]['source_commit']='1'*40
        self.seal(); self.reject('release-provenance')

    def test_changed_missing_and_unlisted_checksum_files_fail(self):
        p=self.artifact/'site/index.html'; original=p.read_bytes()
        p.write_bytes(b'changed\n'); self.reject('checksum-mismatch'); p.write_bytes(original)
        p.unlink(); self.reject('checksum-missing'); p.write_bytes(original)
        (self.artifact/'site/extra.txt').write_text('unlisted'); self.reject('checksum-unlisted')

    def test_unsafe_paths_and_symlinks_fail(self):
        with (self.artifact/'checksums.sha256').open('a') as f: f.write('a'*64+'  ../outside\n')
        self.reject('unsafe-path')
        self.seal()
        (self.artifact/'site/escape').symlink_to(self.root)
        self.reject('artifact-symlink')

    def test_missing_failed_or_mismatched_site_report_fails(self):
        p=self.artifact/'validation/8.15.1.json'; original=p.read_bytes()
        p.unlink(); self.seal(); self.reject('missing-site-validation'); p.write_bytes(original)
        data=json.loads(original); data['status']='fail'; p.write_text(json.dumps(data)); self.seal(); self.reject('site-validation')
        data=json.loads(original); data['inputs']['source_commit']='1'*40; p.write_text(json.dumps(data)); self.seal(); self.reject('validation-provenance')

    def test_stale_passing_validation_cannot_be_resealed(self):
        (self.artifact/'site/8.15.1/index.html').write_text('changed technical content')
        self.seal()
        self.reject('validation-content')

    def test_offline_report_cannot_claim_observed_hosting(self):
        p=self.artifact/'validation/root.json';data=json.loads(p.read_text())
        data['checks']['hosting']['status']='pass';p.write_text(json.dumps(data));self.seal()
        self.reject('offline-evidence-scope')

    def test_selected_pilot_report_cannot_pass_production_acceptance(self):
        p=self.artifact/'validation/root.json';data=json.loads(p.read_text())
        data['inputs']['publication_scope']='selected';p.write_text(json.dumps(data));self.seal()
        self.reject('incomplete-publication-scope')

    def test_validation_can_pin_original_source_separately_from_authored_hugo_commit(self):
        self.metadata['builds'][0]['validation_source_commit']='4'*40
        p=self.artifact/'validation/root.json';data=json.loads(p.read_text())
        data['inputs']['source_commit']='4'*40;p.write_text(json.dumps(data));self.seal()
        result, report=self.run_check()
        self.assertEqual(result.returncode,0,result.stderr+str(report))

    def test_malformed_metadata_or_manifest_still_emits_a_failed_report(self):
        (self.artifact/'artifact.json').write_text('[]')
        self.reject('invalid-input')
        self.seal();self.manifest.write_text('[')
        self.reject('invalid-input')

    def test_report_archive_profile_must_match_root_and_release_identity(self):
        for name,profile in [('root',True),('8.15.1',False),('root',None)]:
            with self.subTest(name=name,profile=profile):
                p=self.artifact/f'validation/{name}.json';original=p.read_bytes()
                report=json.loads(original);report['inputs']['archived']=profile
                p.write_text(json.dumps(report));self.seal();self.reject('validation-profile')
                p.write_bytes(original)

    def test_preview_does_not_pass_production_acceptance(self):
        self.metadata['kind']='preview'; self.seal(); self.reject('preview-artifact')


if __name__ == '__main__':
    unittest.main()
