<h1>Cloud Scripting Overview</h1>

Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour related to your application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.            

<center>![newoverview](/img/newoverview.png)</center>                                           

There are three main pillars of cloud scripting:

* **Actions** - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">script custom actions</a> using <a href="https://docs.jelastic.com/api/" target="_blank">API calls</a>, Linux bash <a href="/1.6/creating-manifest/actions/#cmd" target="_blank">shell command</a>, JS and Java scripts   

* **Events** - specific <a href="/1.6/creating-manifest/events/" target="_blank">triggers</a> for executing actions on a required application lifecycle stage   
  
* **Injection** - supplying default actions, <a href="/1.6/creating-manifest/placeholders/" target="_blank">placeholders</a>, platform API methods, environment variables, request parameters and input settings in custom scripts by default

<p dir="ltr" style="text-align: justify;">The developed Cloud Scripting solutions are wrapped into packages and distributed with Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). This is accomplished through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.</p>

<p dir="ltr" style="text-align: justify;">The example below represents the Cloud Scripting basic use case. This manifest declares the creation of a new environment with the Jelastic-certified Payara Micro cluster image and provides possibility to configure new cluster members while scaling nodes. Within the manifest, the following key parameters are declared:</p>
 
* `nodes` - a environment topology which will be created

* `onAfterScaleIn`, `onAfterScaleOut` - scaling <a href="/1.6/creating-manifest/events/#onafterscalein" target="blank">events</a>            

* `cmd` - action to execute <a href="/1.6/creating-manifest/actions/#cmd" target="blank">shell commands</a>               

* `updateNodes` - custom <a href="/1.6/creating-manifest/actions/#custom-actions" target="blank">action</a>         
* `baseUrl` - external links <a href="/1.6/creating-manifest/basic-configs/#relative-links" target="_blank">relative path</a> 

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
<br>       
<h2> What’s next?</h2>

- Build a simple automation with <a href="/quick-start/" target="_blank">Quick Start</a> Guide                               
 
- Learn how to <a href="/1.6/creating-manifest/basic-configs/" target="_blank">Create Manifest</a>               
 
- Explore the list of available <a href="/1.6/creating-manifest/actions/" target="_blank">Actions</a>                      
 
- See the <a href="/1.6/creating-manifest/events/" target="_blank">Events</a> list the actions can be bound to                       
  
- Find out the list of <a href="/1.6/creating-manifest/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching               
 
- Read how to integrate your <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>                    

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples                                                    
