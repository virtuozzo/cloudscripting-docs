"""Verify a completed artifact offline; a pass does not approve deployment.

checksums.sha256 inventories artifact.json plus every file in site/ and
validation/, and excludes itself. Write --report outside the artifact.
"""
import argparse
import json
from pathlib import Path
import re
import yaml
from .check_site import digest, issue, report_shell, safe_relative, site_digest


THEME = '91b3863e863981905ba45566832022270a56085f'


def full_sha(value):
    return isinstance(value,str) and re.fullmatch('[0-9a-f]{40}',value) is not None


def check_artifact(artifact_dir,manifest_file):
    root, manifest_file=Path(artifact_dir),Path(manifest_file)
    result=report_shell({'artifact_dir':str(root),'manifest_sha256':digest(manifest_file)})
    manifest=yaml.safe_load(manifest_file.read_text())
    metadata=json.loads((root/'artifact.json').read_text())
    if metadata.get('schema_version')!=1:
        issue(result,'artifact-schema','artifact.json','Require schema_version 1')
    if metadata.get('kind')!='production':
        issue(result,'preview-artifact','artifact.json','Full acceptance requires a production artifact profile; previews cannot be promoted')
    if metadata.get('manifest_sha256')!=digest(manifest_file):
        issue(result,'manifest-integrity','artifact.json','Manifest digest mismatch')
    if metadata.get('base_url')!=manifest.get('production_base_url'):
        issue(result,'artifact-base-url','artifact.json',{'expected':manifest.get('production_base_url'),'actual':metadata.get('base_url')})
    if not full_sha(metadata.get('content_commit')) or metadata.get('content_commit')!=manifest['root']['source_commit']:
        issue(result,'root-provenance','artifact.json','content_commit must equal manifest.root.source_commit')
    if metadata.get('theme_commit')!=THEME:
        issue(result,'theme-provenance','artifact.json',{'expected':THEME,'actual':metadata.get('theme_commit')})
    if not full_sha(metadata.get('tooling_commit')):
        issue(result,'tooling-provenance','artifact.json','Require full immutable tooling commit')
    if metadata.get('tools')!={'hugo':'0.124.1','hugo_extended':True,'task':'3.44.1'}:
        issue(result,'tool-versions','artifact.json',metadata.get('tools'))
    wanted={'root':manifest['root'],**{r['id']:r for r in manifest['releases'] if r['publication']=='retained'}}
    prefixes=[r['output_prefix'] for r in wanted.values()]
    actual_prefixes=metadata.get('prefixes',[])
    if actual_prefixes!=prefixes:
        issue(result,'release-prefix','artifact.json',{'expected':prefixes,'actual':actual_prefixes})
    builds=metadata.get('builds',[])
    ids=[b.get('id') for b in builds]
    if len(ids)!=len(set(ids)) or set(ids)!=set(wanted):
        issue(result,'release-builds','artifact.json',{'expected':list(wanted),'actual':ids})
    for build in builds:
        name=build.get('id')
        record=wanted.get(name)
        if not record:
            issue(result,'undeclared-release',str(name),build);continue
        prefix=build.get('output_prefix','')
        if prefix and (not safe_relative(prefix) or not prefix.endswith('/')):
            issue(result,'unsafe-path',str(name),prefix);continue
        if prefix!=record['output_prefix']:
            issue(result,'release-prefix',str(name),{'expected':record['output_prefix'],'actual':prefix})
        if not full_sha(build.get('source_commit')) or build.get('source_commit')!=record['source_commit'] or build.get('source_format')!=record['source_format']:
            issue(result,'release-provenance',str(name),{'expected_commit':record['source_commit'],'expected_format':record['source_format'],'actual':build})
        for f in ('index.html','index.json','sitemap.xml','robots.txt','search/index.html','search.html'):
            if not (root/'site'/prefix/f).is_file():
                issue(result,'missing-release-output',str(name),{'prefix':prefix,'file':f})
        rp=build.get('site_report','')
        if not safe_relative(rp) or not rp.startswith('validation/'):
            issue(result,'unsafe-path',str(name),rp);continue
        if not (root/rp).is_file():
            issue(result,'missing-site-validation',str(name),rp);continue
        report=json.loads((root/rp).read_text())
        if report.get('schema_version')!=1 or report.get('status')!='pass' or report.get('checks',{}).get('offline',{}).get('status')!='pass' or report.get('issues'):
            issue(result,'site-validation',str(name),{'report':rp,'status':report.get('status')})
        inputs=report.get('inputs',{})
        if inputs.get('archived') is not (name!='root'):
            issue(result,'validation-profile',str(name),{'report':rp,'expected_archived':name!='root','actual_archived':inputs.get('archived')})
        if not full_sha(build.get('validation_source_commit')) or inputs.get('source_commit')!=build.get('validation_source_commit') or inputs.get('base_url')!=metadata.get('base_url','')+prefix or inputs.get('site_dir')!='site/'+prefix:
            issue(result,'validation-provenance',str(name),{'report':rp,'inputs':inputs,'expected_site_dir':'site/'+prefix})
        for field in ('baseline_sha256','page_map_sha256'):
            if not isinstance(inputs.get(field),str) or re.fullmatch('[0-9a-f]{64}',inputs[field]) is None:
                issue(result,'validation-provenance',str(name),{'report':rp,'missing_or_invalid':field})
        if inputs.get('publication_scope')!='complete':
            issue(result,'incomplete-publication-scope',str(name),'Production requires complete source inventory, not a selected pilot map')
        excluded=[p for p in prefixes if p] if not prefix else []
        actual_digest=site_digest(root/'site'/prefix,excluded)
        if inputs.get('site_sha256')!=actual_digest:
            issue(result,'validation-content',str(name),{'report':rp,'expected_site_sha256':inputs.get('site_sha256'),'actual_site_sha256':actual_digest})
        if report.get('scope')!='offline':
            issue(result,'offline-evidence-scope',str(name),'Site report must explicitly scope offline evidence')
        for check in ('browser','http','hosting'):
            if report.get('checks',{}).get(check,{}).get('status')!='not_run':
                issue(result,'offline-evidence-scope',str(name),{'report':rp,'check':check,'expected':'not_run'})
    # Exact inventory, not merely "every listed hash matches": unlisted payloads
    # and missing files invalidate the digest, as do symlinks and path traversal.
    files=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix()
        if p.is_symlink():
            issue(result,'artifact-symlink',rel,'Artifact must contain regular files/directories only')
        elif p.is_file() and rel!='checksums.sha256':
            files.add(rel)
            if rel!='artifact.json' and not rel.startswith(('site/','validation/')):
                issue(result,'artifact-layout',rel,'Only site/, validation/, artifact.json and checksums.sha256 are allowed')
    listed=set()
    checksum=root/'checksums.sha256'
    if not checksum.is_file():
        issue(result,'missing-checksums','checksums.sha256','Required exact file inventory')
    else:
        for number,line in enumerate(checksum.read_text().splitlines(),1):
            match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            if not match:
                issue(result,'checksum-format','checksums.sha256',{'line':number,'text':line});continue
            expected,rel=match.groups()
            if not safe_relative(rel) or rel=='checksums.sha256':
                issue(result,'unsafe-path','checksums.sha256',{'line':number,'path':rel});continue
            if rel in listed:
                issue(result,'checksum-duplicate',rel,{'line':number})
            listed.add(rel)
            p=root/rel
            if not p.is_file() or p.is_symlink():
                issue(result,'checksum-missing',rel,'Listed regular file is absent')
            elif digest(p)!=expected:
                issue(result,'checksum-mismatch',rel,{'expected':expected,'actual':digest(p)})
        for rel in sorted(files-listed):
            issue(result,'checksum-unlisted',rel,'File is absent from checksums.sha256')
        result['inputs']['checksums_sha256']=digest(checksum)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('artifact-dir','manifest','report'):
        p.add_argument('--'+name,required=True,type=Path)
    args=p.parse_args()
    # Writing a checker report into its own input would invalidate the artifact.
    if args.report.resolve().is_relative_to(args.artifact_dir.resolve()):
        p.error('--report must be outside --artifact-dir to avoid digest cycles')
    try:
        result=check_artifact(args.artifact_dir,args.manifest)
    except (OSError,ValueError,KeyError,TypeError,AttributeError,yaml.YAMLError) as err:
        result=report_shell({'artifact_dir':str(args.artifact_dir)})
        issue(result,'invalid-input','artifact.json',str(err))
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    raise SystemExit(0 if result['status']=='pass' else 1)


if __name__=='__main__':
    main()
