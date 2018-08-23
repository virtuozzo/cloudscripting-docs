# Events

Any <a href="/creating-manifest/actions/" target="_blank">action</a>, available to be performed by means of <a href="https://docs.jelastic.com/api/" target="_blank">API</a> (including <a href="/creating-manifest/custom-scripts/" target="_blank">custom scripts</a> running), should be bound to some event and executed as a result of this event occurrence.
Each event triggers a particular action on the required application's lifecycle stage. The entry point for executing any action is the [*onInstall*](#oninstall) event.                                  

## Events Execution Rules    

- Such events as *onBeforeDelete* and *onAfterDelete* (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.                              

- The scaling events (*onBeforeScaleOut/onAfterScaleOut*, *onBeforeScaleIn/onAfterScaleIn*, *onBeforeServiceScaleOut/onAfterServiceScaleOut*, *onBeforeSetCloudletCount/onAfterSetCloudletCount*) are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.                                         

- For application server, load balancer and VPS node layers, the *onBeforeCloneNodes/onAfterCloneNodes* events are executed each time the node group is scaled out.                             

- The *onBeforeLinkNodes/onAfterLinkNodes*, *onBeforeUnlinkNodes/onAfterUnlinkNodes*, *onBeforeSetEnvVars/onAfterSetEnvVars*, *onBeforeSetEntryPoint/onAfterSetEntryPoint*, *onBeforeSetRunCmd/onAfterSetRunCmd*, *onBeforeAddVolume/onAfterAddVolume* and *onBeforeRemoveVolume/onAfterRemoveVolume* events can be executed only once per a single *changeTopology* action.                 

- The *onBeforeStartService/onAfterStartService* event can be called only once while performing the *changeTopology* and *createEnvironment* actions.                                      

## Events Filtering

Events can be filtered by any input parameters. As a result, the action is executed only when the called event matches specified filtering rules. Parameter name (e.g. *myalert*) can be specified via a colon: **onAlert [name:myalert]**. Input parameters list is described for every [event](https://docs.cloudscripting.com/creating-manifest/events/#event-list) within **${event.params.}**. Also, it is possible to filter events with comma-separated list of the parameters (**onBeforeRedeployContainer [nodeGroup:cp, sequential:true, useExistingVolumes:true]**). 
In case the parameter name is not specified via colon, engine tries to determine parameter as a [*nodeID*](https://docs.cloudscripting.com/creating-manifest/selecting-containers/#particular-container), if it’s not possible, then it tries to determine a [*nodeGroup*](https://docs.cloudscripting.com/creating-manifest/selecting-containers/#all-containers-by-group), if it’s not possible, after that it tries to determine a [*nodeType*](https://docs.cloudscripting.com/creating-manifest/selecting-containers/#all-containers-by-type). Finally, if no filtering rules are specified, no event triggers.

The following example describes the events filtering by *nodeGroup* (for the <b>*onAfterScaleOut*</b> event), *nodeType* (for the <b>*onAfterRestartNode*</b> event), and *nodeId* (for the <b>*onAfterResetNodePassword*</b> event). Here, filtering by the compute node group (*[cp]*) is set so that the action is executed after compute nodes are scaled out. The *nodeType* filtering is set so that the action is executed after **Apache 2** nodes are restarted. The *nodeID* filtering is set so that the action is executed after a password from the first compute node in the layer is reset.
@@@
```yaml
type: update
name: Event Subscription Example

onInstall:
  createFile [cp]: /tmp/result.txt

onAfterScaleOut [cp]:
  cmd [cp]: echo 'New Compute node has been added' >> /tmp/result.txt

onAfterRestartNode [apache2]:
  cmd [cp]: echo 'Compute node with ID - ${events.response.nodeid} has been restarted' >> /tmp/result.txt

onAfterResetNodePassword [${nodes.cp[0].id}]:
  cmd [${nodes.cp[0].id}]: echo 'First compute node has been restarted' >> /tmp/result.txt
```
``` json
{
  "type": "update",
  "name": "Event Subscription Example",
  "onInstall": {
    "createFile [cp]": "/tmp/result.txt"
  },
  "onAfterScaleOut [cp]": {
    "cmd [cp]": "echo 'New Compute node has been added' >> /tmp/result.txt"
  },
  "onAfterRestartNode [apache2]": {
    "cmd [cp]": "echo 'Compute node with ID - ${events.response.nodeid} has been restarted' >> /tmp/result.txt"
  },
  "onAfterResetNodePassword [${nodes.cp[0].id}]": {
    "cmd [${nodes.cp[0].id}]": "echo 'First compute node has been restarted' >> /tmp/result.txt"
  }
}
```
@@!

where:

- `type` - *update* type presupposes the add-on installation to the existing environment with the predefined listeners for events                                
- `onInstall` - entry point for executing actions                                                                     
    - `cp` - target node group                                  
- `onAfterScaleOut` - event that triggers the action after adding a new compute node                                           
- `onAfterRestartNode` - event that triggers the action after restarting *apache2* compute nodes     
- `onAfterResetNodePassword` - event that triggers the action after resetting a password from the first compute node in the layer       

## Events Execution Sequence

Below you can find the graphs that list actions with adjoining events. Every action has a pair of adjoining events - one of them is executed *before* the action and another one is launched *after* the action, that is when the action is finished.  

!!! note
    The <b>*createEnvironment*</b> action does not have any adjoining events, because events are bound after the environment creation.      
 
The <b>*changeTopology*</b> actions are considered quite time-consuming while being performed via the Jelastic dashboard, therefore, you can automate their workflow with the following CS actions and related events.                                            

<center><img style="height: 900px; padding-right: 69px"  src="/img/changeTopologySequence.png" alt="change topology sequence icon" /></center>

Another demanded actions are related to scaling procedures. The following graph provides a sequence of scaling actions and related events.                     

<center><img style="height: 626px"  src="/img/scalingEventSequence.png" alt="scaling sequence icon" /></center>

## Event List

### onInstall

The <b>*onInstall*</b> event is the entry point for executing any action. If the installation type is *install*, the <b>*onInstall*</b> event is triggered right after the environment creation. If the installation type is *update*, <b>*onInstall*</b> is the first event that is performed during the manifest installation.                          
 
### onUninstall

The <b>*onUninstall*</b> event can be called from the **Add-ons** tab at the Jelastic dashboard. This event is aimed at removing data accumulated through actions that are triggered by the <b>*onInstall*</b> event.                     
  
![uninstall](/img/uninstall.png)    

### onBeforeChangeTopology

The event is executed before changing environment topology via the Jelastic dashboard.

**Event Placeholders:**      

- `${event.params.}`:
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `nodes` - nodes array with detailed info about the topology change                                 
    - `env` - environment settings, e.g. *engine, ssl, ha,* etc 
- `${event.response.}` parameters are absent        

### onAfterChangeTopology

The event is executed once the *changeTopology* action is finished.     

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `domain` - cloned environment name    
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0"*.        
    - `nodeGroups` - node delays:     
        - `restartNodeDelay` - delay for restart    
        - `name` - node group name    
        - `redeployContainerDelay` - delay for container redeployment        
        - `redeployContextDelay` - delay for context redeployment          
        - `restartContainerDelay` - delay for container restart         
    - `nodes` - nodes array with detailed info about the topology change. Explore the full list of available <a href="/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.         
    - `env` - environment information. Explore the full list of available <a href="/creating-manifest/placeholders/#environment-placeholders" target="_blank">environment placeholders</a>.        

### onBeforeScaleOut

The event is executed before adding new node(s) (i.e. scaling *out*) to the existing node group (layer). Scaling in/out can be performed either through <a href="https://docs.jelastic.com/jelastic-dashboard-guide#change-topology" target="_blank">changing topology</a> or <a href="https://docs.jelastic.com/automatic-horizontal-scaling" target="_blank">auto horizontal scaling</a> functionality. The *onBeforeScaleOut* event is run once for each layer upon any node count change.                      

**Event Placeholders:**    

- `${event.params.}`: 
    - `count` - number of nodes that are added     
    - `nodeGroup` - node group that is scaled out       
- `${event.response.}` parameters are absent        

### onAfterScaleOut

The event is executed after adding new node(s) to the existing node group. The *onAfterScaleOut* event is run once for each layer upon any node count change.                       

**Event Placeholders:**  
 
- `${event.params.}`:   
    - `count` - number of nodes that are added      
    - `nodeGroup` - node group that is scaled out     
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.                                

### onBeforeScaleIn

The event is executed before removing node(s) (i.e. scaling *in*) from the target node group. The *onBeforeScaleIn* event is run once for each layer upon any node count change.          

**Event Placeholders:**   
 
- `${event.params.}`:
    - `count` - number of nodes that are removed    
    - `nodeGroup` - node group that is scaled in   
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.                              

### onAfterScaleIn

The event is executed after scaling *in* the corresponding node group. The *onAfterScaleIn* event is run once for each layer upon any node count change.                            

**Event Placeholders:**     

- `${event.params.}`:   
    - `count` - number of nodes that are removed       
    - `nodeGroup` - node group that is scaled in      
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.                                

### onBeforeServiceScaleOut

The event is executed before adding new Docker container(s) to the existing node group. It is run once for each layer upon any node count change. The *onBeforeServiceScaleOut* event is applicable only for Docker containers.      

**Event Placeholders:**    

- `${event.params.}`:     
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeId` - node identifier where event is executed     
- `${event.response.}` parameters are absent       

### onAfterServiceScaleOut

The event is executed after adding new Docker container(s) to the existing node group. It is run once for each layer upon any node count change. The *onAfterServiceScaleOut* event is applicable only for Docker containers.     

**Event Placeholders:**    

- `${event.params.}`:    
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `nodeId` - node identifier where event is executed       
- `${event.response.}` result code. The successful action result is *'0'*.           

### onAlert
This event provides a possibility to bind actions to <a href="https://docs.jelastic.com/load-alerts" target="_blank">Load Alerts</a> and <a href="https://docs.jelastic.com/automatic-horizontal-scaling" target="_blank">Automatic Horizontal Scaling Alerts</a> that are configured through the Jelastic triggers.   

These monitoring triggers are based on the usage of the following resource types:            

- **CLOUDLETS** (CPU, Memory) - available only for the *NOTIFY* action type                                                   

- **CPU**                    

- **MEM** (Memory)                      

- **NET_EXT** - external output and input traffic that are available only for the *NOTIFY* action type                                      

- **NET_EXT_OUT** - external output traffic                         

- **DISK** - disk space amount that is available only for the *NOTIFY* action type                                     

- **INODES** - available only for the *NOTIFY* action type                                                                    

- **Disk I/O** - disk input/output rate                                                                                                   

- **Disk IOPS** - disk input/output rate (in operations per second)                                                            

The units of measurement are *PERCENTAGE* and *SPECIFIC*. The second value is available only for **NET_EXT** and **NET_EXT_OUT** resource types.

The following example illustrates the subscription to the *onAlert* event. Here, the *log* action is executed if one of the triggers within the compute (*[cp]*) layer is invoked.
@@@
```yaml
type: update
name: AddTrigger

onAlert [cp]:
  log: onAlert event has subscribed
```
``` json
{
    "type": "update",
    "name": "AddTrigger",
    "onAlert [cp]": {
        "log": "onAlert event has subscribed"
    }
}
```
@@!

In the following example, the *log* action is executed if the invoked trigger is subscribed to the *onAlert* event with the *custom_name*.

@@@
```yaml
type: update
name: AddTrigger

onAlert [name:custom_name]:
  log: onAlert event has subscribed
```
```json
{
    "type": "update",
    "name": "AddTrigger",
    "onAlert [name:custom_name]": {
        "log": "onAlert event has subscribed"
    }
}
```
@@!

<left><img style="width: 600px"  src="/img/trigger_name.png" alt="trigger name" /></left>

The trigger name can be set up through the dashboard as on the picture above or as described in the example as follows.

The following example shows how a new trigger is being created.
@@@
```yaml
type: update
name : AddTrigger

onInstall:
  environment.trigger.AddTrigger:
    data:
      name: new alert
      nodeGroup: sqldb
      period: 10
      condition:
        type: GREATER
        value: 55
        resourceType: MEM
        valueType: PERCENTAGES
      actions:
        - type: NOTIFY
          customData:
            notify: false
```
``` json
{
  "type": "update",
  "name": "AddTrigger",
  "onInstall": {
    "environment.trigger.AddTrigger": {
      "data": {
        "name": "new alert",
        "nodeGroup": "sqldb",
        "period": "10",
        "condition": {
          "type": "GREATER",
          "value": "55",
          "resourceType": "MEM",
          "valueType": "PERCENTAGES"
        },
        "actions": [
          {
            "type": "NOTIFY",
            "customData": {
              "notify": false
            }
          }
        ]
      }
    }
  }
}
```
@@!
This example involves execution of the Jelastic API *addTrigger* method with a set of required parameters:     

- `name` - name of a notification trigger
- `nodeGroup` - target node group (you can apply trigger to any node group within the chosen environment)
- `period` - load period for nodes
- `condition` - rules for monitoring resources
    - `type` - comparison sign, the available values are *GREATER* and *LESS*
    - `value` - percentage of a resource that is monitored                               
    - `resourceType` - types of resources that are monitored by a trigger, namely *CPU, Memory (RAM), Network, Disk I/O*, and *Disk IOPS*
    - `valueType` - measurement value. Here, *PERCENTAGES*  is the only possible measurement value. The available range is from <b>*0*</b> up to <b>*100*</b>.
- `actions` - object to describe a trigger action
    - `type` - trigger action, the available values are *NOTIFY*, *ADD_NODE*, and *REMOVE_NODE*
    - `customData`:
        - `notify`- alert notification sent to a user via email 

The Jelastic engine sends an alert notification to the Cloud Scripting system when the appropriate trigger is invoked. Therefore, the *onAlert* event provides a possibility to bind actions to alert notifications and execute custom actions.

**Event Placeholders:**     

- `${event.params.}`:
    - `name` - alert name
    - `nodeGroup` - *nodeGroup* where an alert is executed 
    - `resourceType` - resource type that is monitored                  
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*. 

### onBeforeRestartNode

The event is triggered before restarting a node. It is called before the corresponding *restartNodeById* and *restartNodeByGroup* actions.    

**Event Placeholders:**     

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeType` - node type where event is executed
- `${event.response.}` parameters are absent    

### onAfterRestartNode

The event is triggered after restarting a node. It is called subsequently upon the *restartNodeById* and *restartNodeByGroup* actions.

**Event Placeholders:**     
 
- `${event.params.}`:
    - `session` - current user session    
    - `appid` - environment unique appid   
    - `nodeType` - node type where event is executed
- `${event.response.}`:    
    - `nodeid` - restarted node's identifier     
    - `out` - success output message       
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeDelete

The event is called before the *deleteEnvironment* action.       

**Event Placeholders:**   

- `${event.params.}`:    
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `password` - user password     
- `${event.response.}` parameters are absent      

### onBeforeAddNode

The event is triggered before adding a new node to an environment. The *onBeforeAddNode* event is executed for each newly added node.   

There are the following available node groups:         

- *balancer*                

- *compute*                  

- *cache*                    

- *database*             

- *storage*              

- *VPS*                    

- *build*                 

- *docker*               

**Event Placeholders:**   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address           
    - `session` - current user session        
    - `appid` - environment unique appid        
    - `fixedCloudlets` - reserved cloudlets         
    - `flexibleCloudlets` - dynamic cloudlets          
    - `ismaster` *[boolean]* - if *true*, then a new node is treated as the first (i.e. master) one in the current layer     
    - `nodeType` - predefined node type       
- `${event.response.}` parameters are absent        

### onAfterAddNode

The event is triggered after adding a new node to an environment. The *onAfterAddNode* event is executed for each newly added node.     

There are the following available node groups:                   

- *balancer*                

- *compute*                  

- *cache*                    

- *database*             

- *storage*              

- *VPS*                    

- *build*                 

- *docker*                                     
 
**Event Placeholders:**   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address         
    - `session` - current user session      
    - `appid` - environment unique appid
     - `fixedCloudlet`- reserved cloudlets     
     - `flexibleCloudlets` - dynamic cloudlets        
    - `ismaster` *[boolean]* - if *true*, then a new node is treated as the first (i.e. master) one in the current layer          
    - `nodeType` - predefined node type         
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onBeforeCloneNodes

The event is performed before cloning node in the environment. The process of cloning nodes presupposes that new nodes are cloned from the existing ones. 

The *onBeforeCloneNodes* event is applicable only for the next node groups (excluding Docker nodes):                   

- *compute*             

- *balancer*             

- *VPS*                
 
**Event Placeholders:**   

- `${event.params.}`:   
    - `count` - number of nodes to be cloned              
    - `session` - current user session       
    - `appid` - environment unique appid      
    - `nodeGroup` - node group     
    - `flexibleCloudlets` - dynamic cloudlets     
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterCloneNodes

The event is performed after cloning node in the environment. 

The *onAfterCloneNodes* event is applicable only for the next node groups (excluding Docker nodes):                             

- *compute*             

- *balancer*             

- *VPS*                             

**Event Placeholders:**   

- `${event.params.}`:   
    - `count` - number of nodes to be cloned          
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeGroup` - node group      
    - `flexibleCloudlets` - dynamic cloudlets           
- `${event.response.}`:     
    - `result` - result code. The successful action result is *'0'*.       
    - `className` - class name for a new node info, viz. *"com.hivext.api.server.system.persistence.SoftwareNode"*   
    - `array` - new nodes array   

### onBeforeLinkNode

The event is executed before linking nodes to apply configurations to IP addresses. It is compatible only with *compute* and *balancer* node groups and excludes Docker nodes. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking      
    - `session` - current user session       
    - `appid` - environment unique appid       
    - `childNodes` - node identifiers for linking with parent nodes      
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterLinkNode

The event is executed after linking nodes to apply configurations to IP addresses. It is available only for *compute* and *balancer* node groups and excludes Docker nodes.

**Event Placeholders:**   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking     
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `childNodes` - node identifiers for linking with parent nodes          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      
    - `infos` - info with result codes about all nodes' linkings:      
        - `result` - result code     

### onBeforeAttachExtIp

The event is executed before attaching the external IP address. The *onBeforeAttachExtIp* event is triggered each time before the external IP address attachment.

**Event Placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for attaching external IP address        
    - `session` - current user session      
    - `appid` - environment unique appid         
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterAttachExtIp

The event is executed after attaching the external IP address. The *onBeforeAttachExtIp* event is triggered each time upon the external IP address attachment.

**Event Placeholders:**  
  
- `${event.params.}`:   
    - `parentNodes` - node identifiers for attaching external IP address  
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `childNodes` - node identifier for attaching external IP address          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      
    - `object` *[string]* - attached external IP address         

### onBeforeDetachExtIp

The event is executed before detaching the external IP address. The *onBeforeDetachExtIp* event is triggered each time before the external IP address detachment.    

**Event placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for detaching external IP address       
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `ip` - detached IP address     
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterDetachExtIp

The event is executed after detaching the external IP address. The *onAfterDetachExtIp* event is triggered each time upon the external IP address detachment.

**Event Placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for detaching external IP address       
        - `session` - current user session     
        - `appid` - environment unique appid      
        - `ip` - detached external IP address      
- `${event.response.}`:  
    - `result` - parameters are absent       

### onBeforeUpdateVcsProject

The event is carried out before updating the VCS project. For a detailed guidance on the <a href="https://docs.jelastic.com/cli-vcs-deploy" target="_blank">VCS project deployment</a>, refer to the linked page. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `project` - project name       
    - `session` - current user session    
    - `appid` - environment unique appid     
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onAfterUpdateVcsProject

The event is carried out after updating the VCS project. For a detailed guidance on the <a href="https://docs.jelastic.com/cli-vcs-deploy" target="_blank">VCS project deployment</a>, refer to the linked page.      

**Event Placeholders:**   

- `${event.params.}`:   
    - `project` - project name         
    - `session` - current user session      
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onBeforeSetCloudletCount

The event is executed before setting cloudlet count, which implies changing the number of allocated cloudlets per any layer in the environment.                    

**Event Placeholders:**   

- `${event.params.}`:   
    - `fixedCloudlets` - reserved cloudlets value        
    - `flexibleCloudlets` - dynamic cloudlets value         
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeGroup` - predefined node group     
- `${event.response.}`:  
    - `result` - parameters are absent   

### onAfterSetCloudletCount

The event is executed after setting cloudlet count, which implies changing the number of allocated cloudlets per any layer in the environment.                       

**Event Placeholders:**   

- `${event.params.}`:   
    - `fixedCloudlets` - reserved cloudlets value   
    - `flexibleCloudlets` - dynamic cloudlets value      
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `nodeGroup` - predefined node group    
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.       

### onBeforeChangeEngine

The event is performed before changing the engine's version (e.g. from *php 7*  to *php 7.1*) in the required environment. The *onBeforeChangeEngine* event is not compatible with Docker-based environments.     

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid         
    - `settings` - environment settings to change, i.e engine in the present case   
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterChangeEngine

The event is performed after changing the engine's version (e.g. from *php 7*  to *php 7.1*) in the required environment. The *onBeforeChangeEngine* event is not compatible with Docker-based environments.   
 
**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `settings` - environment settings to change, i.e engine in the present case    
- `${event.response.}`:   
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeStart

The event is related to starting environment (executed from the Jelastic dashboard) and is triggered before it. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - parameters are absent       

### onAfterStart

The event is related to starting environment (executed from the Jelastic dashboard) and is triggered after it.                        

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeStop

The event is related to stopping environment (executed from the Jelastic dashboard) and is triggered before it.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterStop

The event is related to stopping environment (executed from the Jelastic dashboard) and is triggered after it. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeClone

The event is related to cloning environment (performed via the Jelastic dashboard by means of the same-named button) and is triggered before it.

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
    - `domain` - cloned environment name      
- `${event.response.}`:  
    - `result` - parameters are absent

### onAfterClone

The event is related to cloning environment (performed via the Jelastic dashboard by means of the same-named button) and is triggered after it.     

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `domain` - cloned environment name       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      
    - `nodeGroups` - node delays:     
        - `restartNodeDelay` - delay for node restart       
        - `name` - node group name    
        - `redeployContainerDelay` - delay for container redeployment     
        - `redeployContextDelay` - delay for context redeployment     
        - `restartContainerDelay` - delay for container restart    
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.       
    - `env` - environment information. Explore the full list of available <a href="/creating-manifest/placeholders/#environment-placeholders" target="_blank">environment placeholders</a>.       

### onBeforeDeploy

The event is bound to the *deploy* action, which is executed at the Jelastic dashboard by deploying any context (i.e. archive with a compressed app) to the environment, and is triggered before it (viz. *deploy* action).    

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid     
    - `atomicDeploy` *[boolean]* - deployment of a context to all nodes at once          
    - `path` - context path       
    - `context` - context name      
    - `archivename` - deployed context display name that is shown at the dashboard         
- `${event.response.}`:  
    - `result` - parameters are absent           

### onAfterDeploy

The event is bound to the *deploy* action, which is executed at the Jelastic dashboard by deploying any context (i.e. archive with a compressed app) to the environment, and is triggered after it (viz. *deploy* action).

**Event Placeholders:**       

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid      
    - `atomicDeploy` *[boolean]* - deployment of a context to all nodes at once        
    - `path` - context path       
    - `context` - context name        
    - `archivename` - deployed context display name that is shown at the dashboard      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.         
    - `responses` - deploy result texts:   
        - `result` - deploy result code for current node ID    
        - `out` - deploy result text      
        - `nodeid` - node identifier       

### onBeforeResetNodePassword

The event is bound to resetting a password (executed at the Jelastic dashboard via the **Reset password** button) and is triggered before it.

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid        
    - `nodeType` - predefined node type       
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterResetNodePassword

The event is bound to resetting a password (executed at the Jelastic dashboard via the **Reset password** button) and is triggered after it.      

**Event Placeholders:**    
    
- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeType` - predefined node type   
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.          

### onBeforeRemoveNode

This event is executed before deleting node(s) from your environment.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeid` - predefined node identifier        
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterRemoveNode

This event is executed after deleting node(s) from your environment.        

**Event Placeholders:**         

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeid` - predefined node identifier     
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeRestartContainer

This event is carried out before restarting container. The *onBeforeRestartContainer* event is triggered before the *restartConteinerById* and *restartConteinerByGroup* actions.     

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - predefined node group     
    - `nodeType` - predefined node type   
- `${event.response.}`:  
    - `result` - parameters are absent        

### onAfterRestartContainer

This event is carried out after restarting container. The *onBeforeRestartContainer* event is triggered after the *restartConteinerById* and *restartConteinerByGroup* actions.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeGroup` - predefined node group     
    - `nodeType` - predefined node type    
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeMigrate

The event is related to the <a href="https://docs.jelastic.com/environment-regions-migration" target="_blank">*migrating environment*</a> action and is called before it.        

**Event Placeholders:**          

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
    - `isOnline` *[boolean]* - online migration that causes no downtime, if set to *'true'*, therefore, setting it as *'false'* leads to the downtime          
    - `hardwareNodeGroup` - predefined hard node group       
- `${event.response.}`:  
    - `result` - parameters are absent                      

### onAfterMigrate

The event is related to <a href="https://docs.jelastic.com/environment-regions-migration" target="_blank">*migrating environment*</a> and is called after it.   

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `isOnline` *[boolean]* - online migration that causes no downtime, if set to *'true'*, therefore, setting it as *'false'* leads to the downtime           
    - `hardwareNodeGroup` - predefined hard node group     
- `${event.response.}`:     
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeRedeployContainer

This event is performed before the container redeployment. It is bound to the *redeployContainerById* and *redeployContainerByGroup* (i.e. redeployment of all containers in a layer) actions. The event is available for Docker containers only.   

**Event Placeholders:**     
 
- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid      
    - `sequential` *[boolean]* - containers sequential redeployment           
    - `nodeGroup` - predefined node group     
    - `useExistingVolumes` - using volumes existing on nodes    
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterRedeployContainer

This event is performed after the container redeployment. It is bound to the *redeployContainerById* and *redeployContainerByGroup* (i.e. redeployment of all containers in a layer) actions. The event is available for Docker containers only.   

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `sequential` *[boolean]* - containers sequential redeployment            
    - `nodeGroup` - predefined node group       
    - `useExistingVolumes` - using volumes existing on nodes      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeLinkNodes


The event is executed before the *linkNodes* action. This event is run for each linking containers action. It is provided for Docker containers only.

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `groupAlias` - alias for linking nodes          
    - `sourceNodeId` - source node for links storage        
    - `targetNodeId` - target node for links storage      
    - `isAutoRestart` *[boolean]* - auto restart after linking  
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterLinkNodes

The event is executed after the *linkNodes* action. This event is run for each linking containers action. It is provided for Docker containers only.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `groupAlias` - alias for linking nodes            
    - `sourceNodeId` - source node for links storage         
    - `targetNodeId` - target node for links storage      
    - `isAutoRestart` *[boolean]* - auto restart after linking  
- `${event.response.}`:   
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeUnlinkNodes

This event is executed before the *unLinkNodes* action and is run for each unlinking containers action. The *onBeforeUnlinkNodes* event is applied for Docker containers only.      

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
    - `alias` - alias for unlinking nodes          
    - `sourceNodeId` - source node for links storage        
    - `targetNodeId` - target node for links storage      
    - `isAutoRestart` *[boolean]* - auto restart after unlinking   
- `${event.response.}`:  
    - `result` - parameters are absent   

### onAfterUnlinkNodes

This event is executed after the *unLinkNodes* action and is run for each unlinking containers action. The *onAfterUnlinkNodes* event is applied for Docker containers only.  

**Event Placeholders:**       

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `alias` - alias for unlinking nodes        
    - `sourceNodeId` - source node for links storage       
    - `targetNodeId` - target node for links storage     
    - `isAutoRestart` *[boolean]* - auto restart after unlinking   
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.       

### onBeforeSetEnvVars

The event is triggered before the *setEnvVars* action. It is executed for every Docker container before setting environment variables. The *onBeforeSetEnvVars* event is applied for Docker containers only.     

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - variables set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterSetEnvVars

The event is triggered after the *setEnvVars* action. It is executed for every Docker container upon setting environment variables. The *onAfterSetEnvVars* event is applied for Docker containers only.

**Event Placeholders:**    

- `${event.params.}`:    
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - current node identifier        
    - `data` - variables set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeSetEntryPoint

This event is called before the *setEntryPoint* action. It is executed for every Docker container before setting the entry point. The *onBeforeSetEntryPoint* event is applied for Docker containers only.   

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeId` - current node identifier         
    - `data` - entry point set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterSetEntryPoint

This event is called after the *setEntryPoint* action. It is executed for every Docker container upon setting the entry point. The *onAfterSetEntryPoint* event is applied for Docker containers only.    

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - entry point set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeSetRunCmd

The event is executed before the *setRunCmd* action. It is triggered for every Docker container, before setting run configs. This event is compatible with Docker containers only.

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - run cmd set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent    
    
### onAfterSetRunCmd

The event is executed after the *setRunCmd* action. It is triggered for every Docker container, upon setting run configs. This event is compatible with Docker containers only.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - run cmd set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeStartService

This event is executed each time before running the Docker *RunCmd* commands. Thus, it is always carried out for each Docker container action, e.g. before starting/restarting container and starting environment.

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
- `${event.response.}`:  
    - `result` - parameters are absent 

### onAfterStartService

This event is executed each time after running the Docker *RunCmd* commands. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.   

### onBeforeAddVolume

The event is performed before adding volumes to Docker container. It is executed once for each Docker container.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeGroup` - current node group        
    - `path` - volume path      
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterAddVolume

This event is performed after adding volumes to Docker container. It is executed once for each Docker container.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group        
    - `path` - volume path        
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.   

### onBeforeRemoveVolume

The *onBeforeRemoveVolume* event is called before removing volumes from Docker container. It is executed once for each Docker container.

**Event Placeholders:**  

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group       
    - `path` - volume path    
- `${event.response.}`:  
    - `result` - parameters are absent 

### onAfterRemoveVolume

The *onAfterRemoveVolume* event is triggered after removing volumes from Docker container. It is executed once for each Docker container.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group  
    - `path` - volume path        
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.                 

<br>       
## What’s next?                            

- Find out how to fetch parameters with <a href="/creating-manifest/placeholders/" target="_blank">Placeholders</a>                                                     

- See how to use <a href="/creating-manifest/conditions-and-iterations/">Conditions and Iterations</a>                              

- Read how to integrate your <a href="/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>            

- Learn how to create your custom <a href="/creating-manifest/addons/" target="_blank">Add-Ons</a>                                

- Check how to handle <a href="/creating-manifest/handling-custom-responses/" target="_blank">Custom Responses</a>     
