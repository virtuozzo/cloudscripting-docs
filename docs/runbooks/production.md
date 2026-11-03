# Production promotion

Local conditional runbook only. Production is `https://www.virtuozzo.com/cloudscripting-docs/`; its physical directory, SSH endpoint and switch capability are still unverified. Complete the hosting contract, real backup and staging acceptance first. The user intends to deploy personally. This file neither triggers a workflow nor changes a server.

## Preconditions and transfer

Record the named deployment, hosting/TLS, acceptance and rollback owners; maintenance/cutover time; observation duration/end; escalation route and rollback triggers. Candidate triggers include lost versions, redirect loops, failed search/feedback, wrong code text, image corruption, incorrect 404/HEAD behavior and elevated server errors. Set measured thresholds and response times with those owners. Keep old-domain TLS, redirects, legacy PHP, workflows and backups available through observation.

Use the **same archive SHA-256** recorded by staging acceptance. No theme pull, source update, preview promotion, rebuild, URL edit or archive repackaging. Repeat the SCP/SSH transfer, digest check, archive-member validation and private extraction from [staging.md](staging.md), substituting only the verified production endpoint and upload path. Record the received digest. Run the complete artifact validation before publishing; the artifact delivery tooling automates this gate.

Capture the real production served-tree/config backups following [rollback.md](rollback.md). Record the old pointer target or real-directory identity. Backups, temporary uploads, artifact metadata and validation reports must be outside all public directories. Confirm enough space for current, prepared, backup and restore copies. Quiesce identified server-side writers until the copy/switch is complete; account for writes after cutover in the rollback plan.

## Prepare a new complete release

The following are GNU/Linux operator templates. All variables must be absolute, verified paths on this host, with distinct non-overlapping upload, backup and public trees. `RELEASE` must be new, on the selected filesystem. `DOCROOT` here means the resolved current physical served directory. The repository-name public URL mapping is a separate confirmed input.

```sh
set -eu
: "${UNPACK:?private extracted accepted artifact}"
: "${DOCROOT:?verified current physical served tree}"
: "${RELEASE:?new complete release directory}"
: "${MANAGED_LIST:?validated private managed-file inventory}"
test ! -e "$RELEASE"
mkdir -- "$RELEASE"
cp -a -- "$UNPACK/site/." "$RELEASE/"
```

Before the copy, validate all retained manifest prefixes and their complete contents; reconcile the actual served-tree inventory, including any deeper extra-candidate routes. The archive must already contain every retained version; do not “preserve” a missing frozen version by silently filling it from a newer root build. Preserve exact filename case on a case-sensitive filesystem, and root versus explicit latest identity.

`MANAGED_LIST` is a reviewed, newline-separated list of regular-file paths relative to `DOCROOT`; no blank, absolute, `..`, control-character, symlink or duplicate/overlapping paths are allowed. Inventory includes hidden files and every non-artifact served file; each must be retained or have an approved disposition. Resolve directory/symlink/live-writer cases with the host owner before using this regular-file template. A managed path colliding with **any** artifact entry or ancestor file aborts preparation; do not overwrite accepted artifact bytes.

```sh
while IFS= read -r relative; do
  test -f "$DOCROOT/$relative"
  test ! -L "$DOCROOT/$relative"
  test ! -e "$RELEASE/$relative"
  test ! -L "$RELEASE/$relative"
  (cd "$DOCROOT" && cp -a --parents -- "$relative" "$RELEASE/")
done < "$MANAGED_LIST"
```

The inventory validation and collision check are required before this block; the loop is not a path validator. Preserve managed files' metadata/ownership and external dependencies. Record a separate exact-case combined served-tree manifest and managed-file hashes after copying, because the combined tree includes an explicit host overlay. The accepted archive digest remains unchanged; verify artifact-owned files against the accepted inventory after the overlay, and ensure no unexpected files. Apply only host-approved permissions; never recursively change unrelated files or shared host ownership.

## Preferred: existing atomic pointer

Use this block only after rehearsal proves the public document root is **already** a symlink (`PUBLIC_POINTER`), the web server follows it, `RELEASE` and pointer are on the same filesystem, GNU `mv -T` provides atomic replacement and caches refresh correctly. Resolve first-time adoption separately. Record `PREVIOUS_TARGET` and prove it points to the backed-up old tree.

```sh
: "${PUBLIC_POINTER:?verified existing document-root symlink}"
: "${NEXT_POINTER:?unused sibling temporary symlink path}"
test -L "$PUBLIC_POINTER"
PREVIOUS_TARGET=$(readlink -f -- "$PUBLIC_POINTER")
test "$PREVIOUS_TARGET" = "$DOCROOT"
test ! -e "$NEXT_POINTER"
test ! -L "$NEXT_POINTER"
ln -s -- "$RELEASE" "$NEXT_POINTER"
mv -Tf -- "$NEXT_POINTER" "$PUBLIC_POINTER"
```

Keep the old release and record both targets. The pointer operation is atomic; coordinated web-server configuration changes are separate. Apply only reviewed host-specific rewrite changes using the host's recorded config-test/reload sequence. If those fail, restore the prior pointer/config as in the rollback runbook. Do not serve artifact metadata or a release directory listing.

## Conditional fallback: existing directory replacement

If atomic symlink switching is unsupported, use this only after staging rehearsal, whole-tree plus rewrite backup verification, explicit managed-file accounting, writer quiescence and a maintenance window. Confirm `PUBLIC_DIRECTORY` is a real non-symlink directory, `RELEASE` is the fully prepared tree on the **same** filesystem, and `RETIRED` is a new sibling outside public URL mappings. Two renames have a visibility gap and are **not atomic**.

```sh
: "${PUBLIC_DIRECTORY:?verified real public directory}"
: "${RETIRED:?new private same-filesystem retired directory}"
test -d "$PUBLIC_DIRECTORY"
test ! -L "$PUBLIC_DIRECTORY"
test ! -e "$RETIRED"
mv -T -- "$PUBLIC_DIRECTORY" "$RETIRED"
if ! mv -T -- "$RELEASE" "$PUBLIC_DIRECTORY"; then
  mv -T -- "$RETIRED" "$PUBLIC_DIRECTORY"
  exit 1
fi
```

If automatic recovery fails, keep maintenance active and use the verified backup/restore procedure; do not delete either tree. Do not apply blanket `rsync --delete` to a live directory. Any host that requires in-place syncing needs a separately rehearsed, inventory-based plan with explicit retained-version/managed-file exclusions and full backup; this document does not authorize an untested substitute.

## Cutover and observation

Install the old-domain host redirect using the actual engine's reviewed host-specific rules. Preserve original path/case, release prefix and query exactly once; the `Location` must not replace fragments. Keep old-domain TLS and certificate renewal functional. Test all redirect/query/browser-fragment cases in staging first; no generic rule is represented here as installed server configuration.

Repeat the staging HTTP and browser checks against actual production: root and latest distinctness, all retained versions, known deep routes, exact-case images, search, version-switch HEAD, real 404, anchors, feedback, sitemap/canonical/robots and redirected old URLs. Production must not inherit the staging host's `noindex` response header. Record results, received archive digest, combined tree/config identities and observation start. Monitor through the named window and execute [rollback.md](rollback.md) on agreed triggers. Retain the prior served tree, rewrite backups, required legacy runtime, source history and recovery access until observation and rollback retention have explicitly ended.
