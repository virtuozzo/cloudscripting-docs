# Selecting Containers For Your Actions

Some actions require a list of containers in which the action will be executed.
There are three ways to select the containers.

- [Particular Container](#particular-container)
- [All Containers By Group](#all-containers-by-group) 
- [All Containers By Type](#all-containers-by-type)

Also there are thee ways to set container filters:

* **Node Selectors** - select node in action name. For example:
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
In this example new file will be created in compute node and new directory will be created in compute node, balancer, and node with id *123*. All node selectors will be executed in declaration order.  

* set node parameters near the action. For example:
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
There parameter *nodeGroup* is available for two actions - `createFile` and `createDirectory`. So these actions will be executed on same **nodeGroup**.

* set required node as parameter in action object;

Node Selectors have higher priority than node parameters near the action but lower than parameters set in action object.   

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