# Selecting Containers For Your Actions

Some actions require a list of containers in which the action will be executed.
There are three ways to select the containers.

- [Particular Container](#particular-container)
- [All Containers By Type](#all-containers-by-type)
- [All Containers By Role](#all-containers-by-role) 

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

See the [Placeholders](placeholders/) documentation for more information.

## All Containers By Type
Use `nodeType` parameter to select all container nodes by software type.

See [Container Types](/reference/container-types/).      	

list of available node types. Sync exec one by one.  
available noteTypes  
See [All Containers By Role](#all-containers-by-role) if you don't know your containers software type or it's not static.  

## All Containers By Role
 
`nodeMission`
list of available node missions. Sync exec one by one,
available nodeMission

- `bl`
- `cp`
- `sqldb`
- `nosqldb`
- `cache`
- `build`
- `vds`
- `docker`


!!! note
    > If you set all three parameters, a container selection would work in the following order: _nodeId -> nodeType -> nodeMission_  - fix
    