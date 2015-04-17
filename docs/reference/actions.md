# Actions

## Selecting containers for your actions
Большинсво операций должно производиться над определенными нодами топологии.   
Некоторые действия   
Есть три способа выбора нод, над которыми производится действие:

### Select one specific container by `nodeId`
 
The value could be static:

    {
      "writeFile": [
        {
          "nodeId": "123",
          
          "path": "/var/www/webroot/hw.txt",
          "body": "Hello World!"
        }
      ]
    }

If you don't know the node ID or the node does not created yet, you can set the value dynamically using special placeholders:  

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

More info about node placeholders in 

### Select all containers in layer by `nodeType`
list of available node types     

### Select all containers in layer by `nodeMission`
list of available node missions

!!! note
    > If you set all three parameters, a container selection would work in the following order: _nodeId -> nodeType -> nodeMission_  - fix

## Container operations

### ExecuteShellCommands

**Scheme:**

```
{
  "executeShellCommands": [
    {
      "nodeId": "int",
      "nodeType" : "string",
      "nodeMission" : "string",
            
      "commands": [
        "command1",
        "command2"
      ],
      
      "user" : "string"
    }
  ]
}
```

**Example:**
```
{}
```

### Deploy
```
{
  "deploy": [
    {
      "archive": "URL",
      "name": "string",
      "context": "string"
    }
  ]
}
```

### Upload
```
{
  "upload": [
    {
      "nodeId": "number",
      "nodeType": "string",
      "nodeMission": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```
### Unpack
### CreateFile
### CreateDirectory
### WriteFile
### AppendFile
### ReplaceInFile
### DeletePath
### RenamePath
### AddContext

## Topology Nodes Management

### AddNodes
### SetCloudletsCount
### SetNodeDisplayName
### RestartNodes

## Database operations

### PrepareSqlDatabase
### RestoreSqlDump
### ApplySqlPatch

## Performing user-defined operations

### Call
### ExecuteScript
### InstallAddon