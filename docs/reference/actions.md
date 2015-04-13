# Actions

## Container operations

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
### ExecuteShellCommands
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