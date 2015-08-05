# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be binded to some event, i.e. executed as a result of this event occurrence.
Each event belongs to a particular entity. For example, the entry point for performing any actions with application is the application’s event onInstall.
Subscription to the particular application’s lifecycle events (e.g. topology changes) can be done via [Environment Level Events](#environment-level-events).
It’s also possible to bind the extension’s execution to the onUninstall event and in such a way implement the included to it custom logic of this extension removal from an environment.

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
        "onAfterRemoveNode" : {}
     }
  }
}
```                              
### BeforeChangeTopology
### AfterChangeTopology
### BeforeRestartNode
### AfterRestartNode
### BeforeDelete
### AfterDelete
### BeforeAddNode
### AfterAddNode
### BeforeCloneNodes
### AfterCloneNodes
### BeforeLinkNode
### AfterLinkNode
### BeforeAttachExtIp
### AfterAttachExtIp
### BeforeDetachExtIp
### AfterDetachExtIp
### BeforeUpdateVcsProject
### AfterUpdateVcsProject
### BeforeSetCloudletCount
### AfterSetCloudletCount
### onAfterChangeEngine
### onBeforeChangeEngine
### BeforeStart
### AfterStart
### BeforeStop
### AfterStop
### BeforeClone
### AfterClone
### BeforeDeploy
### AfterDeploy
### BeforeResetNodePassword
### AfterResetNodePassword 
### BeforeRemoveNode
### AfterRemoveNode


