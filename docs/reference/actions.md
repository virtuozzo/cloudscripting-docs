# Actions

Actions represent the building blocks that perform arbitrary automation functions in your environment, such as:         
- increasing/decreasing CPU or RAM amount     
- adjusting configs according to specific environment's settings             
- restarting a service           
- restarting a container                  
- applying a database patch according to specific environment's settings                                 

The default workflow for any action execution is the following:                             
- replacing [placeholders](placeholders/)         
- getting a list of target containers *[optional]* (for a detailed guidance see the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) section)         
- checking permissions       
- executing the action itself        

Actions are executed when the called [event](events/) matches specified filtering rules. Multiple actions can be combined together into a [custom action](#custom-actions).                 

Thus, the following specific groups of actions are singled out:                 
- [container operations](#container-operations)                  
- [topology management](#topology-nodes-management)            
- [database operations](#database-operations)                 
- [user-defined operations](#performing-user-defined-operations)                       

## Container Operations
There are actions that perform operations inside of a container. For a detailed guidance on how to define a target container visit the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) page.            

Any container operation can be performed using a [cmd](#cmd) action. Herewith, there are also some additional actions provided for your convenience. Thus, all the actions performed in confines of a container can be divided into three groups:                                  
- SSH commands (e.g. [cmd](#cmd))                        
- predefined modules (e.g. [Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))          
- operations with files (e.g. [CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))                    
 
!!! note 
    To process any container operation (except for [cmd](#cmd)), the Cloud Scripting executor will use a default system user with restricted permissions.                   
   
### Cmd   

The *cmd* action executes [SSH](https://docs.jelastic.com/ssh-overview) commands.            
<!--Available for all nodes.-->      

**Example**                  

```json
{
  "cmd [nodeId,nodeType,nodeGroup]": [
    "cmd1",
    "cmd2"
  ],
  "sayYes" : true
}
```
where:       
     
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required). For a detailed guidance see the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) section.              
- `cmd1` and `cmd2` - a set of commands that are being executed. Their values are wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**.     
    Where:    
    - **cmd** - is equal to a Base64 encoded string: **yes | (cmd1;cmd2)**. In case your commands require the interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - a default system user with restricted permissions    
- `sayYes` *[optional]* - the parameter that enables or disables using **yes** utility. The default value is *'true'*.                  

A single SSH command can be passed in a string. For example, executing a bash script from *URL* for all *Tomcat 6* nodes:                 
```example 
{
  "cmd [tomcat6]": "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```
Learn more about [selecting a target container](/creating-templates/selecting-containers/) for your actions within the pointed guide.                   

While accessing containers via *cmd*, a user receives all the required permissions and additionally can manage the main services with **sudo** commands of the following types (and others):       

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

Setting SSH commands in an array:                    
```
{
  "cmd [tomcat6]": [
    "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
  ]
}
```
                             
Downloading and unzipping a *WordPress* plugin on all compute nodes:                
```example
{
  "cmd [cp]": [
    "cd /var/www/webroot/ROOT/wp-content/plugins/",
    "curl -fsSL \"http://example.com/plugin.zip\" -o plugin.zip",
    "unzip plugin.zip"
  ]
}
```
Herewith, the commands' array is executed through a single SSH command.                             
The same can be performed with the help of the [unpack](/reference/actions/#unpack) method.                     


Using **sudo** to reload *Nginx* balancer:

```example
{
  "cmd [nginx]": [
    "sudo /etc/init.d/nginx reload"
  ]
}
```
   
### API 
Executing actions available by means of the [Jelastic Cloud API](http://docs.jelastic.com/api/) methods.                                        

**Examples:**

Restarting all compute nodes in the environment:                      
```
{
    "api [cp]" : "jelastic.environment.control.RestartNodesByGroup"
}
``` 
where:        
       
- `[cp]` - specifying a target node group for API method to be executed at (e.g. *cp*)                                   
- *environment.control.RestartNodesByGroup* - Jelastic API method for restarting nodes by group                                                             

Below you can find one more approach to specify a target node group for API method to be executed at:                               
```
{
    "api" : "jelastic.environment.control.RestartNodesByGroup",
    "nodeGroup" : "cp"
}
```
Learn more about [selecting a target container](/creating-templates/selecting-containers/) for your API actions within the linked guide.                                      
        
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
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)-->
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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at                      
- `sourcePath` - *URL* to download an external file                    
- `destPath` - the container path, where the uploaded file is to be saved                         

### Unpack
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                    
- `sourcePath` - *URL* to download an external archive   
- `destPath` - the container path, where the uploaded archive is to be unpacked                               

### CreateFile
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
```
{
  "createFile [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                          
- `string` - a container path, where a file is to be created                              

### CreateDirectory
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
```
{
  "createDirectory [nodeId, nodeGroup, nodeType]": "string"
}
```
where:  

- `nodeId`, `nodGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                       
- `string` - a container path, where a directory is to be created                         

### WriteFile
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
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
  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                                      
- `path` - the container path, where a file is to be written                
- `body` - content saved to the file                                         

### AppendFile
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                            
- `path` - the container path, where a file is to be appended                                 
- `body` - content saved to the file                               

### ReplaceInFile
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                       
- `path` - the path, where a file is available               
- `replacements` - the list of replacements within the node's configuration files                        
    - `pattern` - regular expressions to find the string (e.g. `app\\.host\\.url\\s*=\\s*.*`)                   
    - `replacement` - the string to replace. Herewith, you can use as replacement any string value, including any combination of [placeholders](placeholders/).                                 

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
      "image": "jelastic/wordpress-web:latest",
      "links": "sourceNodeGroup:alias",
      "env": "object",
      "volumes": "array",
      "volumeMounts": "object",
      "cmd": "array",
      "entrypoint": "object"
    }
  ]
}
```
where:

- `nodeType` - the parameter defining software stack within a node. For a detailed guidance see the [Container Types](/reference/container-types/) page.                        
- `extip` *[optional]* - attaching public IP address to a container. The default value is *'false'*.                     
- `fixedCloudlets` *[optional]* - a number of reserved cloudlets. The default value is *'0'*.                             
- `flexibleCloudlets` *[optional]* - a number of dynamic cloudlets. The default value is *'1'*.                           
- `displayName` *[optional]* - node's display name (i.e. [alias](https://docs.jelastic.com/environment-aliases))                                  
    The following parameters are required for Docker nodes only:                          
- `image` *[optional]* - name and tag of Docker image                            
- `links` *[optional]* - Docker links                         
    - `sourceNodeGroup` - a source node to be linked with a current node                                
    - `alias` - a prefix alias for linked variables                         
- `env` *[optional]* - Docker environment variables                        
- `volumes` *[optional]* - Docker node volumes               
- `volumeMounts` *[optional]* - Docker external volumes mounts                             
- `cmd` *[optional]* - Docker run configs                            
- `entrypoint` *[optional]* - Docker entry points                                          

<!-- SetCloudletsCount -->
### SetNodeDisplayName
Available for all nodes
```
{
  "setNodeDisplayName [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                        
- `string` - node’s display name (i.e. [alias](https://docs.jelastic.com/environment-aliases))                                                                    


### SetNodeCount
Available for all nodes (except for *Docker* containers and *Elastic VPS*)
```
{
  "setNodeCount [nodeId, nodeGroup, nodeType]": "number"
}
```
where:

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                
- `number` - nodes’ total count after action is finished                                          

### SetExtIpEnabled
Available for all nodes
```
{
  "setExtIpEnabled [nodeId, nodeGroup, nodeType]": true or false
}
```
where:               

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                   
- `true` or `false` - the parameter that allows to attach or deatach external IP address                              

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                   

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                       
 
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

- `name` - context’s name    
- `fileName` - the name of the file to be displayed at the dashboard                         
- `type` - the context type with the following possible values:                             
    - `ARCHIVE`    
    - `GIT`    
    - `SVN`    

## Database Operations

### PrepareSqlDatabase
Available for *SQL* databases (except for *Docker* containers)
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at.             
By default the `nodeGroup` value is equal to `sqldb`.                       
- `loginCredentials` - root creadentials for a new node                    
    - `user` - your custom user name                    
    - `password` - your custom password                 
- `newDatabaseName` - your custom database name              
- `newDatabaseUser` - a new user with privileges granted only for a new database instance                           
    - `name` - the custom user name     
    - `password` - the custom password   

!!! note
    The function is executed only for `mysql5`, `mariadb` and `mariadb10` containers.                          

### RestoreSqlDump
Available for *SQL* databases (except for *Docker* container)
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at.                 
By default the `nodeGroup` value is equal to `sqldb`.                         
- `databaseName` - the name of the database to be created                  
- `user` - the user name in the database, on behalf of which the application will be used                
- `password` - the password in the database, on behalf of which the application will be used                         
- `dump` - *URL* to the application's database dump                                

### ApplySqlPatch
Available for *SQL* databases (except for *Docker* containers)                                 
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at.
By default the `nodeGroup` value is equal to `sqldb`.                       
- `databaseName` - the name of the database for a patch to be applied                    
- `user` - the user name in the database, on behalf of which the application will be used                                          
- `password` - the password in the database, on behalf of which the application will be used                              
- `patch` - *SQL* query or link to such a query. It is used only for *SQL* databases. Here, the [placeholders](placeholders/) support is available.                    

!!! note
    The function is executed only for `mysql5`, `mariadb` and `mariadb10` containers.                         

## Performing User-Defined Operations

### Script

```
{
  "script": "string or URL",
  "type": "string",
  "params": "object"
}
```
where:   

- `script` - the script body or a link to it                                                
- `type` *[optional]* - the script type with the following possible values (the default value is *'js'*):                                          
    - `js`    
    - `java`      
- `params` *[optional]* - script parameters                               

<b>For example:</b>
```example
{
  "executeScript": [
    {
      "script" : "return '${this.greeting}';",
      "params" : {
        "greeting" : "Hello World!"
      }
    }
  ]
}
```
!!! note
    Learn more about using [Jelastic Cloud API](http://docs.jelastic.com/api/).

### Sleep
Setting a delay that is measured in milliseconds. The below example shows how to create the delay for one second:                                    
```
{
  "sleep": "1000"
}
```

### installJps
Nesting a *JPS* manifest inside the current manifest file. The nested *JPS* manifest will be installed subsequently after the current one.                  
The action is available for **install** and **update** *jpsType* modes.                         

**Examples**

**Installing add-on via the external link (with *update* `JpsType`):**
```
{
  "installJps" : {
    "jps" : "http://example.com/manifest.jps",
    "settings" : {
      "myparam" : "test"
    }
  }
}
```
where:

- `jps` - *URL* to your custom JPS manifest  
- `settings` - [user custom form](/creating-templates/user-input-parameters/)  

**Installing add-on from the local manifest:**
```
{
  "installJps" : {
    "jpsType" : "update",
    "name" : "test",
    "onInstall" : {
      "log" : "installJps test"
    }
  }
}
```
where:

- `onInstall` - an entry point for performed actions                                 

**Installing a new environment via the external link (with *install* `JpsType`):**
```
{
  "installJps" : {
    "jps" : "http://example.com/manifest.jps",
    "envName" : "env-${fn.random}",
    "settings" : {
      "myparam" : "test"
    }
  } 
}
```
where: 

- `jps` - *URL* to your custom JPS manifest                    
- `envName` - a short domain name of a new environment                                   
- `settings` - [user custom form](/creating-templates/user-input-parameters/)                          

**Installing a new environment from the local manifest:**
```
{
  "installJps" : {
    "jpsType" : "install",
    "region" : "dev",
    "envName" : "env-${fn.random}",
    "name" : "test",
    "nodes" : {
         "nodeType" : "apache2",
          "cloudlets" : 16
    },
    "onInstall" : {
      "log" : "installJps test"
    }
  }
}
```
where:

- `region` - hardware node’s region                        
- `envName` - a short domain name of a new environment                     
- `name` - JPS name  
- `nodes` - an object of new nodes                   
- `onInstall` - an entry point for performed actions               


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

- `id` - an extension *ID* from the *marketplace* or from the *add-ons* section in the manifest                         

<!-- add example -->

### Custom Actions
The declarative code inside a manifest can be divided into separate blocks, named **actions**. Subsequently, the particular actions can be run by means of appealing to call actions with different parameters.             

The example below shows how to create a new file (e.g. the *example.txt* file in the *tmp* directory) by executing a *createFile* action at the compute node:                
```
{
  "jpsType": "update",
  "name": "execution actions",
  "onInstall": {
    "createFile [cp]": "/tmp/example.txt"
  }
}
```
where: 

 - `createFile` - the corresponding *createFile* [action](#createfile)               

The next example illustrates how to create a new custom action (i.e. *customAction*), which can be called for several times:                                      

```
{
	"jpsType": "update",
    "name": "execution actions",
	"onInstall": "customAction",
	"actions": {
		"customAction": {
			"createFile [cp]": "/tmp/example.txt"
		}
	}
}
```
where:  

- `actions` - an object, where custom actions can be predefined                                    

#### Action Placeholders

In order to access any required data or parameters of allocated resources inside a manifest, a special set of placeholders should be used. Parameters sent to a call method are transformed into a separate kit of placeholders, which can be received inside the appropriate action with the help of *${this}* namespace. Access to a node inside environment can be performed according to its type, as well as according to its role in the environment.                           

#### Code Reuse

Outputting `Hello World!` twice in the *greeting.txt*:  
```
{
  "jpsType": "update",
  "name": "Procedures Example",
  "onInstall": [
    {
      "createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
    },
    {
      "call": [
        "greeting",
        "greeting"
      ]
    }
  ],
  "actions": {
    "greeting": {
      "appendFile": [
        {
          "nodeGroup": "cp",
          "path": "${SERVER_WEBROOT}/greeting.txt",
          "body": "Hello World!"
        }
      ]
    }
  }
}
```

#### Call action with parameters 

The following example shows how to pass additional parameters to the custom action, where it can be used in action.                     
Parameters should be passed as an object into custom action:                       


```
{
	"jpsType": "update",
    "name": "execution actions",
	"onInstall": {
		"customAction": {
			"fileName": "example.txt"
		}
	},
	"actions": {
		"customAction": {
			"createFile [cp]": "/tmp/${this.fileName}.txt"
		}
	}
}
```
where:

- `fileName` - additional parameter

Writing `Hello World!` and outputting first and second compute node's IP address:                                    
```
{
	"jpsType": "update",
	"name": "Action Example",
	"onInstall": [{
		"createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
	}, {
		"call": [
			"greeting",
			"greeting", {
				"log": {
					"message": "${nodes.cp[0].address}"
				}
			}, {
				"log": {
					"message": "${nodes.cp[1].address}"
				}
			}
		]
	}],
	"actions": {
		"greeting": {
			"appendFile": [{
				"nodeGroup": "cp",
				"path": "${SERVER_WEBROOT}/greeting.txt",
				"body": "Hello World!"
			}]
		},
		"log": {
			"appendFile": [{
				"nodeGroup": "cp",
				"path": "${SERVER_WEBROOT}/greeting.txt",
				"body": "${this.message}"
			}]
		}
	}
}
```