# Events

Any action, available to be performed by means of API (including custom users’ scripts running), should be binded to some event, i.e. executed as a result of this event occurrence. Each event belongs to a particular entity. For example, the entry point for performing any actions with environment is the environment’s event onInit.

Subscription to the particular application’s lifecycle events (e.g. topology changes) can be done via add-ons. It’s also possible to bind the add-on’s execution to the onUninstall event and in such a way implement the included to it custom logic of this addon removal from an environment.

## Application Level Events

### Install
### Uninstall

## Environment Level Events

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
### BeforeStart
### AfterStart
### BeforeStop
### AfterStop
### BeforeDeploy
### AfterDeploy
### BeforeResetNodePassword
### AfterResetNodePassword 
### BeforeRemoveNode
### AfterRemoveNode


