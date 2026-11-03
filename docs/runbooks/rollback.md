# Backup and rollback

No real server backup has been recorded in the hosting contract. All backup IDs/checksums in `migration/hosting-contract.yaml` intentionally remain null. Public HTTP samples, a Git checkout, reconstructed MkDocs output and the disposable fixture are **not** a rollback backup. Obtain the actual served bytes, exact-case paths, metadata and effective configuration before staging/cutover acceptance.

## Capture the real pre-change state

Hosting owner must identify the physical served tree, every applicable vhost/include/map/rewrite file, old-domain TLS/renewal routing, required PHP/runtime configuration, owner/group, ACL/xattr/SELinux state, external symlink targets and managed writers. A symlink archive alone does not save external target bytes. Quiesce writers or use a consistent filesystem snapshot; record its method/time. Capture secrets only to restricted recovery storage outside Git, public roots and CI logs.

These are **conditional GNU tar/Linux operator commands**, after the owner has confirmed the full backup roots, metadata support, permissions and available space. `CONFIG_ROOT` must cover all required configuration state or be a reviewed snapshot with an explicit original-path restore map. A single `.htaccess` is insufficient if host rules/includes live elsewhere. Do not blindly restore a shared server's entire `/etc` tree.

```sh
set -eu
: "${DOCROOT:?verified physical served directory}"
: "${CONFIG_ROOT:?verified complete scoped configuration root}"
: "${BACKUP:?new private backup directory outside served/config roots}"
test ! -e "$BACKUP"
mkdir -m 700 -- "$BACKUP"
tar --acls --xattrs --numeric-owner -cpf "$BACKUP/served.tar" -C "$DOCROOT" .
tar --acls --xattrs --numeric-owner -cpf "$BACKUP/config.tar" -C "$CONFIG_ROOT" .
(cd "$BACKUP" && sha256sum served.tar config.tar > SHA256SUMS)
(cd "$BACKUP" && sha256sum -c SHA256SUMS)
(cd "$DOCROOT" && find . -print0 | LC_ALL=C sort -z) > "$BACKUP/served.paths0"
(cd "$CONFIG_ROOT" && find . -print0 | LC_ALL=C sort -z) > "$BACKUP/config.paths0"
tar --acls --xattrs --compare -f "$BACKUP/served.tar" -C "$DOCROOT"
tar --acls --xattrs --compare -f "$BACKUP/config.tar" -C "$CONFIG_ROOT"
```

Record archive hashes in the private acceptance record and contract, plus exact-tree byte/metadata manifests, source host/path, date, owner, restore mapping, prior pointer target and metadata tool output. Store an independently verified off-host recovery copy and retention deadline. `SHA256SUMS` next to an archive detects accidental corruption; retain trusted hashes separately to identify the approved recovery state. The path manifests ensure restoration removes files added later, not just overwrites matching paths. Back up their hashes too with the rest of the evidence. Confirm any archive warnings before acceptance; exit zero is necessary but does not prove the scope is complete.

## Rehearse full restoration before acceptance

In a private case-sensitive destination with enough space, check the archived SHA-256 values against the recorded trusted hashes, list members and verify safe relative archive paths and expected inventory. Extract the served and config snapshots to **new, empty, separate** directories (never over a changed live tree):

```sh
: "${RESTORE_SITE:?new private same-filesystem restore directory}"
: "${RESTORE_CONFIG:?new private config restore directory}"
test ! -e "$RESTORE_SITE"
test ! -e "$RESTORE_CONFIG"
(cd "$BACKUP" && sha256sum -c SHA256SUMS)
mkdir -- "$RESTORE_SITE" "$RESTORE_CONFIG"
tar --acls --xattrs --same-owner -xpf "$BACKUP/served.tar" -C "$RESTORE_SITE"
tar --acls --xattrs --same-owner -xpf "$BACKUP/config.tar" -C "$RESTORE_CONFIG"
tar --acls --xattrs --compare -f "$BACKUP/served.tar" -C "$RESTORE_SITE"
tar --acls --xattrs --compare -f "$BACKUP/config.tar" -C "$RESTORE_CONFIG"
(cd "$RESTORE_SITE" && find . -print0 | LC_ALL=C sort -z) > "$BACKUP/restored-served.paths0"
(cd "$RESTORE_CONFIG" && find . -print0 | LC_ALL=C sort -z) > "$BACKUP/restored-config.paths0"
cmp -- "$BACKUP/served.paths0" "$BACKUP/restored-served.paths0"
cmp -- "$BACKUP/config.paths0" "$BACKUP/restored-config.paths0"
```

Restoring original owners may require the hosting operator's privileges; record successful uid/gid, mode, ACL/xattr and SELinux comparisons rather than silently dropping metadata flags. Verify file-byte manifests, symlink targets and the complete scoped config restore map. Test actual restored hosting behavior on staging, including retained versions, managed files/PHP, old redirects, HEAD/search/404 and TLS. Record the actual tested config-test/reload command and result. The local Python fixture tests regular-file byte/path/mode behavior, not these host metadata or HTTP properties.

## Execute rollback on agreed triggers

The named rollback operator keeps maintenance active and quiesces affected writers. Preserve failed-release logs/identities outside the served tree and reconcile any managed writes since the snapshot. Verify trusted backup hashes **before** touching active state. If an unchanged prior immutable release survives, verify its full tree identity and host overlays before switching back; otherwise use the verified fresh `RESTORE_SITE` above. Restoring the old pointer alone does not restore changed config or external state.

For a host with the already rehearsed symlink strategy, set `ROLLBACK_TARGET` to that verified old or restored tree and replace the pointer through a new sibling link:

```sh
: "${ROLLBACK_TARGET:?verified old or fully restored served tree}"
: "${ROLLBACK_POINTER:?new unused sibling temporary link}"
test -L "$PUBLIC_POINTER"
test ! -e "$ROLLBACK_POINTER"
test ! -L "$ROLLBACK_POINTER"
ln -s -- "$ROLLBACK_TARGET" "$ROLLBACK_POINTER"
mv -Tf -- "$ROLLBACK_POINTER" "$PUBLIC_POINTER"
```

For the rehearsed real-directory fallback, use a fresh verified `RESTORE_SITE` on the same filesystem, keeping the failed tree for investigation:

```sh
: "${FAILED_DIRECTORY:?new private same-filesystem failure directory}"
test ! -e "$FAILED_DIRECTORY"
test -d "$PUBLIC_DIRECTORY"
test ! -L "$PUBLIC_DIRECTORY"
mv -T -- "$PUBLIC_DIRECTORY" "$FAILED_DIRECTORY"
if ! mv -T -- "$RESTORE_SITE" "$PUBLIC_DIRECTORY"; then
  mv -T -- "$FAILED_DIRECTORY" "$PUBLIC_DIRECTORY"
  exit 1
fi
```

If the public path is already absent because a prior rename failed, recover that specific recorded state using the preserved prior/restored tree; do not rerun a block with false preconditions. Rollback directory renames have a gap and require maintenance.

Restore the configuration snapshot through the host owner's reviewed original-path mapping and recorded engine-specific config-test/reload sequence while traffic remains in maintenance. Preserve a pre-restore config copy; do not merge old files over new config and leave added includes/maps active. No universal config replacement/reload command is safe to specify until the host configuration layout is confirmed. Record that exact host-specific command sequence and rehearse it before staging acceptance.

Run archive/tree/config comparisons and the real HTTP/browser suite against the restored deployment; confirm the prior root/releases, managed files and rewrite behavior return. Record the incident, restoration time, verified identities and resumed observation window. Keep failed and restored evidence and backups until the agreed retention deadline. Preserve source history, required legacy runtime and recovery access throughout rollback.
