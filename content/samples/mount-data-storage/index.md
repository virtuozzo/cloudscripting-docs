---
draft: false
title: "Mount Data from Storage"
aliases: "/mount-data-storage/"
seoindex: "index, follow"
seotitle: "Mount Data from Storage"
seokeywords: "cloud scripting, storage container, volumeMounts, volumes, mount example"
seodesc: "Mount a storage node volume into application nodes."
menu:
    docs:
        title: "Mount Data from Storage"
        url: "/mount-data-storage/"
        weight: 4
        parent: "samples"
        identifier: "mount-data-storage"
---

# Mount Data from Storage

An install manifest with two layers: an NGINX PHP application server and a shared storage node whose directory is mounted into the application server.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/mount-data-storage) repository on GitHub.

## How it works

- The *storage* node exposes its data to the environment; the application node declares `/var/www/webroot/ROOT` in `volumes` and mounts it from the storage node group with `volumeMounts`.
- `sourcePath: /data` is the directory on the storage node; `readOnly: false` lets the application write to it.
- Scaling the *cp* layer later gives every new node the same mount, because the mount is part of the layer definition.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

# Optional parameter. If id is not specified it will be generated automatically.
id: mount-data-storage

# Defines the required name parameter
name: mount Data Storage

homepage: "https://docs.cloudscripting.com/"

description:
  short: Mount a storage node volume into application nodes.
  text: |
    Cloud Scripting package that provisions application and storage nodes and mounts a shared volume
    from the storage node group into the application node filesystem.

# The infrastructure of the environment.
nodes:
  - volumeMounts:
      /var/www/webroot/ROOT:
        readOnly: false
        sourcePath: /data
        sourceNodeGroup: storage
    volumes:
      - /var/www/webroot/ROOT
    nodeType: nginxphp
    cloudlets: 8
    nodeGroup: cp

  - nodeType: storage
    cloudlets: 8
    nodeGroup: storage
    displayName: Storage
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "id": "mount-data-storage",
  "name": "mount Data Storage",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Mount a storage node volume into application nodes.",
    "text": "Cloud Scripting package that provisions application and storage nodes and mounts a shared volume\nfrom the storage node group into the application node filesystem.\n"
  },
  "nodes": [
    {
      "volumeMounts": {
        "/var/www/webroot/ROOT": {
          "readOnly": false,
          "sourcePath": "/data",
          "sourceNodeGroup": "storage"
        }
      },
      "volumes": [
        "/var/www/webroot/ROOT"
      ],
      "nodeType": "nginxphp",
      "cloudlets": 8,
      "nodeGroup": "cp"
    },
    {
      "nodeType": "storage",
      "cloudlets": 8,
      "nodeGroup": "storage",
      "displayName": "Storage"
    }
  ]
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/mount-data-storage/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Basic Configs](/basic-configs/)
- [Specifying Target Container](/selecting-containers/)
- [Samples](/samples/)
