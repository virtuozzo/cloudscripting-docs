# Staging preparation and rehearsal

Complete the host inputs below before staging acceptance. Preserve the existing served site, server configuration and any required legacy runtime until cutover and rollback acceptance. The retired checkout sources remain available in Git history.

The selected structure matches Application Management: manual workflow dispatch, SCP transfer, SSH operator session and a repository-named public directory. Production is `https://www.virtuozzo.com/cloudscripting-docs/`. The inferred test URL `https://test-site.virtuozzo.com/cloudscripting-docs/` and directory `/var/www/webroot/cloudscripting-docs/` are **unverified**. `/var/www/webroot/ROOT/site/` is the old workflow's recorded target, not proof of a current document root. Reference username `jelastic`, port `22`, and secret names `TEST_HOST_IP`, `PROD_HOST_IP`, `SSH_KEY` are conventions only. Do not paste secret values into reports or Git.

## 1. Complete host evidence before staging acceptance

Record these facts, dates, owners and evidence locations in `migration/hosting-contract.yaml`; store private configuration and archives outside Git and outside the document root.

| Required input | Evidence to collect |
| --- | --- |
| Confirmed staging URL, host/port/user and public-directory mapping | Hosting owner identifies vhost and full physical paths; sibling repository is not evidence |
| Backing server, modules, host maps, includes and effective rewrite rules | Approved read-only config dump; nginx public header alone proves none of these |
| Owner/group, modes, ACLs, xattrs, SELinux, symlink following, free space | Filesystem inventory and tool versions; identify whether both paths are on the same filesystem |
| Switch method | Confirm existing symlink document root, atomic replace and cache behavior; otherwise maintenance-window replacement |
| Managed files and writers | Explicit exact-case paths, owners, hashes, collision decisions, and quiescence method; include hidden files, ACME, PHP and uploads/logs where applicable |
| Actual live releases and paths | Whole served-tree inventory reconciled with 24 retained manifest records, candidate refs, deeper paths and supported URLs |
| Old-domain redirect/TLS and rewrite runtime | Identify owner, host-scoped rules/maps, certificate renewal exclusions and config-test/reload commands |
| Feedback | Hugo uses approved GitHub issue link; decide continued routing/runtime for legacy `issue_report.php`; preserve rollback bytes/runtime |
| Staging isolation | Host-side `X-Robots-Tag: noindex, nofollow` on all responses, including errors; access restriction where supported; verify without changing artifact bytes |
| Backup/restore and people | Real tree/config archives, hashes, metadata, recovery location, restore rehearsal, named owners and observation window |

Operator-run read-only examples, **after** setting `CONFIRMED_DOCROOT` and `CONFIRMED_REWRITE_ROOT` from the host owner's evidence:

```sh
set -eu
: "${CONFIRMED_DOCROOT:?set verified served physical directory}"
: "${CONFIRMED_REWRITE_ROOT:?set verified configuration snapshot root}"
readlink -f -- "$CONFIRMED_DOCROOT"
stat -- "$CONFIRMED_DOCROOT" "$CONFIRMED_REWRITE_ROOT"
df -P -- "$CONFIRMED_DOCROOT" "$CONFIRMED_REWRITE_ROOT"
find "$CONFIRMED_DOCROOT" -type f -print
```

These are GNU/Linux templates; confirm `find`, `stat`, `readlink`, `tar`, `sha256sum`, `cp`, `mv` and `ln` versions on the actual host. Ask the hosting owner to export the effective config using the actual server's read-only command (for example `nginx -T`, or `apachectl -M` plus the enabled vhost/includes). Config output can contain private information; keep it private. Record the exact config-test/reload commands; these depend on the host and are not inferred here. No SSH commands have been executed for this preparation.

## 2. Freeze one production artifact

Run the full-artifact validator before packaging: `uv run --locked python -m scripts.migration.check_artifact --artifact-dir "$ARTIFACT_DIR" --manifest migration/release-sources.yaml --report "$VALIDATION_REPORT"`. Require successful per-release validation, current root **and** explicit latest identities, complete retained release prefixes, case-sensitive asset manifest, no preview/draft markers, pinned theme/tool/source provenance and closed publication decisions. Local fixture checks do not replace observed host verification.

Package exactly the accepted `site/`, `artifact.json`, `checksums.sha256` and `validation/`; metadata stays outside the public tree. Record the archive SHA-256 as `APPROVED_SHA`, validation reports, release manifest SHA and build identity outside the archive. A digest without a trusted acceptance record is not approval. Reuse this archive for staging and production; do not rebuild on the server or promote a preview.

```sh
set -eu
: "${ARTIFACT_ARCHIVE:?accepted full archive path}"
: "${APPROVED_SHA:?accepted archive SHA-256}"
printf '%s  %s\n' "$APPROVED_SHA" "$ARTIFACT_ARCHIVE" | sha256sum -c -
: "${CONFIRMED_STAGE_SSH:?verified user@host}"
: "${CONFIRMED_SSH_PORT:?verified SSH port}"
: "${CONFIRMED_UPLOAD_DIR:?private remote upload directory}"
scp -P "$CONFIRMED_SSH_PORT" -- "$ARTIFACT_ARCHIVE" "$CONFIRMED_STAGE_SSH:$CONFIRMED_UPLOAD_DIR/"
ssh -p "$CONFIRMED_SSH_PORT" "$CONFIRMED_STAGE_SSH"
```

Each shell block enables `set -eu` independently; stop if any prerequisite or command fails. The remote block must enable these options again because SSH starts a separate shell. Run these only as the deploying operator when staging work is scheduled. Paths in SCP targets must use the host-approved path syntax. Inside that SSH session, set the verified paths and accepted digest; repeat `sha256sum -c` against the received archive **before extraction**. Validate archive entries are relative, contain no `..`, symlinks, hardlinks or special nodes, and match the accepted complete artifact inventory. Extract to a new private directory, never over the served tree:

```sh
set -eu
: "${UPLOAD:?received archive path}"
: "${APPROVED_SHA:?accepted archive SHA-256}"
: "${UNPACK:?new private absolute directory}"
printf '%s  %s\n' "$APPROVED_SHA" "$UPLOAD" | sha256sum -c -
test ! -e "$UNPACK"
mkdir -- "$UNPACK"
tar -xzf "$UPLOAD" --no-same-owner -C "$UNPACK"
(cd "$UNPACK" && sha256sum -c checksums.sha256)
```

Archive-member and complete inventory validation are mandatory prior to this block; `sha256sum -c` alone does not detect unexpected extra files. Keep the archive immutable and validation reports private. Use a production-URL artifact on staging, retaining production canonical metadata. Keep browser traffic on staging using a verified host mapping/proxy for absolute production URLs; do not patch artifact URLs or create a separate draft build. A second staging rebuild would invalidate same-artifact promotion.

## 3. Back up, prepare and switch

Use [rollback.md](rollback.md) to capture and verify the entire real staging served tree and all applicable rewrite/config state, including metadata, before replacing anything. Use the production preparation/switch blocks in [production.md](production.md) with **staging-specific verified paths**. Rehearse the selected strategy and complete restoration on staging; record the backup IDs, hashes, old/new pointer targets, command output and restored tree/config manifests. Do not convert an existing directory into a symlink during an ordinary release switch; that adoption needs its own host-specific rehearsal.

## 4. Validate HTTP and browser behavior

Use actual confirmed URLs, with `curl -I` for HEAD and `curl -sS -D headers -o body` for GET. Record status/Location and compare bodies where appropriate. Check root, all retained release roots and sampled deep routes, explicit latest, version-switch HEAD fallback, unknown pages/releases returning **404**, search query retention, prefixed resources, canonical/sitemap/robots, and non-indexing error responses. Verify exact-case images against their own hashes. Do not accept `curl -L` success alone: inspect the redirect chain for loops, double prefixes or a missing-path fallback to root.

Rehearse the old-domain redirect on an isolated vhost with the actual intended engine/rules. Preserve the original escaped path and query once; add `/cloudscripting-docs/` exactly once. Do not put `#...` in `Location`; browser fragments are never sent in HTTP requests. In a real browser, open `https://docs.cloudscripting.com/8.15.1/creating-manifest/actions/?q=example#oninstall` through that isolated host mapping, confirm final URL/query/fragment and scroll target, and test `/search.html?q=...` plus exact-case image URLs. Keep old-domain HTTPS and ACME renewal working. Verify root and explicit latest remain different.

Check desktop/mobile rendering, keyboard navigation, exact code/copy text, feedback, search queries, version-switch GET/HEAD behavior, case-sensitive images, canonical/sitemap/robots output, real 404 responses and rollback restoration. Record the exact archive digest and reports. Staging acceptance requires the real host facts and restore proof above; this document and fixture tests establish local preparation only.
