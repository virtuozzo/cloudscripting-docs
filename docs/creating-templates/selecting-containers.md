# Selecting Containers For Your Actions

Running a specific [action](/reference/actions/) requires to select a target container, in confines of which this action will be executed. Thus, it is possible to specify a particular container, all containers within a layer by their [*nodeGroup*](/reference/container-types/#containers-by-groups-nodegroup) value (e.g. *sql*) or all containers of the same type by the [*nodeType*](/reference/container-types/#containers-by-types-nodetype) value (e.g. *MySQL*).  

Also, there are three possible approaches to set containers filtering:

* **Node Selectors** - specifying a target node within the name of the action 

For example:
```
[{
    "createFile [cp]" : {
          "path" : "/tmp/test.txt"
    }
}, {
    "createDirectory [cp,bl,123]" : {
          "path" : "/tmp/test.txt"
    }
}]
```
In the example above, a new file will be created in the compute node (*[cp]*) and new directory will be created in the compute node (*[cp]*), balancer (*[bl]*), and node with ID *123*. Actions for the specified nodes are be executed in the declared order.     

* setting a target node next to the performed action   

For example:     
```
{
  "createFile": {
    "path": "/tmp/test.txt"
  },
  "createDirectory": {
    "path": "/tmp/test"
  },
  "nodeGroup": "cp"
}
``` 
Herein, the `createFile` and `createDirectory` actions are applied to the specified *nodeGroup*, namely compute node (*[cp]*).     
 
* setting a required node as a parameter in the action object

!!! note 
    > **Node Selectors** have higher priority than nodes specified next to the action but lower than parameters set in the action object.   

Have a look at a detailed description on approaches provided for container selection:
- [Particular Container](#particular-container)
- [All Containers By Group](#all-containers-by-group) 
- [All Containers By Type](#all-containers-by-type)

## Particular Container
Use `nodeId` parameter to select a particular container.
If you know the ID of a container on which you want to perform an action, you can set it statically:  

```
{
  "writeFile": [
    {
      "nodeId": "123",
      "path": "/var/www/webroot/hw.txt",
      "body": "Hello World!"      
    }
  ]
}
```

If you don't know the container's ID or the container does not created yet, you can set the value dynamically using special placeholders:  

```
{
  "writeFile": [
    {
      "nodeId": "${nodes.apache2[0].id}",
      "path": "/var/www/webroot/hw.txt",
      "body": "Hello World!"
    }
  ]
}
```

See the [Placeholders](/reference/placeholders/) documentation for more information.

## All Containers By Type
Use `nodeType` parameter to select all container nodes by software type.

See [Container Types](/reference/container-types/).      	

list of available node types. Sync exec one by one.
available noteTypes
See [All Containers By Role](#all-containers-by-group) if you don't know your containers software type or it's not static.  

## All Containers By Group
 
`nodeGroup`
list of available predefined node groups. Sync exec one by one,
available nodeGroup

- `bl`
- `cp`
- `sqldb`
- `nosqldb`
- `cache`
- `build`
- `vds`

In Docker® case nodeGroup is not defined, it can be any.

!!! note
    > If you set all three parameters, a container selection would work in the following order: _nodeId -> nodeGroup -> nodeType_
    
More details about nodeGroup [here](/reference/container-types/#containers-by-group)