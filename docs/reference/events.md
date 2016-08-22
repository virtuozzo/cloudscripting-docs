# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be bound to some event, i.e. executed as a result of this event occurrence.
Each event belongs to a particular entity. For example, the entry point for performing any actions with application is the application’s event *onInstall*.
Subscription to a particular application’s lifecycle events (e.g. topology changes) can be done via [Environment Level Events](#environment-level-events).
It’s also possible to bind extension’s execution to the *onUninstall* event and, in such a way, implement the included to it custom logic of this extension removal from an environment.

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

### Install
### Uninstall

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

## Events parameters and response placeholders
### BeforeChangeTopology
```
{
  "event":{
    "params": {
        "session": "string",
        "actionkey": "string",
        "hx_lang": "string",
        "charset": "string",
        "appid": "string",
        "env": "string",
        "ruk": "string"
      }
  }
}
```
### AfterChangeTopology
```
{
  "event": {
    "params": {
      "session": "string",
      "actionkey": "string",
      "hx_lang": "string",
      "charset": "string",
      "appid": "string",
      "env": "string",
      "ruk": "string"
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
### BeforeRestartNode
```
{
  "event":{
    "params": {
        "session": "string",
        "actionkey": "string",
        "hx_lang": "string",
        "charset": "string",
        "appid": "string",
        "nodeType": "string",
        "ruk": "string"
      }
  }
}
```
### AfterRestartNode
```
{
  "event":{
    "params": {
        "session": "string",
        "actionkey": "string",
        "hx_lang": "string",
        "charset": "string",
        "appid": "string",
        "nodeType": "string",
        "ruk": "string"
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
### BeforeDelete
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "password": "string",
      "ruk": "string"
    }
  }
}
```
### AfterDelete
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "password": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeAddNode
```
{
  "event": {
    "params": {
      "extip": "boolean",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "fixedCloudlets": "number",
      "startService": "number",
      "ismaster": "boolean",
      "flexibleCloudlets": "number",
      "appid": "string",
      "nodeGroup": "string",
      "nodeType": "string",
      "metadata": "string"
    }
  }
}
```
### AfterAddNode
```
{
  "event": {
    "params": {
      "extip": "boolean",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "fixedCloudlets": "number",
      "startService": "number",
      "ismaster": "boolean",
      "flexibleCloudlets": "number",
      "appid": "string",
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
### BeforeCloneNodes
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "count": "number",
      "session": "string",
      "actionkey": "string",
      "appid": "number",
      "nodeGroup": "string"
    }
  }
}
```
### AfterCloneNodes
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "count": "number",
      "session": "string",
      "actionkey": "string",
      "appid": "number",
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
### BeforeLinkNode
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "parentNodes": "number",
      "session": "string",
      "appid": "string",
      "childNodes": "string"
    }
  }
}
```
### AfterLinkNode
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "parentNodes": "number",
      "session": "string",
      "appid": "string",
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
### BeforeAttachExtIp
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string",
      "nodeid": "number"
    }
  }
}
```
### AfterAttachExtIp
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string",
      "nodeid": "number"
    },
    "response": {
      "result": "number",
      "object": "string"
    }
  }
}
```
### BeforeDetachExtIp
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string",
      "ip": "string",
      "nodeid": "number"
    }
  }
}
```
### AfterDetachExtIp
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string",
      "ip": "string",
      "nodeid": "number"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeUpdateVcsProject
```
{
  "event": {
    "params": {
      "project": "string",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    }
  }
}
```
### AfterUpdateVcsProject
```
{
  "event": {
    "params": {
      "project": "string",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeSetCloudletCount
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "appid": "string",
      "nodeGroup": "string"
    }
  }
}
```
### AfterSetCloudletCount
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "appid": "string",
      "nodeGroup": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeChangeEngine
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "settings": "string",
      "appid": "string"
    }
  }
}
```
### AfterChangeEngine
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "settings": "string",
      "appid": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeStart
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    }
  }
}
```
### AfterStart
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeStop
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    }
  }
}
```
### AfterStop
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeClone
```
{
  "event": {
    "params": {
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "domain": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    }
  }
}
```
### AfterClone
```
{
  "event": {
    "params": {
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "domain": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
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
### BeforeDeploy
```
{
  "event": {
    "params": {
      "atomicDeploy": "boolean",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "path": "string",
      "context": "string",
      "appid": "string",
      "charset": "string",
      "archivename": "string",
      "ruk": "string"
    }
  }
}
```
### AfterDeploy
```
{
  "event": {
    "params": {
      "atomicDeploy": "boolean",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "path": "string",
      "context": "string",
      "appid": "string",
      "charset": "string",
      "archivename": "string",
      "ruk": "string"
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
### BeforeResetNodePassword
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "charset": "string",
      "appid": "string",
      "nodeType": "string",
      "ruk": "string"
    }
  }
}
```
### AfterResetNodePassword 
```
{
  "event": {
    "params": {
      "session": "string",
      "hx_lang": "string",
      "charset": "string",
      "appid": "string",
      "nodeType": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeRemoveNode
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "session": "string",
      "actionkey": "string",
      "appid": "string",
      "nodeid": "number"
    }
  }
}
```
### AfterRemoveNode
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "session": "string",
      "actionkey": "string",
      "appid": "string",
      "nodeid": "number"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeRestartContainer
```
{
  "event": {
    "params": {
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "nodeGroup": "string",
      "nodeType": "string",
      "ruk": "string"
    }
  }
}
```
### AfterRestartContainer
```
{
  "event": {
    "params": {
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "nodeGroup": "string",
      "nodeType": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeMigrate
```
{
  "event": {
    "params": {
      "isOnline": "boolean",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "hardwareNodeGroup": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    }
  }
}
```
### AfterMigrate
```
{
  "event": {
    "params": {
      "isOnline": "boolean",
      "actionkey": "string",
      "session": "string",
      "hx_lang": "string",
      "hardwareNodeGroup": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeRedeployContainer
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "sequential": "boolean",
      "nodeId": "number",
      "actionkey": "string",
      "session": "string",
      "tag": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string",
      "useExistingVolumes": "string"
    }
  }
}
```
### AfterRedeployContainer
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "sequential": "boolean",
      "nodeId": "number",
      "actionkey": "string",
      "session": "string",
      "tag": "string",
      "hx_lang": "string",
      "appid": "string",
      "charset": "string",
      "ruk": "string",
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
### BeforeLinkDockerNodes
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "groupAlias": "string",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "appid": "string",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    }
  }
}
```
### AfterLinkDockerNodes
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "groupAlias": "string",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "appid": "string",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeUnlinkDockerNodes
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "appid": "string",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    }
  }
}
```
### AfterUnlinkDockerNodes
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "appid": "string",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeSetDockerEnvVars
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "actionkey": "string",
      "session": "string",
      "data": "string",
      "appid": "string"
    }
  }
}
```
### AfterSetDockerEnvVars
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "alias": "string",
      "sourceNodeId": "number",
      "appid": "string",
      "targetNodeId": "number",
      "isAutoRestart": "boolean"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeSetDockerEntryPoint
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "data": "string",
      "appid": "string"
    }
  }
}
```
### AfterSetDockerEntryPoint
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "data": "string",
      "appid": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeSetDockerRunCmd
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "data": "",
      "appid": "string"
    }
  }
}
```
### AfterSetDockerRunCmd
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "data": "",
      "appid": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeStartDockerService
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string"
    }
  }
}
```
### AfterStartDockerService
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "appid": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeAddDockerVolume
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "path": "string",
      "appid": "string"
    }
  }
}
```
### AfterAddDockerVolume
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "path": "string",
      "appid": "string"
    },
    "response": {
      "result": "number"
    }
  }
}
```
### BeforeRemoveDockerVolume
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "nodeId": "number",
      "_rnd": "number",
      "actionkey": "string",
      "session": "string",
      "path": "string",
      "appid": "string"
    }
  }
}
```
### AfterRemoveDockerVolume
Only for Docker&reg;
```
{
  "event": {
    "params": {
      "event": {
        "params": {
          "nodeId": "number",
          "_rnd": "number",
          "actionkey": "string",
          "session": "string",
          "path": "string",
          "appid": "string"
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

Events can be filtered by *nodeGroup*, *nodeType*, *nodeId*. Events filtering is optional. By default every event is listened by all environment.
So defined actions will be executed only when called events match specified filter rules.

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
- `number` - *nodeId* value
