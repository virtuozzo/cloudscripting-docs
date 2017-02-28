<h1>Cloud Scripting Overview</h1>

Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour related to your application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.            

<center>![newoverview](/img/newoverview.png)</center>                                           

There are three main pillars of cloud scripting:

* **Actions** - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">script custom actions</a> using <a href="https://docs.jelastic.com/api/" target="_blank">API calls</a>, Linux bash <a href="/reference/actions/#cmd" target="_blank">shell command</a>, JS and Java scripts   

* **Events** - specific <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">triggers</a> for executing actions on a required application lifecycle stage   
  
* **Injection** - supplying default actions, <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">placeholders</a>, platform API methods, environment variables, request parameters and input settings in custom scripts by default

<p dir="ltr" style="text-align: justify;">The developed Cloud Scripting solutions are wrapped into packages and distributed with Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). This is accomplished through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.</p>

<p dir="ltr" style="text-align: justify;">The example below represents the Cloud Scripting basic use case. This manifest declares the creation of a new environment with the Jelastic-certified Payara Micro cluster image and provides possibility to configure new cluster members while scaling nodes. Within the manifest, the following <a href="http://docs.cloudscripting.com/reference/actions/" target="blank">actions</a> execution is predefined:</p>             
 
* `cmd` - action to execute <a href="/reference/actions/#cmd" target="blank">shell commands</a>               

* `forEach` - iteration <a href="/creating-templates/conditions-and-iterations/#by-all-nodes" target="blank">object</a>        

* `addClusterMembers` - user-defined <a href="/reference/actions/#custom-actions" target="blank">custom action</a>         

* `onAfterScaleIn, onBeforeServiceScaleOut` - scaling <a href="/reference/events/#onafterscalein" target="blank">events</a>            

```json
{
  "type": "install",
  "name": "Simple Payara Micro Cluster",
  "nodes": [
    {
      "cloudlets": 16,
      "nodeGroup": "cp",
      "image": "jelastic/payara-micro-cluster",
      "env": {
        "HAZELCAST_GROUP": "CHANGE_ME",
        "HAZELCAST_PASSWORD": "CHANGE_ME",
        "VERT_SCALING": "true"
      },
      "volumes": [
        "/opt/payara/deployments",
        "/opt/payara/config",
        "/var/log"
      ]
    }
  ],
  "onBeforeServiceScaleOut[nodeGroup:cp]": "addClusterMembers",
  "onAfterScaleIn[nodeGroup:cp]": {
    "forEach(event.response.nodes)": {
      "cmd [cp]": "$PAYARA_PATH/bin/clusterManager.sh --removehost ${@i.intIP}"
    }
  },
  "onInstall": "addClusterMembers",
  "actions": {
    "addClusterMembers": {
      "forEach(nodes.cp)": {
        "cmd [cp]": "$PAYARA_PATH/bin/clusterManager.sh --addhost ${@i.intIP}"
      }
    }
  }
}
```


<h2>What’s next?</h2>

* Build a simple automation with <a href="http://docs.cloudscripting.com/quick-start/" target="_blank">Quick Start</a> Guide                               
* Learn how to <a href="http://docs.cloudscripting.com/creating-templates/basic-configs/" target="_blank">Create Manifest</a>   
* Explore the list of available <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a>    
* See the <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">Events</a> list the actions can be bound to    
* Find out the list of <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching  
* Read how to integrate your <a href="http://docs.cloudscripting.com/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a>         
* Examine a bunch of <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> with operation and package examples                                                   
