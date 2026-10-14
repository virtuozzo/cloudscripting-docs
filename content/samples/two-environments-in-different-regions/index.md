---
draft: false
title: "Create Two Environments in Different Regions"
aliases: "/two-environments-in-different-regions/"
seoindex: "index, follow"
seotitle: "Create Two Environments in Different Regions"
seokeywords: "cloud scripting, regions, CreateEnvironment, script action, multi-region example"
seodesc: "Create two environments from a single package in different regions."
menu:
    docs:
        title: "Two Environments in Regions"
        url: "/two-environments-in-different-regions/"
        weight: 6
        parent: "samples"
        identifier: "two-environments-in-different-regions"
---

# Create Two Environments in Different Regions

An install manifest that creates its own environment in one region and, from the `onInstall` event, provisions a second identical environment in another region through the platform API.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/two-environments-from-one-jps-in-diff-regions) repository on GitHub.

## How it works

- `region` selects the region for the environment described by `nodes`.
- The `onInstall` script calls `env.control.CreateEnvironment` with a generated environment name and a second region.
- Region identifiers (`default_hn_group`, `default_hn2_group`) are platform specific; replace them with the regions available at your hosting provider before running the sample.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

# Optional parameter. If id is not specified it will be generated automatically.
id: two-environments-from-one-jps-in-diff-regions

# Defines the required name parameter
name: 2Envs

homepage: "https://docs.cloudscripting.com/"

description:
  short: Create two environments from a single package in different regions.
  text: |
    Cloud Scripting package that creates the first environment in the specified region and,
    on the onInstall event, runs a script that provisions a second environment in another region.

# The infrastructure of the environment.
nodes:
  - cloudlets: 16
    nodeType: nginxphp

# Target region
region: default_hn_group

# The entry point for executing actions
onInstall:
  script: "https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/two-environments-from-one-jps-in-diff-regions/scripts/createSecondEnvironment.js"
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "id": "two-environments-from-one-jps-in-diff-regions",
  "name": "2Envs",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Create two environments from a single package in different regions.",
    "text": "Cloud Scripting package that creates the first environment in the specified region and,\non the onInstall event, runs a script that provisions a second environment in another region.\n"
  },
  "nodes": [
    {
      "cloudlets": 16,
      "nodeType": "nginxphp"
    }
  ],
  "region": "default_hn_group",
  "onInstall": {
    "script": "https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/two-environments-from-one-jps-in-diff-regions/scripts/createSecondEnvironment.js"
  }
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Script: createSecondEnvironment.js

The `script` action downloads [createSecondEnvironment.js](https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/two-environments-from-one-jps-in-diff-regions/scripts/createSecondEnvironment.js) at installation time:

```javascript
var sAppid = getParam("TARGET_APPID"),
    sSession = getParam("session"),
    sRegion = "default_hn2_group",
    sEnvGeneratedName = generateEnvName(),
    oNodes = [{
        "nodeType": "nginxphp",
        "flexibleCloudlets": 10
    }],
    oEnv = {
        "region": sRegion,
        "shortdomain": sEnvGeneratedName
    },
    sActionkey = "createenv;" + sEnvGeneratedName;

function generateEnvName(sPrefix) {
    sPrefix = sPrefix || "env-";

    return sPrefix + parseInt(Math.random() * 100000, 10);
}

return jelastic.env.control.CreateEnvironment(sAppid, sSession, sActionkey, oEnv, oNodes);
```

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/two-environments-from-one-jps-in-diff-regions/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Custom Scripts](/custom-scripts/)
- [Basic Configs](/basic-configs/)
- [Samples](/samples/)
