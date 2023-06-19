# Basic Configs

The JPS manifest is a file with <b>*.jps*</b> extension, with code written in JSON or YAML format. This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for a successful installation of an application. The basis of the code is represented by the following string:
@@@
```yaml
type: string
name: any required name
```
``` json
{
    "type": "string",
    "name": "any required name"
}
```
@@!

- *type*
    - `install` - create at least one environment
    - `update` - add-on of the existing environment
- *name* - JPS custom name           

This is a mandatory body part of the application package, which includes the information about JPS name and the type of the application installation (the <b>*'install'*</b> mode initiates a new environment creation required for a deployment, the <b>*'update'*</b> mode performs actions on the existing environment).
This basic string should be extended with the settings required by the application you are packing. The following configuration details are included beside the <b>*'type': " "*</b> parameter:

## Manifest Overview

There is a set of available parameters to define a manifest installation behaviour, custom description and design, application icons and success texts etc.

**Basic Template**
@@@
```yaml
type: string
version: string
name: string
logo: string
description: string
homepage: string
categories: array
baseUrl: string
settings: object
targetRegions: object
nodeGroupAlias: object
nodes: array
engine: string
region: string
ssl: boolean
ha: boolean
displayName: string
skipNodeEmails: boolean
appVersion: string
onInstall: object/string
startPage: string
actions: array
addons: array
success: object/string
mixins: array
envGroups: array/string
...: object
```
``` json
{
  "type": "string",
  "version": "string",
  "name": "string",
  "logo": "string",
  "description": "object/string",
  "homepage": "string",
  "categories": "array",
  "baseUrl": "string",
  "settings": "object",
  "targetRegions" : "object",
  "nodeGroupAlias": "object",
  "nodes": "array",
  "engine": "string",
  "region": "string",
  "ssl": "boolean",
  "ha": "boolean",
  "displayName": "string",
  "skipNodeEmails": "boolean",
  "appVersion": "string",
  "onInstall": "object/array",
  "startPage": "string",
  "actions": "array",
  "addons": "array",
  "success": "object/string",
  "mixins": "array",
  "envGroups": "array/string",
  "...": "object"
}
```
@@!

- `type` *[optional]* - type of the application installation. Available values are **install** and **update**. More details described above 
- `version` - *[optional]* - JPS type supported by the Jelastic Platform. See the <a href="/jelastic-cs-correspondence/" target="_blank">correspondence between version</a> page
- `name` *[required]* - JPS custom name
- `logo` *[optional]* - JPS image that will be displayed within custom add-ons
- `description` - text string that describes a template. This section should always follow the template format version section
- `homepage` *[optional]* - link to any external application source
- `categories` - categories available for manifests filtering                                                                        
- `baseUrl` *[optional]* - custom <a href="#relative-links" target="_blank">relative links</a>                                       
- `settings` *[optional]* - custom form with <a href="../visual-settings/" target="_blank">predefined user input elements</a>
- `targetRegions` *[optional]* - filtering available regions on Jelastic platform. Option will be used only with **type** `install`
    - `type` *[optional]* [array] - region's virtualization types
    - `name` *[optional]* [string] - text or JavaScript RegExp argument to filtering region's by name
- `region` *[optional]* - region, where an environment will be installed. Option will be used only with **type** `install`
`targetRegions` has a higher priority than `region`. So in case when both of options have been set regions will be filtered according to the `targetRegions` rules
- `nodeGroupAlias` *[optional]* - an ability to set aliases for existed in environments *nodeGroup*. Mode details [here](selecting-containers/#nodegroup-aliases)
- `nodes` - an array to describe information about nodes for an installation. Option will be used only with **type** `install`
- `engine` *[optional]* - engine <a href="../selecting-containers/#engine-versions" target="_blank">version</a>, by **default** `java6`
- `ssl` *[optional]* - Jelastic SSL status for an environment, by **default** `false`. Parameter is available only with **type** `install` mode
- `ha` *[optional]* - high availability for Java stacks, by **default** `false`. Parameter is available only with **type** `install` mode
- `displayName` *[optional]* - display name for an environment. Required option for **type** `install`
- `skipNodeEmails` *[optional]* - an ability to skip sending emails about creating nodes. Emails are related only to nodes where implemented reset password functionality
- `appVersion` *[optional]* - custom version of an application
- `onInstall` *[optional]* - <a href="../events/#oninstall" target="_blank">event</a> that is an entry point for actions execution
- `startPage` *[optional]* - an [entry point](basic-configs/#entry-points) to be opened via the **Open in browser** button through a successful installation message
- `actions` *[optional]* - objects to describe all <a href="../actions/#custom-actions" target="_blank">custom actions</a>
- `addons` *[optional]* - includes JPS manifests with the **type** `update` as a new JPS installation. More details [here](addons/)
- `success` *[optional]* - success text that will be sent via email and will be displayed at the dashboard after installation. There is an ability to use Markdown syntax. More details [here](visual-settings/#success-text-customization).
- `mixins` *[optional]* - includes(mixes) the functionality and data from one manifest into another by URL or object. More details [here](mixins/)
- `envGroups` *[optional]* [array] - specifies a new environment group(s) or existing one(s) the new environment will belong to. The parameter can be set up as a string or as an array of strings: *envGroups [“MyGroup”]* or *envGroups [“MyGroup”,”ParentGroup/ChildGroup”]*. See more regarding [environment groups management](https://docs.jelastic.com/environment-groups-management)
- "..." - the list of <a href="../events/" target="_blank">events</a> can be predefined before manifest is installed  

### envGroups

New environment can be assigned to either one or several groups upon creation with *envGroups* parameter. In case the group defined in *envGroups* does not exist it will be created. For example:

@@@
```yaml
type: install
name: EnvGroup

nodes:
  nodeType: apache
  cloudlets: 4
envGroups: 
  - Group1/Group2
  - Group3
```
```json
{
  "type": "install",
  "name": "EnvGroup",
  "nodes": {
    "nodeType": "apache",
    "cloudlets": 4
  },
  "envGroups": [
    "Group1/Group2",
    "Group3"
  ]
}
```
@@!

where:  
*group1* - parent group for *group2*  
*group2* - it is a group the created environment will belong to  
*group3* - it is another group the created environment will belong to   

## Environment Installation

The environment can be installed in case when the `type` parameter is set to **install**. Then the set of nodes with their parameters should be defined also.

### Nodes Definition

The list of available parameters are:

- `nodeType` *[required]* - the defined node type. The list of available stacks are <a href="../selecting-containers/#supported-stacks" target="_blank">here</a> 
- `cloudlets` *[required]* - a number of dynamic cloudlets. The recommended value is 4. The value below can disable some services in the container 
- `fixedCloudlets` *[optional]* - amount of fixed cloudlets. The default value is 1.
- `count` *[optional]* - amount of nodes in one group. The default value is 1. To set up the parameter dynamically see an [example](#count-parameter).
- `nodeGroup` *[optional]* - the defined node layer. A docker-based containers can be predefined in any custom node group.
- `displayName` *[optional]* - node's display name (i.e. <a href="https://docs.jelastic.com/environment-aliases" target="_blank">alias</a>)                                         
- `extip` *[optional]* - attaching public IP address to a container. The default value is *'false'*
- `addons` *[optional]* - a list of addons, which will be installed in current `nodeGroup`. Addons will be installed after environment installation and `onInstall` action will be finished. [More details here](/creating-manifest/addons/)
- `tag` *[optional]* - an image tag for `dokerized` Jelastic templates with `nodeType` parameter. Full list of supported tag [here](/creating-manifest/selecting-containers/#dokerized-template-tags)
- `scalingMode` *[optional]* - *stateless* or *stateful* [scaling](https://docs.jelastic.com/horizontal-scaling) mode, the possible values are *'STATELESS'* or *'STATEFUL'* respectively. The default value is *'STATEFUL'* for *nodeGroup* types: *bl,cp,vds*. For the rest of *nodeGroup* types the default value is *'STATELESS'*
- `diskLimit` *[optional]* - sets a storage size limit. The default value is equal to disk quota for current *nodeGroup*. It is measured in GB by default. The MB and TB can be used as well. Examples:
    - 10 = 10 GB
    - 10G = 10GB
    - 100M = 100MB
    - 1T = 1TB
- `distribution` *[optional]* - defines environment distribution across hardware hosts within the platform

The following parameters are available for Docker and Docker-based nodes only:   
                       
- `image` *[optional]* - name and tag of Docker image                            
- `links` *[optional]* - Docker links                         
    - `sourceNodeGroup` - source node to be linked with a current node                                
    - `alias` - prefix alias for linked variables                         
- `env` *[optional]* - Docker environment variables                        
- `volumes` *[optional]* - Docker node volumes               
- `volumeMounts` *[optional]* - Docker external volumes mounts                             
- `cmd` *[optional]* - Docker run configs                            
- `entrypoint` *[optional]* - Docker entry points
<!-- startService section -->
- `startService` *[optional]* - defines whether to run defined service or not. By default `true`
- `cluster` *[optional]* - enables auto-clustering functionality for specific stacks. [Learn more](#cluster)  
- `validation` *[optional]* - validates, sets, and limits node creation parameters in the layer. [Learn more](#validation)  
- `adminUrl` *[optional]* - allows to override default web administration interface URL for the *nodeTypes* that support such administration interface and it's applied to all nodes of the layer. Such *nodeTypes* are *[MySQL, MariaDB](https://jelastic.com/blog/mysql-mariadb-database-auto-clustering-cloud-hosting/)*, *[PostgreSQL](https://jelastic.com/blog/postgresql-auto-clustering-master-slave-replication/)*, *[MongoDB](https://jelastic.com/blog/mongodb-auto-clustering/)*, *[LiteSpeed ADC](https://jelastic.com/blog/litespeed-web-adc-load-balancing/)*, *[LiteSpeed Web Server](https://jelastic.com/blog/litespeed-web-server/)*, *[Couchbase](https://jelastic.com/blog/auto-scalable-couchbase-cluster-in-docker-containers/)*, *[Redis](https://docs.jelastic.com/redis/)*, *[GlassFish](https://jelastic.com/blog/glassfish-payara-auto-clustering-cloud-hosting/)*, *[WildFly](https://jelastic.com/blog/wildfly-managed-domain-in-containers-auto-micro-clustering-and-scaling/)*, *[Payara](https://jelastic.com/blog/glassfish-payara-auto-clustering-cloud-hosting/)*. The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings) 
- `isClusterSupport` *[optional]* - allows to override clustering support and it's applied to all nodes of the layer. If the setting is not used the default value is applied. At the moment, it may be applicable to the templates with label “clusterEnabled = 1”. And setting can be used to hide the *Auto-Clustering* field for a DAS node. The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings)
- `isRedeploySupport` *[optional]*[boolean] - disables [redeploy](https://docs.jelastic.com/container-redeploy/) functionality through the *nodeGroup* settings. It is applicable to the all nodes of the layer. Respectively the **Redeploy** button gets hidden in the dashboard. The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings)
- `isDeploySupport` *[optional]*[boolean] - disables deployment  through the *nodeGroup* settings. The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings)  
- `isResetServicePassword` *[optional]* - hides the password reset button on the UI. The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings). Possible values:  
    - *false* - hides buttons at all levels
    - *NODE* - displays buttons only at the level of the nodes (containers)
    - *NODEGROUP* - displays buttons only at the *nodeGroup* level
- `isSLBAccessEnabled` *[optional]{boolean}* - enables/disables access to the node or respective *nodeGroup* through the [Shared Load Balancer](https://docs.jelastic.com/shared-load-balancer/#deny-access-via-shared-load-balancer). By default `true`  


#### count Parameter

The number of nodes can be passed via any field described in [visual-settings](../visual-settings/) section.
For example the *radio-fieldset* can be utilized to pass the number of *nodes* to be installed within specified *nodeGroup*:  
@@@
```yaml
jpsType: install
name: MyNodes
settings:
  fields:
  - caption: Arbitrary number of Nodes
    type: radio-fieldset
    name: mode
    default: one
    values:
      one: 1 node
      two: 2 nodes
      three: 3 nodes
    showIf:
      one:
      - inputType: hidden
        type: string
        name: nodes
        default: 1
      two:
      - type: string
        inputType: hidden
        name: nodes
        default: 2
      three:
      - type: string
        inputType: hidden
        name: nodes
        default: 3
nodes:
  nodeType: apache2
  nodeGroup: cp
  count: "${settings.nodes}"
```
``` json
{
  "jpsType": "install",
  "name": "MyNodes",
  "settings": {
    "fields": [
      {
        "caption": "Arbitrary number of Nodes",
        "type": "radio-fieldset",
        "name": "mode",
        "default": "one",
        "values": {
          "one": "1 node",
          "two": "2 nodes",
          "three": "3 nodes"
        },
        "showIf": {
          "one": [
            {
              "inputType": "hidden",
              "type": "string",
              "name": "nodes",
              "default": 1
            }
          ],
          "two": [
            {
              "type": "string",
              "inputType": "hidden",
              "name": "nodes",
              "default": 2
            }
          ],
          "three": [
            {
              "type": "string",
              "inputType": "hidden",
              "name": "nodes",
              "default": 3
            }
          ]
        }
      }
    ]
  },
  "nodes": {
    "nodeType": "apache2",
    "nodeGroup": "cp",
    "count": "${settings.nodes}"
  }
}
```
@@!

Another example with *spinner* field:   

@@@
```yaml
jpsType: install
name: MyNodes
settings:
  fields:
  - caption: Arbitrary number of Nodes
    type: spinner
    name: nodes
    increment: 1
    default: 1
    min: 1
  - caption: Cloudlets
    type: spinner
    name: cldts
    increment: 2
    default: 4
    min: 4
nodes:
  nodeType: apache2
  nodeGroup: cp
  count: ${settings.nodes}
  cloudlets: ${settings.cldts}
```
```json
  {
  "jpsType": "install",
  "name": "MyNodes",
  "settings": {
    "fields": [
      {
        "caption": "Arbitrary number of Nodes",
        "type": "spinner",
        "name": "nodes",
        "increment": 1,
        "default": 1,
        "min": 1
      },
      {
        "caption": "Cloudlets",
        "type": "spinner",
        "name": "cldts",
        "increment": 2,
        "default": 4,
        "min": 4
      }
    ]
  },
  "nodes": {
    "nodeType": "apache2",
    "nodeGroup": "cp",
    "count": "${settings.nodes}",
    "cloudlets": "${settings.cldts}"
  }
}
```
@@!

#### startService Parameter

The *startService* flag is responsible for a service launch and its addition to the autoload while container creation. By default, this parameter is enabled but can be deactivated by changing the *startService* value to false.

The *startService* flag works only for custom dockers and for dockerized templates, and, accordingly, does not affect the cartridges and legacy native templates.

##### Conditions that Define Service Behavior

The service doesn’t start as it is not added to autoload in the following cases:

-   the [RestartContainersByGroup](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartContainersByGroup) or [RestartContainer](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartContainer) methods are called through the API

-   the environment is stopped/started

-   the environment is cloned

-   the environment is created with *startServiceOnCreation=false*

-   the Restart button is pressed at the dashboard calling the [RestartContainersByGroup](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartContainersByGroup) and [RestartContainer](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartContainer) API methods (only for managed dockerized containers)


You can force adding the service to autoload by calling the *ExecDockerRunCmd* method


The service starts if:

-   the container is redeployed (starts at every boot time)

-   the container is scaled (starts at the newly added nodes)

-   the Restart button is pressed at the dashboard calling the [RestartNodesByGroup](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartNodesByGroup) and [RestartNodeById](http://apidoc.devapps.jelastic.com/5.4-private/#!/api/environment.Control-method-RestartNodeById) API methods (only for native Docker containers)

<!-- end of startService section -->

#### Cluster

In Jelastic the following *[nodeTypes](https://docs.cloudscripting.com/creating-manifest/selecting-containers/#supported-stacks)* can be clusterized with help of built-in [Auto-Сlustering feature](https://ops-docs.jelastic.com/auto-clustering-templates/):  

  * Application Servers: GlassFish, WildFly, Payara  
  * SQL Databases: MySQL, MariaDB, PostgreSQL
  * NoSQL Databases: Couchbase, MongoDB 
  * Storage Server: Shared Storage Container  

*Auto-Clustering* can be enabled via `cluster` parameter or using *Auto-Clustering* switch at the dashboard:  
![autoclustering-switch](/img/autoclustering-switch.png)  

#### cluster parameter

To enable *Auto-Clustering* the `cluster` parameter is used as:  

  * *boolean* value - *true* invokes cluster creation with default configuration parameters  
  
!!! note 
    - Default topology that will be created for the MySQL and MariaDB is [master-slave](https://jelastic.com/blog/mysql-mariadb-database-auto-clustering-cloud-hosting/) replication cluster with 2 nodes of HA ProxySQL load balancer in front of
    - In case of PostgreSQL there is only one topology available - [master-slave](https://jelastic.com/blog/postgresql-auto-clustering-master-slave-replication/) 
    - The WildFly cluster is created in [Managed Domain Mode](https://jelastic.com/blog/wildfly-managed-domain-in-containers-auto-micro-clustering-and-scaling/) with topology that comrises one Domain Controller node and Worker nodes. Number of Worker nodes is defined by *[count](basic-configs/#nodes-definition)* parameter  	        
    - The Payara/GlassFish cluster is created with topology that comrises one [DAS node and Worker nodes](https://jelastic.com/blog/glassfish-payara-auto-clustering-cloud-hosting/). Number of Worker nodes is defined by *[count](basic-configs/#nodes-definition)* parameter   
    - The MongoDB cluster is created as [replica-set](https://jelastic.com/blog/mongodb-replica-set-master-slave-failover/) with topology that comrises tree nodes one *Primary* and two *Secondary* nodes   
    - The Couchbase is created as [cluster with 3 interconnected Couchbase containers](https://jelastic.com/blog/auto-scalable-couchbase-cluster-in-docker-containers/)   
    - The Storage cluster is based on scalable network filesystem [GlusterFS](https://www.gluster.org/). The default cluster topology comprises 3 storage nodes  
   
For example:  

@@@
```yaml
type: install
name: Auto-Cluster

nodes:
  - nodeType: payara
    cluster: true
```
```json
{
  "type": "install",
  "name": "Auto-Cluster",
  "nodes": [
    {
      "nodeType": "payara",
      "cluster": true
    }
  ]
}
```
@@!  
  
 
  * *object* - this is applicable for MySQL/MariaDB only. Object contains multiple options can be passed as configuration parameters:   
    * `scheme` *[optional]* - configures database [replication scheme](https://jelastic.com/blog/mysql-mariadb-database-auto-clustering-cloud-hosting/) for:  
      * `mysql` - **slave** (Master-Slave), **master** (Master-Master), **single** (Single Primary Group Replication), **multi** (Multi Primary Group Replication)  
      * `mariadb` - **slave** (Master-Slave), **master** (Master-Master), **galera** (Galera Cluster)  
    * `is_proxysql` *[optional][boolean]* - *'true'* adds a ProxySQL load balancer layer to the topology and configures it as an entry point to the database cluster  
    * `db_user` *[optional]* - sets up a database username. If not defined the system will generate one by default  
    * `db_pass` *[optional]* - sets up a password for `db_user`. If not defined the system will generate one by default  
  
A [cluster configuration object](https://ops-docs.jelastic.com/auto-clustering-templates/#clusterization-package) should be passed to the `cluster` field to enable custom auto-clustering

For example *Master-Master* replication topology with ProxySQL node as the entry point:  
  
@@@
```yaml
type: install
name: Auto-Cluster

nodes:
  - nodeType: mysql
    cluster:
      scheme: master
      is_proxysql: true
      db_user: "mydbuser"
      db_pass: "mydbpasswd"
```
```json
{
  "type": "install",
  "name": "Auto-Cluster",
  "nodes": [
    {
      "nodeType": "mysql",
      "cluster": {
        "scheme": "master",
        "is_proxysql": true,
        "db_user": "mydbuser",
        "db_pass": "mydbpasswd"
      }
    }
  ]
}
```
@@!  

![autoclustering-mysql](/img/autoclustering-mysql.png)  

Once the cluster parameters were applied to respective layer, you won't be able to change them.

### Validation

The validation parameter properties allow to:  

  * minCount - specify minimum number of nodes in the layer
  * maxCount - specify maximum number of nodes in the layer
  * scalingMode - set up a *[scalingMode](https://docs.cloudscripting.com/creating-manifest/basic-configs/#nodes-definition)* parameter for the layer
      
 
Following example shows how to restrict a scaling limit of worker nodes between 3 and 5 for Payara Cluster:  

@@@
```yaml
type: install
name: Validation
nodes:
 nodeType: payara
 validation:
   minCount: 3
   maxCount: 5 
```
```json
{
  "type": "install",
  "name": "Validation",
  "nodes": {
    "nodeType": "payara",
    "validation": {
      "minCount": 3,
      "maxCount": 5
    }    
  }
}
```
@@!  

Respectively trying to decrease below 3 the number of worker nodes in the wizard the corresponding warning will be displayed:  

![validation-min](/img/autoclustering-min-count.png)

In case `minCount` is equal to `maxCount` parameter the scaling is inaccessible for the layer.
The setting is stored in *nodeGroup* settings and [can be overridden via API](#update-nodegroup-settings).

<!-- RegionFiltering section -->
### Regions Filtering

Jelastic provides a possibility to use multiple availability regions within a single PaaS installation. The number of hardware regions depends on user account and hosting provider. 

If multiple regions are available, the environment will be created at one that is chosen based on the following filtering rules:  

-   taking the default region according to the user account settings
-   stating a specific region name in the **region** parameter within JPS manifest
-   specifying filter conditions (described below) in the **targetRegions** parameter within JPS manifest

!!! note

    In case both options (*targetRegions* and *region*) are added to the manifest, the *region* option will be ignored.

The *targetRegions* option has multiple additional parameters for filtering the regions:

-   `name` *[optional]{string}* - text or JavaScript RegExp argument to filter regions by name that can be found in JCA -> Hardware Nodes -> Name column :   
*“targetRegions”: { “name”: “hn01.azure-cus” }*  
-   `uniqueName` *[optional]{string}* - name alias :   
*“targetRegions”: { “uniqueName”: “hn01.azure-cus” }*
-   `displayName` *[optional]{string}* - text or JavaScript RegExp argument to filter regions by name that is displayed at the dashboard:   
*“targetRegions”: { “displayName”: “Azure CUS” }*
-   `isActive` *[optional]{boolean}* - filters regions by logical values true or false, according to its status in JCA->Regions->Status column :   
*“targetRegions”: { “isActive”: “false” }*
-   `isRegionMigrationAllowed` *[optional]{boolean}* - filters regions by logical values true or false, according to the possibility to enable live migration:   
*“targetRegions”: { “isRegionMigrationAllowed”: “true” }*
-   `region` *[optional]{number}* - filters by region’s id:   
*“targetRegions”: { “region”: “1” }*
-   `vzTypes` *[optional]{string array}* - text or JavaScript RegExp argument to filter region’s by virtualization type: “pvc”, “vz6”, “pcs-storage”, “vz7”, where “pvc” for Parallels Virtuozzo Containers, “vz6” for Virtuozzo 6, “pcs-storage” for Parallels Cloud Storage, “vz7” for Virtuozzo 7:   
*“targetRegions”: { “vzTypes”: “pvc” }*
-   `type` *[optional]{string array}* - vzTypes alias:   
*“targetRegions”: { “type”: “pvc” }*

!!! note
    All fields in filter could be passed as an Array of Strings or String. Each string could be a valid JavaScript RegExp argument. Even boolean values can be as RegExp argument. Examples:   
    *“targetRegions”: {“isActive”: “f.\*” }*   
    *“targetRegions”: { “displayName”: [".\*O.\*", “.\*A.\*”, “.\*P.\*”] }* 
<!-- RegionFiltering section -->


<!--##Docker Actions-->
### Nodes Actions

Specific Cloud Scripting actions for Docker containers include operations of *volumes*, *links* and *environment variables* management.
<br>

There are three available parameters to set Docker volumes:  

- *volumes* - list of volume paths   
- *volumeMounts* - mount configurations  
- *volumesFrom* - list of nodes the volumes are imported from    

All of the fields are set within the Docker object:
@@@
```yaml
type: install
name: docker volumes

nodes:
  nodeGroup: sqldb
  image: centos:7
  volumes: []
  volumeMount: {}
  volumesFrom: []
```
``` json
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
@@!

**Volumes**<br>
This field represents a string array:
@@@
```yaml
- volumes:
  - /external
  - /data
  - /master
  - /local
```
``` json
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
@@!

**VolumeMounts**<br>
This parameter is an object. It can be set like within the example below:
@@@
```yaml
volumeMounts:
  /example-path:
    sourcePath: ''
    sourceNodeId: 0
    sourceNodeGroup: ''
    sourceHost: ''
    readOnly: true
```
``` json
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
@@!
Here:  

- `/example-path` - path to place the volume at a target node  
- `sourcePath` *[optional]* - default value that repeats volume path (*/example-path* in our sample)
- `sourceNodeId` -  node identifier the volume should be mounted from (optional, in case of the `sourceNodeGroup` parameter using)       
- `sourceHost` *[optional]* - parameter for <a href="https://docs.jelastic.com/configure-external-nfs-server" target="_blank">external mounts</a> usage
- `readOnly` - defines write data permissions at source node, the default value is `false`   
- `sourceNodeGroup` - any available *nodeGroup* within a source environment (ignored if the `sourceNodeId` parameter is specified). The list of mounted volumes is defined by a master node.    

In case not all source node volumes are required to be mounted, the particular ones can be specified:
@@@
```yaml
- sourceNodeGroup: storage
  volumes: 
    - /master
    - /local
```
``` json
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
@@!

<h4>VolumeMounts examples</h4>
 
**Master Node Mount:**
Samples to mount a particular volume by exact node identifier & path (*/master*) and to mount all volumes from the layer master node by *nodeGroup* (*/master-1*)
@@@
```yaml
volumeMounts:
  /master:
    sourcePath: /master
    sourceNodeId: 81725
    readOnly: true
  /master-1:
   sourceNodeGroup: current-node-group
```
``` json
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
@@!

Here, *sourcePath* and *readOnly* parameters are optional.

**Mount Data Container:**
<br>
Samples to mount all volumes from a particular node by exact node identifier & path (*/node*) and to mount master node volumes by *nodeGroup* type (*/data*)
@@@
```yaml
volumeMounts:
  /node:
    sourceNodeId: 45
  /data:
    sourceNodeGroup: storage
```
``` json
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
@@!

**External Server Mounts:**
<br>
Sample to mount a volume (*/external*) from external server by indicating its host (`sourceHost`), path (`sourcePath`) and access permissions (`readOnly`).
@@@
```yaml
volumeMounts:
  /external:
    sourceHost: external.com
    sourcePath: /remote-path
    readOnly: true
```
``` json
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
@@!
**Short Set for External Server:**
<br>
Sample to mount a number of volumes from external server by specifying the required parameters (i.e. volume path, `sourceHost`, `sourcePath`, access permissions) for each of them within one string.     
@@@
```yaml
volumeMounts:
  /ext-domain: aws.com
  /ext-domain/ro: aws.com;ro
  /ext-domain/path: aws.com:/121233
  /ext-domain/path/ro: aws.com:/121233:ro
```
``` json
{
  "volumeMounts": {
    "/ext-domain": "aws.com",
    "/ext-domain/ro": "aws.com:ro",
    "/ext-domain/path": "aws.com:/121233",
    "/ext-domain/path/ro": "aws.com:/121233:ro"
  }
}
```
@@!

Here, "*ro*" stands for *readOnly* permissions.

<!--
##volumesFrom

`volumesFrom` is an list object.    
There are two ways to select the volume source container:
``` json
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
``` json
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
``` json
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

#### Environment Variables

Docker environment <a href="https://docs.jelastic.com/docker-variables" target="_blank">variable</a> is an optional topology object. The *env* instruction allows to set the required environment variables to specified values. 
@@@
```yaml
type: install
name: Environment variables

nodes:
  - nodeGroup: cp
    image: wordpress:latest
    env:
      WORDPRESS_VERSION: 4.6.1
      PHP_INI_DIR: /usr/local/etc/php
```
``` json
{
  "type": "install",
  "name": "Environment variables",
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
@@!

Environment variables can manage to control nodes availability from outside to the platform. <a href="https://docs.jelastic.com/setting-custom-firewall" target="_blank">Jelastic Container Firewall</a> feature was implemented in Jelastic version 5.4 and new firewall rules can be set during creating new environment.<br>
 The reserved environment variable for this option is - **JELASTIC_PORTS**. This parameter defines which ports will be added in *inbound* rules. All rules in this case will be added for both protocols (**TCP/UDP**).

@@@
```yaml
jpsType: install
name: JELASTIC_PORTS env variable
nodes:
  nodeType: apache2
  nodeGroup: cp
  env:
    JELASTIC_PORTS: 3306, 33061, 33062
```
```json
{
  "jpsType": "install",
  "name": "JELASTIC_PORTS env variable",
  "nodes": {
    "nodeType": "apache2",
    "nodeGroup": "cp",
    "env": {
      "JELASTIC_PORTS": "3306, 33061, 33062"
    }
  }
}
```
@@!
All ports for output traffic are opened by default.

Another one reserved environment variables is **ON_ENV_INSTALL**. This variable is responsible for executing new JPS installation after new nodeGroup (layer of nodes) has been created.<br>
This variable for **nodeGroup** can be set in JPS or via dashboard. More info about Docker configuration is Jelastic dashboard <a href="https://docs.jelastic.com/docker-configuration" target="_blank">here</a>.

!!! note
    > By default in manifest from the **ON_ENV_INSTALL** variable *\${settings.nodeGroup}* placeholder is defined. It will be a nodeGroup value where this manifest is executed.

**ON_ENV_INSTALL** can consists of manifest URL (string) or an object.<br>
URL is a external link for manifest with any *type* - `install` or `update`. An object could has two options:

 - `jps` - link, source of external manifest
 - `settings` - a list of any parameters which will be defined in external manifest in *\${settings.\*}* scope.

In the first example **ON_ENV_INSTALL** is defined like simple URL:
@@@
```yaml
type: install
name: ON ENV INSTALL
nodes:
  nodeType: nginxphp
  env:
    ON_ENV_INSTALL: http://example.com/manifest.jps
```
```json
{
  "type": "install",
  "name": "ON ENV INSTALL",
  "nodes": {
    "nodeType": "nginxphp",
    "env": {
      "ON_ENV_INSTALL": "http://example.com/manifest.jps"
    }
  }
}
```
@@!

Another one example displays an ability to set any custom options which can be used in executed manifest from variable:

@@@
```yaml
type: install
name: ON ENV INSTALL
nodes:
  nodeType: nginxphp
  env:
    ON_ENV_INSTALL:
      jps: http://example.com/manifest.jps
      settings:
        customSetting: mySetting
```
```json
{
  "type": "install",
  "name": "ON ENV INSTALL",
  "nodes": {
    "nodeType": "nginxphp",
    "env": {
      "ON_ENV_INSTALL": {
        "jps": "http://example.com/manifest.jps",
        "settings": {
          "customSetting": "mySetting"
        }
      }
    }
  }
}
```
@@!
In the example above in *manifest.jps* a **\${settings.customSetting}** placeholder is available with value *mySetting*.
Any number of custom parameters in *settings* can be set.

#### Links

Docker <a href="https://docs.jelastic.com/docker-links" target="_blank">links</a> option allows to set up interaction between Docker containers, without having to expose internal ports to the outside world.
<br>

The example below illustrates the way to link *sql* and *memcached* nodes to *cp* container.
@@@
```yaml
- image: wordpress:latest
  links:
    - db:DB
    - memcached:MEMCACHED
  cloudlets: 8
  nodeGroup: cp
  displayName: AppServer

- image: mysql5:latest
  cloudlets: 8
  nodeGroup: db
  displayName: database

- image: memcached:latest
  cloudlets: 4
  nodeGroup: memcached
  displayName: Memcached
```
``` json
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
@@!
where:

- `links` - object that defines nodes to be linked to *cp* node by their *nodeGroup* and these links names            
- `db` - MYSQL server `nodeGroup` (environment layer)  
- `memcached` - Memcached server `nodeGroup` (environment layer)   

As a result, all the environment variables within *db* and *memcached* nodes will be also available at *cp* container.  
 
Here, environment variables of linked nodes will have the names, predefined within the `links` array.     
For example:  

- variable *MYSQL_ROOT_PASSWORD* from *sql* node is *DB_MYSQL_ROOT_PASSWORD* in *cp* node   
- variable *IP_ADDRESS* from *memcached* node is *MEMCACHED_IP_ADDRESS* in *cp* node

### Entry Points
There is an ability to set custom entry points - the button *Open in Browser*, which can be clicked when JPS with type `install` is installed.
![open-in-browser.png](/img/open-in-browser.png)

Entry Points can be set in `startPage` option. The default `startPage` value is an installed environment URL (even it hasn't been defined).
Entry Points can include any general placeholders - which have been defined during environment installation.  
The *startPage* parameter can be specified for any *JPS* type with options as follows:  
- for **type:install** with environment:  
    - the **Open in browser** button is always displayed  
    - the *startPage* parameter can be specified either relative or absolute link to the environment  
- for **type:install** without environment:  
    - the **Open in browser** button is displayed if the *startPage* parameter is specified in the manifest  
    - the *startPage* parameter can be specified with absolute link only  
- for **type:update**  
    - the **Open in browser** button is displayed if the *startPage* parameter is specified in the manifest  
    - the *startPage* parameter can be specified by absolute link or by link relative to the environment   

For example:  
@@@
```yaml
type: install
baseUrl: https://docs.cloudscripting.com/
nodes:
  nodeType: apache
  cloudlets: 8
startPage: ${baseUrl}creating-manifest/basic-configs/
```
```json
{
  "type": "install",
  "baseUrl": "https://docs.cloudscripting.com/",
  "nodes": {
    "nodeType": "apache",
    "cloudlets": 8
  },
  "startPage": "${baseUrl}creating-manifest/basic-configs/"
}
```
@@!

The case where any custom directory of created environment can be opened in *Open in Browser* button:
@@@
```yaml
type: install
nodes:
  nodeType: apache
  cloudlets: 8
startPage: ${env.url}customDirectory/
```
```json
{
  "type": "install",
  "nodes": {
    "nodeType": "apache",
    "cloudlets": 8
  },
  "startPage": "${env.url}customDirectory/"
}
```
@@!

###Skip Node Emails

By default in Jelastic, a user is informed via email about adding new nodes into environments. In Cloud Scripting there is an ability to set an option to skip these emails upon environment creation:  
- globally for all *nodeTypes*
- for specific *nodeTypes*
This option does not affect the email notification upon node addition by scaling.   
  
For all *nodeTypes* in the environment:  

@@@
```yaml
type: install
name: skipNodeEmails
nodes:
  - nodeType: redis
    cloudlets: 4
  - nodeType: mysql
    cloudlets: 4
skipNodeEmails: true
```
```json
{
  "type": "install",
  "name": "skipNodeEmails",
  "nodes": [
    {
      "nodeType": "redis",
      "cloudlets": 4
    },
    {
      "nodeType": "mysql",
      "cloudlets": 4
    }
  ],
  "skipNodeEmails": true
}
```
@@!

For specific *nodeTypes*:  

@@@
```yaml
type: install
name: skipNodeEmails
nodes:
  - nodeType: redis
    cloudlets: 4
    skipNodeEmails: true
  - nodeType: mysql
    cloudlets: 4
    skipNodeEmails: false
```
```json
{
  "type": "install",
  "name": "skipNodeEmails",
  "nodes": [
    {
      "nodeType": "redis",
      "cloudlets": 4,
      "skipNodeEmails": true
    },
    {
      "nodeType": "mysql",
      "cloudlets": 4,
      "skipNodeEmails": false
    }
  ]
}
```
@@!

### Update nodeGroup settings

You can update *nodeGroup* settings through the API method [environment.control.ApplyNodeGroupData](https://docs.jelastic.com/api/#!/api/environment.Control-method-ApplyNodeGroupData).

For example:

```
https://app.jelastic.com/1.0/environment/control/rest/applynodegroupdata?data={"isDeploySupport":false}&envName=env-1&session=1dx1d2eb8c6b29cddfb28cfd4e93f80c15c&nodeGroup=cp  
```
  
<br>
## JPS execution without environment
 
The JPS manifest can be executed without binding to any environment.  
@@@
```yaml
type: install
name: "Add-on without environment"

description: |
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas euismod sapien eu risus venenatis, at faucibus dui cursus. Vestibulum a ipsum eget nibh aliquet vestibulum. Ut vestibulum ultrices sem quis ultricies. Pellentesque maximus nisl nec metus convallis egestas. Ut posuere leo quis semper tristique. In bibendum sem quis aliquet porttitor.

startPage: https://example.com/

onInstall:
  - log: test
```
``` json
{
  "type": "install",
  "name": "Add-on without environment",
  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas euismod sapien eu risus venenatis, at faucibus dui cursus. Vestibulum a ipsum eget nibh aliquet vestibulum. Ut vestibulum ultrices sem quis ultricies. Pellentesque maximus nisl nec metus convallis egestas. Ut posuere leo quis semper tristique. In bibendum sem quis aliquet porttitor.\n",
  "startPage": "https://example.com/",
  "onInstall": [
    {
      "log": "test"
    }
  ]
}
```
@@!
  
The JPS will be installed without creating the environment if you specify `type`: `install` in the manifest and do not specify the `nodes`.  
In case there is a subscription for some kind of events and no environment specified in the manifest, the subscription will be ignored and no logging (SUBSCRIBE messages) should be displayed in a [console](/troubleshooting/#troubleshooting).  
If the environment is not specified the list of the following actions can be performed:  
- [install](/creating-manifest/actions/#install)  
- [script](/creating-manifest/actions/#script)  
- [api](/creating-manifest/actions/#api)  
- [call action](/creating-manifest/actions/#call-action-with-parameters)  
- [foreach](/creating-manifest/conditions-and-iterations/#foreach)  
- [if](/creating-manifest/conditions-and-iterations/#conditions)  
- [return](/creating-manifest/actions/#return)  
- [set](/creating-manifest/actions/#set)  
- [setGlobals](/creating-manifest/actions/#setglobals)  
- [assert](/creating-manifest/actions/#assert)  
- log  
- [sleep](/creating-manifest/actions/#sleep)  
  
For the rest of the [actions](/creating-manifest/actions), an error will be displayed in the console:  
{ "result": 11022, "error": "can't find node by the given parameters" }

The error 11022 is ignored and gets to no crash report.

##Relative Links

The relative links functionality is intended to specify the JPS file’s base URL, in relation to which the subsequent links can be set throughout the manifest. This source destination (URL) can point either to the text of the file or its raw code. Therefore, it is passed in the manifest through the <b>*baseUrl*</b> parameter or specified while <a href="https://docs.jelastic.com/environment-export-import" target="_blank">importing</a> a corresponding JPS file via the Jelastic dashboard.          

!!! note
    > The *baseUrl* value declared within the manifest has higher priority than installation via URL (i.e. <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Import</a>).                

**Example**
@@@
```yaml
type: update
name: Base URL test
baseUrl: https://github.com/jelastic-jps/minio/blob/master

onInstall:
  log: Base URL test
  
onAfterRestartNode [cp]:
  script: build-cluster.js
  
success: README.md
```
``` json
{
    "type" : "update",
    "name" : "Base URL test",
    "baseUrl" : "https://github.com/jelastic-jps/minio/blob/master",
    "onInstall" : {
        "log" : "Base URL test"
    },
    "onAfterRestartNode [cp]" : {
        "script" : "build-cluster.js"
    },
    "success" : "README.md"
}
```
@@!

In case of the manifest installation via URL by means of the Jelastic **Import** functionality, the `baseUrl` placeholder will be defined if the specified path is set as in the example below:      
  
```
${baseUrl}/manifest.jps
```
where:                

- ${baseUrl}={protocol}//{domain}/{path}
- <b>*{protocol}*</b> - *http* or *https* protocols              
- <b>*{domain}*</b> - domain name of the website, where the manifest is stored                     
- <b>*{path}*</b> - directory path                
- <b>*manifest.jps*</b> - name of the file jps package                   

There are the following Cloud Scripting rules applied while parsing file's relative path:   
                      
- `baseUrl` parameter is being defined                            
- verification that the linked file’s text doesn't contain whitespaces (including tabs and line breaks)                                     
- verification that the linked file’s text doesn't contain semicolons and round brackets                                  

If installation is being run from <a href="https://github.com/jelastic-jps" target="_blank">*GitHub*</a> and URL includes <b>*‘/blob/’*</b>, it will be replaced with <b>*‘/raw/’*</b>. In case the `baseUrl` parameter is defined without a slash at the end, it will be added automatically.              

There are a list of JPS blocks which can use resources from **related** links:

- `logo` - JPS application image is shown while jps installation
- `script` - <a href="../actions/#script" target="_blank">action</a>, for executing javascript and java scripts
- `description` - information about JPS which is shown before install process
- `success` - message after successful application installation

Relative links in these blocks check a file availability by URL. If file by defined link is absent (404 response code) a simple text will be displayed in that blocks.

For example:

@@@
```yaml
type: update
name: Relative Path Detection
baseUrl: https://example.com/
success: text.txt
```
```json
{
  "type": "update",
  "name": "Relative Path Detection",
  "baseUrl": "https://example.com/",
  "success": "text.txt"
}
```
@@!

In the example above the text *text.txt* will be displayed in success email notification and in success window in Jelastic dashboard when JPS installation will be finished. If URL **https://example.com/text.txt** has any content then that content will be displayed.

The Cloud Scripting engine also supports a `${baseUrl}` placeholder. It can be used throughout the users’ customs scripts (within the <a href="../actions/#cmd" target="_blank">*cmd*</a> and <a href="../actions/#script" target="_blank">*script*</a> actions).                 

For example:
@@@
```yaml
type: update
name: Test Base URL
baseUrl: http://example.com/

onInstall:
  cmd [cp]: curl -fSs '${baseUrl}script.sh'    
```
``` json
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
@@!
                       
