---
draft: false
title: "Cloud Scripting Overview"
aliases: "/overview/"
seoindex: "index, follow"
seotitle: "Cloud Scripting Overview"
seokeywords: "cloud scripting, cloud scripting overview"
seodesc: "Cloud Scripting (CS) is a tool, designed to program the behaviour of Virtuozzo Application Management related to the application lifecycle for automating"
menu:
    docs:
        title: "Overview"
        url: "/overview/"
        weight: 1
        parent: "getting-started"
        identifier: "overview"
---

# Cloud Scripting Overview
**Cloud Scripting (CS)** is a tool, designed to program the behaviour of Virtuozzo Application Management related to the application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.            

<center><img src="newoverview.svg" alt="newoverview"></center>                                           

There are three main pillars of cloud scripting:

* **Actions** - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to [script custom actions](/custom-scripts/) using [API calls](https://www.virtuozzo.com/application-platform-api-docs/), Linux bash [shell command](/actions/#cmd), JS and Java scripts   
* **Events** - specific [triggers](/events/) for executing actions on a required application lifecycle stage   
* **Injection** - supplying default actions, [placeholders](/placeholders/), platform API methods, environment variables, request parameters and input settings in custom scripts by default

The developed Cloud Scripting solutions are wrapped into packages and distributed through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via [import](https://www.virtuozzo.com/application-platform-docs/environment-import/) functionality.

The example below represents the Cloud Scripting basic use case. This manifest declares the creation of a new environment with the Payara Micro cluster image certified by Virtuozzo Application Management and provides possibility to configure new cluster members while scaling nodes. Within the manifest, the following key parameters are declared:
 
* `nodes` - a environment topology which will be created
* `onAfterScaleIn`, `onAfterScaleOut` - scaling [events](/events/#onafterscalein)            
* `cmd` - action to execute [shell commands](/actions/#cmd)               
* `updateNodes` - custom [action](/actions/#custom-actions)         
* `baseUrl` - external links [relative path](/basic-configs/#relative-links) 

{{< tabs >}}
{{< tabs-item title="YAML" >}}
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
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
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
{{< /tabs-item >}}
{{< /tabs >}}

## What's next?

- Build a simple automation with [Quick Start](/quick-start/) Guide                               
- Learn how to [Create Manifest](/basic-configs/)               
- Explore the list of available [Actions](/actions/)                      
- See the [Events](/events/) list the actions can be bound to                       
- Find out the list of [Placeholders](/placeholders/) for automatic parameters fetching               
- Read how to integrate your [Custom Scripts](/custom-scripts/)                    
- Examine a bunch of [Samples](/samples/) with operation and package examples
