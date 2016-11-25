# Actions

Actions are the building blocks that perform arbitrary automation functions in your environment. Such as:                
- increasing/decreasing CPU or RAM amount     
- adjusting configs according to specific environment's parameters     
- restarting a service           
- restarting a container                  
- applying a database patch according to specific environment's parameters                  
     
The default workflow for any action is the following:   
- replacing [placeholders](placeholders/)    
- getting target containers list *[optional]* (see the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) section)     
- checking permissions    
- executing the action itself    

Actions are executed when the called [event](events/) matches specified filter rules. 
Multiple actions can be combined together into a [procedure](procedures/). 
It is possible to execute each procedure with different input parameters using a [call](#call) action. 

## Container Operations
There are actions that perform some operations inside of a container. See the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) page.

Any container operation can be performed using [ExecuteShellCommands](#executeshellcommands) action. Moreover, there are also several actions provided for convenience, that can be divided into three groups:   
- SSH commands ([ExecuteShellCommands](#executeshellcommands))    
- Predefined modules ([Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))    
- File operations ([CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))       
 
!!! note 
    To process any container operation except [ExecuteShellCommands](#executeshellcommands), Cloud Scripting executor will use a default system user with restricted permissions.    
   
### ExecuteShellCommands
Execute several SSH commands. Available for all nodes.

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
where:  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required. See the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) section.    
- `commands` - a set of commands that are executed. Its value is wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**.     
    Where:    
    - **cmd** - equals to a Base64 encoded string: **yes | (cmd1;cmd2)**. In case your commands require interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - default system user with restricted permissions.    
- `sayYes` - optional parameter, that enables or disables the usage of **yes** utility. The default value is *'true'*.        


While accessing containers via *executeShellCommands*, a user receives all the required permissions and additionally can manage the main services with <b>sudo</b> commands of the following kinds (and others):

```no-highlight
sudo /etc/init.d/jetty start  
sudo /etc/init.d/mysql stop
sudo /etc/init.d/tomcat restart  
sudo /etc/init.d/memcached status  
sudo /etc/init.d/mongod reload  
sudo /etc/init.d/nginx upgrade  
sudo /etc/init.d/httpd help;  
```                                                        
     
<b>For example:</b>  

Executing bash script from URL for all the *Tomcat 6* nodes:

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
                             
Downloading and unzipping a *WordPress* plugin on all the compute nodes: 
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
The same can be performed with the help of the unpack method: --link--


Using <b>sudo</b> to reload *Nginx* balancer:

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
Available for compute nodes (except for *Docker* containers)
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
Available for all nodes (except for *Docker* containers and *Elastic VPS*)
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
where:  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. 

### Unpack
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `sourcePath`    
- `destPath`     

### CreateFile
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.            
- `path` 

### CreateDirectory
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:  
- `nodeId`, `nodGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.           
- `path` 

### WriteFile
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                                 
- `path`    
- `body`    

### AppendFile
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                             
- `path`    
- `body`    

### ReplaceInFile
Available for all nodes (except for *Docker* containers and *Elastic VPS*) 
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                   
- `path`    
- `replacements` - the list of replacements within the node's configuration files    
    - `pattern` - regular expressions to find the string (e.g. `app\\.host\\.url\\s*=\\s*.*`)    
    - `replacement` - string to replace. You can use as replacement any string value, including any combination of [placeholders](placeholders/).    

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

- `nodeType` - container defining software stack within a node. See [Container Types](/reference/container-types/). 
- `extip` *[optional]* - attaching public IP address to the container. The default value is *'false'*.
- `fixedCloudlets` *[optional]*. The default value is *'0'*. 
- `flexibleCloudlets` *[optional]*. The default value is *'1'*.
- `displayName` *[optional]*
- `dockerName` *[optional]* - required only if `nodeType` equals to `docker`
- `dockerTag` *[optional]* 
- `dockerLinks` *[optional]*
    - `sourceNodeId`
    - `targetNodeId`
    - `alias`  
- `dockerEnvVars` *[optional]*
- `metadata` *[optional]*   

<!-- SetCloudletsCount -->
### SetNodeDisplayName
Available for all nodes
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    

### SetNodeCount
Available for all nodes (except for *Docker* containers and *Elastic VPS*)
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
where:  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
 - `count` - nodes total count after action is finished

###SetExtIpEnabled
Available for all nodes
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
where:  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `enabled` - parameter that allows to attach or deatach external IP address

### RestartNodes
Available for all nodes (except for *Elastic VPS*)
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.  

### RestartContainers
Available for all nodes
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.   
 
### AddContext
Available for compute nodes (except for *Docker* containers)
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
where:  
- `name`    
- `fileName`    
- `type` - context type with the following possible values:    
    - `ARCHIVE`    
    - `GIT`    
    - `SVN`    

## Database Operations

### PrepareSqlDatabase
Available nodes: *SQL* Databases (except for *Docker* containers)
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
where:   
- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed.
By default `nodeGroup` equals to `sqldb`.    
- `loginCredentials`    
    - `user`    
    - `password`    
- `newDatabaseName`    
- `newDatabaseUser`    
    - `name`    
    - `password`    

!!! note
    The function is executed only with `mysql5`, `mariadb` and `mariadb10` node types.

### RestoreSqlDump
Available nodes: *SQL* Databases (except for *Docker* container)
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
where:
- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed.
By default `nodeGroup` equals to `sqldb`.    
- `databaseName` - name of the database to be created    
- `user` - user name in the database, on behalf of which the application will be used    
- `password` - password in the database, on behalf of which the application will be used    
- `dump` - link to the application database dump    

### ApplySqlPatch
Available Nodes: *SQL* Databases (except for *Docker* containers)
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
where:  
- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed.
By default `nodeGroup` equals to `sqldb`.    
- `databaseName` - name of the database for patch to be applied    
- `user` - user name in the database, on behalf of which the application will be used    
- `password` - password in the database, on behalf of which the application will be used    
- `patch` - *SQL* query or link to such a query. It is used only for *SQL* databases. Here, the [placeholders](placeholders/) support is available.    

!!! note
    The function is executed only with `mysql5`, `mariadb` and `mariadb10` node types.

## Performing User-Defined Operations

### Call
Call arbitrary [procedure](procedures/).

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
where:   
- `script` - script body or a link to such a script body    
- `type` *[optional]* - script type with the following possible values:    
    - `js`    
    - `java`      
The default value is *'js'*.    
- `params` *[optional]* - script parameters    

!!! note
    Learn more about using [Jelastic Cloud API](http://docs.jelastic.com/api/).
       
<b>For example:</b>
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
where:  
- `id` - an extension ID from the *marketplace* or from the *add-ons* section in the manifest

<!-- add example -->