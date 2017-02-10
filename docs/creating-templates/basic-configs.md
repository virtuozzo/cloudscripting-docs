# Basic Configs

The above two units display the outer side of a JPS usage and now let’s have a closer look at the inner side - a code of a package with all required configurations.

The JPS manifest is a file with <b>*.json*</b> extension, which contains an appropriate code written in JSON format. This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for a successful installation of an application. The basis of the code is represented by the following string:

```
{
    "type": "string",
    "name": "any require name"
}
```

- *type*
    - `install` - application    
    - `update` - extension    
- *name* - JPS custom name           

This is a mandatory body part of the application package, which includes the information about JPS name and the type of the application installation (the <b>*'install'*</b> mode initiates a new environment creation required for a deployment, the <b>*'update'*</b> mode performs actions on the existing environment).
This basic string should be extended with the settings required by the application you are packing. The following configuration details are included beside the <b>*'type': { }*</b> parameter:

<h2>Application Workflow</h2>

**Basic Template**
```
{
  "type": "string",
  "name": "string",
  "baseUrl": "string",
  "settings": "object",
  "version": "string",
  "appVersion": "string",
  "nodes": "array",
  "engine": "string",
  "region": "string",
  "displayName": "string",
  "ssl": "boolean",
  "ha": "boolean",
  "description": "object/string",
  "categories": "array",
  "logo": "string",
  "homepage": "string",
  "type": "string",
  "success": "object/string",
  "startPage": "string",
  "actions": "array",
  "addons": "array",
  "onInstall": "object/array"
}
```

- `name` *[required]* - JPS custom name      
- `baseUrl` *[optional]* - custom <a href="http://docs.cloudscripting.com/creating-templates/relative-links/" target="_blank">relative links</a>                                       
- `settings` *[optional]* - custom form with <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">predefined user input elements</a>                        
- `version` - *[optional]* - JPS type supported by the Jelastic Platform. See the <a href="http://docs.cloudscripting.com/jelastic-cs-correspondence/" target="_blank">correspondence between version</a> page.
- `appVersion` *[optional]* - custom version of an application            
- `nodes` - object to describe information about nodes for an installation. Required option for **type** `install`.               
- `engine` *[optional]* - engine <a href="http://docs.cloudscripting.com/reference/container-types/#engine-versions-engine" target="_blank">version</a>, by **default** `java6`            
- `region` *[optional]* - region, where an environment will be installed. Required option for **type** `install`.             
- `displayName` *[optional]* - display name for an environment. Required option for **type** `install`.          
- `ssl` *[optional]* - Jelastic SSL status for an environment, by **default** `false`             
- `ha` *[optional]* - high availability for Java stacks, by **default** `false`                                
- `description` - text string that describes a template. This section should always follow the template format version section.            
- `categories` - categories available for manifests filtering                                        
- `logo` *[optional]* - JPS image that will be displayed within custom add-ons                    
- `homepage` *[optional]* - link to any external aplication source            
- `type` *[optional]* - language type of an application                
- `success` *[optional]* - success text that will be sent via email and will be displayed at the dashboard after installation          
- `startPage` *[optional]* - path to be opened via the **Open in browser** button through a successful installation message                                        
- `actions` *[optional]* - objects to describe all <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank">custom actions</a>             
- `addons` *[optional]* - includes JPS manifests with the **type** `update` as a new JPS installation      
- `onInstall` *[optional]* - <a href="http://docs.cloudscripting.com/reference/events/#oninstall" target="_blank">event</a> that is an entry point for actions execution                               

##Docker Actions

Specific Cloud Scripting actions for Docker containers include operations of *volumes*, *links* and *environment variables* management.
<br>
<!--**Volumes**-->

There are three available parameters to set Docker volumes:  
- *volumes* - list of volume paths   
- *volumeMounts* - mount configurations  
- *volumesFrom* - list of nodes the volumes are imported from    

All of the fields are set within the Docker object:
```
{
  "type": "install",
  "name": "docker volumes",
  "nodes": [
    {
      "nodeGroup": "sqldb",
      "image": "centos:7",
      "volumes": [],
      "volumeMounts": {},
      "volumesFrom": []
    }
  ]
}
```
<h3>Volumes</h3>
This field represents a string array:  
```
[
  {
    "volumes": [
      "/external",
      "/data",
      "/master",
      "/local"
    ]
  }
]
```

<h3>VolumeMounts</h3>
This parameter is an object. It can be set like within the example below:    
```
{
  "volumeMounts": {
    "/example-path": {
      "sourcePath": "",
      "sourceNodeId": 0,
      "sourceNodeGroup": "",
      "sourceHost": "",
      "readOnly": true
    }
  }
}
```
Here:  

- `/example-path` - path to place the volume at a target node  
- `sourcePath [optional]` - default value that repeats volume path (*/example-path* in our sample)    
- `sourceNodeId` -  node identifier the volume should be mounted from (optional, in case of the `sourceNodeGroup` parameter using)       
- `sourceHost [optional]` - parameter for <a href="https://docs.jelastic.com/configure-external-nfs-server" target="_blank">external mounts</a> usage    
- `readOnly` - defines write data permissions at source node, the default value is `false`   
- `sourceNodeGroup` - any available <a href="http://docs.cloudscripting.com/reference/container-types/#containers-by-groups-nodegroup" target="_blank">*nodeGroup*</a> within a source environment (ignored if the `sourceNodeId` parameter is specified). The list of mounted volumes is defined by a master node.    

In case not all source node volumes are required to be mounted, the particular ones can be specified:
```
[
  {
    "sourceNodeGroup": "storage",
    "volumes": [
      "/master",
      "/local"
    ]
  }
]
```

<h4>*VolumeMounts* examples</h4>
 
**Master Node Mount:**   
Samples to mount a particular volume by exact node identifier & path (*/master*) and to mount all volumes from the layer master node by *nodeGroup* (*/master-1*)
```
{
  "volumeMounts": {
    "/master": {
      "sourcePath": "/master",
      "sourceNodeId": 81725,
      "readOnly": true
    },
    "/master-1": {
      "sourceNodeGroup": "current-node-group"
    }
  }
}
```

Here, *sourcePath* and *readOnly* parameters are optional.

**Mount Data Container:**
<br>
Samples to mount all volumes from a particular node by exact node identifier & path (*/node*) and to mount master node volumes by *nodeGroup* type (*/data*)

```
{
  "volumeMounts": {
    "/node": {
      "sourceNodeId": 45
    },
    "/data": {
      "sourceNodeGroup": "storage"
    }
  }
}
```

**External Server Mounts:**
<br>
Sample to mount a volume (*/external*) from external server by indicating its host (`sourceHost`), path (`sourcePath`) and access permissions (`readOnly`).
```
{
  "volumeMounts": {
    "/external": {
      "sourceHost": "external.com",
      "sourcePath": "/remote-path",
      "readOnly": true
    }
  }
}
```
**Short Set for External Server:**
<br>
Sample to mount a number of volumes from external server by specifying the required parameters (i.e. volume path, `sourceHost`, `sourcePath`, access permissions) for each of them within one string.     
```
{
  "volumeMounts": {
    "/ext-domain": "aws.com",
    "/ext-domain/ro": "aws.com:ro",
    "/ext-domain/path": "aws.com:/121233",
    "/ext-domain/path/ro": "aws.com:/121233:ro"
  }
}
```

Here, "*ro*" stands for *readOnly* permissions.

<!--
##volumesFrom

`volumesFrom` is an list object.    
There are two ways to select the volume source container:
```
[
  {
    "sourceNodeId": "49",
    "readOnly": true
  },{
    "sourceNodeGroup": "storage",
    "readOnly": true
  }
]
```

In case to import not full source node volumes list You can set like below:
```
[
  {
    "sourceNodeGroup": "storage",
    "volumes": [
      "/master",
      "/local"
    ]
  }
]
```

Simple set examples above:
```
[
  49,
  "storage",
  "storage:ro"
]
```
where:   
- *49* - like { sourceNodeId : 49, readOnly : false }  
- *"storage"* - like { sourceNodeGroup : "storage", readOnly : false }  
- *"storage:ro"* - like { sourceNodeGroup : "storage", readOnly : true }
-->

<h3>Docker Environment Variables</h3>

Docker environment <a href="https://docs.jelastic.com/docker-variables" target="_blank">variable</a> is an optional topology object. The *env* instruction allows to set the required environment variables to specified values. 

```
{
  "type": "install",
  "name": "docker environment variables",
  "nodes": [
    {
      "nodeGroup": "cp",
      "image": "wordpress:latest",
      "env": {
        "WORDPRESS_VERSION": "4.6.1",
        "PHP_INI_DIR": "/usr/local/etc/php"
      }
    }
  ]
}
```

<h3>Docker Links</h3>

Docker <a href="https://docs.jelastic.com/docker-links" target="_blank">links</a> option allows to set up interaction between Docker containers, without having to expose internal ports to the outside world.
<br>

The example below illustrates the way to link *sql* and *memcached* nodes to *cp* container.
```
[
  {
    "image": "wordpress:latest",
    "links": [
      "db:DB",
      "memcached:MEMCACHED"
    ],
    "cloudlets": 8,
    "nodeGroup": "cp",
    "displayName": "AppServer"
  },
  {
    "image": "mysql5:latest",
    "cloudlets": 8,
    "nodeGroup": "db",
    "displayName": "Database"
  },
  {
    "image": "memcached:latest",
    "cloudlets": 4,
    "nodeGroup": "memcached",
    "displayName": "Memcached"
  }
]
```
where:

- `links` - object that defines nodes to be linked to *cp* node by their *nodeGroup* and these links names            
- `db` - MYSQL server `nodeGroup` (environment layer)  
- `memcached` - Memcached server `nodeGroup` (environment layer)   

As a result, all the environment variables within *db* and *memcached* nodes will be also available at *cp* container.  
 
Here, environment variables of linked nodes will have the names, predefined within the `links` array.     
For example:  
- variable *MYSQL_ROOT_PASSWORD* from *sql* node is *DB_MYSQL_ROOT_PASSWORD* in *cp* node   
- variable *IP_ADDRESS* from *memcached* node is *MEMCACHED_IP_ADDRESS* in *cp* node

##Relative Links

The relative links functionality is intended to specify the JPS file’s base URL, in relation to which the subsequent links can be set throughout the manifest. This source destination (URL) can point either to the text of the file or its raw code. Therefore, it is passed in the manifest through the <b>*baseUrl*</b> parameter or specified while <a href="https://docs.jelastic.com/environment-export-import" target="_blank">importing</a> a corresponding JPS file via the Jelastic dashboard.          

!!! note
    > The *baseUrl* value declared within the manifest has higher priority than installation via URL (i.e. <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Import</a>).                

**Example**
```
{
    "type" : "update",
    "name" : "Base URL test",
    "baseUrl" : "https://github.com/jelastic-jps/minio/blob/master",
    "onInstall" : {
        "log" : "Base URL test"
    },
    "onAfterRestartNode[nodeGroup:cp]" : {
        "script" : "build-cluster.js"
    },
    "success" : "README.md"
}
```

In case of the manifest installation via URL by means of the Jelastic **Import** functionality, the `baseUrl` placeholder will be defined if the specified path is set as in the example below:      
  
```
{protocol}://{domain}/myfile.extension
```
where:                

- <b>*{protocol}*</b> - *http* or *https* protocols              
- <b>*{domain}*</b> - domain name of the website, where the manifest is stored                     
- <b>*myfile.extension*</b> - name of the file with indicated extension (i.e. *jps*) at the end                     

There are the following Cloud Scripting rules applied while parsing file's relative path:                         
  - `baseUrl` parameter is being defined                            
  - verification that the linked file’s text doesn't contain whitespaces (including tabs and line breaks)                                     
  - verification that the linked file’s text doesn't contain semicolons and round brackets                                  

If installation is being run from <a href="https://github.com/jelastic-jps" target="_blank">*GitHub*</a> and URL includes <b>*‘/blob/’*</b>, it will be replaced with <b>*‘/raw/’*</b>. In case the `baseUrl` parameter is defined without a slash at the end, it will be added automatically.              

 
The Cloud Scripting engine also supports a `${baseUrl}` placeholder. It can be used throughout the users’ customs scripts (within the <a href="http://docs.cloudscripting.com/reference/actions/#cmd" target="_blank">*cmd*</a> and <a href="http://docs.cloudscripting.com/reference/actions/#script" target="_blank">*script*</a> actions).                 

For example:

```
{
  "type" : "update",
  "name" : "Test Base URL",
  "baseUrl" : "http://example.com/",
  "onInstall" : {
    "cmd [cp]" : {
      "curl -fSs '${baseUrl}script.sh'"
    }
  }
}
```


<h3>Success Text Customization</h3>

It is possible to customize (in confines of a manifest) the *success* text, which is displayed upon successful application installation either at the dashboard or via email notification.         

- Setting a relative to `baseUrl` link, which points path to the <b>*README.md*</b> file for its content to be displayed within the *success* response.                    
```
{
    "type" : "update",
    "name" : "Success Text first example",
    "baseUrl" : "https://github.com/jelastic-jps/minio",
    "onInstall" : {
        "log" : "success text first example"
    },
    "success" : "README.md"
}
```

- Customizing the *success* return text by means of the external link.                    
```
{
  "type": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
}
```

As it was mentioned above, the success response is distinguished between two values:                        

 - text displayed at the dashboard after application installation is successfully conducted                       
 
```
{
  "type": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": {
    "text": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
  }
}
```
 
 - message delivered via email notifying about the successful application setup                             
 
```
{
  "type": "update",
  "name": "Success Text Test 4",
  "baseUrl": "https://github.com/jelastic-jps/lets-encrypt",
  "onInstall": {
    "log": "success text test 4"
  },
  "success": {
    "email": "README.md",
    "en": "README.md",
    "ru": "https://github.com/jelastic-jps/lets-encrypt/blob/master/README.md"
  }
}
```

In the last example above, the localization functionality is applied, which depends upon the Jelastic Platform selected language.                        