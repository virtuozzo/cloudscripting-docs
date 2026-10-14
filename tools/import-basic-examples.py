#!/usr/bin/env python3
"""Generate sample pages from a checkout of https://github.com/jelastic-jps/basic-examples.

Usage (from the repository root):

    git clone --depth 1 https://github.com/jelastic-jps/basic-examples /tmp/basic-examples
    python3 tools/import-basic-examples.py --repo /tmp/basic-examples --out content/samples

Each example in EXAMPLES becomes a page bundle under content/samples/<slug>/ with the
manifest shown as YAML (verbatim, comments included) and JSON tabs, any helper script,
and a deploy section. The explanatory prose lives in EXAMPLES below; re-run the script
after the repository changes to refresh the manifests.
"""
import argparse
import json
import os
import re

import yaml

REPO_URL = "https://github.com/jelastic-jps/basic-examples"
RAW_URL = "https://raw.githubusercontent.com/jelastic-jps/basic-examples/master"

# One entry per example directory: slug, titles, SEO, prose, links.
EXAMPLES = [
    {
        "dir": "introduction", "slug": "hello-world", "weight": 1,
        "title": "Hello World", "menu": "Hello World",
        "keywords": "cloud scripting, hello world, manifest example, deploy action",
        "intro": "The smallest useful Cloud Scripting package: an install manifest that provisions "
                 "one Apache node and deploys an application into it.",
        "points": [
            "`type: install` creates a new environment; `nodes` describes it as a single Apache node "
            "with 4 cloudlets in the *cp* node group.",
            "`globals.appSource` keeps the application archive URL in one place, so the manifest "
            "references it as `${globals.appSource}`.",
            "The `onInstall` event runs the [deploy](/actions/#deploy) action, which uploads the "
            "archive into the *ROOT* context.",
            "`success` is the text the dashboard shows when the installation finishes.",
        ],
        "next": [("Quick Start", "/quick-start/"), ("Basic Configs", "/basic-configs/"),
                 ("Actions", "/actions/"), ("Events", "/events/")],
    },
    {
        "dir": "automatic-vertical-scaling", "slug": "automatic-vertical-scaling", "weight": 2,
        "title": "Automatic Vertical Scaling", "menu": "Automatic Vertical Scaling",
        "keywords": "cloud scripting, vertical scaling, nginx worker_processes, add-on example",
        "intro": "An update package (add-on) for an NGINX load balancer that keeps the "
                 "`worker_processes` setting in line with the CPU cores available to the node.",
        "points": [
            "`type: update` installs the package into an existing environment; `targetNodes` limits "
            "the installation to environments with an *nginx* or *nginx-dockerized* node.",
            "The `adjustWorkersCount` action runs a [cmd](/actions/#cmd) command on the balancer "
            "layer (`cmd [bl]`) as *root*: it rewrites `worker_processes` from `/proc/cpuinfo` and "
            "reloads NGINX.",
            "The action is bound to the `onInstall` event and to `onAfterSetCloudletCount`, "
            "filtered by node type, so it reruns whenever the cloudlet count changes.",
        ],
        "next": [("Add-Ons", "/addons/"), ("Events", "/events/"),
                 ("Specifying Target Container", "/selecting-containers/"), ("Samples", "/samples/")],
    },
    {
        "dir": "automatic-horizontal-scaling", "slug": "automatic-horizontal-scaling", "weight": 3,
        "title": "Automatic Horizontal Scaling", "menu": "Automatic Horizontal Scaling",
        "keywords": "cloud scripting, horizontal scaling, triggers, script action, add-on example",
        "intro": "An update package that enables automatic horizontal scaling for the compute "
                 "layer of an existing environment by creating load triggers through the platform API.",
        "points": [
            "`targetNodes.nodeGroup: cp` makes the package installable only into environments that "
            "have a *cp* node group.",
            "The `onInstall` event runs a JavaScript file fetched from the repository with the "
            "[script](/actions/#script) action.",
            "The script reads the account quota for the maximum number of nodes, removes any "
            "existing *ADD_NODE* and *REMOVE_NODE* triggers, and creates two new ones: add a node "
            "when CPU load stays above 80% for 5 minutes, remove one when it stays below 5% for "
            "15 minutes.",
        ],
        "next": [("Custom Scripts", "/custom-scripts/"), ("Actions", "/actions/"),
                 ("Placeholders", "/placeholders/"), ("Samples", "/samples/")],
    },
    {
        "dir": "mount-data-storage", "slug": "mount-data-storage", "weight": 4,
        "title": "Mount Data from Storage", "menu": "Mount Data from Storage",
        "keywords": "cloud scripting, storage container, volumeMounts, volumes, mount example",
        "intro": "An install manifest with two layers: an NGINX PHP application server and a "
                 "shared storage node whose directory is mounted into the application server.",
        "points": [
            "The *storage* node exposes its data to the environment; the application node declares "
            "`/var/www/webroot/ROOT` in `volumes` and mounts it from the storage node group with "
            "`volumeMounts`.",
            "`sourcePath: /data` is the directory on the storage node; `readOnly: false` lets the "
            "application write to it.",
            "Scaling the *cp* layer later gives every new node the same mount, because the mount "
            "is part of the layer definition.",
        ],
        "next": [("Basic Configs", "/basic-configs/"), ("Specifying Target Container", "/selecting-containers/"),
                 ("Samples", "/samples/")],
    },
    {
        "dir": "install-add-on-inside-manifest", "slug": "install-add-on-inside-manifest", "weight": 5,
        "title": "Install Add-on within Environment Manifest", "menu": "Add-on within Manifest",
        "keywords": "cloud scripting, add-on, addons, public ip, setExtIpEnabled, manifest example",
        "intro": "An install manifest that declares an add-on inline and attaches it to a node while "
                 "the environment is being created. The add-on toggles a public IP address.",
        "points": [
            "The Apache node lists `setExtIp` in its `addons` array, so the add-on is installed "
            "right after the node is provisioned.",
            "The top-level `addons` block defines the add-on: its `onInstall` event enables the "
            "external IP through [setExtIpEnabled](/actions/#setextipenabled), and `onUnInstall` "
            "disables it again.",
            "After installation the add-on appears in the dashboard's **Add-ons** panel, where "
            "**Uninstall** detaches the IP address.",
        ],
        "next": [("Add-Ons", "/addons/"), ("Actions", "/actions/"),
                 ("Events", "/events/"), ("Samples", "/samples/")],
    },
    {
        "dir": "two-environments-from-one-jps-in-diff-regions",
        "slug": "two-environments-in-different-regions", "weight": 6,
        "title": "Create Two Environments in Different Regions", "menu": "Two Environments in Regions",
        "keywords": "cloud scripting, regions, CreateEnvironment, script action, multi-region example",
        "intro": "An install manifest that creates its own environment in one region and, from the "
                 "`onInstall` event, provisions a second identical environment in another region "
                 "through the platform API.",
        "points": [
            "`region` selects the region for the environment described by `nodes`.",
            "The `onInstall` script calls `env.control.CreateEnvironment` with a generated "
            "environment name and a second region.",
            "Region identifiers (`default_hn_group`, `default_hn2_group`) are platform specific; "
            "replace them with the regions available at your hosting provider before running "
            "the sample.",
        ],
        "next": [("Custom Scripts", "/custom-scripts/"), ("Basic Configs", "/basic-configs/"),
                 ("Samples", "/samples/")],
    },
    {
        "dir": "custom-registry", "slug": "custom-registry", "weight": 7,
        "title": "Deploy an Image from a Custom Registry", "menu": "Custom Registry",
        "keywords": "cloud scripting, docker registry, private registry, settings, image, manifest example",
        "intro": "An install manifest that asks the user for a container image and private "
                 "registry credentials, then provisions a node from that image.",
        "points": [
            "`settings.fields` builds the installation form: image name, registry URL, user and "
            "password (the latter with `inputType: password`).",
            "The node definition reads the answers through `${settings.*}` placeholders and passes "
            "the credentials in the `registry` block.",
        ],
        "next": [("Visual Settings", "/visual-settings/"), ("Placeholders", "/placeholders/"),
                 ("Basic Configs", "/basic-configs/"), ("Samples", "/samples/")],
    },
    {
        "dir": "subscriptions", "slug": "subscriptions", "weight": 8,
        "title": "Subscription Upgrade Flow", "menu": "Subscription Upgrade Flow",
        "keywords": "cloud scripting, subscriptions, onApplySubscriptionSettings, onBeforeMoveProduct, marketplace, jpsVersion",
        "intro": "An install manifest for a marketplace product sold by subscription. It shows how "
                 "a package reacts when the subscription settings change or the product is moved.",
        "points": [
            "`settings.schema` declares the subscription parameters (cloudlets, disk limit, "
            "migration flag) and `settings.fields` renders the installation form for them.",
            "`onInstall` installs a nested package with the [install](/actions/#install) action "
            "and stores its unique name in `globals.installationId` for later calls.",
            "`onBeforeMoveProduct` stops the move with a warning when the *Migration Disabled* "
            "setting is on; `onApplySubscriptionSettings` runs the nested package's "
            "`applyEnvSettings` action, which resizes cloudlets and disk limits through the API.",
            "`jpsVersion: 6.1.1` marks the minimum platform version these events require.",
        ],
        "next": [("Events", "/events/"), ("Visual Settings", "/visual-settings/"),
                 ("Custom Scripts", "/custom-scripts/"), ("Samples", "/samples/")],
    },
]


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def script_actions(manifest_text):
    """Return (name, url) for script actions that point into the repository."""
    return [(os.path.basename(url), url) for url in re.findall(r"script:\s*\"?(%s/[^\"\s]+)" % re.escape(RAW_URL), manifest_text)]


def render(ex, repo):
    src = os.path.join(repo, ex["dir"])
    manifest = read(os.path.join(src, "manifest.yaml")).rstrip("\n")
    as_json = json.dumps(yaml.safe_load(manifest), indent=2, ensure_ascii=False)
    desc = yaml.safe_load(manifest).get("description") or {}
    short = desc.get("short", "") if isinstance(desc, dict) else str(desc)

    out = [
        "---",
        "draft: false",
        f"title: {yaml_str(ex['title'])}",
        f"aliases: {yaml_str('/' + ex['slug'] + '/')}",
        'seoindex: "index, follow"',
        f"seotitle: {yaml_str(ex['title'])}",
        f"seokeywords: {yaml_str(ex['keywords'])}",
        f"seodesc: {yaml_str(short or ex['intro'])}",
        "menu:",
        "    docs:",
        f"        title: {yaml_str(ex['menu'])}",
        f"        url: {yaml_str('/' + ex['slug'] + '/')}",
        f"        weight: {ex['weight']}",
        '        parent: "samples"',
        f"        identifier: {yaml_str(ex['slug'])}",
        "---",
        "",
        f"# {ex['title']}",
        "",
        ex["intro"],
        "",
        f"The source is kept in the [basic-examples]({REPO_URL}/tree/master/{ex['dir']}) repository on GitHub.",
        "",
        "## How it works",
        "",
    ]
    out += [f"- {p}" for p in ex["points"]]
    out += ["", "## Manifest", "", "{{< tabs >}}", '{{< tabs-item title="YAML" >}}', "```yaml", manifest, "```",
            "{{< /tabs-item >}}", '{{< tabs-item title="JSON" >}}', "```json", as_json, "```",
            "{{< /tabs-item >}}", "{{< /tabs >}}", ""]
    for name, url in script_actions(manifest):
        local = os.path.join(src, "scripts", name)
        if os.path.isfile(local):
            out += [f"## Script: {name}", "",
                    f"The `script` action downloads [{name}]({url}) at installation time:", "",
                    "```javascript", read(local).rstrip("\n"), "```", ""]
    out += [
        "## Deploy the sample",
        "",
        "Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, "
        "open the **URL** tab, and paste the raw manifest link.",
        "",
        "```text",
        f"{RAW_URL}/{ex['dir']}/manifest.yaml",
        "```",
        "",
        "The [Quick Start](/quick-start/) guide walks through the import dialog step by step.",
        "",
        "## What's next?",
        "",
    ]
    out += [f"- [{t}]({u})" for t, u in ex["next"]]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="local checkout of jelastic-jps/basic-examples")
    ap.add_argument("--out", default="content/samples")
    args = ap.parse_args()
    for ex in EXAMPLES:
        dest = os.path.join(args.out, ex["slug"])
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, "index.md"), "w", encoding="utf-8") as fh:
            fh.write(render(ex, args.repo))
        print("wrote", os.path.join(dest, "index.md"))


if __name__ == "__main__":
    main()
