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
- get target containers list *[optional]* (see the [Selecting Containers For Your Actions](/creating-templates/selecting-containers/) section) 
- check rights
- execute the action itself

Actions can be executed when an [Event](events/) with a matching filter is triggered. 
Multiple Actions can be combined together into a [Procedure](procedures/). 
Each Procedure could be executed with different input parameters using [Call](#call) action. 

## Container Operations
Actions that performs some operations inside of a container. See [Selecting Containers For Your Actions](/creating-templates/selecting-containers/).

Any container operation could be done using [ExecuteShellCommands](#executeshellcommands) action. 
Nevertheless, there are also a several actions provided for convenience.
All of them could be separated in three groups:

- SSH commands ([ExecuteShellCommands](#executeshellcommands))
- Predefined modules ([Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))
- File operations ([CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))   
 
!!! note 
    To perform any Container Operation except [ExecuteShellCommands](#executeshellcommands) Cloud Scripting executor will use a default system user with restricted permissions.    
   
### ExecuteShellCommands
Execute a several SSH commands.  
Available Nodes: all

**Definition**

```json
{
  "executeShellCommands": [
    {
      "nodeId": "int or string",
      "nodeGroup" : "string",
      "nodeType" : "string",
            
      "commands": [
        "cmd1",
        "cmd2"
      ],
      
      "sayYes" : "boolean"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed. 
One of these parameters is required. See [Selecting containers for your actions](#selecting-containers-for-your-actions).
- `commands` - a set of commands that gets executed. 
    Its value is wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**. 
    Where:
    - **cmd** equals a Base64 encoded string: **yes | (cmd1;cmd2)**. 
        It means that if your commands requires interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - default system user with restricted permissions.
- `sayYes` - optional parameter that enables or disables using of **yes** utility. Defaults to: **true**.    


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
        "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
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
      "nodeGroup": "cp",
      "commands": [
        "cd /var/www/webroot/ROOT/wp-content/plugins/",
        "curl -fsSL \"http://example.com/plugin.zip\" -o plugin.zip",
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
Available Nodes: compute (except *Docker-based*)
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
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "upload": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed. 

### Unpack
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "unpack": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `sourcePath`
- `destPath` 

### CreateFile
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "createFile": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
            
      "path" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path` 

### CreateDirectory
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "createFile": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
            
      "path" : "string"
    }
  ]
}
```

- `nodeId`, `nodGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path` 

### WriteFile
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "writeFile": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
            
      "path" : "string",
      "body" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path`
- `body`

### AppendFile
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "appendFile": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
            
      "path" : "string",
      "body" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `path`
- `body`

### ReplaceInFile
Available Nodes: all except *Docker-based* and *Elastic VPS* 
```
{
  "replaceInFile": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
            
      "path" : "string",
      "replacements" : [{
        "pattern" : "string",
        "replacement" : "string"
      }]
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
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
Available Nodes: all
```
{
  "setNodeDisplayName": [
    {
      "nodeId": "string or number",     
      "nodeGroup": "string", 
      "nodeType": "string",            
      "displayName" : "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.

### SetNodeCount
Available Nodes: all (except *Docker-based* and *Elastic VPS*)
```
{
  "setNodeCount":[
   {
     "nodeId": "string or number",
     "nodeGroup": "string",
     "nodeType": "string",
     "count" : "number"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
 - `count` - total nodes count after action will be finished

###SetExtIpEnabled
Available Nodes: all
```
{
  "setExtIpEnabled": [
    {
      "nodeId": "string or number",
      "nodeGroup": "string",
      "nodeType": "string",
      "enabled" : true or false
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
- `enabled` - defines to attach aot deattach external IP address

### RestartNodes
Available Nodes: all (except *Elastic VPS*)
```
{
  "restartNodes": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.

### RestartContainers
Available Nodes: all
```
{
  "restartContainers": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determines containers on which the action should be executed.
 One of those three parameters is required.
 
### AddContext
Available Nodes: compute (except *Docker-based*)
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
Available Nodes: SQL Databases (except *Docker-based*)
```
{
  "prepareSqlDatabase": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeGroup` equals `sqldb`.
- `loginCredentials`
    - `user`
    - `password`
- `newDatabaseName`
- `newDatabaseUser`
    - `name`
    - `password`

!!! note
    Works only for `mysql5`, `mariadb`, `mariadb10` container node types.

### RestoreSqlDump
Available Nodes: SQL Databases (except *Docker-based*)
```
{
  "restoreSqlDump": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
      "databaseName": "string",
      "user": "string",
      "password": "string",
      "dump": "URL"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeGroup` equals `sqldb`.
- `databaseName` - name of the database to create
- `user` - user name in the database on behalf of which the application will be used
- `password` - password in the database on behalf of which the application will be used
- `dump` - link to the application database dump

### ApplySqlPatch
Available Nodes: SQL Databases (except *Docker-based*)
```
{
  "applySqlPatch": [
    {
      "nodeId": "number or string",
      "nodeGroup": "string",
      "nodeType": "string",
      "databaseName": "string",
      "user": "string",
      "password": "string",
      "patch": "string or URL"
    }
  ]
}
```

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determines containers on which the action should be executed.
**Default**: `nodeGroup` equals `sqldb`.
- `databaseName` - name of the database to apply patch
- `user` - user name in the database on behalf of which the application will be used
- `password` - password in the database on behalf of which the application will be used
- `patch` - SQL query or link to such query. it is used only for SQL databases, supports [Placeholders](placeholders/).

!!! note
    Works only for `mysql5`, `mariadb`, `mariadb10` container node types.

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
      "script" : "string or URL",
      "type" : "string",      
      "params" : "object"
    }
  ]
}
```
- `script` - script body or a link to such scirpt body
- `type` *[optional]* - script type. Possible values:
    - `js`
    - `java`   
    - `php`. Removed from CS version 0.9 and Jelastic version 5.0   
**Default**: js
- `params` *[optional]* - script parameters

!!! note
    Learn more about using [Jelastic Cloud API](http://docs.jelastic.com/api/)
       
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

### ForEach

Iterable object map:

```
{
  "env": {
    "nodes": [],
    "contexts": [],
    "extdomains": []
  },
  "nodes": {},
  "settings": {},
  "license": {},
  "event": {
    "params": {},
    "response": {}
  },
  "this": {}
}
```
- `settings` - fields values predefined at [user setting form](http://docs.cloudscripting.local/creating-templates/user-input-parameters/) (Optional).
- `license` - parameters from prepopulate action (Optional).
- `event` - object of parameters from [events](http://docs.cloudscripting.local/reference/events/). This parameters separate on before and after event parameters (Optional). So [actions](/reference/actions/) can be used before and after executing event.
- `this` - parameters object is sent with procedures name(Optional). Mode details about `this` parameter is [here](/reference/placeholders/#procedure-placeholders)

####Iteration can be executed by `env.nodes`, `nodes`, `env.contexts` and `env.extdomains` objects:

```
{
  "forEach(env.extdomains)": [
    {
      "writeFile": {
        "nodeGroup": "cp",
        "path": "/var/lib/jelastic/keys/${@i}.txt",
        "body": "hello"
      }
    }
  ]
}
```

- `@i` - default iterator name

```
{
  "forEach(env.contexts)": [
    {
      "writeFile": {
        "nodeGroup": "cp",
        "path": "/var/lib/jelastic/keys/${@i.context}.txt",
        "body": "1"
      }
    }
  ]
}
```

- `env.contexts` - deployed in environment contexts
- `env.extdomains` - binded external domains 

Full placeholders list [here](/reference/placeholders/)

Scaling nodes example:
```
{
	"jpsType": "install",
	"application": {
		"name": "Scaling Example",
		"env": {
			"onAfterScaleIn[nodeGroup:cp]": {
				"call": "ScaleNodes"
			},
			"onAfterScaleOut[nodeGroup:cp]": {
				"call": "ScaleNodes"
			}
		},
		"procedures": [{
			"id": "ScaleNodes",
			"onCall": [{
				"forEach(nodes.cp)": {
					"execCmd": {
						"commands": [
							"{commands to rewrite all Compute nodes internal IP addresses in balancer configs. Here balancer node is NGINX}",
							"/etc/init.d/nginx reload"
						],
						"nodeGroup": "bl"
					}
				}
			}]
		}]
	}
}
```
In `execCmd` action compute nodes addresses are rewrited in balancer node and reload nginx service.
Events are `onAfterScaleIn` and `onAfterScaleOut` will executed after add or remove compute node.

####Iteration by all nodes in environment:

```
{
  "forEach(env.nodes)": [{
    "executeShellCommands": {
	  "nodeId": "${@i.id}",
		"commands": [
	      "echo ${@i.address} > /tmp/example.txt"
		]
	}
  }]
}
```

####Iteration by compute nodes with custom iterator name:
```
{
  "forEach(cp:nodes.cp)": {
    "execCmd" : {
      "nodeId": "${@cp.id}",
      "nodeGroup": "${@cp.nodeGroup}",
      "nodeType": "${@cp.nodeType}",
      "commands": [
        "echo ${@cp.address} > /tmp/example.txt"
      ]
    }
  }
}
```

- `@cp` - custom iterator name (optional)

Custom iterator name can be used for nesting cycles one into another:
```
{
  "forEach(item:env.nodes)": [
    {
      "forEach(env.nodes)": [
        {
          "execCmd": {
            "nodeId": "${@i.id}",
            "commands": "[[ '${@i.id}' -eq '${@item.id}' ]] && touch /tmp/${@}.txt || touch /tmp/${@}${@}.txt"
          }
        }
      ]
    }
  ]
}
```
- `@` iterator number

In this case every environment node will have only one conjunction by nodeId.