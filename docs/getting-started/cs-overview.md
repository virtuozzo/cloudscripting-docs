# Cloud Scripting Overview

**Cloud Scripting (CS)** is a tool designed to program the behavior of Virtuozzo Application Platform related to the application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.

<center>![newoverview](/img/newoverview.svg)</center>

There are three main pillars of cloud scripting:

- **Actions** - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and the ability to [script custom actions](/creating-manifest/custom-scripts/) using [API calls](https://www.virtuozzo.com/application-platform-api-docs/), Linux bash [shell command](/creating-manifest/actions/#cmd), JS and Java scripts
- **Events** - specific [triggers](/creating-manifest/events/) for executing actions on a required application lifecycle stage
- **Injection** - supplying default actions, [placeholders](/creating-manifest/placeholders/), platform API methods, environment variables, request parameters and input settings in custom scripts by default

The developed Cloud Scripting solutions are wrapped into packages and distributed through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via [import](https://www.virtuozzo.com/application-platform-docs/environment-import/) functionality.

The example below represents the Cloud Scripting basic use case. This manifest declares the creation of a new environment with the Payara Micro cluster image certified by Virtuozzo Application Platform and provides the ability to configure new cluster members while scaling nodes. Within the manifest, the following key parameters are declared:

- `nodes` - an environment topology which will be created
- `onAfterScaleIn`, `onAfterScaleOut` - scaling [events](/creating-manifest/events/#onafterscalein)
- `cmd` - action to execute [shell commands](/creating-manifest/actions/#cmd)
- `updateNodes` - custom [action](/creating-manifest/actions/#custom-actions)
- `baseUrl` - external links [relative path](/creating-manifest/basic-configs/#relative-links)

@@@
```yaml
type: install
name: Advanced Payara Micro Cluster
baseUrl: https://github.com/jelastic-jps/payara/raw/master/addons

nodes:
  count: 1
  cloudlets: 16
  nodeGroup: cp
  image: jelastic/payara-micro-cluster
  env:
    HAZELCAST_GROUP: ${fn.uuid}
    HAZELCAST_PASSWORD: ${fn.password}
  volumes:
    - /opt/payara/deployments
    - /opt/payara/config
    - /var/log

onInstall:
  - forEach(nodes.cp):
      updateNodes:
        option: add
        ip: ${@i.intIP}
  - install: ${baseUrl}/application-storage/manifest.jps

onAfterScaleOut[cp]:
  forEach(event.response.nodes):
    updateNodes:
      option: add
      ip: ${@i.intIP}

onAfterScaleIn[cp]:
  forEach(event.response.nodes):
    updateNodes:
      option: remove
      ip: ${@i.intIP}

actions:
 updateNodes:
   cmd[cp]: $PAYARA_PATH/bin/clusterManager.sh --${this.option}host ${this.ip}

description: |
  Example: The package automatically provisions Payara Micro cluster,
  mounts storage container and deploys test war applications.

success: https://github.com/jelastic-jps/payara/blob/master/payara-micro-cluster-advanced/scripts/successText.md

logo: https://raw.githubusercontent.com/jelastic-jps/payara/master/images/70.png
homepage: http://docs.cloudscripting.com/
```
```json
{
  "type": "install",
  "name": "Advanced Payara Micro Cluster",
  "nodes": [{
    "count": 1,
    "cloudlets": 16,
    "nodeGroup": "cp",
    "image": "jelastic/payara-micro-cluster",
    "env": {
      "HAZELCAST_GROUP": "${fn.uuid}",
      "HAZELCAST_PASSWORD": "${fn.password}"
    },
    "volumes": [
      "/opt/payara/deployments",
      "/opt/payara/config",
      "/var/log"
    ]
  }],
  "onInstall": [
    {
      "forEach(nodes.cp)": {
        "updateNodes": {
          "option": "add",
          "ip": "${@i.intIP}"
        }
      }
    },
    {
      "install": "${baseUrl}/application-storage/manifest.jps"
    }
  ],
  "onAfterScaleOut[cp]": {
    "forEach(event.response.nodes)": {
      "updateNodes": {
        "option": "add",
        "ip": "${@i.intIP}"
      }
    }
  },
  "onAfterScaleIn[cp]": {
    "forEach(event.response.nodes)": {
      "updateNodes": {
        "option": "remove",
        "ip": "${@i.intIP}"
      }
    }
  },
  "actions": {
    "updateNodes": {
      "cmd[cp]": "$PAYARA_PATH/bin/clusterManager.sh --${this.option}host ${this.ip}"
    }
  },
  "success": "https://github.com/jelastic-jps/payara/blob/master/payara-micro-cluster-advanced/scripts/successText.md",
  "baseUrl": "https://github.com/jelastic-jps/payara/raw/master/addons",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/payara/master/images/70.png",
  "description": "Example: The package automatically provisions Payara Micro cluster, mounts storage container and deploys test war applications.",
  "homepage": "http://docs.cloudscripting.com/"
}
```
@@!

## What's next?

- Build a simple automation with [Quick Start](/getting-started/quick-start/) Guide
- Learn how to [Create Manifest](/creating-manifest/basic-configs/)
- Explore the list of available [Actions](/creating-manifest/actions/)
- See the [Events](/creating-manifest/events/) list the actions can be bound to
- Find out the list of [Placeholders](/creating-manifest/placeholders/) for automatic parameters fetching
- Read how to integrate your [Custom Scripts](/creating-manifest/custom-scripts/)
- Examine a bunch of [Samples](/samples/) with operation and package examples
