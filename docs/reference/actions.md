# Actions

Actions are the building blocks that can perform arbitrary automation tasks in your environments.
For example:

- increase/decrease CPU or RAM amount  
- adjust configs according to specific environment parameters
- restart a service
- restart a container
- apply a database patch according to specific environment parameters  
...     

Default workflow for any action:

- replace [Placeholders](placeholders/)
- get target containers list *[optional]* (see the [Selecting Containers For Your Actions](#selecting-containers-for-your-actions) section) 
- check rights
- execute the action itself

Actions can be executed when an [Event](events/) with a matching filter is triggered. 
Multiple Actions can be combined together into a [Procedure](procedures/). 
Each Procedure could be executed with different input parameters using [Call](#call) action. 

## Container Operations
Actions that performs some operations inside of a container. See [Selecting Containers For Your Actions](creating-templates/selecting-containers/).

Any container operation could be done using [ExecuteShellCommands](#executeshellcommands) action. 
Nevertheless, there are also a several actions provided for convenience.
All of them could be separated in three groups:

- SSH commands ([ExecuteShellCommands](#executeshellcommands))
- Predefined modules ([Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))
- File operations ([CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))   
 
!!! note 
    > To perform any Container Operation except [ExecuteShellCommands](#executeshellcommands) Cloud Scripting executor will use a default system user with restricted permissions.    
   
### ExecuteShellCommands
Execute a several SSH commands.

**Definition**

```json
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
    Its value is wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**. 
    Where:
    - **cmd** equals a Base64 encoded string: **yes | (cmd1;cmd2)**. 
        It means that if your commands requires interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - default system user with restricted permissions.
- `sayYes` - optional parameter that enables or disables using of **yes** utility. Defaults to: **true**.    

!!! note 
    The **ExecuteShellCommands** method will fail if any of your commands write something in standard error stream  (**stderr**).
    For example,` wget` and `curl` utils will write their output to _stderr_ by default.   
    To avoid this:
          
    - you can use special flags for _curl_ : `curl -fsS http://example.com/ -o example.txt`
    - or just redirect standard error stream (_stdout_) to standard output stream (_stderr_) if it fits your needs: `curl http://example.com/ -o example.txt 2>&1` 

While accessing containers via **executeShellCommands**, a user receives all required permissions and additionally can manage the main services with sudo commands of the following kind (and others):

```no-highlight
sudo /etc/init.d/jetty start  
sudo /etc/init.d/mysql stop
sudo /etc/init.d/tomcat restart  
sudo /etc/init.d/memcached status  
sudo /etc/init.d/mongod reload  
sudo /etc/init.d/nginx upgrade  
sudo /etc/init.d/httpd help;  
```                                                        
     
**Examples**  

Execute bash script from URL for all Tomcat 6 nodes:

```example
{
  "executeShellCommands": [
    {
      "nodeType": "tomcat6",
      "commands": [
        "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
      ]
    }
  ]
}

```
                             
Download and unzip a WordPress plugin on all compute nodes: 
```example
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


Using **sudo** to reload **Nginx** balancer:

```example
{
  "executeShellCommands": [
    {
      "nodeType": "nginx",
      "commands": [
        "sudo /etc/init.d/nginx reload"
      ]
    }
  ]
}
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
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed. 

### Unpack
```
{
  "unpack": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `sourcePath`
- `destPath` 

### CreateFile
```
{
  "createFile": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
            
      "path" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path` 

### CreateDirectory
```
{
  "createFile": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
            
      "path" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path` 

### WriteFile
```
{
  "writeFile": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
            
      "path" : "string",
      "body" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path`
- `body`

### AppendFile
```
{
  "appendFile": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
            
      "path" : "string",
      "body" : "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path`
- `body`

### ReplaceInFile
```
{
  "replaceInFile": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
            
      "path" : "string",
      "replacements" : [{
        "pattern" : "string",
        "replacement" : "string"
      }]
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
One of those three parameters is required. 
- `path`
- `replacements` - the list of replacements in the configuration files on the node
    - `pattern` - regular expressions to find the string (e.g. `app\\.host\\.url\\s*=\\s*.*`)
    - `replacement` - string to replace. You can use as replacement any string value including any combination of [Placeholders](placeholders/).

<!-- DeletePath -->
<!-- RenamePath --> 

## Topology Nodes Management

### AddNodes
```
{
  "addNodes": [
    {
      "nodeType": "string",
      "extip": "boolean",      
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "displayName": "string",
      
      "dockerName": "string",
      "dockerTag": "string",
      "dockerLinks": [
        {
          "sourceNodeId": "string",
          "targetNodeId": "string",
          "alias": "string"
        }
      ],
      "dockerEnvVars": "object",
      "metadata": {
        "layer": "string"
      }
    }
  ]
}
```

- `nodeType` - container node software type. See [Container Types](/reference/container-types/). 
- `extip` *[optional]* - Attach public IP address to the container. **Default**: false
- `fixedCloudlets` *[optional]*. **Default**: 0 
- `flexibleCloudlets` *[optional]*. **Default**: 1
- `displayName` *[optional]*
- `dockerName` *[optional]* - required only if `nodeType` equals `docker`. 
- `dockerTag` *[optional]* 
- `dockerLinks` *[optional]*
    - `sourceNodeId`
    - `targetNodeId`
    - `alias`  
- `dockerEnvVars` *[optional]*
- `metadata` *[optional]*   

<!-- SetCloudletsCount -->
### SetNodeDisplayName
```
{
  "setNodeDisplayName": [
    {
      "nodeId": "string or number",
            
      "displayName" : "string"
    }
  ]
}
```

- `nodeId` - container node ID
- `displayName`

### RestartNodes
```
{
  "restartNodes": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
 
### AddContext
```
{
  "addContext": [
    {
      "name": "string",
      "fileName": "string",
      "type": "string"
    }
  ]
}
```

- `name`
- `fileName`
- `type` - context type. Possible values:
    - `ARCHIVE`
    - `GIT`
    - `SVN`

## Database Operations

### PrepareSqlDatabase
```
{
  "prepareSqlDatabase": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
      "loginCredentials": {
        "user": "string",
        "password": "string"
      },
      "newDatabaseName": "string",
      "newDatabaseUser": {
        "name": "string",
        "password": "string"
      }
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` *[optiona;]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeMission` equals `sqldb`.
- `loginCredentials`
    - `user`
    - `password`
- `newDatabaseName`
- `newDatabaseUser`
    - `name`
    - `password`

!!! note
    > Works only for `mysql5`, `mariadb`, `mariadb10` container node types.

### RestoreSqlDump
```
{
  "restoreSqlDump": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
      "databaseName": "string",
      "user": "string",
      "password": "string",
      "dump": "URL"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` *[optiona;]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeMission` equals `sqldb`.
- `databaseName` - name of the database to create
- `user` - user name in the database on behalf of which the application will be used
- `password` - password in the database on behalf of which the application will be used
- `dump` - link to the application database dump

### ApplySqlPatch
```
{
  "applySqlPatch": [
    {
      "nodeId": "number or string",
      "nodeType": "string",
      "nodeMission": "string",
      "databaseName": "string",
      "user": "string",
      "password": "string",
      "patch": "string or URL"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` *[optiona;]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeMission` equals `sqldb`.
- `databaseName` - name of the database to apply patch
- `user` - user name in the database on behalf of which the application will be used
- `password` - password in the database on behalf of which the application will be used
- `patch` - SQL query or link to such query. it is used only for SQL databases, supports [Placeholders](placeholders/).

!!! note
    > Works only for `mysql5`, `mariadb`, `mariadb10` container node types.

## Performing User-Defined Operations

### Call
Call arbitrary [Procedure](procedures/)

```
{
  "call" : "string or array of strings"
}
```

Or:

```
{
  "call" : [{
    "procedure" : "string",
    "params" : "object"
  }]
}
```

### ExecuteScript
```
{
  "executeScript": [
    {
      "type" : "string",
      "script" : "string or URL",
      "params" : "object"
    }
  ]
}
```
- `type` - script type. Possible values:
    - `js`
    - `java`
    - `php`

- `script` - script body or a link to such scirpt body
- `params` *[optional]* - script parameters

**Examples**
```example
{
  "executeScript": [
    {
      "type" : "js",
      "script" : "return '${this.greeting}';",
      "params" : {
        "greeting" : "Hello World!"
      }
    }
  ]
}
```

### InstallAddon
```
{
  "installAddon": [
    {
        "id" : "string"
    }
  ]
}
```

- `id` - an extention ID from marketplace or from `addons` section in manifest

<!-- add example -->