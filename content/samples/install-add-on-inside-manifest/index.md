---
draft: false
title: "Install Add-on within Environment Manifest"
aliases: "/install-add-on-inside-manifest/"
seoindex: "index, follow"
seotitle: "Install Add-on within Environment Manifest"
seokeywords: "cloud scripting, add-on, addons, public ip, setExtIpEnabled, manifest example"
seodesc: "Install an add-on defined inside the manifest."
menu:
    docs:
        title: "Add-on within Manifest"
        url: "/install-add-on-inside-manifest/"
        weight: 5
        parent: "samples"
        identifier: "install-add-on-inside-manifest"
---

# Install Add-on within Environment Manifest

An install manifest that declares an add-on inline and attaches it to a node while the environment is being created. The add-on toggles a public IP address.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/install-add-on-inside-manifest) repository on GitHub.

## How it works

- The Apache node lists `setExtIp` in its `addons` array, so the add-on is installed right after the node is provisioned.
- The top-level `addons` block defines the add-on: its `onInstall` event enables the external IP through [setExtIpEnabled](/actions/#setextipenabled), and `onUnInstall` disables it again.
- After installation the add-on appears in the dashboard's **Add-ons** panel, where **Uninstall** detaches the IP address.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

# Optional parameter. If id is not specified it will be generated automatically.
id: install-add-on-inside-manifest

# Defines the required name parameter
name: example

homepage: "https://docs.cloudscripting.com/"

description:
  short: Install an add-on defined inside the manifest.
  text: |
    Cloud Scripting package that provisions an Apache node and installs the setExtIp add-on.
    Demonstrates add-ons declaration and lifecycle event bindings (onInstall/onUnInstall).

# The infrastructure of the environment.
nodes:
  - nodeType: apache2
    cloudlets: 16
    addons:
      - setExtIp

# Application server/runtime engine
engine: php7.0

addons:
  id: setExtIp
  onInstall: attacheIp
  onUnInstall: deAttacheIp
  actions:
    attacheIp:
      setExtIpEnabled:
        nodeType: apache2
        enabled: true
    deAttacheIp:
      setExtIpEnabled:
        nodeType: apache2
        enabled: false

# Text displayed upon successful installation either at the Dashboard or via email notification
success: Environment with add-on installed successfully!
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "id": "install-add-on-inside-manifest",
  "name": "example",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Install an add-on defined inside the manifest.",
    "text": "Cloud Scripting package that provisions an Apache node and installs the setExtIp add-on.\nDemonstrates add-ons declaration and lifecycle event bindings (onInstall/onUnInstall).\n"
  },
  "nodes": [
    {
      "nodeType": "apache2",
      "cloudlets": 16,
      "addons": [
        "setExtIp"
      ]
    }
  ],
  "engine": "php7.0",
  "addons": {
    "id": "setExtIp",
    "onInstall": "attacheIp",
    "onUnInstall": "deAttacheIp",
    "actions": {
      "attacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": true
        }
      },
      "deAttacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": false
        }
      }
    }
  },
  "success": "Environment with add-on installed successfully!"
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/install-add-on-inside-manifest/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Add-Ons](/addons/)
- [Actions](/actions/)
- [Events](/events/)
- [Samples](/samples/)
