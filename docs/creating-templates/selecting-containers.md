# Selecting Containers For Your Actions

Running a specific [action](/reference/actions/) requires to select a target container, in confines of which this action will be executed. Thus, it is possible to specify a particular container, all containers within a layer by their [*nodeGroup*](/reference/container-types/#containers-by-groups-nodegroup) value (e.g. *sql*) or all containers of the same type by their [*nodeType*](/reference/container-types/#containers-by-types-nodetype) value (e.g. *MySQL*).      

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
In the example above, a new file will be created in the compute node (*[cp]*) and a new directory will be created in the compute node (*[cp]*), balancer (*[bl]*) and node with ID *123*. Actions for the specified nodes are executed in the declared order.       

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

Learn more on this parameter [here](/reference/actions/#custom-actions).      

!!! note 
    > **Node Selectors** have higher priority than nodes specified next to the action but lower than parameters set in the action object.     

Have a look at more detailed descriptions on approaches provided for container selection:          
- [Particular Container](#particular-container)   
- [All Containers By Group](#all-containers-by-group)    
- [All Containers By Type](#all-containers-by-type)   

## Particular Container   
The `nodeId` parameter is used to select a particular container for the action to be executed at it. If you know the Node ID (displayed at the Jelastic dashboard next to the required node) of a container, you can set it statically.   
  
For example:     

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

If you don't know container's ID or container hasn't been created yet, you can set the dynamic value using special placeholders.     

For example:    

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

Visit the [Placeholders](/reference/placeholders/) documentation page for more information.      

## All Containers By Group   
 
The `nodeGroup` value is used to point out all containers within a specific layer.   

Jelastic platform supports the following predefined *nodeGroup* values:     
- *bl*  
- *cp*  
- *sqldb*   
- *nosqldb*   
- *cache*  
- *build*   
- *vds*         

Actions for a specified *nodeGroup* are executed successively one by one. For Docker containers the *nodeGroup* value is not predefined, therefore, it can be stated to any value above or your custom one. Visit the [Containers by Groups](/reference/container-types/#containers-by-group) documentation page for more information.        

## All Containers By Type
The `nodeType` parameter is applied to select all containers built upon the same software stacks. Visit the [Containers by Types](/reference/container-types/) documentation page to explore the provided containers listed according to their type.    	  

!!! note
    > If you set all three parameters, the container selection would be executed in the following order: <b>*_nodeId -> nodeGroup -> nodeType_*</b>. 
