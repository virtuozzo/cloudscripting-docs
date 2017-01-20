# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be bound to some event, i.e. executed as a result of this event occurrence.
Each event refers to a particular entity. For example, the entry point for executing any action with application is the *onInstall* event.
<br>
## Events Subsribtion Example
```
{
  "jpsType": "install",
  "name": "Event Subsribtion Example",
  "nodes": [
    {
      "image": "jelastic/nginx-php",
      "volumeMounts": {
        "/var/www/webroot/ROOT": {
          "readOnly": false,
          "sourcePath": "/data",
          "sourceNodeGroup": "storage"
        }
      },
      "volumes": [
        "/var/www/webroot/ROOT"
      ],
      "cloudlets": 8,
      "nodeGroup": "cp",
      "displayName": "AppServer"
    },
    {
      "image": "jelastic/storage",
      "cloudlets": 8,
      "nodeGroup": "storage",
      "displayName": "Storage"
    }
  ],
  "globals": {
    "customDirectory": "/tmp/CloudSCripting"
  },
  "onInstall": {
    "createDirectory [cp]": "${globals.customDirectory}"
  },
  "onAfterScaleOut [nodeGroup:cp]": {
    "cmd [cp]": "echo 'New Compute node has been added' >> ${globals.customDirectory}/addedNodes.txt"
  },
  "onAfterRestartNode [nodeGroup:cp]": {
    "cmd [cp]": "echo 'Compute node with ID - ${events.response.nodeid} has been restarted' >> ${globals.customDirectory}/addedNodes.txt"
  }
}
```
where:

- `jpsType` - *install* type presupposes a creation of a new environment with a predefined set of `nodes`                               
- `globals` - creating [custom global placeholder](/reference/placeholders/#custom-global-placeholders) named *customDirectory*                    
- `onInstall` - first event that will be executed upon environment installation, i.e. creating a new *CloudSCripting* directory                           
- `onAfterScaleOut` - event that will be performed upon new compute node addition, namely writing the appropriate message to the <b>*addedNodes.txt*</b> file                     
- `onAfterRestartNode` - event that will be triggered upon restarting a compute node, viz. writing a message to the <b>*fileaddedNodes.txt*</b> file with a record on which node has been restarted               

##Event Execution Rules
- Such events as *Install* & *Uninstall* application, as well as *BeforeDelete* and *AfterDelete* ones (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.
- The *ScaleIn*, *ScaleOut* and *ServiceScaleOut* events are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.
- For application server, load balancer and VPS node layers, the *cloneNodes* event is executed each time the node group is scaled out
- *UnlinkDockerNodes*, *LinkDockerNodes*, *SetDockerEnvVars*, *SetDockerEntryPoint*, *SetDockerRunCmd*, *AddDockerVolume* and *RemoveDockerVolume* events can be executed only once per a single *changeTopology* action
- The *StartDockerService* event can be called only once while performing the *changeTopology* and *createEnvironment* scaling actions.

## Event parameters and response placeholders

### onInstall

The *onInstall* event is the entry point for executing any action. In case *jpsType* is **install**, the *onInstall* event will be carried out right after environment creation.      
If *jpsType* is set as **update**, *onInstall* is the first event to be performed during the manifest installation.      
 
###onUninstall

The *onUninstall* event can be called from the **Add-ons** tab at the Jelastic dashboard.     
This event is aimed at removing data, which was accumulated as a result of the *onInstall* action execution.           
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
    - `env` - environment information. Explore the full list of available [environment placehosders](http://docs.cloudscripting.com/reference/placeholders/#environment-placeholders).      

### onBeforeScaleOut

The event will be executed before adding new node(s) (i.e. scaling *out*) to the existing node group (viz. layer). Scaling out/in can be performed either through [*changing topology*](https://docs.jelastic.com/jelastic-dashboard-guide#change-topology) or [auto horizontal scaling](https://docs.jelastic.com/automatic-horizontal-scaling) functionality.    
The *onBeforeScaleOut* event will be run only once for each layer. 

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

The event will be executed after scaling in the corresponding node group. The *onAfterScaleIn* event will be run only once for each layer.

**Event Placeholders:**     

- `${event.params.}`:   
    - `count` - number of nodes that are removed       
    - `nodeGroup` - node group that is scaled in      
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available [node placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders).    

###onBeforeServiceScaleOut

The event will be executed before adding new Docker container(s) to the existing node group. It will be run only once for each layer. 
The *onBeforeServiceScaleOut* event is applicable only for Docker containers.

**Event Placeholders:**    

- `${event.params.}`:     
    - `session` - current user session    
    - `appid` - environment unique appid     
    - `nodeId` - node identifier, where event is executed     
- `${event.response.}` parameters are absent       

###onAfterServiceScaleOut   

The event will be executed after adding new Docker container(s) to the existing node group. It will be run only once for each layer.
The *onAfterServiceScaleOut* event is applicable only for Docker containers.  

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
    - `nodeType` - node type where event is executing
- `${event.response.}` parameters are absent.    

### onAfterRestartNode

The event will be triggered after restarting a node. It will be called subsequently upon the *restartNodeById* and *restartNodeByGroup* actions.

Event placeholders:    
 
- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeType` - node type where event is executing
- `${event.response.}`:
    - `nodeid` - restarted node identifier   
    - `out` - success output message   
    - `result` - result code. 0 is success action result.

### onBeforeDelete

Event will be called before the action *delete Environment* will start.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `password` - user password   
- `${event.response.}` parameters are absent.  

### onAfterDelete

Event will be called after the action *delete Environment* will start.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `password` - user password
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.   

### onBeforeAddNode

Event will be run before adding new node into environment.

The list of possible node groups:

- compute;
- db;
- balancer
- build;
- VDS
- cache;
- docker;

Event will execute for every new node.

Event placeholders:   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address with new node   
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `fixedCloudlets` - fixed cloudlets   
    - `flexibleCloudlets` - flexible cloudlets   
    - `ismaster` *[boolean]* - if true than new node will be first in current group   
    - `nodeType` - predefined node type   
- `${event.response.}` parameters are absent.   

### onAfterAddNode

Event will be run after adding new node into environment.

The list of possible node groups:

- compute;
- db;
- balancer
- build;
- VDS
- cache;
- docker;

Event will execute for every new node.

Event placeholders:   

- `${event.params.}`:   
    - `extip` *[boolean]* - external IP address with new node    
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `fixedCloudlets` - fixed cloudlets   
    - `flexibleCloudlets` - flexible cloudlets   
    - `ismaster` *[boolean]* - if true than new node will be first in current group   
    - `nodeType` - predefined node type   
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  

### onBeforeCloneNodes

Event will be executed before cloning node in environment. 
Event avaible only when nodeGroup doesn't *docker* and only for such *node groups*:

- compute;
- balancer;
- VDS

Event placeholders:   

- `${event.params.}`:   
    - `count` - nodes count to clone       
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `nodeGroup` - nodes group   
    - `flexibleCloudlets` - flexible cloudlets     
- `${event.response.}`:  
    - `result` - parameters are absent.  

### onAfterCloneNodes

Event will be executed after cloning node in environment. 
By *cloning nodes* means that new nodes are clonned from existing. Event avaible only when nodeGroup doesn't *docker* and only for such *node groups*:

- compute;
- balancer;
- VDS

Event placeholders:   

- `${event.params.}`:   
    - `count` - nodes count to clone       
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `nodeGroup` - nodes group   
    - `flexibleCloudlets` - flexible cloudlets        
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  
    - `className` - class name for new node info - "com.hivext.api.server.system.persistence.SoftwareNode".   
    - `array` - new nodes array   

### onBeforeLinkNode

Event will be executed before linking nodes with each others for configure IP addresses. 
It is available only for *node groups* - *compute* nodes and *balancers* in case if these nodes are not Docker containers. 

Event placeholders:   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking  
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `childNodes` - node identifier for linking with parents     
- `${event.response.}`:  
    - `result` - parameters are absent. 

### onAfterLinkNode

Event will be executed after linking nodes with each others for configure IP addresses. 
It is available only for *node groups* - *compute* nodes and *balancers* in case if these nodes are not Docker containers. 

Event placeholders:   

- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking  
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `childNodes` - node identifier for linking with parents          
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  
    - `infos` - info with result codes about all nodes links:   
        - `result` - result code   

### onBeforeAttachExtIp

Event can handles custom actions before the action *attache Ext IP address* will execute.
*onBeforeAttachExtIp* executes every time for each attaching IP address.

Event placeholders:   

- `${event.params.}`:   
    - `nodeid` - node identifier for attaching external IP address    
    - `session` - current user session   
    - `appid` - environment unique appid      
- `${event.response.}`:  
    - `result` - parameters are absent. 

### onAfterAttachExtIp

Event can handles custom actions after the action *attache Ext IP address* will execute.
*onAftereAttachExtIp* executes every time for each attaching IP address.

Event placeholders: 
  
- `${event.params.}`:   
    - `parentNodes` - node identifiers for linking  
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `childNodes` - node identifier for linking with parents       
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  
    - `obejct` *[String]* - attached extrenal IP address      

### onBeforeDetachExtIp

Event can handles custom actions before the action *deattache Ext IP address* will execute.
*onBeforeDeattachExtIp* executes every time for each deattaching IP address.

Event placeholders:   

- `${event.params.}`:   
    - `nodeid` - node identifier for attaching external IP address    
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `ip` - deattached IP address   
- `${event.response.}`:  
    - `result` - parameters are absent. 

### onAfterDetachExtIp

Event can handles custom actions after the action *deattache Ext IP address* will execute.
*onBeforeDeattachExtIp* executes every time for each deattaching IP address.

Event placeholders:   

- `${event.params.}`:   
    - `nodeid` - node identifier for attaching external IP address    
        - `session` - current user session   
        - `appid` - environment unique appid    
        - `ip` - deattached IP address    
- `${event.response.}`:  
    - `result` - parameters are absent.    
  
### onBeforeUpdateVcsProject

Event will execute before *update vcs project* action will start.
Details about [VCS project deployment here](https://docs.jelastic.com/cli-vcs-deploy). 

Event placeholders:   

- `${event.params.}`:   
    - `project` - project name      
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.    
    
### onAfterUpdateVcsProject

Event will execute when *update vcs project* action will finished.
Details about [VCS project deployment here](https://docs.jelastic.com/cli-vcs-deploy).

Event placeholders:   

- `${event.params.}`:   
    - `project` - project name      
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result. 
    
### onBeforeSetCloudletCount

Event will execute before action *set cloudlet count* start. Action means changing cloudlets count on any node layer in environment. 

Event placeholders:   

- `${event.params.}`:   
    - `fixedCloudlets` - fixed cloudlets value
    - `flexibleCloudlets` - flexible cloudlets value     
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - predefined node group   
- `${event.response.}`:  
    - `result` - parameters are absent.

### onAfterSetCloudletCount

Event will execute after action *set cloudlet count* start. Action means changing cloudlets count on any node layer in environment.

Event placeholders:   

- `${event.params.}`:   
    - `fixedCloudlets` - fixed cloudlets value
    - `flexibleCloudlets` - flexible cloudlets value     
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - predefined node group  
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  

### onBeforeChangeEngine

Change engine version in existing environment. For example, php or java engine version. Event doesn't available for docker containers.
Event will execute before changing engine version.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `settings` - environment settings to change. For example `engine`, `ssl`.   
- `${event.response.}`:  
    - `result` - parameters are absent.
    
### onAfterChangeEngine

Change engine version in existing environment. For example, php or java engine version. Event doesn't available for docker containers.
Event will execute after changing engine version.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `settings` - environment settings to change. For example `engine`, `ssl`.
- `${event.response.}`:  
    - `result` - result code. 0 is success action result. 
    
### onBeforeStart

Event relates to *start environment* action. Can be executed from Jelastic dashboard. Event will execute before the environment will be started.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - parameters are absent.

### onAfterStart

Event relates to *start environment* action. Can be executed from Jelastic dashboard. Event will execute after the environment will be started.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result. 

### onBeforeStop

Event relates to *stop environment* action. Can be executed from Jelastic dashboard. Event will execute before the environment will be stopped.

Event placeholders:    

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - parameters are absent.

### onAfterStop

Event relates to *stop environment* action. Can be executed from Jelastic dashboard. Event will execute after the environment will be stopped.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  

### onBeforeClone

Event relates to *clone environment* action. Can be executed from Jelastic dashboard by click on *clone environment* button. Event will execute before the environment will be clonned.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `domain` - cloned environment name    
- `${event.response.}`:  
    - `result` - parameters are absent.

### onAfterClone

Event relates to *clone environment* action. Can be executed from Jelastic dashboard by click on *clone environment* button. Event will execute after the environment will be clonned.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `domain` - cloned environment name    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  
    - `nodeGroups` - node delays:     
        - `restartNodeDelay` - delay for restart    
        - `name` - node group name    
        - `redeployContainerDelay` - delay for container redeploy     
        - `redeployContextDelay` - delay for redeploy context     
        - `restartContainerDelay` - delay for restart container    
    - `nodes` - nodes array with detailed info about nodes. Full node placeholders [here](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders) 
    - `env` - environment informartion. Full environment placehosders list [here](http://docs.cloudscripting.com/reference/placeholders/#environment-placeholders)    

### onBeforeDeploy

Event relates to *deploy* action. Can be executed from Jelastic dashboard by deploying any context into environment. Event will execute before the archive will be deployed.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    ,
    - `atomicDeploy` *[boolean]* - deploy archive on all nodes in one time    
    - `path` - context path     
    - `context` - context name    
    - `archivename` - deployed display name    
- `${event.response.}`:  
    - `result` - parameters are absent.   

### onAfterDeploy

Event relates to *deploy* action. Can be executed from Jelastic dashboard by deploying any context into environment. Event will execute after the archive will be deployed.

Event placeholders:      

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    ,
    - `atomicDeploy` *[boolean]* - deploy archive on all nodes in one time    
    - `path` - context path     
    - `context` - context name    
    - `archivename` - deployed display name  
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.     
    - `responses` - deploy result texts:   
        - `result` - deploy result code for current node id
        - `out` - deploy result text    
        - `nodeid` - ndoe identifier    

### onBeforeResetNodePassword

Event relates to *reset node password* action. Can be executed from Jelastic dashboard by resetting password on node (sql for example). Event will execute before the password will be reset.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    ,
    - `nodeType` - predefined node type      
- `${event.response.}`:  
    - `result` - parameters are absent.   

### onAfterResetNodePassword 

Event relates to *reset node password* action. Can be executed from Jelastic dashboard by resetting password on node (sql for example). Event will execute after the password will be reset.

Event placeholders:   
    
- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    ,
    - `nodeType` - predefined node type  
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.     

### onBeforeRemoveNode

Event will be run before remove node from environment.

Event placeholders:      

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeid` - predefined node identifier      
- `${event.response.}`:  
    - `result` - parameters are absent.   

### onAfterRemoveNode

Event will be run after remove node from environment.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeid` - predefined node identifier  
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.  

### onBeforeRestartContainer

Event will be executed before the restart container action will start. Event proceed on actions *restartConteinerById* and *restartConteinerByGroup*.

Event placeholders:    

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - predefined node group   
    - `nodeType` - predefined node type
- `${event.response.}`:  
    - `result` - parameters are absent.   
  
### onAfterRestartContainer

Event will be executed after the restart container action will start. Event proceed on actions *restartConteinerById* and *restartConteinerByGroup*.

Event placeholders:      

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - predefined node group   
    - `nodeType` - predefined node type 
- `${event.response.}`:  
    - `result` - result code. 0 is success action result. 

### onBeforeMigrate

Event relates to *migrate environment* action. Can be executed from Jelastic dashboard by [migrating environment](https://docs.jelastic.com/environment-regions-migration) to another region. Event will execute before the environment will be migrate.

Event placeholders:     

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `isOnline` *[boolean]* - online migration, with down time        
    - `hardwareNodeGroup` - predefined hard node group    
- `${event.response.}`:  
    - `result` - parameters are absent.  
    
### onAfterMigrate

Event relates to *migrate environment* action. Can be executed from Jelastic dashboard by [migrating environment](https://docs.jelastic.com/environment-regions-migration) to another region. Event will execute after the environment will be migrate.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `isOnline` *[boolean]* - online migration, with down time        
    - `hardwareNodeGroup` - predefined hard node group    
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeRedeployContainer

Event will be executed before the action *redeploy container* will run. It relates to actions *redeployContainerById* and *redeployContainerByGroup* (cases when will redeploy one container or all container group). 

For Docker containers only

Event placeholders:  
 
- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `sequential` *[boolean]* - sequential redeploy containers        
    - `nodeGroup` - predefined node group    
    - `useExistingVolumes` - using existing volumes on nodes
- `${event.response.}`:  
    - `result` - parameters are absent.  
    
### onAfterRedeployContainer

Event will be executed after the action *redeploy container* will run. It relates to actions *redeployContainerById* and *redeployContainerByGroup* (cases when will redeploy one container or all container group).

For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `sequential` *[boolean]* - sequential redeploy containers        
    - `nodeGroup` - predefined node group    
    - `useExistingVolumes` - using existing volumes on nodes  
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.

### onBeforeLinkDockerNodes

Event will be executed before the action *linkDockerNodes* will run. This event will execute for every linking containers action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `groupAlias` - alias for links nodes        
    - `sourceNodeId` - source node for links storage       
    - `targetNodeId` - target node for links storage    
    - `isAutoRestart` *[boolean]* - auto restart after links
- `${event.response.}`:  
    - `result` - parameters are absent.  
    
### onAfterLinkDockerNodes

Event will be executed after the action *linkDockerNodes* will run. This event will execute for every linking containers action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `groupAlias` - alias for links nodes        
    - `sourceNodeId` - source node for links storage       
    - `targetNodeId` - target node for links storage    
    - `isAutoRestart` *[boolean]* - auto restart after links
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeUnlinkDockerNodes

Event will be executed before the action *unLinkDockerNodes* will run. This event will execute for every unlinking containers action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `alias` - alias for unlinks nodes        
    - `sourceNodeId` - source node for links storage       
    - `targetNodeId` - target node for links storage    
    - `isAutoRestart` *[boolean]* - auto restart after links
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterUnlinkDockerNodes

Event will be executed after the action *unLinkDockerNodes* will run. This event will execute for every unlinking containers action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `alias` - alias for unlinks nodes        
    - `sourceNodeId` - source node for links storage       
    - `targetNodeId` - target node for links storage    
    - `isAutoRestart` *[boolean]* - auto restart after links
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.

### onBeforeSetDockerEnvVars

Event will be executed before the [action *setDockerEnvVars*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets environment variables action. 
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - variables set for container       
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterSetDockerEnvVars

Event will be executed after the [action *setDockerEnvVars*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets environment variables action. 
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - variables set for container     
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeSetDockerEntryPoint

Event will be executed before the [action *setDockerEntryPoint*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets entry point action. 
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - entry point set for container       
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterSetDockerEntryPoint

Event will be executed after the [action *setDockerEntryPoint*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets entry point action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - entry point set for container     
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeSetDockerRunCmd

Event will be executed before the [action *setDockerRunCmd*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets run commands action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - run cmd set for container       
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterSetDockerRunCmd

Event will be executed after the [action *setDockerRunCmd*](/reference/docker-actions/#docker-environment-variables) will run. This event will execute for every docker container which sets run commands action.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
    - `data` - run cmd set for container     
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeStartDockerService

Event will execute every time when Docker RunCmd commands will be execute. So this event will execute always for each docker container. For example, before starting container, restarting container and start environment.
For Docker containers only.

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterStartDockerService

Event will execute every time when Docker RunCmd commands will be execute. So this event will execute always for each docker container. For example, after starting container, restarting container and start environment.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeId` - curent node identifier        
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeAddDockerVolume

Event will perform before adding volumes into docker container. It will execute once for every Docker container.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - curent node group      ,
    - `path` - volume path    
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterAddDockerVolume

Event will perform after adding volumes into docker container. It will execute once for every Docker container.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - curent node group      ,
    - `path` - volume path      
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
### onBeforeRemoveDockerVolume

Event will perform before removing volumes into docker container. It will execute once for every Docker container.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - curent node group      ,
    - `path` - volume path    
- `${event.response.}`:  
    - `result` - parameters are absent. 
    
### onAfterRemoveDockerVolume

Event will perform after removing volumes into docker container. It will execute once for every Docker container.
For Docker containers only

Event placeholders:   

- `${event.params.}`:   
    - `session` - current user session   
    - `appid` - environment unique appid    
    - `nodeGroup` - curent node group
    - `path` - volume path      
- `${event.response.}`:  
    - `result` - result code. 0 is success action result.
    
## Events filtering

Optionally, events can be filtered by *nodeGroup*, *nodeType* and *nodeId* parameters. As a result, the defined actions will be executed only when the called event matches specified filter rules. 
<br><br>
Otherwise (i.e. if no filtering rules are specified), every Event is listened by all environment entities.

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