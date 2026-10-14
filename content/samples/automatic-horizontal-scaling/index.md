---
draft: false
title: "Automatic Horizontal Scaling"
aliases: "/automatic-horizontal-scaling/"
seoindex: "index, follow"
seotitle: "Automatic Horizontal Scaling"
seokeywords: "cloud scripting, horizontal scaling, triggers, script action, add-on example"
seodesc: "Enable horizontal autoscaling for a target node group."
menu:
    docs:
        title: "Automatic Horizontal Scaling"
        url: "/automatic-horizontal-scaling/"
        weight: 3
        parent: "samples"
        identifier: "automatic-horizontal-scaling"
---

# Automatic Horizontal Scaling

An update package that enables automatic horizontal scaling for the compute layer of an existing environment by creating load triggers through the platform API.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-horizontal-scaling) repository on GitHub.

## How it works

- `targetNodes.nodeGroup: cp` makes the package installable only into environments that have a *cp* node group.
- The `onInstall` event runs a JavaScript file fetched from the repository with the [script](/actions/#script) action.
- The script reads the account quota for the maximum number of nodes, removes any existing *ADD_NODE* and *REMOVE_NODE* triggers, and creates two new ones: add a node when CPU load stays above 80% for 5 minutes, remove one when it stays below 5% for 15 minutes.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: update

# Optional parameter. If id is not specified it will be generated automatically.
id: automatic-horizontal-scaling

# Defines the required name parameter
name: Compute Nodes Horizontal Scaling

homepage: "https://docs.cloudscripting.com/"

description:
  short: Enable horizontal autoscaling for a target node group.
  text: |
    Cloud Scripting package that runs on install and enables automatic horizontal scaling
    for the selected targetNodes node group.

# Target Nodes — optional method that defines compatible environments for a JPS update.
# Available only for update installations.
targetNodes:
  nodeGroup:
    - cp

# The entry point for executing actions
onInstall:
  script: "https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/automatic-horizontal-scaling/scripts/enableAutoScaling.js"
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "update",
  "id": "automatic-horizontal-scaling",
  "name": "Compute Nodes Horizontal Scaling",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Enable horizontal autoscaling for a target node group.",
    "text": "Cloud Scripting package that runs on install and enables automatic horizontal scaling\nfor the selected targetNodes node group.\n"
  },
  "targetNodes": {
    "nodeGroup": [
      "cp"
    ]
  },
  "onInstall": {
    "script": "https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/automatic-horizontal-scaling/scripts/enableAutoScaling.js"
  }
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Script: enableAutoScaling.js

The `script` action downloads [enableAutoScaling.js](https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/automatic-horizontal-scaling/scripts/enableAutoScaling.js) at installation time:

```javascript
var APPID = getParam("TARGET_APPID"),
    QUOTA_MAX_NODES = "environment.maxsamenodescount",
    VALUE_TYPE = "PERCENTAGES",
    RESOURCE_TYPE = "CPU",
    NODE_GROUP = "cp",
    oTriggerActions,
    nMaxNodesCount,
    oRespTurnOn,
    aQuotas,
    oData,
    oResp;
    
    oTriggerActions = {
        add: "ADD_NODE",
        remove: "REMOVE_NODE"
    };

oResp = jelastic.billing.account.GetQuotas(appid, session);

if (oResp.result != 0) {
    return oResp;
}

aQuotas = oResp.array;

for (var i = 0, n = aQuotas.length; i < n; i += 1) {

    if (aQuotas[i].quota && aQuotas[i].quota.name == QUOTA_MAX_NODES) {
        nMaxNodesCount = aQuotas[i].value;
        break;
    }
}

oResp = jelastic.env.trigger.GetTriggers(APPID, session, oTriggerActions.add);

if (oResp.array.length > 0) {
    oResp = jelastic.env.trigger.DeleteTrigger(APPID, session, oResp.array[0].id);
}

oData = {
    isEnabled: true,
    name: "hs-add",
    nodeGroup: NODE_GROUP,
    period: 5,
    condition: {
        type: "GREATER",
        value: 80,
        resourceType: RESOURCE_TYPE,
        valueType: VALUE_TYPE
    },
    actions: [
        {
            type: oTriggerActions.add,
            customData: {
                limit: nMaxNodesCount || 3,
                count: 1,
                notify: false
            }
        }
    ]
};

oRespTurnOn = jelastic.env.trigger.AddTrigger(APPID, session, oData);

if (oRespTurnOn.result != 0) {
    return oRespTurnOn;
}


oResp = jelastic.env.trigger.GetTriggers(APPID, session, oTriggerActions.remove);

if (oResp.array.length > 0) {
    oResp = jelastic.env.trigger.DeleteTrigger(APPID, session, oResp.array[0].id);
}

oData = {
    isEnabled: true,
    name: "hs-remove",
    nodeGroup: NODE_GROUP,
    period: 15,
    condition: {
        type: "LESS",
        value: 5,
        resourceType: RESOURCE_TYPE,
        valueType: VALUE_TYPE
    },
    actions: [
        {
            type: oTriggerActions.remove,
            customData: {
                limit: 2,
                count: 1,
                notify: false
            }
        }
    ]
};

oRespTurnOff = jelastic.env.trigger.AddTrigger(APPID, session, oData);

return oRespTurnOff;
```

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/automatic-horizontal-scaling/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Custom Scripts](/custom-scripts/)
- [Actions](/actions/)
- [Placeholders](/placeholders/)
- [Samples](/samples/)
