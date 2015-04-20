# Actions

## General action workflow

- replace
- select a containers
- check rights
- execute the action itself

## Selecting containers for your actions

Большинсво операций должно производиться над определенными нодами топологии.   
Есть три способа выбора нод, над которыми производится действие:

### Select one specific container by `nodeId`
 
The value could be static:

    {
      "writeFile": [
        {
          "nodeId": "123",
          
          "path": "/var/www/webroot/hw.txt",
          "body": "Hello World!"
          ...
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
list of available node types. Sync exec one by one.     

### Select all containers in layer by `nodeMission`
list of available node missions. Sync exec one by one,

!!! note
    > If you set all three parameters, a container selection would work in the following order: _nodeId -> nodeType -> nodeMission_  - fix

## Container operations

### ExecuteShellCommands


**Definition:**

```
{
  "executeShellCommands": [
    {
      "nodeId": "int or string",
      "nodeType" : "string",
      "nodeMission" : "string",
            
      "commands": [
        "cmd1",
        "cmd2"
      ],
      
      "sayYes" : "boolean"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed. 
One of these parameters is required. See [Selecting containers for your actions](#selecting-containers-for-your-actions).
- `commands` - a set of commands that gets executed. 
    Its value is wrapped by the underlying Cloud Scripting executor via __echo cmd | base64 -d | su user__. 
    Where:
    - __cmd__ equals a Base64 encoded string: __yes | (cmd1;cmd2)__. 
        It means that if your commands requires interactive input, by default the Cloud Scripting executor will always try to give a positive answer using __yes__ utility.        
    - __user__ - default system user with restricted permissions.
- `sayYes` - optional parameter that enables or disables using of __yes__ utility. Defaults to: __true__.    

!!! note 
    The __ExecuteShellCommands__ method will fail if any of your commands write something in standard error stream (__stderr__).
    For example,` wget` and `curl` utils will write their output to _stderr_ by default.   
    To avoid this:
          
    - you can use special flags for _curl_ : `curl -fsS http://example.com/ -o example.txt`
    - or just redirect standard error stream (_stdout_) to standard output stream (_stderr_) if it fits your needs: `curl http://example.com/ -o example.txt 2>&1` 
     
**Examples**

Download and unzip a WordPress plugin on all compute nodes:
 
```
{
  "executeShellCommands": [
    {
      "nodeMission": "cp",
      "commands": [
        "cd /var/www/webroot/ROOT/wp-content/plugins/",
        "curl -fsS \"http://example.com/plugin.zip\" -o plugin.zip",
        "unzip plugin.zip"
      ]
    }
  ]
}
```
The same could be done by unpack method: --link--

Example 2

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