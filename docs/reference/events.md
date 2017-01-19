# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be bound to some event, i.e. executed as a result of this event occurrence.
Each event refers to a particular entity. For example, the entry point for executing any action with application is the *onInstall* event.
<br>
<br>
Subscription to a particular application lifecycle event (e.g. topology change) can be done via [Environment Level Events](#environment-level-events).
It’s also possible to bind extension execution to the *onUninstall* event - in such a way, you can implement custom logic of this extension removal from an environment.

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

- `jpsType` - *install* type means that new environment with `nodes` will be created.  
- `globals` - create [Custom Global Placeholder](/reference/placeholders/#custom-global-placeholders) named customDirectory 
- `onInstall` - first event which will be executed when environment will been installed - create new folder *CloudSCripting* in directory 
- `onAfterScaleOut` - event will be performed after new compute node has been added - write message into file *addedNodes.txt*  
- `onAfterRestartNode` - event will be performed after restart compute node - write message into file *addedNodes.txt* what node has been restarted
                            
                            
##Event Execution Rules
- Such events as *Install* & *Uninstall* application, as well as *BeforeDelete* and *AfterDelete* ones (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.
- The *ScaleIn*, *ScaleOut* and *ServiceScaleOut* events are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.
- For application server, load balancer and VPS node layers, the *cloneNodes* event is executed each time the node group is scaled out
- *UnlinkDockerNodes*, *LinkDockerNodes*, *SetDockerEnvVars*, *SetDockerEntryPoint*, *SetDockerRunCmd*, *AddDockerVolume* and *RemoveDockerVolume* events can be executed only once per a single *changeTopology* action
- The *StartDockerService* event can be called only once while performing the *changeTopology* and *createEnvironment* scaling actions.

## Event parameters and response placeholders

### onInstall

**onInstall** is an entry point for actions execution.
In case `jpsType` is *install*, event **onInstall** will be executed right after environment creation. In case `jpsType` is *update*, **onInstall** event is performed first event while manifest instalation.
 
###onUninstall

*onUninstall* event can be called from Add-ons tab in Jelastic Dashboard.
This event means to do actions for removing data which were installed by *onInstall* action.
![onUninstall](/img/addon-install.jpg)

### onBeforeChangeTopology

Event will be executed before changing environment topology from Jelastic Dashboard.

Event placeholders:      

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodes` - nodes description for change topology    
    - `env` - environment settings: `engine`, `ssl`, `ha` etc 
- `${event.response.}` parameters are absent.    

### onAfterChangeTopology

Event execution will start when action *change Topology* will be finished.

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
    
### onBeforeScaleOut

Event execution will start before the customer will add all new nodes to existing node Group (layer of nodes). New nodes can be added via [*change topology*](https://docs.jelastic.com/jelastic-dashboard-guide#change-topology) action or via [autoscaling feature](https://docs.jelastic.com/automatic-horizontal-scaling).
Event will run only once for every nodeGroup. 

Event placeholders:    

- `${event.params.}`:
    - `count` - nodes count to scale into topology    
    - `nodeGroup` - node group where will new nodes will be added      
- `${event.response.}` parameters are absent.  

### onAfterScaleOut

Event execution will start after the customer will add all new nodes to existing node Group.
Event will run only once for every nodeGroup. 

Event placeholders:  
 
- `${event.params.}`:   
    - `count` - nodes count to scale into topology    
    - `nodeGroup` - node group where will new nodes will be added 
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about nodes. Full node placeholders [here](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders) 
    
### onBeforeScaleIn

Event will run before removing any stack node from Jelastic environment. Can be executed only once for every nodeGroup.

Event placeholders:   
 
- `${event.params.}`:
    - `count` - nodes count to remove from topology
    - `nodeGroup` - node group where will new nodes will be removed
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about nodes. Full node placeholders [here](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders) 
    
### onAfterScaleIn

Event will be run after removing any stack node from Jelastic environment. Can be executed only once for every nodeGroup.

Event placeholders:     

- `${event.params.}`:   
    - `count` - nodes count to remove from topology    
    - `nodeGroup` - node group where will new nodes will be removed 
- `${event.response.}`:  
    - `nodes` - nodes array with detailed info about nodes. Full node placeholders [here](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders) 

###onBeforeServiceScaleOut

Event will be executed before additing new docker containers to existing nodeGroup. Can be executed only once for every nodeGroup (nodes layer). Event available only for Docker containers.

Event placeholders:    

- `${event.params.}`:     
    - `session` - current user session   
    - `appid` - environment unique appid   
    - `nodeId` - node identifier where event is executing   
- `${event.response.}` parameters are absent.    

###onAfterServiceScaleOut   

Event will be executed before removing docker containers to existing nodeGroup. Can be executed only once for every nodeGroup (nodes layer). Event available only for Docker containers.

Event placeholders:    

- `${event.params.}`:    
    - `session` - current user session    
    - `appid` - environment unique appid   
    - `nodeId` - node identifier where event is executing       
- `${event.response.}` result code. 0 is success action result.     

### onBeforeRestartNode

Event will be executed before the restart node action will start. Event proceed on actions *restartNodeById* and *restartNodeByGroup*.

Event placeholders:     

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeType` - node type where event is executing
- `${event.response.}` parameters are absent.    

### onAfterRestartNode

Event will be executed after the restart node action will start. Event proceed on actions *restartNodeById* and *restartNodeByGroup*.

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
    - `nodeGroup` - curent node group      ,
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