<h1>Cloud Scripting Overview</h1>

Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour throughout applications lifecycle for automating frequent DevOps tasks, complex CI/CD flows and clustering configurations.            

<center>![newoverview](/img/newoverview.png)</center>                                           

There are three main pillars of cloud scripting:

* **Actions** - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="/creating-manifest/custom-scripts/" target="_blank">script custom actions</a> using Linux shell command, JavaScript and Java snippets, and API calls                                  

* **Events** - specific triggers for executing actions on a required application lifecycle stage such as start, deploy, scale, update and others. There is a wide range of application events, some of them are listed <a href="/creating-manifest/events/" target="_blank">here</a>                                                           
  
* **Injection** - supplying default actions, environment variables, <a href="/creating-manifest/placeholders/" target="_blank">placeholders</a>, API methods, request parameters and input settings in custom scripts by default                                    

<p dir="ltr" style="text-align: justify;">The developed Cloud Scripting solutions are wrapped into packages and distributed with Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). This is accomplished through preparing a manifest file in JSON or YAML format. Such packaged solutions can be effortlessly deployed to the platform via <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.</p>

<h2>Areas to Use</h2>                     

* Provisioning of clustered environment topologies from simple blueprints                                                  

* One click deploy with zero downtime re-deployment                                              

* Multi-cloud deployment scenarios                               

* Automating scaling up and down, in and out                                 

* Continuous Integration and Continuous Deployment                         

* Automating management of Docker containers                             

* Health checking and alerting about application issues                            

* Custom integration with 3d party services and tools (GitHub, SendGrid, cPanel etc)                                 

* Automated data replication, backup and disaster recovery                                                     

<h2>Example</h2>                  

<p dir="ltr" style="text-align: justify;">The example below represents the Cloud Scripting basic use case. This manifest declares creation of an environment with Jelastic-certified Payara Micro Cluster, run inside Docker containers. It is provisioned with the embedded possibility to automatically scale in/out based on the incoming load and implements auto-detection of changing application servers number to adjust load balancing configs correspondingly. Within the manifest, the following key parameters are used:</p>  
 
* `onAfterScaleIn`, `onBeforeServiceScaleOut` - scaling <a href="/creating-manifest/events/#onafterscalein" target="blank">events</a>               

* `addClusterMembers` - custom <a href="/creating-manifest/actions/#custom-actions" target="blank">action</a>                 

* `forEach` - iteration <a href="/creating-manifest/conditions-and-iterations/#foreach" target="blank">object</a>              

* `cmd` - action to execute <a href="/creating-manifest/actions/#cmd" target="blank">shell commands</a>                            

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
<br>       
<h2>What’s next?</h2>

- Build a simple automation with <a href="/quick-start/" target="_blank">Quick Start</a> Guide                               
 
- Learn how to <a href="/creating-manifest/basic-configs/" target="_blank">Create Manifest</a>               
 
- Explore the list of available <a href="/creating-manifest/actions/" target="_blank">Actions</a>                      
 
- See the <a href="/creating-manifest/events/" target="_blank">Events</a> list the actions can be bound to                       
  
- Find out the list of <a href="/creating-manifest/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching               
 
- Read how to integrate your <a href="/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>                    

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples                                                    
