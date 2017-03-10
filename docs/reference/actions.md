# Actions

Actions represent a scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">script custom actions</a> using <a href="https://docs.jelastic.com/api/" target="_blank">API calls</a>, Linux bash shell command, JS, and Java scripts.                 

With the help of actions you can achieve automation of the tasks related to:                                              
* increasing or decreasing CPU or RAM amount      
* adjusting configs according to specific environment's settings              
* restarting a service or a container                 
* applying a database patch according to specific environment's settings                                  

The default workflow for any action execution is the following:                  
* replacing <a href="http://docs.cloudscripting.com/reference/placeholders" target="_blank">placeholders</a>                                     
* getting a list of target containers (for a detailed guidance, see the <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Container</em></a> page)                
* checking permissions        
* executing the action itself         

Actions are executed when the called <a href="http://docs.cloudscripting.com/reference/events" target="_blank">event</a> matches specified filtering rules.               

Thus, the following specific groups of actions are singled out:               
* [Container Operations](#container-operations)                   
* [Topology Nodes Management](#topology-nodes-management)             
* [Database Operations](#database-operations)                  
* [User-Defined Operations](#user-defined-operations)                        

## Container Operations

There are actions that perform operations inside of a container. For a detailed guidance on how to set a target container, visit the <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Containers</e</a> page.                        

Any container operation can be performed using a [*cmd*](#cmd) action. Moreover, there are also some additional actions provided for your convenience. Thus, all the actions performed in confines of a container can be divided into three groups:                  
* SSH commands ([*cmd*](#cmd))                          
* predefined modules ([*deploy*](#deploy), [*upload*](#upload), [*unpack*](#unpack))           
* operations with files ([*createFile*](#createfile), [*createDirectory*](#createdirectory), [*writeFile*](#writefile), [*appendFile*](#appendfile), [*replaceInFile*](#replaceinfile))                     

!!! note 
    To process any container operation (except for [cmd](#cmd)), the Cloud Scripting executor will use a default system user with restricted permissions.                   

### cmd

The *cmd* action executes <a href="https://docs.jelastic.com/ssh-overview" target="_blank">SSH</a> commands.             
<!--Available for all nodes.-->      

**Example**                  
``` json
{
  "cmd [nodeId,nodeType,nodeGroup]": [
    "cmd1",
    "cmd2"
  ],
  "sayYes" : true
}
```
where:       
     
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required). For a detailed guidance, see the <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Containers</em></a> section.                   
- `cmd1` and `cmd2` - set of commands that are being executed. Their values are wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**.     
    Where:    
    - **cmd** - is equal to a Base64 encoded string: **yes | (cmd1;cmd2)**. In case your commands require the interactive input, by default the Cloud Scripting executor will always try to give a positive answer, using **yes** utility.        
    - **user** - default system user with restricted permissions    
- `sayYes` *[optional]* - parameter that enables or disables using **yes** utility. The default value is *'true'*.                  

A single SSH command can be passed in a string. For example, executing a bash script from URL for all *Tomcat 6* nodes.                    
``` json 
{
  "cmd [tomcat6]": "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```
Learn more about <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Container</em></a> for your actions within the pointed guide.                      

While accessing containers via *cmd*, a user receives all the required permissions and additionally can manage the main services with **sudo** commands of the following types (and others).            
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

Setting SSH commands in an array.                    
``` json
{
  "cmd [tomcat6]": [
    "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
  ]
}
```
                             
Downloading and unzipping a WordPress plugin on all the compute nodes. Here, the commands array is executed through a single SSH command. The same can be performed with the help of the [unpack](#unpack) method.                              
``` json
{
  "cmd [cp]": [
    "cd /var/www/webroot/ROOT/wp-content/plugins/",
    "curl -fsSL \"http://example.com/plugin.zip\" -o plugin.zip",
    "unzip plugin.zip"
  ]
}
```

Herewith, the commands array is executed through a single SSH command. The same can be performed with the help of the [unpack](/reference/actions/#unpack) method.                       

Using **sudo** to reload Nginx balancer.       
``` json
{
  "cmd [nginx]": [
    "sudo /etc/init.d/nginx reload"
  ]
}
```
   
### api

Executing actions available by means of the <a href="http://docs.jelastic.com/api" target="_blank">Jelastic Cloud API</a> methods.     

There are a number of parameters required by Jelastic API, which are defined automatically:
* *envName* - environment domain name where the API method is executed     
* *appid* - unique environment identifier that can be passed into API instead of the *envName*     
* *session* - unique session of a current user            

Target containers, selected for API methods execution can be passed by the node keywords. API methods can be executed at all nodes within a single <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-group" target="blank"><em>nodeGroup</em></a> (i.e. layer) or <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-type" target="blank"><em>nodeType</em></a>. Also, API methods can be run on a <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#particular-container" target="_blank">particular node</a>. In this case, the Node ID is required, which is available either through the <a href="http://docs.cloudscripting.com/reference/placeholders/#node-placeholders" target="_blank">node placeholders</a> or a set of [custom action parameters](#custom-actions) (*this*).

**Examples**

Restarting all compute nodes in an environment.                      
``` json
{
    "api [cp]" : "jelastic.environment.control.RestartNodesByGroup"
}
``` 
where:        
       
- `api [cp]` - specifying a target node group for the API method to be executed at (e.g. *cp*). Learn more details about <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Container</em></a> within the linked page.                                        
- *jelastic.environment.control.RestartNodesByGroup* - Jelastic API method for restarting nodes by group              

This parameter (*jelastic.environment.control.RestartNodesByGroup*) can be simplified like shown in the example below.    
``` json
{
    "api [cp]" : "environment.control.RestartNodesByGroup"
}
```

Below, you can find one more approach to specify a target node group for the API method to be executed at.                               
``` json
{
    "api" : "jelastic.environment.control.RestartNodesByGroup",
    "nodeGroup" : "cp"
}
```
Learn more about <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers" target="_blank"><em>Specifying Target Container</em></a> for your API actions within the linked guide.                                        
        
### deploy

Available for compute nodes (except for *Docker* containers)
``` json
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
where:

- `archive` - URL to the archive with a compressed application
- `name` - application's name that will be displayed at the dashboard
- `context`- desired context for the deployed app

### upload

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)-->
``` json
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
- `sourcePath` - URL to download an external file                    
- `destPath` - container path where the uploaded file is to be saved                         

### unpack

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
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
- `sourcePath` - URL to download an external archive   
- `destPath` - container path where the uploaded archive is to be unpacked                               

### createFile

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
{
  "createFile [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                          
- `string` - container path where a file is to be created                              

### createDirectory

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
{
  "createDirectory [nodeId, nodeGroup, nodeType]": "string"
}
```
where:  

- `nodeId`, `nodGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                       
- `string` - container path where a directory is to be created                         

### writeFile

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
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
- `path` - container path where a file is to be written                
- `body` - content that is saved to the file                                         

### appendFile

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
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
- `path` - container path where a file is to be appended                                 
- `body` - content saved to the file                               

### replaceInFile

Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VDS*)--> 
``` json
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
- `path` - path where a file is available               
- `replacements` - list of replacements within the node's configuration files                        
    - `pattern` - regular expressions to find a string (e.g. *app\\.host\\.url\\s*=\\s*.**)                   
    - `replacement` - you can use as a replacement any string value, including any combination of <a href="http://docs.cloudscripting.com/reference/placeholders" target="_blank">placeholders</a>                                            

<!-- DeletePath -->
<!-- RenamePath --> 

## Topology Nodes Management

### addNodes
``` json
{
  "addNodes": [
    {
      "nodeType": "string",
      "extip": "boolean",      
      "fixedCloudlets": "number",
      "flexibleCloudlets": "number",
      "displayName": "string",
      "dockerName": "jelastic/wordpress-web:latest",
      "registryUrl": "string",
      "registryUser": "string",
      "registryPassword": "string",
      "dockerTag": "string",
      "dockerLinks": "sourceNodeGroup:alias",
      "dockerEnvVars": "object",
      "dockerVolumes": "array",
      "volumeMounts": "object",
      "dockerRunCmd": "array",
      "dockerEntryPoint": "object"
    }
  ]
}
```
where:

- `nodeType` *[required]* - parameter thet defines software stack. For a detailed guidance, see the <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#predefined-nodetype-values" target="_blank">Container Types</a> page. For docker containers `nodeType` value is **docker**.                        
- `extip` *[optional]* - attaching public IP address to a container. The default value is *'false'*.                     
- `fixedCloudlets` *[optional]* - number of reserved cloudlets. The default value is *'0'*.                             
- `flexibleCloudlets` *[optional]* - number of dynamic cloudlets. The default value is *'1'*.                           
- `displayName` *[optional]* - node's display name (i.e. <a href="https://docs.jelastic.com/environment-aliases" target="_blank">alias</a>)                                         
    The following parameters are required for Docker nodes only:                          
- `dockerName` *[optional]* - name and tag of Docker image
- `registryUrl` *[optional]* - custom docker regitry
- `registryUser` *[optional]* - docker registry username
- `registryPassword` *[optional]* - docker registry password
- `dockerTag` - docker tag to installing
- `dockerLinks` *[optional]* - Docker links                         
    - `sourceNodeGroup` - source node to be linked with a current node                                
    - `alias` - prefix alias for linked variables                         
- `dockerEnvVars` *[optional]* - Docker environment variables                        
- `dockerVolumes` *[optional]* - Docker node volumes               
- `volumeMounts` *[optional]* - Docker external volumes mounts                             
- `dockerRunCmd` *[optional]* - Docker run configs                            
- `dockerEntryPoint` *[optional]* - Docker entry points                                          

<!-- SetCloudletsCount -->
### setNodeDisplayName

Available for all nodes
``` json
{
  "setNodeDisplayName [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                        
- `string` - node’s display name (i.e. <a href="https://docs.jelastic.com/environment-aliases" target="_blank">alias</a>)                                                                        


### setNodeCount

Available for all nodes
``` json
{
  "setNodeCount [nodeId, nodeGroup, nodeType]": "number"
}
```
where:

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                
- `number` - total number of nodes after the action is finished                                          

### setExtIpEnabled
Available for all nodes
``` json
{
  "setExtIpEnabled [nodeId, nodeGroup, nodeType]": true or false
}
```
where:               

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed at (one of these parameters is required)                                   
- `true` or `false` - parameter that allows to attach or detach public IP address                              

### restartNodes

Available for all nodes (except for *Elastic VDS*)
``` json
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

### restartContainers

Available for all nodes
``` json
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

### addContext

Available for compute nodes (except for *Docker* containers)
``` json
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
- `fileName` - name of the file to be displayed at the dashboard                         
- `type` - context type with the following possible values:                             
    - `ARCHIVE`    
    - `GIT`    
    - `SVN`    

## Database Operations

### prepareSqlDatabase

Available for *SQL* databases (except for *Docker* containers)
``` json
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at. By default the *nodeGroup* value is equal to *sqldb*.                            
- `loginCredentials` - root creadentials to a new node                    
    - `user` - username                    
    - `password` - password                 
- `newDatabaseName` - your custom database name              
- `newDatabaseUser` - new user with privileges granted only for a new database instance                           
    - `name` - custom username that is set for a new database  
    - `password` - custom password that is generated for a new database 

!!! note
    The function is executed only for *mysql5*, *mariadb* and *mariadb10* containers.                          

### restoreSqlDump

Available for *SQL* databases (except for *Docker* container)
``` json
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at. By default the *nodeGroup* value is equal to *sqldb*.                                    
- `databaseName` - name of a database that is created                  
- `user` - username in the database, on behalf of which the application will be used                
- `password` - password in the database, on behalf of which the application will be used                         
- `dump` - URL to the application's database dump                                

### applySqlPatch

Available for *SQL* databases (except for *Docker* containers)                                 
``` json
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

- `nodeId`, `nodeGroup`, `nodeType` *[optional]* - parameters that determine containers for the action to be executed at. By default the *nodeGroup* value is equal to *sqldb*.                                   
- `databaseName` - name of a database for a patch to be applied                    
- `user` - username in the database, on behalf of which the application will be used                                          
- `password` - password in the database, on behalf of which the application will be used                              
- `patch` - *SQL* query or a link to it. It is used only for *SQL* databases. Here, the <a href="http://docs.cloudscripting.com/reference/placeholders" target="_blank">placeholders</a> support is available.                    

!!! note
    The function is executed only for *mysql5*, *mariadb* and *mariadb10* containers.                         

## User-Defined Operations

### script

``` json
{
  "script": "string or URL",
  "type": "string",
  "params": "object"
}
```
where:   

- `script` - script body or a link to it                                                
- `type` *[optional]* - script type with the following possible values (the default value is *'js'*):                                          
    - `js`    
    - `java`      
- `params` *[optional]* - script parameters                               

<b>Example</b>
``` json
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
    Learn more about using <a href="http://docs.jelastic.com/api" target="_blank">Jelastic Cloud API</a>.    

### sleep
Setting a delay that is measured in milliseconds. The below example shows how to create a delay for one second.                                               
``` json
{
  "sleep": "1000"
}
```

### install
Nesting a JPS manifest inside the current manifest file. The nested JPS manifest will be installed subsequently after the current one. The action is available for *install* and *update* installation types.                              

**Examples**

Installing add-on via the external link (with *update* type).            
``` json
{
  "install" : {
    "jps" : "http://example.com/manifest.jps",
    "settings" : {
      "myparam" : "test"
    }
  }
}
```
where:

- `jps` - URL to your custom JPS manifest  
- `settings` - user <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">custom form</a>           

Installing add-on from the local manifest.         
``` json
{
  "install" : {
    "type" : "update",
    "name" : "test",
    "onInstall" : {
      "log" : "install test"
    }
  }
}
```
where:

- `onInstall` - entry point for performed actions                                 

Installing a new environment via the external link (with *install* type).                 
``` json
{
  "install" : {
    "jps" : "http://example.com/manifest.jps",
    "envName" : "env-${fn.random}",
    "settings" : {
      "myparam" : "test"
    }
  } 
}
```
where: 

- `jps` - URL to your custom JPS manifest                    
- `envName` - short domain name of a new environment                                   
- `settings` - user <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">custom form</a>                                               

Installing a new environment from the local manifest.             
``` json
{
  "install" : {
    "type" : "install",
    "region" : "dev",
    "envName" : "env-${fn.random}",
    "name" : "test",
    "nodes" : {
         "nodeType" : "apache2",
          "cloudlets" : 16
    },
    "onInstall" : {
      "log" : "install test"
    }
  }
}
```
where:

- `region` - hardware node region                        
- `envName` - short domain name of a new environment                     
- `name` - JPS name  
- `nodes` - object of new nodes                   
- `onInstall` - entry point for performed actions               


### installAddon

You can install a few custom add-ons within a single manifest, therefore, add-ons can be installed to:             
* an existing environment, if installation type is *update*  
* a new environment, if installation type is *install*. In this case, add-ons will be installed sequentially one by one right after a new environment set up.     

All the add-ons will have installation type *update* by default.   

The example below shows how to pass the add-on identifier to *installAddon* action. This add-on should be described in the *addons* section. The custom add-on with the *firstAddon* identifier will create a new file in a compute node in the *tmp* directory.
``` json
{
	"type": "update",
	"name": "Install Add-on example",
	"onInstall": {
		"installAddon": {
			"id": "firstAddon"
		}
	},
	"addons": [{
		"id": "firstAddon",
		"name": "firstAddon",
		"onInstall": {
			"createFile [cp]": "/tmp/exampleFile.txt"
		}
	}]
}
```
where:  

- `id` - identifier for a custom add-on                           

The installed add-ons can be located within the **Add-ons** tab at the Jelastic dashboard. 

<center>![new-addon](/img/new-addon.png)</center>

In the following example, the *nodeGroup* parameter is passed to the *installAddon* action, targeting an add-on at the *bl* (balancer) node group.                    
``` json
{
  "installAddon": {
    "id": "firstAddon",
    "nodeGroup": "bl"
  }
}
```

Consequently, the installed add-on will be marked as set up at the balancer (*bl*) layer. 

<!-- add example -->

### Custom Actions

The declarative code inside a manifest can be divided into separate blocks, named **actions**. Subsequently, particular actions can be run by means of calling actions with different parameters.             

The example below shows how to create a new file (e.g. the <b>*example.txt*</b> file in the <b>*tmp*</b> directory) by executing a *createFile* action at the compute node.                 
``` json
{
  "type": "update",
  "name": "execution actions",
  "onInstall": {
    "createFile [cp]": "/tmp/example.txt"
  }
}
```
where: 

 - `createFile` - corresponding [*createFile*](#createfile) action                     

The next example illustrates how to create a new custom action (i.e. *customAction*), which can be called for several times.                                                        
``` json
{
	"type": "update",
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

- `actions` - object where custom actions can be predefined                                    

#### Action Placeholders

In order to access any required data or parameters of allocated resources inside a manifest, a special set of placeholders should be used. The parameters, sent to a call method, are transformed into a separate kit of placeholders, which can be further used within the appropriate actions by means of *${this}*  namespace. Access to a node inside environment can be gained according to its type, as well as according to its role in the environment.                           

#### Code Reuse

Outputting Hello World! twice in the <b>*greeting.txt*</b>:  
``` json
{
  "type": "update",
  "name": "Actions Example",
  "onInstall": [
    {
      "createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
    },
    "greeting",
    "greeting"
  ],
  "actions": {
    "greeting": {
      "appendFile [cp]": [
        {
          "path": "${SERVER_WEBROOT}/greeting.txt",
          "body": "Hello World!"
        }
      ]
    }
  }
}
```

#### Call Action with Parameters

The following example shows how to pass additional parameters to the custom action. The parameters should be passed as an object to the custom action.                 

``` json
{
	"type": "update",
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

Writing Hello World! and outputting the first and the second compute nodes IP addresses.                                                             
``` json
{
  "type": "update",
  "name": "Action Example",
  "onInstall": [
    {
      "createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
    },
    "greeting",
    "greeting",
    {
      "log": {
        "message": "${nodes.cp[0].address}"
      }
    },
    {
      "log": {
        "message": "${nodes.cp[1].address}"
      }
    }
  ],
  "actions": {
    "greeting": {
      "appendFile [cp]": {
        "path": "${SERVER_WEBROOT}/greeting.txt",
        "body": "Hello World!"
      }
    },
    "log": {
      "appendFile [cp]": {
        "path": "${SERVER_WEBROOT}/greeting.txt",
        "body": "${this.message}"
      }
    }
  }
}
```