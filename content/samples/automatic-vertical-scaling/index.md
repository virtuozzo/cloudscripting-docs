---
draft: false
title: "Automatic Vertical Scaling"
aliases: "/automatic-vertical-scaling/"
seoindex: "index, follow"
seotitle: "Automatic Vertical Scaling"
seokeywords: "cloud scripting, vertical scaling, nginx worker_processes, add-on example"
seodesc: "Automatically adjust NGINX worker_processes after vertical scaling."
menu:
    docs:
        title: "Automatic Vertical Scaling"
        url: "/automatic-vertical-scaling/"
        weight: 2
        parent: "samples"
        identifier: "automatic-vertical-scaling"
---

# Automatic Vertical Scaling

An update package (add-on) for an NGINX load balancer that keeps the `worker_processes` setting in line with the CPU cores available to the node.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-vertical-scaling) repository on GitHub.

## How it works

- `type: update` installs the package into an existing environment; `targetNodes` limits the installation to environments with an *nginx* or *nginx-dockerized* node.
- The `adjustWorkersCount` action runs a [cmd](/actions/#cmd) command on the balancer layer (`cmd [bl]`) as *root*: it rewrites `worker_processes` from `/proc/cpuinfo` and reloads NGINX.
- The action is bound to the `onInstall` event and to `onAfterSetCloudletCount`, filtered by node type, so it reruns whenever the cloudlet count changes.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: update

# Optional parameter. If id is not specified it will be generated automatically.
id: automatic-vertical-scaling

# Defines the required name parameter
name: Nginx Balancer Vertical Scaling

homepage: "https://docs.cloudscripting.com/"

# Target Nodes — optional method that defines compatible environments for a JPS update.
# Available only for update installations.
targetNodes:
  nodeType:
    - nginx
    - nginx-dockerized

description:
  short: Automatically adjust NGINX worker_processes after vertical scaling.
  text: |
    Cloud Scripting package for update installations. It recalculates the NGINX worker_processes value
    based on available CPU cores and reloads NGINX after installation and after cloudlet count changes.

# The entry point for executing actions
onInstall: adjustWorkersCount

onAfterSetCloudletCount[nodeType:nginx]: adjustWorkersCount
onAfterSetCloudletCount[nodeType:nginx-dockerized]: adjustWorkersCount

# Actions list
actions:
  adjustWorkersCount:
    "cmd [bl]": "sed -i \"s|worker_processes.*|worker_processes $(cat /proc/cpuinfo | grep -c 'cpu cores');|g\" /etc/nginx/nginx.conf; sudo /etc/init.d/nginx reload 2>&1"
    user: root
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "update",
  "id": "automatic-vertical-scaling",
  "name": "Nginx Balancer Vertical Scaling",
  "homepage": "https://docs.cloudscripting.com/",
  "targetNodes": {
    "nodeType": [
      "nginx",
      "nginx-dockerized"
    ]
  },
  "description": {
    "short": "Automatically adjust NGINX worker_processes after vertical scaling.",
    "text": "Cloud Scripting package for update installations. It recalculates the NGINX worker_processes value\nbased on available CPU cores and reloads NGINX after installation and after cloudlet count changes.\n"
  },
  "onInstall": "adjustWorkersCount",
  "onAfterSetCloudletCount[nodeType:nginx]": "adjustWorkersCount",
  "onAfterSetCloudletCount[nodeType:nginx-dockerized]": "adjustWorkersCount",
  "actions": {
    "adjustWorkersCount": {
      "cmd [bl]": "sed -i \"s|worker_processes.*|worker_processes $(cat /proc/cpuinfo | grep -c 'cpu cores');|g\" /etc/nginx/nginx.conf; sudo /etc/init.d/nginx reload 2>&1",
      "user": "root"
    }
  }
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/automatic-vertical-scaling/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Add-Ons](/addons/)
- [Events](/events/)
- [Specifying Target Container](/selecting-containers/)
- [Samples](/samples/)
