---
draft: false
title: "Subscription Upgrade Flow"
aliases: "/subscriptions/"
seoindex: "index, follow"
seotitle: "Subscription Upgrade Flow"
seokeywords: "cloud scripting, subscriptions, onApplySubscriptionSettings, onBeforeMoveProduct, marketplace, jpsVersion"
seodesc: "Describe subscriptions upgrade flow in Cloud Scripting packages."
menu:
    docs:
        title: "Subscription Upgrade Flow"
        url: "/subscriptions/"
        weight: 8
        parent: "samples"
        identifier: "subscriptions"
---

# Subscription Upgrade Flow

An install manifest for a marketplace product sold by subscription. It shows how a package reacts when the subscription settings change or the product is moved.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/subscriptions) repository on GitHub.

## How it works

- `settings.schema` declares the subscription parameters (cloudlets, disk limit, migration flag) and `settings.fields` renders the installation form for them.
- `onInstall` installs a nested package with the [install](/actions/#install) action and stores its unique name in `globals.installationId` for later calls.
- `onBeforeMoveProduct` stops the move with a warning when the *Migration Disabled* setting is on; `onApplySubscriptionSettings` runs the nested package's `applyEnvSettings` action, which resizes cloudlets and disk limits through the API.
- `jpsVersion: 6.1.1` marks the minimum platform version these events require.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

jpsVersion: 6.1.1

# Optional parameter. If id is not specified it will be generated automatically.
id: subscriptions-upgrade-test-flow

# Defines the required name parameter
name: Describe subscriptions upgrade flow in JPS packages

homepage: "https://docs.cloudscripting.com/"

description:
  short: Describe subscriptions upgrade flow in Cloud Scripting packages.
  text: |
    Demonstrates how subscription settings can be applied to an existing installation by handling
    subscription lifecycle events and executing a custom action to update environment resources.

# Defines user input parameters including simple and UI-based for a JPS installation/update.
settings:
  schema:
    - caption: Cloudlets
      name: cloudlets
    - caption: Disk Limit
      name: diskspace
    - caption: Migration Disabled
      name: migrationDisabled

  fields:
    - caption: Cloudlets
      type: spinner
      name: cloudlets
      default: 8
      max: 32
    - caption: Disk Limit
      type: spinner
      name: diskspace
      default: 30
      max: 100
    - caption: Migration Disabled
      name: migrationDisabled
      type: checkbox
      value: false
    - type: separator
    - type: envname
      name: envName
      caption: Environment
      dependsOn: region
      required: true
    - type: string
      name: displayName
      caption: Display Name
      default: Subscriptions test flow
    - caption: Region
      type: regionlist
      name: region
      disableInactive: true
      selectFirstAvailable: true

# The entry point for executing actions
onInstall:
  - install:
      envName: ${settings.envName}
      region: ${settings.region}
      displayName: ${settings.displayName}

      jps:
        type: install
        name: ${settings.displayName}
        # The infrastructure of the environment.
        nodes:
          nodeType: nginxphp
          nodeGroup: cp
          cloudlets: ${settings.cloudlets}
          diskLimit: ${settings.diskspace}

        # Actions list
        actions:
          applyEnvSettings:
            script: |
              var envs = '${this.targetAppid}'.split(',');
              for (var i=0, n = envs.length; i < n; i++) {
                let targetAppid = envs[i];
                let resp = jelastic.env.control.GetEnvInfo(targetAppid, session);
                if (resp.result != 0) return resp;
                let node = resp.nodes[0];
                if (String(node.flexibleCloudlets) != '${this.cloudlets}') {
                  resp = jelastic.env.control.SetCloudletsCountByGroup({ appid: targetAppid, session: session, nodeGroup: node.nodeGroup, fixedCloudlets: node.fixedCloudlets, flexibleCloudlets: '${this.cloudlets}'});
                  if (resp.result != 0) return resp;
                }
                if (String(node.diskLimit) != '${this.diskspace}') {
                  resp = jelastic.env.control.SetDiskLimitByGroup({ appid: targetAppid, session: session, nodeGroup: node.nodeGroup, limit: '${this.diskspace}' });
                  if (resp.result != 0) return resp;
                }
              }
              return { result: 0 };

  - setGlobals:
      installationId: ${response.uniqueName}

onBeforeMoveProduct:
  if (${settings.migrationDisabled:false}):
    stopEvent:
      type: warning
      message: Migration is prohibited.

onAfterMoveProduct:
  log: onAfterMoveProduct

onApplySubscriptionSettings:
  marketplace.installation.ExecuteAction:
    appUniqueName: ${globals.installationId}
    action: applyEnvSettings
    settings:
      targetAppid: ${event.params.targetAppid}
      cloudlets: ${event.params.settings.cloudlets}
      diskspace: ${event.params.settings.diskspace}000

# Text displayed upon successful installation either at the Dashboard or via email notification
success:
  text: |
    Please use the following data to access!
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "jpsVersion": "6.1.1",
  "id": "subscriptions-upgrade-test-flow",
  "name": "Describe subscriptions upgrade flow in JPS packages",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Describe subscriptions upgrade flow in Cloud Scripting packages.",
    "text": "Demonstrates how subscription settings can be applied to an existing installation by handling\nsubscription lifecycle events and executing a custom action to update environment resources.\n"
  },
  "settings": {
    "schema": [
      {
        "caption": "Cloudlets",
        "name": "cloudlets"
      },
      {
        "caption": "Disk Limit",
        "name": "diskspace"
      },
      {
        "caption": "Migration Disabled",
        "name": "migrationDisabled"
      }
    ],
    "fields": [
      {
        "caption": "Cloudlets",
        "type": "spinner",
        "name": "cloudlets",
        "default": 8,
        "max": 32
      },
      {
        "caption": "Disk Limit",
        "type": "spinner",
        "name": "diskspace",
        "default": 30,
        "max": 100
      },
      {
        "caption": "Migration Disabled",
        "name": "migrationDisabled",
        "type": "checkbox",
        "value": false
      },
      {
        "type": "separator"
      },
      {
        "type": "envname",
        "name": "envName",
        "caption": "Environment",
        "dependsOn": "region",
        "required": true
      },
      {
        "type": "string",
        "name": "displayName",
        "caption": "Display Name",
        "default": "Subscriptions test flow"
      },
      {
        "caption": "Region",
        "type": "regionlist",
        "name": "region",
        "disableInactive": true,
        "selectFirstAvailable": true
      }
    ]
  },
  "onInstall": [
    {
      "install": {
        "envName": "${settings.envName}",
        "region": "${settings.region}",
        "displayName": "${settings.displayName}",
        "jps": {
          "type": "install",
          "name": "${settings.displayName}",
          "nodes": {
            "nodeType": "nginxphp",
            "nodeGroup": "cp",
            "cloudlets": "${settings.cloudlets}",
            "diskLimit": "${settings.diskspace}"
          },
          "actions": {
            "applyEnvSettings": {
              "script": "var envs = '${this.targetAppid}'.split(',');\nfor (var i=0, n = envs.length; i < n; i++) {\n  let targetAppid = envs[i];\n  let resp = jelastic.env.control.GetEnvInfo(targetAppid, session);\n  if (resp.result != 0) return resp;\n  let node = resp.nodes[0];\n  if (String(node.flexibleCloudlets) != '${this.cloudlets}') {\n    resp = jelastic.env.control.SetCloudletsCountByGroup({ appid: targetAppid, session: session, nodeGroup: node.nodeGroup, fixedCloudlets: node.fixedCloudlets, flexibleCloudlets: '${this.cloudlets}'});\n    if (resp.result != 0) return resp;\n  }\n  if (String(node.diskLimit) != '${this.diskspace}') {\n    resp = jelastic.env.control.SetDiskLimitByGroup({ appid: targetAppid, session: session, nodeGroup: node.nodeGroup, limit: '${this.diskspace}' });\n    if (resp.result != 0) return resp;\n  }\n}\nreturn { result: 0 };\n"
            }
          }
        }
      }
    },
    {
      "setGlobals": {
        "installationId": "${response.uniqueName}"
      }
    }
  ],
  "onBeforeMoveProduct": {
    "if (${settings.migrationDisabled:false})": {
      "stopEvent": {
        "type": "warning",
        "message": "Migration is prohibited."
      }
    }
  },
  "onAfterMoveProduct": {
    "log": "onAfterMoveProduct"
  },
  "onApplySubscriptionSettings": {
    "marketplace.installation.ExecuteAction": {
      "appUniqueName": "${globals.installationId}",
      "action": "applyEnvSettings",
      "settings": {
        "targetAppid": "${event.params.targetAppid}",
        "cloudlets": "${event.params.settings.cloudlets}",
        "diskspace": "${event.params.settings.diskspace}000"
      }
    }
  },
  "success": {
    "text": "Please use the following data to access!"
  }
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/subscriptions/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Events](/events/)
- [Visual Settings](/visual-settings/)
- [Custom Scripts](/custom-scripts/)
- [Samples](/samples/)
