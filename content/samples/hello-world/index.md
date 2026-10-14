---
draft: false
title: "Hello World"
aliases: "/hello-world/"
seoindex: "index, follow"
seotitle: "Hello World"
seokeywords: "cloud scripting, hello world, manifest example, deploy action"
seodesc: "A basic Cloud Scripting package example."
menu:
    docs:
        title: "Hello World"
        url: "/hello-world/"
        weight: 1
        parent: "samples"
        identifier: "hello-world"
---

# Hello World

The smallest useful Cloud Scripting package: an install manifest that provisions one Apache node and deploys an application into it.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/introduction) repository on GitHub.

## How it works

- `type: install` creates a new environment; `nodes` describes it as a single Apache node with 4 cloudlets in the *cp* node group.
- `globals.appSource` keeps the application archive URL in one place, so the manifest references it as `${globals.appSource}`.
- The `onInstall` event runs the [deploy](/actions/#deploy) action, which uploads the archive into the *ROOT* context.
- `success` is the text the dashboard shows when the installation finishes.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

# Optional parameter. If id is not specified it will be generated automatically.
id: introduction-hello-world

# Defines the required name parameter
name: My Cloud Scripting

homepage: "https://docs.cloudscripting.com/"

description:
  short: A basic Cloud Scripting package example.
  text: |
    Provisions an environment with a single Apache node and, on the onInstall event,
    runs the deploy action to deploy the HelloWorld application into the ROOT context.

nodes:
  cloudlets: 4
  count: 1
  nodeGroup: cp
  nodeType: apache

# Global variables for the package.
globals:
  appSource: "https://github.com/jelastic-jps/basic-examples/raw/master/introduction/HelloWorld.zip"

# The entry point for executing actions
onInstall:
  deploy:
    archive: ${globals.appSource}
    name: Hello World
    context: ROOT

# Text displayed upon successful installation either at the Dashboard or via email notification
success: First application deployed successfully!
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "id": "introduction-hello-world",
  "name": "My Cloud Scripting",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "A basic Cloud Scripting package example.",
    "text": "Provisions an environment with a single Apache node and, on the onInstall event,\nruns the deploy action to deploy the HelloWorld application into the ROOT context.\n"
  },
  "nodes": {
    "cloudlets": 4,
    "count": 1,
    "nodeGroup": "cp",
    "nodeType": "apache"
  },
  "globals": {
    "appSource": "https://github.com/jelastic-jps/basic-examples/raw/master/introduction/HelloWorld.zip"
  },
  "onInstall": {
    "deploy": {
      "archive": "${globals.appSource}",
      "name": "Hello World",
      "context": "ROOT"
    }
  },
  "success": "First application deployed successfully!"
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/introduction/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Quick Start](/quick-start/)
- [Basic Configs](/basic-configs/)
- [Actions](/actions/)
- [Events](/events/)
