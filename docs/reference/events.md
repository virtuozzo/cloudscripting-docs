# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be bound to some event, i.e. executed as a result of this event occurrence.
Each event refers to a particular entity. For example, the entry point for executing any action with application is the *onInstall* event.
<br>
<br>
Subscription to a particular application lifecycle event (e.g. topology change) can be done via [Environment Level Events](#environment-level-events).
It’s also possible to bind extension execution to the *onUninstall* event - in such a way, you can implement custom logic of this extension removal from an environment.

## Application Level Events
```
{
  "jpsType": "update",
  "application": {    
    "onInstall": {},
    "onUninstall": {}
  }
}
```

### onInstall
### onUninstall

## Environment Level Events
```
{
  "jpsType": "update",
  "application": {
     "env" : {
        "onBeforeChangeTopology": {},
        "onAfterChangeTopology": {},
        "onBeforeScaleOut": {},
        "onAfterScaleOut": {},
        "onBeforeScaleIn": {},
        "onAfterScaleIn": {},
        "onBeforeRestartNode" : {},
        "onAfterRestartNode" : {},
        "onBeforeDelete" : {},
        "onAfterDelete" : {},
        "onBeforeAddNode" : {},
        "onAfterAddNode" : {},
        "onBeforeCloneNodes" : {},
        "onAfterCloneNodes" : {},
        "onBeforeLinkNode" : {},
        "onAfterLinkNode" : {},
        "onBeforeAttachExtIp" : {},
        "onAfterAttachExtIp" : {},
        "onBeforeDetachExtIp" : {},
        "onAfterDetachExtIp" : {},
        "onBeforeUpdateVcsProject" : {},
        "onAfterUpdateVcsProject" : {},
        "onBeforeSetCloudletCount" : {},
        "onAfterSetCloudletCount" : {},
        "onAfterChangeEngine" : {},
        "onBeforeChangeEngine" : {},
        "onBeforeStart" : {},
        "onAfterStart" : {},
        "onBeforeStop" : {},
        "onAfterStop" : {},
        "onBeforeClone" : {},
        "onAfterClone" : {},
        "onBeforeDeploy" : {},
        "onAfterDeploy" : {},
        "onBeforeResetNodePassword" : {},
        "onAfterResetNodePassword " : {},
        "onBeforeRemoveNode" : {},
        "onAfterRemoveNode" : {},
        "onBeforeRestartContainer" : {},
        "onAfterRestartContainer" : {},        
        "onBeforeMigrate" : {},        
        "onAfterMigrate" : {},
        "onBeforeRedeployContainer" : {},        
        "onAfterRedeployContainer" : {},  
        "onBeforeLinkDockerNodes" : {},        
        "onAfterLinkDockerNodes" : {},
        "onBeforeUnlinkDockerNodes" : {},        
        "onAfterUnlinkDockerNodes" : {},
        "onBeforeSetDockerEnvVars" : {},        
        "onAfterSetDockerEnvVars" : {},
        "onBeforeSetDockerEntryPoint" : {},        
        "onAfterSetDockerEntryPoint" : {},
        "onBeforeSetDockerRunCmd" : {},        
        "onAfterSetDockerRunCmd" : {},
        "onBeforeStartDockerService": {},
        "onAfterStartDockerService": {},
        "onBeforeAddDockerVolume" : {},        
        "onAfterAddDockerVolume" : {},
        "onBeforeRemoveDockerVolume" : {},        
        "onAfterRemoveDockerVolume" : {}                                                                                                                                                                                                        
     }
  }
}
```                              
##Event execution rules
- Such events as *Install* & *Uninstall* application, as well as *BeforeDelete* and *AfterDelete* ones (which refer to an environment deletion) can be executed just once. Other events can be used as much times as required.
- The *ScaleIn*, *ScaleOut* and *ServiceScaleOut* events are called once upon any node count change. Herewith, count of the *addNode* or *removeNode* actions’ execution refer to the number of nodes that should be added/removed per a single scaling event.
- For application server, load balancer and VPS node layers, the *cloneNodes* procedure is executed each time the node group is scaled out
- *UnlinkDockerNodes*, *LinkDockerNodes*, *SetDockerEnvVars*, *SetDockerEntryPoint*, *SetDockerRunCmd*, *AddDockerVolume* and *RemoveDockerVolume* events can be executed only once per a single *changeTopology* action
- The *StartDockerService* event can be called only once while performing the *changeTopology* and *createEnvironment* scaling actions.

## Event parameters and response placeholders
### onBeforeChangeTopology
```
{
  "event":{
    "params": {
        "env": "string"
      }
  }
}
```
### onAfterChangeTopology
```
{
  "event": {
    "params": {
      "env": "string"
    },
    "response": {
      "response": {
        "result": "number",
        "nodes": [
          {}
        ],
        "env": {},
        "right": "string"
      },
      "result": "number"
    }
  }
}
```
### onBeforeScaleOut
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    }
  }
}
```
### onAfterScaleOut
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    },
    "response": {
      "nodes": [
        {}
      ]
    }
  }
}
```
### onBeforeScaleIn
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    },
    "response": {
      "nodes": [
        {}
      ]
    }
  }
}
```
### onAfterScaleIn
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    },
    "response": {
      "nodes": [
        {}
      ]
    }
  }
}
```
### onBeforeRestartNode
```
{
  "event":{
    "params": {
        "nodeType": "string"
      }
  }
}
```
### onAfterRestartNode
```
{
  "event":{
    "params": {
        "nodeType": "string"
      },
    "response": {
          "result": "number",
          "responses": [
        {
          "result": "number",
          "nodeid": "number",
          "out": "string"
        }
      ]
    }
  }
}
```
### onBeforeDelete
```
{
  "event": {
    "params": {
      "password": "string"
    }
  }
}
```
### onAfterDelete
```
{
  "event": {
    "params": {
      "password": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeAddNode
```
{
  "event": {
    "params": {
      "extip": "boolean",
      "fixedCloudlets": "number",
      "startService": "number",
      "ismaster": "boolean",
      "flexibleCloudlets": "number",
      "nodeGroup": "string",
      "nodeType": "string",
      "metadata": "string"
    }
  }
}
```
### onAfterAddNode
```
{
  "event": {
    "params": {
      "extip": "boolean",
      "fixedCloudlets": "number",
      "startService": "number",
      "ismaster": "boolean",
      "flexibleCloudlets": "number",
      "nodeGroup": "string",
      "nodeType": "string",
      "metadata": "string"
    },
    "response": {
      "result": "number",
      "node": {}
    }
  }
}
```
### onBeforeCloneNodes
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    }
  }
}
```
### onAfterCloneNodes
```
{
  "event": {
    "params": {
      "count": "number",
      "nodeGroup": "string"
    },
    "response": {
      "result": 0,
      "className": "string",
      "array": [
        {}
      ]
    }
  }
}
```
### onBeforeLinkNode
```
{
  "event": {
    "params": {
      "parentNodes": "number",
      "childNodes": "string"
    }
  }
}
```
### onAfterLinkNode
```
{
  "event": {
    "params": {
      "parentNodes": "number",
      "childNodes": "string"
    },
    "response": {
      "result": "number",
      "infos": [
        {
          "result": "number"
        }
      ]
    }
  }
}
```
### onBeforeAttachExtIp
```
{
  "event": {
    "params": {
      "nodeid": "number"
    }
  }
}
```
### onAfterAttachExtIp
```
{
  "event": {
    "params": {
      "nodeid": "number"
    },
    "response": {
      "result": "number",
      "object": "string"
    }
  }
}
```
### onBeforeDetachExtIp
```
{
  "event": {
    "params": {
      "ip": "string",
      "nodeid": "number"
    }
  }
}
```
### onAfterDetachExtIp
```
{
  "event": {
    "params": {
      "ip": "string",
      "nodeid": "number"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeUpdateVcsProject
```
{
  "event": {
    "params": {
      "project": "string"
    }
  }
}
```
### onAfterUpdateVcsProject
```
{
  "event": {
    "params": {
      "project": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeSetCloudletCount
```
{
  "event": {
    "params": {
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "nodeGroup": "string"
    }
  }
}
```
### onAfterSetCloudletCount
```
{
  "event": {
    "params": {
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "nodeGroup": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeChangeEngine
```
{
  "event": {
    "params": {
      "settings": "string"
    }
  }
}
```
### onAfterChangeEngine
```
{
  "event": {
    "params": {
      "settings": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeStart
```
{
  "event": {
    "params": {}
  }
}
```
### onAfterStart
```
{
  "event": {
    "params": {},
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeStop
```
{
  "event": {
    "params": {}
  }
}
```
### onAfterStop
```
{
  "event": {
    "params": {},
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeClone
```
{
  "event": {
    "params": {
      "domain": "string"
    }
  }
}
```
### onAfterClone
```
{
  "event": {
    "params": {
      "domain": "string"
    },
    "response": {
      "result": "number",
      "nodes": [
        {}
      ],
      "env": {}
    }
  }
}
```
### onBeforeDeploy
```
{
  "event": {
    "params": {
      "atomicDeploy": "boolean",
      "path": "string",
      "context": "string",
      "archivename": "string"
    }
  }
}
```
### onAfterDeploy
```
{
  "event": {
    "params": {
      "atomicDeploy": "boolean",
      "path": "string",
      "context": "string",
      "archivename": "string"
    },
    "response": {
      "result": "number",
      "responses": [
        {
          "result": "number",
          "nodeid": "number",
          "out": "string"
        }
      ]
    }
  }
}
```
### onBeforeResetNodePassword
```
{
  "event": {
    "params": {
      "nodeType": "string"
    }
  }
}
```
### onAfterResetNodePassword 
```
{
  "event": {
    "params": {
      "nodeType": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeRemoveNode
```
{
  "event": {
    "params": {
      "nodeid": "number"
    }
  }
}
```
### onAfterRemoveNode
```
{
  "event": {
    "params": {
      "nodeid": "number"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeRestartContainer
```
{
  "event": {
    "params": {
      "nodeGroup": "string",
      "nodeType": "string"
    }
  }
}
```
### onAfterRestartContainer
```
{
  "event": {
    "params": {
      "nodeGroup": "string",
      "nodeType": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeMigrate
```
{
  "event": {
    "params": {
      "isOnline": "boolean",
      "hardwareNodeGroup": "string"
    }
  }
}
```
### onAfterMigrate
```
{
  "event": {
    "params": {
      "isOnline": "boolean",
      "hardwareNodeGroup": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeRedeployContainer
For Docker containers only
```
{
  "event": {
    "params": {
      "sequential": "boolean",
      "nodeId": "number",
      "tag": "string",
      "useExistingVolumes": "string"
    }
  }
}
```
### onAfterRedeployContainer
For Docker containers only
```
{
  "event": {
    "params": {
      "sequential": "boolean",
      "nodeId": "number",
      "tag": "string",
      "useExistingVolumes": "string"
    },
    "response": {
      "result": "number",
      "responses": [
        {
          "result": "number",
          "error": "",
          "nodeid": "number",
          "out": "string"
        }
      ]
    }
  }
}
```
### onBeforeLinkDockerNodes
For Docker containers only
```
{
  "event": {
    "params": {
      "groupAlias": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    }
  }
}
```
### onAfterLinkDockerNodes
For Docker containers only
```
{
  "event": {
    "params": {
      "groupAlias": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeUnlinkDockerNodes
For Docker containers only
```
{
  "event": {
    "params": {
      "alias": "string",
      "sourceNodeId": "number",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    }
  }
}
```
### onAfterUnlinkDockerNodes
For Docker containers only
```
{
  "event": {
    "params": {
      "alias": "string",
      "sourceNodeId": "number",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeSetDockerEnvVars
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "data": "string"
    }
  }
}
```
### onAfterSetDockerEnvVars
For Docker containers only
```
{
  "event": {
    "params": {
      "alias": "string",
      "sourceNodeId": "number",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeSetDockerEntryPoint
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "data": "string"
    }
  }
}
```
### onAfterSetDockerEntryPoint
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "data": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeSetDockerRunCmd
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "data": ""
    }
  }
}
```
### onAfterSetDockerRunCmd
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "data": ""
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeStartDockerService
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number"
    }
  }
}
```
### onAfterStartDockerService
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeAddDockerVolume
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "path": "string"
    }
  }
}
```
### onAfterAddDockerVolume
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "path": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### onBeforeRemoveDockerVolume
For Docker containers only
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "path": "string"
    }
  }
}
```
### onAfterRemoveDockerVolume
For Docker containers only
```
{
  "event": {
    "params": {
      "event": {
        "params": {
          "nodeId": "number",
          "path": "string"
        }
      }
    },
    "response": {
      "result": "number"
    }
  }
}
```
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