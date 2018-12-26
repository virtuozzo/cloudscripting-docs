# Events

Any <a href="/1.6/creating-manifest/actions/" target="_blank">action</a>, available to be performed by means of <a href="https://docs.jelastic.com/api/" target="_blank">API</a> (including <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">custom scripts</a> running), should be bound to some event and executed as a result of this event occurrence.

Each event triggers a particular action on the required application's lifecycle stage. The entry point for executing any action is the [*onInstall*](#oninstall) event.

## Events Execution Rules

- Such events as *onBeforeDelete* and *onAfterDelete* (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.
- The scaling events (*onBeforeScaleOut/onAfterScaleOut*, *onBeforeScaleIn/onAfterScaleIn*, *onBeforeServiceScaleOut/onAfterServiceScaleOut*, *onBeforeSetCloudletCount/onAfterSetCloudletCount*) are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.
- For application server, load balancer and VPS node layers, the *onBeforeCloneNodes/onAfterCloneNodes* events are executed each time the node group is scaled out.
- The *onBeforeLinkNodes/onAfterLinkNodes*, *onBeforeUnlinkNodes/onAfterUnlinkNodes*, *onBeforeSetEnvVars/onAfterSetEnvVars*, *onBeforeSetEntryPoint/onAfterSetEntryPoint*, *onBeforeSetRunCmd/onAfterSetRunCmd*, *onBeforeAddVolume/onAfterAddVolume* and *onBeforeRemoveVolume/onAfterRemoveVolume* events can be executed only once per a single *changeTopology* action.
- The *onBeforeStartService/onAfterStartService* event can be called only once while performing the *changeTopology* and *createEnvironment* actions.

## Events Filtering

Events can be filtered by any input parameters. As a result, the action is executed only when the called event matches specified filtering rules. Parameter name (e.g. *myalert*) can be specified via a colon: **onAlert [name:myalert]**. Input parameters list is described for every [event](/creating-manifest/events/#event-list) within **${event.params.}**. Also, it is possible to filter events with comma-separated list of the parameters (**onBeforeRedeployContainer [nodeGroup:cp, sequential:true, useExistingVolumes:true]**). 
In case the parameter name is not specified via colon, engine tries to determine parameter as a [*nodeID*](/creating-manifest/selecting-containers/#particular-container), if it’s not possible, then it tries to determine a [*nodeGroup*](/creating-manifest/selecting-containers/#all-containers-by-group), if it’s not possible, after that it tries to determine a [*nodeType*](/creating-manifest/selecting-containers/#all-containers-by-type). Finally, if no filtering rules are specified, no event triggers.

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

There are few options to filter executed events:

1. onBeforeRestartNode [cp] or [apache] or [1234] - short filters for events
2. onBeforeRestartNode [nodeGroup: cp] or [nodeType: apache] or [nodeId: 1234] - full filters sets
3. Combines of different simple filters from first or second points above in one -
onBeforeRestartNode[1234, 5678] (executing `event` only on nodes checked by unique identifiers) or onBeforeRestartNode[nodeGroup: cp, nodeId: 123]

Such reserved keywords like *nodeGroup*, *nodeType* and *nodeId* in event filtering are not case sensitive, so they can be declared in any way.


## Events Execution Sequence

Below you can find the graphs that list actions with adjoining events. Every action has a pair of adjoining events - one of them is executed *before* the action and another one is launched *after* the action, that is when the action is finished.

!!! note

      The <b>*createEnvironment*</b> action does not have any adjoining events, because events are bound after the environment creation.

The <b>*changeTopology*</b> actions are considered quite time-consuming while being performed via the Jelastic dashboard, therefore, you can automate their workflow with the following CS actions and related events.

<center><img style="height: 900px; padding-right: 69px" src="/img/changeTopologySequence.png" alt="change topology sequence icon" /></center>

Another demanded actions are related to scaling procedures. The following graph provides a sequence of scaling actions and related events.

<center><img style="height: 626px" src="/img/scalingEventSequence.png" alt="scaling sequence icon" /></center>

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
    - `env` - environment settings, e.g. *engine, ssl, ha, region* etc
- `${event.response.}` parameters are absent

### onAfterChangeTopology

The event is executed once the *changeTopology* action is finished.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodes` - nodes array with detailed info about the topology change
    - `env` - environment settings, e.g. *engine, ssl, ha, region* etc
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0"*.
    - `envGroups` - environment groups array
    - `right` - account right for environment
    - `nodeGroups` - node delays:
        - `restartNodeDelay` - delay for restart
        - `name` - node group name
        - `redeployContainerDelay` - delay for container redeployment
        - `redeployContextDelay` - delay for context redeployment
        - `restartContainerDelay` - delay for container restart
    - `nodes` - nodes array with detailed info about the topology change. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.
    - `env` - environment information. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#environment-placeholders" target="_blank">environment placeholders</a>.

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
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.

### onBeforeScaleIn

The event is executed before removing node(s) (i.e. scaling *in*) from the target node group. The *onBeforeScaleIn* event is run once for each layer upon any node count change.

**Event Placeholders:**

- `${event.params.}`:
    - `count` - number of nodes that are removed
    - `nodeGroup` - node group that is scaled in
- `${event.response.}`:
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.

### onAfterScaleIn

The event is executed after scaling *in* the corresponding node group. The *onAfterScaleIn* event is run once for each layer upon any node count change.

**Event Placeholders:**

- `${event.params.}`:
    - `count` - number of nodes that are removed
    - `nodeGroup` - node group that is scaled in
- `${event.response.}`:
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.

### onBeforeServiceScaleOut

The event is executed before adding new Docker container(s) to the existing node group. It is run once for each layer upon any node count change. The *onBeforeServiceScaleOut* event is applicable only for Docker containers.

**Event Placeholders:**

- `${event.params.}`:
    - `count` - nodes count which have been added
    - `nodeGroup` - node layer where event is executed
- `${event.response.}`:
    - `nodes` - nodes array which will be added to the environment. All parameters from that array can be used in a same action as placeholders value. For example, placeholder *{event.response.nodes[0].url}* will be an address of first added node.

### onAfterServiceScaleOut

The event is executed after adding new container(s) to the existing node group. It is run once for each layer upon any node count change. The *onAfterServiceScaleOut* event is applicable only for Docker containers.

**Event Placeholders:**

- `${event.params.}`:
    - `nodeGroup` - node layer where event is executed
    - `count` - nodes count which have been added
- `${event.response.}`
    - `nodes` - nodes array which was added to the environment. All parameters from that array can be used in a same action as placeholders value. For example, placeholder *{event.response.nodes[0].url}* will be an address of first added node.

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
    - `valueType` - measurement value. Here, *PERCENTAGES* is the only possible measurement value. The available range is from <b>*0*</b> up to <b>*100*</b>.
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
    - `nodeGroup` - node group (*nodemission*) where event is executed
    - `env` - environment short name within which the event is called
    - `name` - environment display name
- `${event.response.}` parameters are absent

### onAfterRestartNode

The event is triggered after restarting a node. It is called subsequently upon the *restartNodeById* and *restartNodeByGroup* actions.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeType` - node type where event is executed
    - `nodeGroup` - node group (*nodemission*) where event is executed
    - `env` - environment short name within which the event is called
    - `name` - environment display name
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
    - `env` - environment short name (only domain name)
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
    - `extipv4` *[nubmer]* - external IPv4 address count
    - `extipv6` *[nubmer]* - external IPv6 address count
    - `session` - current user session
    - `appid` - environment unique appid
    - `fixedCloudlets` - reserved cloudlets
    - `flexibleCloudlets` - dynamic cloudlets
    - `ismaster` *[boolean]* - if *true*, then a new node is treated as the first (i.e. master) one in the current layer
    - `env` - environment domain name
    - `tag` - template tag
    - `nodeType` - predefined node type
    - `nodetype` - same as `nodeType` parameter
    - `nodeGroup` - predefined node group
    - `nodegroup` - same as `nodeGroup` parameter
    - `name` - template node name
    - `fixedCloudlets` - fixed cloudlets count for future node
    - `flexibleCloudlets` - flexible cloudlet count
    - `diskLimit` - current node disk limit
    - `startService` *[boolean]* - value to start main service in container
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
    - `extipv4` *[nubmer]* - external IPv4 address count
    - `extipv6` *[nubmer]* - external IPv6 address count
    - `session` - current user session
    - `appid` - environment unique appid
    - `fixedCloudlets` - reserved cloudlets
    - `flexibleCloudlets` - dynamic cloudlets
    - `ismaster` *[boolean]* - if *true*, then a new node is treated as the first (i.e. master) one in the current layer
    - `env` - environment domain name
    - `tag` - template tag
    - `nodeType` - predefined node type
    - `nodetype` - same as `nodeType` parameter
    - `nodeGroup` - predefined node group
    - `nodegroup` - same as `nodeGroup` parameter
    - `name` - template node name
    - `fixedCloudlets` - fixed cloudlets count for future node
    - `flexibleCloudlets` - flexible cloudlet count
    - `diskLimit` - current node disk limit
    - `startService` *[boolean]* - value to start main service in container
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
    - `nodegroup` - same value as `nodeGroup`
    - `env` - environment short name
    - `name` - environment display name
- `${event.response.}` parameters are absent

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
    - `nodegroup` - same value as `nodeGroup`
    - `env` - environment short name
    - `name` - environment display name
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
    - `env` - environment short name
- `${event.response.}`- parameters are absent

### onAfterLinkNode

The event is executed after linking nodes to apply configurations to IP addresses. It is available only for *compute* and *balancer* node groups and excludes Docker nodes.

**Event Placeholders:**

- `${event.params.}`:
    - `parentNodes` - node identifiers for linking
    - `session` - current user session
    - `appid` - environment unique appid
    - `childNodes` - node identifiers for linking with parent nodes
    - `env` - environment short name
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
    - `envName` - environment unique appid
    - `appid` - application unique appid
    - `name` - environment display name
    - `env` - environment short domain name
- `${event.response.}`:
    - `result` - parameters are absent

### onAfterAttachExtIp

The event is executed after attaching the external IP address. The *onBeforeAttachExtIp* event is triggered each time upon the external IP address attachment.

**Event Placeholders:**

- `${event.params.}`:
    - `nodeid` - node identifier for attaching external IP address
    - `session` - current user session
    - `envName` - environment unique appid
    - `appid` - application unique appid
    - `name` - environment display name
    - `env` - environment short domain name
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.
    - `obejct` *[string]* - attached external IP address

### onBeforeDetachExtIp

The event is executed before detaching the external IP address. The *onBeforeDetachExtIp* event is triggered each time before the external IP address detachment.

**Event placeholders:**

- `${event.params.}`:
    - `nodeid` - node identifier for detaching external IP address
    - `session` - current user session
    - `envName` - environment unique appid
    - `appid` - application unique appid
    - `ip` - detached IP address
    - `name` - environment display name
    - `env` - environment short domain name
- `${event.response.}` - parameters are absent
  
### onAfterDetachExtIp

The event is executed after detaching the external IP address. The *onAfterDetachExtIp* event is triggered each time upon the external IP address detachment.

**Event Placeholders:**

- `${event.params.}`:
    - `nodeid` - node identifier for detaching external IP address
    - `session` - current user session
    - `envName` - environment unique appid
    - `appid` - application unique appid
    - `ip` - detached IP address
    - `name` - environment display name
    - `env` - environment short domain name
- `${event.response.}`:
    - `result` - parameters are absent

### onBeforeUpdateVcsProject

The event is carried out before updating the VCS project. For a detailed guidance on the <a href="https://docs.jelastic.com/cli-vcs-deploy" target="_blank">VCS project deployment</a>, refer to the linked page.

**Event Placeholders:**

- `${event.params.}`:
    - `projectId` - project id
    - `session` - current user session
    - `appid` - environment unique appid
    - `envName` - environment unique identifier
    - `context` - project context name
    - `env` - environment short domain name
    - `nodeGroup` *[optional]* - predefined node group
    - `nodegroup` *[optional]* - same value as `nodeGroup`
    - `nodeid` *[optional]* - node unique identifier
    - `delay` *[optional]* - delay between deploys on nodes (in case if mode than two nodes in one nodeGroup are available).
- `${event.response.}`- parameters are absent

### onAfterUpdateVcsProject

The event is carried out after updating the VCS project. For a detailed guidance on the <a href="https://docs.jelastic.com/cli-vcs-deploy" target="_blank">VCS project deployment</a>, refer to the linked page.

**Event Placeholders:**

- `${event.params.}`:
    - `projectId` - project id
    - `session` - current user session
    - `appid` - environment unique appid
    - `envName` - environment unique identifier
    - `context` - project context name
    - `env` - environment short domain name
    - `nodeGroup` *[optional]* - predefined node group
    - `nodegroup` *[optional]* - same value as `nodeGroup`
    - `nodeid` *[optional]* - node unique identifier
    - `delay` *[optional]* - delay between deploys on nodes (in case if mode than two nodes in one nodeGroup are available).
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
    - `nodegroup` - same value as `nodeGroup`
    - `env` - environment short domain name
    - `name` - environment display name
- `${event.response.}`: parameters are absent

### onAfterSetCloudletCount

The event is executed after setting cloudlet count, which implies changing the number of allocated cloudlets per any layer in the environment.

**Event Placeholders:**

- `${event.params.}`:
    - `fixedCloudlets` - reserved cloudlets value
    - `flexibleCloudlets` - dynamic cloudlets value
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeGroup` - predefined node group
    - `nodegroup` - same value as `nodeGroup`
    - `env` - environment short domain name
    - `name` - environment display name
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.

### onBeforeChangeEngine

The event is performed before changing the engine's version (e.g. from *php 7* to *php 7.1*) in the required environment. The *onBeforeChangeEngine* event is not compatible with Docker-based environments.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `settings` - environment settings to change, i.e engine in the present case
- `${event.response.}`:
    - `result` - parameters are absent

### onAfterChangeEngine

The event is performed after changing the engine's version (e.g. from *php 7* to *php 7.1*) in the required environment. The *onAfterChangeEngine* event is not compatible with Docker-based environments.

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
    - `env` - environment short domain name
- `${event.response.}` - parameters are absent

### onAfterStart

The event is related to starting environment (executed from the Jelastic dashboard) and is triggered after it.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `env` - environment short domain name
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.

### onBeforeStop

The event is related to stopping environment (executed from the Jelastic dashboard) and is triggered before it.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `env` - environment short domain name
- `${event.response.}`: parameters are absent


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
    - `srcenv` - source environment, parent environment for clone.
    - `targetenv` - cloned environment name. The same value as `domain`
- `${event.response.}` - parameters are absent

### onAfterClone

The event is related to cloning environment (performed via the Jelastic dashboard by means of the same-named button) and is triggered after it.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `domain` - cloned environment name
    - `srcenv` - source environment, parent environment for clone.
    - `targetenv` - cloned environment name. The same value as `domain`
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.
    - `envGroups` - environment groups array
    - `nodeGroups` - node delays:
        - `restartNodeDelay` - delay for node restart
        - `name` - node group name
        - `redeployContainerDelay` - delay for container redeployment
        - `redeployContextDelay` - delay for context redeployment
        - `restartContainerDelay` - delay for container restart
    - `nodes` - nodes array with detailed info about topology. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">node placeholders</a>.
    - `env` - environment information. Explore the full list of available <a href="/1.6/creating-manifest/placeholders/#environment-placeholders" target="_blank">environment placeholders</a>.

### onBeforeBuildProject

The event is related to build project action and is triggered before it (executed from the Jelastic dashboard).

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `project` - project name in Jelastic dashboard
    - `env` - environment name where action is executed
    - `nodeid` - environment name where action is executed
    - `projectid` - project unique identifier in Jelastic dashboard
- `${event.response.}`:
    - `result` - parameters are absent

### onAfterBuildProject

The event is related to build project action and is triggered after it (executed from the Jelastic dashboard).

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `project` - project name in Jelastic dashboard
    - `env` - environment name where action is executed
    - `nodeid` - environment name where action is executed
    - `projectid` - project unique identifier in Jelastic dashboard
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.

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
    - `nodeGroup` - predefined node group
- `${event.response.}`:
    - `result` - parameters are absent

### onAfterResetNodePassword

The event is bound to resetting a password (executed at the Jelastic dashboard via the **Reset password** button) and is triggered after it.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeGroup` - predefined node group
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
    - `env` - the same value `envName`
    - `name` - environment display name
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.

### onBeforeRestartContainer

This event is carried out before restarting container. The *onBeforeRestartContainer* event is triggered before the *restartConteinerById* action.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeGroup` - predefined node group
    - `nodeType` - predefined node type
    - `envName` - environment short domain name
    - `env` - the same value `envName`
    - `name` - environment display name
    - `nodeid` - node unique identifier where method is executed
- `${event.response.}` - parameters are absent

### onAfterRestartContainer

This event is carried out after restarting container. The *onAfterRestartContainer* event is triggered after the *restartConteinerById* action.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `nodeGroup` - predefined node group
    - `nodeType` - predefined node type
    - `envName` - environment short domain name
    - `env` - the same value `envName`
    - `name` - environment display name
    - `nodeid` - node unique identifier where method is executed
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
- `${event.response.}` - parameters are absent

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
    - `nodegroup` - same value as `nodeGroup`
    - `name` - environment display name
    - `env` - environment domain name
    - `tag` - chosen tag for redeploy
    - `useExistingVolumes` - using volumes existing on nodes
- `${event.response.}` - parameters are absent

### onAfterRedeployContainer

This event is performed after the container redeployment. It is bound to the *redeployContainerById* and *redeployContainerByGroup* (i.e. redeployment of all containers in a layer) actions. The event is available for Docker containers only.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `sequential` *[boolean]* - containers sequential redeployment
    - `nodeGroup` - predefined node group
    - `nodegroup` - same value as `nodeGroup`
    - `name` - environment display name
    - `env` - environment domain name
    - `tag` - chosen tag for redeploy
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
    - `alias`
    - `sourceNodeId` - source node for links storage
    - `sourcenodeid` - an alias for `sourceNodeId`
    - `sourcenodename` - source node name
    - `targetNodeId` - target node for links storage
    - `targetnodeid` - an alias to `targetNodeId`
    - `targetnodename` - target node name
    - `env` - environment domain name
    - `isAutoRestart` *[boolean]* - auto restart after linking
- `${event.response.}` - parameters are absent

### onAfterLinkNodes

The event is executed after the *linkNodes* action. This event is run for each linking containers action. It is provided for Docker containers only.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `groupAlias` - alias for linking nodes
    - `alias` - an alias for `groupAlias`
    - `sourceNodeId` - source node for links storage
    - `sourcenodeid` - an alias for `sourceNodeId`
    - `sourcenodename` - source node name
    - `targetNodeId` - target node for links storage
    - `targetnodeid` - an alias to `targetNodeId`
    - `targetnodename` - target node name
    - `env` - environment domain name
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
    - `sourcenodeid` an alias for `sourceNodeId`
    - `targetNodeId` - target node for links storage
    - `targetnodeid` an alias for `targetNodeId`
    - `targetnodename` - target node name
    - `sourcenodename` - source node name
    - `alias` - an alias for `groupAlias`
    - `env` - environment domain name
    - `isAutoRestart` *[boolean]* - auto restart after unlinking
- `${event.response.}` - parameters are absent

### onAfterUnlinkNodes

This event is executed after the *unLinkNodes* action and is run for each unlinking containers action. The *onAfterUnlinkNodes* event is applied for Docker containers only.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `alias` - alias for unlinking nodes
    - `sourceNodeId` - source node for links storage
    - `sourcenodeid` an alias for `sourceNodeId`
    - `targetNodeId` - target node for links storage
    - `targetnodeid` an alias for `targetNodeId`
    - `targetnodename` - target node name
    - `sourcenodename` - source node name
    - `alias` - an alias for `groupAlias`
    - `env` - environment domain name
    - `isAutoRestart` *[boolean]* - auto restart after unlinking
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*.

### onBeforeSetEnvVars

The event is triggered before the *setEnvVars* action. It is executed for every Docker or dockerized container before setting environment variables.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment domain name
    - `nodeId` - current node identifier
    - `nodeid` - an alias, the same value as `nodeId`
    - `data` - variables set for a container
- `${event.response.}` - parameters are absent

### onAfterSetEnvVars

The event is triggered after the *setEnvVars* action. It is executed for every Docker or dockerized container upon setting environment variables.
  
**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment domain name
    - `nodeId` - current node identifier
    - `nodeid` - an alias, the same value as `nodeId`
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
- `${event.response.}` - parameters are absent

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
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeId` - current node identifier
    - `nodeid` - an alias for `nodeId`
    - `data` - run cmd set for a container
- `${event.response.}` - parameters are absent

### onAfterSetRunCmd

The event is executed after the *setRunCmd* action. It is triggered for every Docker container, upon setting run configs. This event is compatible with Docker containers only.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeId` - current node identifier
    - `nodeid` - an alias for `nodeId`
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
- `${event.response.}` - parameters are absent

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
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeGroup` - current node group
    - `nodeId` - current node identifier
    - `nodeid` - the same value as `nodeId`, an alias
    - `path` - volume path
- `${event.response.}` - parameters are absent
  
### onAfterAddVolume

This event is performed after adding volumes to Docker container. It is executed once for each Docker container.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeGroup` - current node group
    - `nodeId` - current node identifier
    - `nodeid` - the same value as `nodeId`, an alias
    - `path` - volume path
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*
    - `nodeid` - current node identifier

### onBeforeRemoveVolume

The *onBeforeRemoveVolume* event is called before removing volumes from Docker container. It is executed once for each Docker container.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeId` - current node identifier
    - `nodeid` - the same value as `nodeId`, an alias
    - `nodeGroup` - current node group
    - `path` - volume path
- `${event.response.}` - parameters are absent

### onAfterRemoveVolume

The *onAfterRemoveVolume* event is triggered after removing volumes from Docker container. It is executed once for each Docker container.

**Event Placeholders:**

- `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `name` - environment display name
    - `env` - environment short domain name
    - `nodeId` - current node identifier
    - `nodeid` - the same value as `nodeId`, an alias
    - `nodeGroup` - current node group
    - `path` - volume path
- `${event.response.}`:
    - `result` - result code. The successful action result is *'0'*
    - `nodeid` - current node identifier

### onBeforeInit   
### onBeforeInstall   
It is possible to dynamically fill in the manifest fields using *onBeforeInit* and *onBeforeInstall* events.

#### onBeforeInit
The *onBeforeInit* event is executed:   

-   on *GetAppInfo* request, which is called to display application
   installation dialog in the dashboard   
-   on application installation


Placeholders do not work inside *onBeforeInit*, since even *globals* can be defined dynamically.
You can override all the parameters of the manifest, except for:

-   `type`
-   `name`
-   `baseUrl`

#### onBeforeInstall
The *onBeforeInstall* event is executed before application installation but after *onBeforeInit*.
The placeholders **\${globals.}** and **\${settings.}** can be used within *onBeforeInstall*. All of the manifest parameters can be overridden, except for:

-   `type`
-   `name`
-   `baseUrl`
-   `globals`
-   `settings`

*onBeforeInit* and *onBeforeInstall* can treat JavaScript code, written as:

-   string
@@@
```yaml
type: update
name: "Ability to dynamically determine UI in JPS"  
onBeforeInit: |
  return {
    result: 0,
    settings : {
      fields: [{
        type : "string",
        caption: "Custom Field",
        name : "custom_field",
        "default" : "test"
      }]
    }
  };
onInstall:
assert: "'${settings.custom_field}' == 'test'"
```
```json
{
  "type": "update",
  "name": "Ability to dynamically determine UI in JPS",
  "onBeforeInit": "return { \n  result: 0, \n  settings : {\n    fields: [{ \n      type : \"string\", \n      caption: \"Custom Field\",\n      name : \"custom_field\", \n      \"default\" : \"test\" \n    }]\n  }\n};\n",
  "onInstall": null,
  "assert": "'${settings.custom_field}' == 'test'"
}

```
@@!
>
-   string array
@@@
```yaml
type: update
name: test
onBeforeInit:
- return {
- "  result: 0,"
- "  settings : {"
- "    fields: [{"
- "      type : 'string',"
- "      caption: 'Custom Field',"
- "      name : 'custom_field',"
- "      'default' : 'test'"
- "    }]"
- "  }"
- "};"
```
```json
{
    "type": "update",
    "name": "test",
    
    "onBeforeInit": [
        "return {",
        "  result: 0,",
        "  settings : {",
        "    fields: [{",
        "      type : 'string',",
        "      caption: 'Custom Field',",
        "      name : 'custom_field',",
        "      'default' : 'test'",
        "    }]",
        "  }",
        "};"
    ]
}
```
@@!
>
-   URL
@@@
```yaml
type: update  
name: "Ability to dynamically determine UI in JPS"  
onBeforeInit: https://gist.githubusercontent.com/SlavaKatiukha/4160926fdd7df13ae097a5194d42023e/raw/eff5ffa6015b8f997bfa31558524033193b6092a/
onInstall:  
assert: "'${settings.custom_field}' == 'test'"
```
```json
{
"type": "update",  
"name": "Ability to dynamically determine UI in JPS",  
"onBeforeInit": "https://gist.githubusercontent.com/SlavaKatiukha/4160926fdd7df13ae097a5194d42023e/raw/eff5ffa6015b8f997bfa31558524033193b6092a/",
"onInstall": [
                { 
        "assert": [ 
            "'${settings.custom_field}' == 'test'" 
                    ]
                }
            ]
}
```
@@!
>
-   filepath in case the baseUrl was determined
@@@
```yaml
type: update  
name: "Ability to dynamically determine UI in JPS"  
baseUrl: https://gist.githubusercontent.com/SlavaKatiukha/4160926fdd7df13ae097a5194d42023e/raw/eff5ffa6015b8f997bfa31558524033193b6092a/
onBeforeInit: InitManifestTest.cs  
onInstall:  
assert: "'${settings.custom_field}' == 'test'"
``` 
```json
{
"type": "update",  
"name": "Ability to dynamically determine UI in JPS",  
"baseUrl": "https://gist.githubusercontent.com/SlavaKatiukha/4160926fdd7df13ae097a5194d42023e/raw/eff5ffa6015b8f997bfa31558524033193b6092a/" , 
"onBeforeInit": "InitManifestTest.cs",  
"onInstall": [
                { 
        "assert": [ 
            "'${settings.custom_field}' == 'test'" 
                    ]
                }
            ]
}
``` 
@@!

The script outputs JS-object. The object contains code **result** and manifest customized field set in JSON.

-   If the script has completed successfully with **result: 0**, then all the fields in the script response are applied to the manifest.  
-   In case the script has completed unsuccessfully with **result: 11041** along with message “**JPS manifest initialization error**”, the  attached object data provides the details about an error.

### onBeforeSwapExtDomains
The event is executed before swapping the external domain names between two environments via API or Jelastic dashboard

**Event Placeholders:**

-   `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `targetAppid`  - "string" application identifier of the second environment
-   `${event.response.}`:  parameters are absent

### onAfterSwapExtDomains
The event is executed after swapping the external domain names between two environments via API or Jelastic dashboard.

**Event Placeholders:**

-   `${event.params.}`:
    - `session` - current user session
    - `appid` - environment unique appid
    - `targetAppid` - "string" application identifier of the second environment
-   `${event.response.}`:
    - `result` - result code. The successful action result is '0'

### onAfterConfirmTransfer
The event is called upon user confirms changing of an environment ownership from one Jelastic account to another within a single hosting service provider. Confirmation occurs once user clicks on a link in an appropriate email.

Event subscription example:

@@@
```yaml
type: update
name: 'Environment Transfer Testing script'
 
onAfterConfirmTransfer:
  - log: env ${env.name} transfer confirmed
```
``` json
{
  "type": "update",
  "name": "Environment Transfer Testing script",
  "onAfterConfirmTransfer": [
    {
      "log": "env ${env.name} transfer confirmed"
    }
  ]
}
```
@@!

<br>

## What’s next?

- Find out how to fetch parameters with <a href="/1.6/creating-manifest/placeholders/" target="_blank">Placeholders</a>

- See how to use <a href="/1.6/creating-manifest/conditions-and-iterations/">Conditions and Iterations</a>

- Read how to integrate your <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>

- Learn how to create your custom <a href="/1.6/creating-manifest/addons/" target="_blank">Add-Ons</a>

- Check how to handle <a href="/1.6/creating-manifest/handling-custom-responses/" target="_blank">Custom Responses</a>
