# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be bound to some event, i.e. executed as a result of this event occurrence.
Each event refers to a particular entity. For example, the entry point for executing any action with application is the [*onInstall*](#oninstall) event.
<br>
## Events Subscription Example            
```
{
  "jpsType": "update",
  "name": "Event Subsribtion Example",
  "onInstall": {
    "createFile [cp]": "/tmp/result.txt"
  },
  "onAfterScaleOut [nodeGroup:cp]": {
    "cmd [cp]": "echo 'New Compute node has been added' >> /tmp/result.txt"
  },
  "onAfterRestartNode [nodeGroup:cp]": {
    "cmd [cp]": "echo 'Compute node with ID - ${events.response.nodeid} has been restarted' >> /tmp/result.txt"
  }
}
```
where:

- `jpsType` - *update* type presupposes installing add-on in the existing environment with the predefined listeners for *events*                                 
- `onInstall` - first event that will be executed upon environment installation                                                
    - cp - predefined `actions` and `events` in the example require a compute node, therefore, they are filtered by *nodeGroup* as **cp**                                       
- `onAfterScaleOut` - event that will be performed upon new compute node addition                                         
- `onAfterRestartNode` - event that will be triggered upon restarting a compute node                           

##Events Execution Rules
- Such events as *Install* & *Uninstall* application, as well as *BeforeDelete* and *AfterDelete* ones (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.
- The *ScaleIn*, *ScaleOut* and *ServiceScaleOut* events are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.
- For application server, load balancer and VPS node layers, the *cloneNodes* event is executed each time the node group is scaled out
- *UnlinkNodes*, *LinkNodes*, *SetEnvVars*, *SetEntryPoint*, *SetRunCmd*, *AddVolume* and *RemoveVolume* events can be executed only once per a single *changeTopology* action
- The *StartService* event can be called only once while performing the *changeTopology* and *createEnvironment* scaling actions.

## Event Execution Sequence
Below are presented a graphs where all actions with adjoined their events are displayed. Every action has the pair of events. One of them will be executed before action and another one will be started when this action is finished.  

!!! note
    The action `createEnvironment` does not have any event subscribers because they are subscribed after environment creation.    
 
One of the most complicated acts in Jelastic Dashboard is `changeTopology`. The graph below describes a list of a possible actions and their sequence:  
<center><img style="height: 900px"  src="/img/changeTopologySequence.png" alt="change topology sequence icon" /></center>

The another one action is scaling nodes in environment within one *nodeGroup* (node layer). The graph below describes a list of possible actions and related events:

<center><img style="height: 626px"  src="/img/scalingEventSequence.png" alt="scaling sequence icon" /></center>



## Events List

### onInstall

The *onInstall* event is the entry point for executing any action. In case *jpsType* is **install**, the *onInstall* event will be carried out right after environment creation. If *jpsType* is set as **update**, *onInstall*  is the first event to be performed during the manifest installation.           
 
###onUninstall

The *onUninstall* event can be called from the **Add-ons** tab at the Jelastic dashboard. This event is aimed at removing data, which was accumulated as a result of the *onInstall* action execution.            
  
![onUninstall](/img/addon-install.jpg)    

### onBeforeChangeTopology

The event will be executed before changing environment topology via the Jelastic dashboard.

**Event Placeholders:**      

- `${event.params.}`:
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `nodes` - nodes description for a topology change       
    - `env` - environment settings, e.g. `engine`, `ssl`, `ha`, etc 
- `${event.response.}` parameters are absent        

### onAfterChangeTopology

The event will be executed once the *changeTopology* action is finished.     

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
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).     
    - `env` - environment information. Explore the full list of available [environment placeholders](http://docs.cloudscripting.com/reference/placeholders/#environment-placeholders).      

### onBeforeScaleOut

The event will be executed before adding new node(s) (i.e. scaling *out*) to the existing node group (viz. layer). Scaling out/in can be performed either through [changing topology](https://docs.jelastic.com/jelastic-dashboard-guide#change-topology) or [auto horizontal scaling](https://docs.jelastic.com/automatic-horizontal-scaling) functionality. The *onBeforeScaleOut* event will be run only once for each layer.    

**Event Placeholders:**    
 
- `${event.params.}`: 
    - `count` - number of nodes that are added     
    - `nodeGroup` - node group that is scaled out       
- `${event.response.}` parameters are absent        

### onAfterScaleOut

The event will be executed after adding new node(s) to the existing node group. The *onAfterScaleOut* event will be run only once for each layer.   

**Event Placeholders:**  
 
- `${event.params.}`:   
    - `count` - number of nodes that are added      
    - `nodeGroup` - node group that is scaled out     
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).      

### onBeforeScaleIn

The event will be executed before removing node(s) (i.e. scaling *in*) from the target node group. The *onBeforeScaleIn* event will be run only once for each layer.

**Event Placeholders:**   
 
- `${event.params.}`:
    - `count` - number of nodes that are removed    
    - `nodeGroup` - node group that is scaled in   
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).      

### onAfterScaleIn

The event will be executed after scaling *in* the corresponding node group. The *onAfterScaleIn* event will be run only once for each layer.

**Event Placeholders:**     

- `${event.params.}`:   
    - `count` - number of nodes that are removed       
    - `nodeGroup` - node group that is scaled in      
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).    

###onBeforeServiceScaleOut

The event will be executed before adding new Docker container(s) to the existing node group. It will be run only once for each layer. The *onBeforeServiceScaleOut* event is applicable only for Docker containers.      

**Event Placeholders:**    

- `${event.params.}`:     
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeId` - node identifier, where event is executed     
- `${event.response.}` parameters are absent       

###onAfterServiceScaleOut   

The event will be executed after adding new Docker container(s) to the existing node group. It will be run only once for each layer. The *onAfterServiceScaleOut* event is applicable only for Docker containers.     

**Event Placeholders:**    

- `${event.params.}`:    
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `nodeId` - node identifier, where event is executed       
- `${event.response.}` result code. The successful action result is *'0'*.           

### onBeforeRestartNode

The event will be triggered before restarting a node. It will be called before the corresponding *restartNodeById* and *restartNodeByGroup* actions.    

**Event Placeholders:**     

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeType` - node type, where event is executed
- `${event.response.}` parameters are absent    

### onAfterRestartNode

The event will be triggered after restarting a node. It will be called subsequently upon the *restartNodeById* and *restartNodeByGroup* actions.

**Event Placeholders:**     
 
- `${event.params.}`:
    - `session` - current user session    
    - `appid` - environment unique appid   
    - `nodeType` - node type, where event is executed
- `${event.response.}`:    
    - `nodeid` - restarted node's identifier     
    - `out` - success output message       
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeDelete

The event will be called before the *deleteEnvironment* action.       

**Event Placeholders:**   

- `${event.params.}`:    
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `password` - user password     
- `${event.response.}` parameters are absent      

### onAfterDelete

The event will be called after the *deleteEnvironment* action.    

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `password` - user password  
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.       

### onBeforeAddNode

The event will be triggered before adding a new node to an environment. The *onBeforeAddNode* event will be executed for each newly added node.   

There are the following available node groups:   
- *compute*   
- *database*   
- *balancer*  
- *build*  
- *VDS*  
- *cache*  
- *docker*  

**Event Placeholders:**   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address           
    - `session` - current user session        
    - `appid` - environment unique appid        
    - `fixedCloudlets` - reserved cloudlets         
    - `flexibleCloudlets` - dynamic cloudlets          
    - `ismaster` *[boolean]* - if true, then a new node will be treated as first (i.e. master) one in the current layer     
    - `nodeType` - predefined node type       
- `${event.response.}` parameters are absent        

### onAfterAddNode

The event will be triggered after adding a new node to an environment. The *onAfterAddNode* event will be executed for each newly added node.     

There are the following available node groups:  
- *compute*  
- *database*  
- *balancer*   
- *build*   
- *VDS*   
- *cache*   
- *docker*   

**Event Placeholders:**   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address         
    - `session` - current user session      
    - `appid` - environment unique appid
     - `fixedCloudlet`- reserved cloudlets     
     - `flexibleCloudlets` - dynamic cloudlets        
    - `ismaster` *[boolean]* - if true, then a new node will be treated as first (i.e. master) one in the current layer          
    - `nodeType` - predefined node type         
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onBeforeCloneNodes

The event will be performed before cloning node in the environment. The process of cloning nodes presupposes that new nodes are cloned from the existing ones. 

The *onBeforeCloneNodes* event is applicable only for the next node groups (excluding Docker-based nodes):      
- *compute*   
- *balancer*  
- *VDS*    
 
**Event Placeholders:**   

- `${event.params.}`:   
    - `count` - number of nodes to be cloned              
    - `session` - current user session       
    - `appid` - environment unique appid      
    - `nodeGroup` - nodes group     
    - `flexibleCloudlets` - dynamic cloudlets     
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterCloneNodes

The event will be performed after cloning node in the environment. 

The *onAfterCloneNodes* event is applicable only for the next node groups (excluding Docker-based nodes):                               
- *compute*              
- *balancer*                 
- *VDS*                 

**Event Placeholders:**   

- `${event.params.}`:   
    - `count` - number of nodes to be cloned          
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeGroup` - nodes group      
    - `flexibleCloudlets` - dynamic cloudlets           
- `${event.response.}`:     
    - `result` - result code. The successful action result is *'0'*.       
    - `className` - class name for a new node info, viz. *"com.hivext.api.server.system.persistence.SoftwareNode"*   
    - `array` - new nodes array   

### onBeforeLinkNode

The event will be executed before linking nodes to apply configurations to IP addresses. It is compatible only with *compute* and *balancer* node groups and excludes Docker-based nodes. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking      
    - `session` - current user session       
    - `appid` - environment unique appid       
    - `childNodes` - node identifier for linking with parent nodes      
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterLinkNode

The event will be executed after linking nodes to apply configurations to IP addresses. It is available only for *compute* and *balancer* node groups and excludes Docker-based nodes.

**Event Placeholders:**   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking     
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `childNodes` - node identifier for linking with parent nodes          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      
    - `infos` - info with result codes about all nodes' linkings:      
        - `result` - result code     

### onBeforeAttachExtIp

The event can handle custom action before the *attache Ext IP address* action execution. The *onBeforeAttachExtIp* event is triggered each time before the external IP address attachment.

**Event Placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for attaching external IP address        
    - `session` - current user session      
    - `appid` - environment unique appid         
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterAttachExtIp

The event can handle custom action after the *attache Ext IP address* action execution. The *onBeforeAttachExtIp* event is triggered each time upon the external IP address attachment.

**Event Placeholders:**  
  
- `${event.params.}`:   
    - `parentNodes` - node identifiers for attaching external IP address  
    - `session` - current user session     
    - `appid` - environment unique appid     
    - `childNodes` - node identifier for attaching external IP address          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      
    - `obejct` *[string]* - attached extrenal IP address         

### onBeforeDetachExtIp

The event can handle custom action before the *detach Ext Ip address* action execution. The *onBeforeDetachExtIp* event is triggered each time before the external IP address detachment.    

**Event placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for detaching external IP address       
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `ip` - detached IP address     
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterDetachExtIp

The event can handle custom action after the *detach Ext Ip address* action execution. The *onAfterDetachExtIp* event is triggered each time upon the external IP address detachment.

**Event Placeholders:**   

- `${event.params.}`:   
    - `nodeid` - node identifier for detaching external IP address       
        - `session` - current user session     
        - `appid` - environment unique appid      
        - `ip` - detached external IP address      
- `${event.response.}`:  
    - `result` - parameters are absent       

### onBeforeUpdateVcsProject

The event will be carried out before the *update vcs project* action. For a detailed guidance on the [VCS project deployment](https://docs.jelastic.com/cli-vcs-deploy) refer to the linked page. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `project` - project name       
    - `session` - current user session    
    - `appid` - environment unique appid     
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onAfterUpdateVcsProject

The event will be carried out after the *update vcs project* action. For a detailed guidance on the [VCS project deployment](https://docs.jelastic.com/cli-vcs-deploy) refer to the linked page.      

**Event Placeholders:**   

- `${event.params.}`:   
    - `project` - project name         
    - `session` - current user session      
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.        

### onBeforeSetCloudletCount

The event will be executed before the *set cloudlet count* action, which implies changing the amount of allocated cloudlets per any layer in the environment.       

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

The event will be executed after the *set cloudlet count* action, which implies changing the amount of allocated cloudlets per any layer in the environment.          

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

The event will be performed before changing the engine's version (e.g. from *php 7* to *php 7.1*) in the required environment. The *onBeforeChangeEngine* event is not compatible with Docker-based environments.     

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid         
    - `settings` - environment settings to change, i.e `engine` in the present case   
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterChangeEngine

The event will be performed after changing the engine's version (e.g. from *php 7* to *php 7.1*) in the required environment. The *onBeforeChangeEngine* event is not compatible with Docker-based environments.   
 
**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `settings` - environment settings to change, i.e `engine` in the present case    
- `${event.response.}`:   
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeStart

The event is related to the *start environment* action (executed from the Jelastic dashboard) and is triggered before it. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - parameters are absent       

### onAfterStart

The event is related to the *start environment* action (executed from the Jelastic dashboard) and is triggered after it.     

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeStop

The event is related to the *stop environment* action (executed from the Jelastic dashboard) and is triggered before it.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterStop

The event is related to the *stop environment* action (executed from the Jelastic dashboard) and is triggered after it. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeClone

The event is related to the *clone environment* action (performed via the Jelastic dashboard by means of the same-named button) and is triggered before it.

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
    - `domain` - cloned environment name      
- `${event.response.}`:  
    - `result` - parameters are absent

### onAfterClone

The event is related to the *clone environment* action (performed via the Jelastic dashboard by means of the same-named button) and is triggered after it.     

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
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).       
    - `env` - environment information. Explore the full list of available [environment placeholders](http://docs.cloudscripting.com/reference/placeholders/#environment-placeholders).       

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

The event is bound to the *reset node password* action (executed at the Jelastic dashboard via the **Reset password** button) and is triggered before it.

**Event Placeholders:**     

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid        
    - `nodeType` - predefined node type       
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterResetNodePassword 

The event is bound to the *reset node password* action (executed at the Jelastic dashboard via the **Reset password** button) and is triggered after it.      

**Event Placeholders:**    
    
- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeType` - predefined node type   
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.          

### onBeforeRemoveNode

This event will be executed before deleting node(s) from your environment.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeid` - predefined node identifier        
- `${event.response.}`:  
    - `result` - parameters are absent      

### onAfterRemoveNode

This event will be executed after deleting node(s) from your environment.        

**Event Placeholders:**         

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeid` - predefined node identifier     
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeRestartContainer

This event will be carried out before restarting container. The *onBeforeRestartContainer* event is triggered before the *restartConteinerById* and *restartConteinerByGroup* actions.     

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - predefined node group     
    - `nodeType` - predefined node type   
- `${event.response.}`:  
    - `result` - parameters are absent        

### onAfterRestartContainer

This event will be carried out after restarting container. The *onBeforeRestartContainer* event is triggered after the *restartConteinerById* and *restartConteinerByGroup* actions.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeGroup` - predefined node group     
    - `nodeType` - predefined node type    
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

### onBeforeMigrate

The event is related to the [*migrate environment*](https://docs.jelastic.com/environment-regions-migration) action and is called before it.        

**Event Placeholders:**          

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid       
    - `isOnline` *[boolean]* - online migration that causes no downtime, if set value is *'true'*, therefore, setting it as *'false'* will lead to the downtime          
    - `hardwareNodeGroup` - predefined hard node group       
- `${event.response.}`:  
    - `result` - parameters are absent                      

### onAfterMigrate

The event is related to the [*migrate environment*](https://docs.jelastic.com/environment-regions-migration) action and is called after it.   

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `isOnline` *[boolean]* - online migration that causes no downtime, if set value is *'true'*, therefore, setting it as *'false'* will lead to the downtime           
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

The event will be executed before the *linkNodes* action. This event will be run for each linking containers action. Obviously, it is provided for Docker containers only.

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

The event will be executed after the *linkNodes* action. This event will be run for each linking containers action. Obviously, it is provided for Docker containers only.

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

The event will be triggered before the [*setEnvVars*](/reference/docker-actions/#docker-environment-variables) action. It is executed for every docker container upon setting environment variables. The *onBeforeSetEnvVars* event is applied for Docker containers only.     

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - variables set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterSetEnvVars

The event will be triggered before the [*setEnvVars*](/reference/docker-actions/#docker-environment-variables) action. It is executed for every docker container upon setting environment variables. The *onAfterSetEnvVars* event is applied for Docker containers only.

**Event Placeholders:**    

- `${event.params.}`:    
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - current node identifier        
    - `data` - variables set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeSetEntryPoint

This event will be called before the [*setEntryPoint*](/reference/docker-actions/#docker-environment-variables) action. It is executed for every docker container upon setting the entry point. The *onBeforeSetEntryPoint* event is applied for Docker containers only.   

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeId` - current node identifier         
    - `data` - entry point set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent    

### onAfterSetEntryPoint

This event will be called after the [*setEntryPoint*](/reference/docker-actions/#docker-environment-variables) action. It is executed for every docker container upon setting the entry point. The *onAfterSetEntryPoint* event is applied for Docker containers only.    

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - entry point set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.    

### onBeforeSetRunCmd

The event will be executed before the [*setRunCmd*](/reference/docker-actions/#docker-environment-variables) action. It is triggered for every docker container, upon setting run configs. This event is compatible with Docker containers only.

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - run cmd set for a container         
- `${event.response.}`:  
    - `result` - parameters are absent    
    
### onAfterSetRunCmd

The event will be executed after the [*setRunCmd*](/reference/docker-actions/#docker-environment-variables) action. It is triggered for every docker container, upon setting run configs. This event is compatible with Docker containers only.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session      
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
    - `data` - run cmd set for a container       
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.     

### onBeforeStartService


**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
- `${event.response.}`:  
    - `result` - parameters are absent 

### onAfterStartService

This event will be executed each time after running the Docker *RunCmd* commands. 

**Event Placeholders:**   

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid      
    - `nodeId` - current node identifier          
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.   

### onBeforeAddVolume

The event will be performed before adding volumes to Docker container. It will be executed once for each Docker container.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeGroup` - current node group        
    - `path` - volume path      
- `${event.response.}`:  
    - `result` - parameters are absent     

### onAfterAddVolume

This event will be performed after adding volumes to Docker container. It will be executed once for each Docker container.

**Event Placeholders:**      

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group        
    - `path` - volume path        
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.   

### onBeforeRemoveVolume

The *onBeforeRemoveVolume* event will be called before removing volumes from Docker container. It will be executed once for each Docker container.

**Event Placeholders:**  

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group       
    - `path` - volume path    
- `${event.response.}`:  
    - `result` - parameters are absent 

### onAfterRemoveVolume

The *onAfterRemoveVolume* event will be triggered after removing volumes from Docker container. It will be executed once for each Docker container.

**Event Placeholders:**    

- `${event.params.}`:   
    - `session` - current user session     
    - `appid` - environment unique appid      
    - `nodeGroup` - current node group  
    - `path` - volume path        
- `${event.response.}`:  
    - `result` - result code. The successful action result is *'0'*.      

## Events Filtering

Optionally, events can be filtered by *nodeGroup*, *nodeType* and *nodeId* parameters. As a result, the defined actions will be executed only when the called event matches specified filtering rules. 
<br><br>
Otherwise (i.e. if no filtering rules are specified), every **Event** is listened by all environment entities.

<b>Examples</b>

###By nodeGroup
```
{
  "onBeforeScaleOut[nodeGroup:cp]": {
    "writeFile": {
      "nodeGroup": "cp",
      "path": "/tmp/apache2.txt",
      "body": "hello"
    }
  }
}
```
###By nodeType
```
{
  "onBeforeScaleIn[nodeType:tomcat7]": {
    "writeFile": {
      "nodeType": "tomcat7",
      "path": "/tmp/tomcat7.txt",
      "body": "hello"
    }
  }
}
```
###By nodeId
```
{
  "onBeforeRestartNode[nodeId:number]": {
    "writeFile": {
      "nodeId": "number",
      "path": "/tmp/tomcat7.txt",
      "body": "hello"
    }
  }
}
```
where     

- `number` - *nodeId* value for the corresponding instance