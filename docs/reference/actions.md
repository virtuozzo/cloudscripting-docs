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
Multiple actions can be combined together into a [custom action](#custom-actions). 

## Container Operations
There are actions that perform some operations inside of a container. See the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) page.

Any container operation can be performed using [cmd](#cmd) action. Moreover, there are also several actions provided for convenience, that can be divided into three groups:   
- SSH commands ([cmd](#cmd))    
- Predefined modules ([Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))    
- File operations ([CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))       
 
!!! note 
    To process any container operation except [cmd](#cmd), Cloud Scripting executor will use a default system user with restricted permissions.    
   
### Cmd
Execute several SSH commands. 
<!--Available for all nodes.-->

**Definition**

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required. See the [Selecting Containers for your Actions](/creating-templates/selecting-containers/) section.    
- `cmd1` and `cmd2` - a set of commands that are executed. Its value is wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**.     
    Where:    
    - **cmd** - equals to a Base64 encoded string: **yes | (cmd1;cmd2)**. In case your commands require interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - default system user with restricted permissions.    
- `sayYes` - optional parameter, that enables or disables the usage of **yes** utility. The default value is *'true'*.        

One single ssh command can be passed in string. For example, executing bash script from URL for all the *Tomcat 6* nodes:
```example
{
  "cmd [tomcat6]": "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```
More info about selecting containers [here](/creating-templates/selecting-containers/).

While accessing containers via *Cmd*, a user receives all the required permissions and additionally can manage the main services with **sudo** commands of the following kinds (and others):

```no-highlight
sudo /etc/init.d/jetty start  
sudo /etc/init.d/mysql stop
sudo /etc/init.d/tomcat restart  
sudo /etc/init.d/memcached status  
sudo /etc/init.d/mongod reload  
sudo /etc/init.d/nginx upgrade  
sudo /etc/init.d/httpd help;  
```                                                        
     
**For example:**  

SSH commands can be set in array. For example:
```
{
  "cmd [tomcat6]": [
    "curl -fsSL http://example.com/script.sh | /bin/bash -s arg1 arg2"
  ]
}
```
                             
Downloading and unzipping a *WordPress* plugin on all the compute nodes: 
```example
{
  "cmd [cp]": [
    "cd /var/www/webroot/ROOT/wp-content/plugins/",
    "curl -fsSL \"http://example.com/plugin.zip\" -o plugin.zip",
    "unzip plugin.zip"
  ]
}
```
In this case commands array will be execute like one ssh command.
The same can be performed with the help of the [unpack method](/reference/actions/#unpack)


Using **sudo** to reload *Nginx* balancer:

```example
{
  "cmd [nginx]": [
    "sudo /etc/init.d/nginx reload"
  ]
}
```
   
### Api 
Executing [Jelastic Cloud API](http://docs.jelastic.com/api/)
**Examples:**

Restart all compute node in environment:    
```
{
    "api [cp]" : "jelastic.environment.control.RestartNodesByGroup"
}
```
where:

- **environment.control.RestartNodesByGroup** - Jelastic public API restart nodes by group  

Another filtering form by node group. [See more details here](/creating-templates/selecting-containers/): 
```
{
    "api" : "jelastic.environment.control.RestartNodesByGroup",
    "nodeGroup" : "cp"
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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed.   
- `sourcePath` - URL to download external file   
- `destPath` - container path where save uploaded file 

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `sourcePath` - URL to download external archive   
- `destPath` - container path where unpack uploaded archive     

### CreateFile
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
```
{
  "createFile [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.            
- `string` - container path where create file 

### CreateDirectory
Available for all nodes
<!--Available for all nodes (except for *Docker* containers and *Elastic VPS*)--> 
```
{
  "createFile [nodeId, nodeGroup, nodeType]": "string"
}
```
where:  

- `nodeId`, `nodGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.           
- `string` - container path where create directory

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                                 
- `path` - container path where write file  
- `body` - content to save in file    

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                             
- `path` - container path where write file    
- `body` - content to save in file   

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

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.                   
- `path` - path where file is available   
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

- `nodeType` - container defining software stack within a node. See [Container Types](/reference/container-types/). 
- `extip` *[optional]* - attaching public IP address to the container. The default value is *'false'*.
- `fixedCloudlets` *[optional]*. The default value is *'0'*. 
- `flexibleCloudlets` *[optional]*. The default value is *'1'*.
- `displayName` *[optional]* - node display name  
- `image` *[optional]* - docker image name and tag. Required only for docker node    
- `links` *[optional]* - docker links.   
    - `sourceNodeGroup` - sounce node for link with current node   \
    - `alias` - prefix alias for linked variables   
- `env` *[optional]* - docker environment variables
- `volumes` *[optional]* - docker node volumes 
- `volumeMounts` *[optional]* - docker external volumes mounts   
- `cmd` *[optional]* - docker run commands   
- `entrypoint` *[optional]* - docker entry points   

<!-- SetCloudletsCount -->
### SetNodeDisplayName
Available for all nodes
```
{
  "setNodeDisplayName [nodeId, nodeGroup, nodeType]": "string"
}
```
where:   

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `string` - display name for node  


### SetNodeCount
Available for all nodes (except for *Docker* containers and *Elastic VPS*)
```
{
  "setNodeCount [nodeId, nodeGroup, nodeType]": "number"
}
```
where:
  
- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `number` - nodes total count after action is finished

### SetExtIpEnabled
Available for all nodes
```
{
  "setExtIpEnabled [nodeId, nodeGroup, nodeType]": true or false
}
```
where:  

- `nodeId`, `nodeGroup`, `nodeType` - parameters that determine containers for the action to be executed. One of these parameters is required.    
- `true` or `false` - parameter that allows to attach or deatach external IP address

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

- `name` - content name    
- `fileName` - display file name at dashboard    
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
- `loginCredentials` - root creadentials for new node     
    - `user` - custom user name.     
    - `password` - custom password    
- `newDatabaseName` - custom database name    
- `newDatabaseUser` - new user with privileges only for new database    
    - `name` - custom user name     
    - `password` - custom password   

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

### script

```
{
  "script": "string or URL",
  "type": "string",
  "params": "object"
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
      "script" : "return '${this.greeting}';",
      "params" : {
        "greeting" : "Hello World!"
      }
    }
  ]
}
```

### Sleep
Custom delay. Can be set by user in milisecond. Example below shows how to create delay for one second:
```
{
  "sleep": "1000"
}
```

### installJps
Install jps manifests inside current jps. Available for jptType `install` and `update`.

**Install add-on via external link.**
`jpsType` - **update** example:
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

- `jps` - URL for custom jps manifest  
- `settings` - [user custom form](/creating-templates/user-input-parameters/)  

**Install add-on from local manifest**
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

- `onInstall` - entry point for execute actions  

**Install new environemnt via external link**
`jpsType` - **install** example:
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

- `jps` - URL for custom jps manifest  
- `envName` - new environment short domain name  
- `settings` - [user custom form](/creating-templates/user-input-parameters/)  

**Install new environemnt from local manifest**
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

- `region` - hardwareNode region  
- `envName` - new environment short domain name  
- `name` - jps name  
- `nodes` - an object of new nodes  
- `onInstall` - entry point for execute actions  


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

### Custom Actions
The declarative code inside a manifest can be divided into a separate blocks, named **actions**. Afterwards, the particular actions can be run by means of appealing to Call actions with different parameters.

The example below shows how to create new file. This manifest example call Jelastic predefined action **createFile** on compute node where is created txt file *example.txt* in tmp directory:

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

 - `createFile` - [Jelastic action](#createfile)   

The next example shows creating new custom action named *customAction*:

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

- `actions` - an object where can be predefined custom actions   

Action **customAction** can be called several times.

####Action Placeholders

In order to access any required data or parameters of allocated resources inside the manifest, a special set of placeholders should be used. Sent to the Call method parameters are transformed in a separate kit of placeholders, that can be received inside the appropriate action with the help of ${this} namespace. Access to the nodes inside environment can be performed according to the node’s type, as well as according to its role in an environment.

#### Code Reuse

Output `Hello World!` two times in `greeting.txt`:  
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

This one example shows how to pass additional parameters in custom action where it can be used in action.
Parameters should be passed as an object in custom action:

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

Write `Hello World!` and output first and second compute node IP address 
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