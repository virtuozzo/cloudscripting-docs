# Specifying Target Container

Running a specific <a href="../actions/" target="_blank">action</a> requires to specify a target container, in confines of which this action is executed. Thus, it is possible to specify a [particular container](#particular-container), all containers within a layer by the [*nodeGroup*](#all-containers-by-group) value, or all containers of the same type by the [*nodeType*](#all-containers-by-type) value.                                 

### Particular Container

The <em>nodeId</em> parameter is used to specify a particular container for the action execution. If you know the Node ID of your container (displayed at the Virtuozzo Application Platform dashboard next to the required node), you can set it statically as follows.                                           

@@@
```yaml
writeFile:
  - nodeId: 123
    path: /var/www/webroot/hw.txt
    body: Hello World!
```
``` json
{
  "writeFile": [
    {
      "nodeId": "123",
      "path": "/var/www/webroot/hw.txt",
      "body": "Hello World!"      
    }
  ]
}
```
@@!
If you don't know the Node ID or a container is not created yet, you can set a dynamic value, using special placeholders as follows.

@@@
```yaml
writeFile:
  - nodeId: ${nodes.apache2[0].id}
    path: /var/www/webroot/hw.txt
    body: Hello World!
```
``` json
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
@@!
For more information, visit the <a href="../placeholders/" target="_blank"><em>Placeholders</em></a> documentation page.                               

### All Containers By Group        
 
The *nodeGroup* parameter is used to specify all containers within a specific [layer](#predefined-nodegroup-values).                              

The Virtuozzo Application Platform supports the following predefined *nodeGroup* values:     

- *bl*                   
 
- *cp*                  

- *cache*                   

- *sqldb*                   

- *nosqldb*                       

- *storage*                   

- *vds* (for VPS)                 

- *build*                           

Actions for the specified <em>nodeGroup</em> are executed successively one by one. For Docker containers the <em>nodeGroup</em> value is not predefined, therefore, you can state it to any value above or your custom one.                              

!!! note
    If you state a custom <em>nodeGroup</em> value for Docker containers, the corresponding container is placed to the <em>Extra</em> layer. Subsequently, this <em>nodeGroup</em> value can be used within the same-named actions field to point to the particular <em>Extra</em> layer.
    ![dockerextra](/img/dockerextra.png)         

### All Containers By Type

The <em>nodeType</em> parameter is used to specify all containers that are built upon the same software [stacks](#supported-stacks ).                                   	  

<b>Examples</b>     

Using the *nodeType* parameter while performing the <a href="../actions/#writefile" target="_blank">**writeFile**</a> action.                         
@@@
```yaml
writeFile:
  nodeType: apache2
  path: /tmp/example.txt
  body: Hello World
```
``` json
{
  "writeFile": {
    "nodeType": "apache2",
    "path": "/tmp/example.txt",
    "body": "Hello World"
  }
} 
```
@@!
where:                

- `writeFile` - action to write data to the file                                                         
- `nodeType` - parameter that specifies the node type                                             
- `path` - parameter that specifies the path to the file                        
- `body` - data that is written to the file                                             

Using the *engine* and *nodeType* parameters while creating a new environment.
@@@
```yaml
type: install
name: install Tomcat7 node
engine: java7

nodes:
  nodeType: tomcat7
```
``` json
{
  "type": "install",
  "name": "install Tomcat7 node",
  "engine": "java7",
  "nodes": {
    "nodeType": "tomcat7"
  }
}
```
@@!
where:          

- `engine` - parameter that specifies the engine version                               
- `nodeType` - parameter that specifies the node type                                                    

## Selector Types                                    

There are three alternative approaches, provided to specify a target container in a manifest:                                               

- specifying a target container within a name of an action (**node selectors**)     

Through the following example, a new file is created in the compute layer (<em>[cp]</em>) and a new directory is created in the compute (<em>[cp]</em>) and balancer (<em>[bl]</em>) layers, and container with the Node ID <em>123</em>. Actions for the specified containers are executed in the declared order.

@@@
```yaml
- createfile [cp]:
    path: /tmp/test.txt

- createDirectory [cp,bl,123]:
    path: /tmp/test
```
``` json
[
  {
    "createFile [cp]": {
      "path": "/tmp/test.txt"
    }
  },
  {
    "createDirectory [cp,bl,123]": {
      "path": "/tmp/test"
    }
  }
]
```
@@!

A defined action in manifest could be executed in all nodes of all layers within an environment where JPS is executed.
For example:

@@@
```yaml
type: update
name: cmd in all nodes
onInstall:
  cmd [*]: echo hello world!
```
```json
{
  "type": "update",
  "name": "cmd in all nodes",
  "onInstall": {
    "cmd [*]": "echo hello world!"
  }
}
```
@@!

There is a console log screen which displays that `cmd` action has been executed in all nodes by unique identifier one by one:

![wildcard-mask](/img/wildcard-mask.jpg)

- specifying a target container next to the performed action                                       

Through the following example, the <a href="../actions/#createfile" target="_blank">**createFile**</a> and <a href="../actions/#createdirectory" target="_blank">**createDirectory**</a> actions are applied to the specified <em>nodeGroup</em>, namely the compute layer (<em>[cp]</em>).
@@@
```yaml
- createFile:
    path: /tmp/test.txt
  createDirectory:
    path: /tmp/test
  nodeGroup: cp
```
``` json
[
  {
    "createFile": {
      "path": "/tmp/test.txt"
    },
    "createDirectory": {
      "path": "/tmp/test"
    },
    "nodeGroup": "cp"
  }
]
```
@@!
 
- specifying a target container as a parameter in the *actions* object     

Learn more on this parameter within the <a href="../actions/#custom-actions" target="_blank"><em>Custom Actions</em></a> documentation page.                                      

!!! note 
    <b>Node selectors</b> have higher priority than containers specified next to the action, but lower than parameters set in the *actions* object.   
    If you specify all three parameters (*nodeId*, *nodeGroup*, and *nodeType*), actions for indicated containers are executed in the following order: <b>*_nodeId -> nodeGroup -> nodeType_*</b>.

## NodeGroup Aliases

An existed nodes in environments can be targeted not only by their defined *nodeGroup*s and by aliases. That aliases could be defined in manifests like in example:
@@@
```yaml
type: update
name: Alias for nodeGroup
nodeGroupAlias:
  cp: sqldb2
onInstall:
  log: ${nodes.sqldb2.id}
```
```json
{
  "type": "update",
  "name": "Alias for nodeGroup",
  "nodeGroupAlias": {
    "cp": "sqldb2"
  },
  "onInstall": {
    "log": "${nodes.sqldb2.id}"
  }
}
```
@@!

In the example above JPS add-on with `type` *update* could be applied on any existing environment. In this case all compute nodes with **nodeGroup** *cp* can be called by aliases (Nodes with **nodeGroup** *sqldb2* are absent in environment). So the example result is displayed in the screen:
![nodeGroup-alias](/img/nodeGroupAlias.png)

!!! note
    `nodeGroupAlias` option works only within current JPS manifest.

## Supported Stacks                                  

The supported software stacks are categorized in the table below with specified names and aliases that can be used within Cloud Scripting, as well as the links to the available tags.


| nodeGroup                            | Supported nodeType Values (Aliases)                                                                                                                                                                                        | Supported Tags Link |
|--------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| bl                                   | nginx-dockerized (nginx), varnish-dockerized (varnish), haproxy(haproxy2), apache-lb (apache-balancer), litespeedadc (litespeedadc2, litespeedadc3)                                                                                                                                                                                           | [Load-Balancers](https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/#lb)      |
| cp                                   | dotnet (dotnet5, dotnet3, dotnet7, dotnet6), apache (apache2), apache-python (apache2-python), apache-ruby (apache2-ruby), glassfish (glassfish5, glassfish6, glassfish3), golang, javaengine, jenkins (jenkins2), jetty (jetty10, jetty9, jetty11), lemp, litespeedphp (litespeedphp5, litespeedphp6), llsmp (llsmp6, llsmp5), nginxphp-dockerized (nginxphp), nginxruby (nginx-ruby), nodejs (nodejs14-supervisor, nodejs14-npm, nodejs16-forever, nodejs14-pm2, nodejs16-supervisor, nodejs16-pm2, nodejs14-forever, nodejs16-npm), payara (payara5, payara3), springboot, tomcat (tomcat85, tomcat9, tomcat10, tomcat8, tomcat11, tomcat6, tomcat7), tomee-dockerized (tomee), wildfly (wildfly26-preview, wildfly24, wildfly26, wildfly25, wildfly25-preview, wildfly27, wildfly24-preview, wildfly27-preview) | [Application Servers](https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/#app-servers) |
| sqldb, nosqldb                       | couchbase,  mariadb-dockerized (mariadb10, mariadb1010, mariadb106, mariadb107, mariadb104, mariadb109, mariadb108, mariadb103, mariadb105),  mongodb-dockerized (mongodb),  mysql (mysql5, mysql8),  opensearch (opensearch2, opensearch1),  perconadb (percona5.7, percona8, percona5, percona8.0),  postgresql (postgres14, postgres11, postgres12, postgres13),  redis (redis7, redis6)        | [Databases](https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/#databases)           |
| vps, cache, build, storage, extra | centos-vps (centos7),  debian-vps (debian10, debian9, debian11),  dockerengine,  kubernetes,  logstash (logstash8, logstash7),  maven (maven3),  memcached-dockerized (memcached),  opensearchdashboards (opensearchdashboards1, opensearchdashboards2),  pgpool2 (pgpool2-4),  proxysql,  storage,  ubuntu-vps (ubuntu22, ubuntu16, ubuntu20, ubuntu18),  windows2019                                                                                                                                 | [Additional Stacks](https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/#additional)   |

!!! note
    In case the root privileges are required within the certified template, it should be created as custom docker via [image](basic-configs/#environment-installation) parameter. If so, take into account that some functionality/automation won’t be available such as Custom SSL, Managed Firewall, etc. To create custom docker follow the **Supported Tags Link** column to get the proper name of certified Virtuozzo docker images.

<a href="https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/#engines">Engine versions</a>

|Stacks|Java|PHP|Ruby|Python|Nodejs|.NET|Go|
|--------|----------|-----------|-----------|--------|---------|---------|---------|
|engine|adoptopenjdk-8 <br>adoptopenjdk-11 <br>adoptopenjdk-13 <br>adoptopenjdk-14 <br>adoptopenjdk-15 <br>adoptopenjdk-16 <br>correttojdk-8 <br>correttojdk-11 <br>correttojdk-15 <br>correttojdk-16 <br>correttojdk-17 <br>correttojdk-18 <br>correttojdk-19 <br>dragonwell-8 <br>graalvm-19 <br>graalvm-21 <br>graalvm-22 <br>jdk-8 <br>jdk-11 <br>openj9-8 <br>openj9-11 <br>openj9-14 <br>openj9-15 <br>openj9-16 <br>openjdk-8 <br>openjdk-11 <br>openjdk-13 <br>openjdk-14 <br>openjdk-15 <br>openjdk-16 <br>openjdk-17 <br>openjdk-18 <br>openjdk-19 <br>openjdk-20 <br>openjdk-21 <br>temurinjdk-8 <br>temurinjdk-11 <br>temurinjdk-17 <br>temurinjdk-18 <br>temurinjdk-19 <br>zulujdk-8 <br>zulujdk-11 <br>zulujdk-13 <br>zulujdk-14 <br>zulujdk-15 <br>zulujdk-16 <br>zulujdk-17 <br>zulujdk-18 <br>zulujdk-19<br>|php7.4<br>php8.0<br>php8.1|ruby2.7<br>ruby3.0<br>ruby3.1<br>|python3.6<br>python3.7<br>python3.8<br>python3.9<br>python3.10<br>python3.11<br>|nodejs14-npm <br>nodejs14-forever <br>nodejs14-pm2 <br>nodejs14-supervisor <br>nodejs16-npm <br>nodejs16-forever <br>nodejs16-pm2 <br>nodejs16-supervisor<br>|dotnet3 <br>dotnet5 <br>dotnet6 <br>dotnet7|go14 <br>go15 <br>go16 <br>go17 <br>go18 <br>go19 <br>|

!!! note
    The list of supported <a href="https://www.virtuozzo.com/application-platform-docs/software-stacks-versions/" target="_blank">software stacks</a> can vary depending on your Virtuozzo Application Platform version - it can be checked at your dashboard.    
    
## Selecting Hardware Hosts

There is an ability in Virtuozzo Application Platform to select the hardware for the user's application with the help of the [multi zones](https://www.virtuozzo.com/application-platform-ops-docs/multi-zones/) approach. If a user is aware all of the [labels](https://www.virtuozzo.com/application-platform-ops-docs/multi-zones/#host-labels) assigned for the hardware hosts within the platform he can decide which hosts across all of the available regions can be used to install the user's environment.  
Hardware host selection is performed by **distribution** parameter which defines the logic in the [layer specifics](basic-configs/#nodes-definition), which consist of the following two options:  

- `zones` - sets a filter for allowed zones (groups of hosts custom-defined by labels) in the “{name}: {value}” format, e.g. zones: [{provider: azure}, {provider: amazon}]  

- `mode` - defines the behavior in case of the target zone unavailability  

    - *SOFT* - the operation should proceed on the next zone/host defined by the multi zones algorithm (this option is used by default)  

    - *STRICT* - the operation should be terminated with an error  

!!! note
    - the distribution is performed in the within of a single host group (i.e. user environment region)  
    - the default zone *{name}* can be skipped when providing zones parameter, i.e. the *zones: [“a”, “b”]* and *zones: [{zone: a}, {zone: b}]* expressions are equal  
    - if zones with two or more *{value}* are specified for a single *{name}*, hosts with either of these values will be allowed for distribution  
    - if zones with two or more *{name}* are specified, only hosts with all these labels will be allowed for distribution  
    - if zones are not specified, distribution is performed across all hosts   
    - the maximum number of elements in zones is 10  
    - the maximum number of unique *{value}* per each *{name}* is 20    

For example, the distribution configured in the following package ensures nodes are created only on the hosts with the **disk: ssd** label.  

@@@
```yaml
name: "multi-zone"
type: install

nodes:
  nodeType: docker
  fixedCloudlets: 1
  flexibleCloudlets: 8
  image: jelastic/tomcat:latest
  count: 2
  distribution:
    mode: SOFT
    zones: 
    - disk: ssd
```
```json
{
  "name": "multi-zone",
  "type": "install",
  "nodes": {
    "nodeType": "docker",
    "fixedCloudlets": 1,
    "flexibleCloudlets": 8,
    "image": "jelastic/tomcat:latest",
    "count": 2,
    "distribution": {
      "mode": "SOFT",
      "zones": [
        {
          "disk": "ssd"
        }
      ]
    }
  }
}
```
@@!

The *zones* parameter can be provided dynamically defining pair of label name and value via user interface.  
For example:  

@@@
```yaml
name: "multi-zone"
type: install

settings:
  fields:
  - hideLabel: false
    type: string
    caption: Label name
    name: labelname
  - hideLabel: false
    type: string
    caption: Label value
    name: labelvalue
    
nodes:
  - nodeType: tomcat
    cloudlets: 6
    distribution:
      mode: SOFT
      zones: 
      - "${settings.labelname}": "${settings.labelvalue}"
```
```json
      {
  "name": "multi-zone",
  "type": "install",
  "settings": {
    "fields": [
      {
        "hideLabel": false,
        "type": "string",
        "caption": "Label name",
        "name": "labelname"
      },
      {
        "hideLabel": false,
        "type": "string",
        "caption": "Label value",
        "name": "labelvalue"
      }
    ]
  },
  "nodes": [
    {
      "nodeType": "tomcat",
      "cloudlets": 6,
      "distribution": {
        "mode": "SOFT",
        "zones": [
          {
            "${settings.labelname}": "${settings.labelvalue}"
          }
        ]
      }
    }
  ]
}
```
@@!


<h2>What’s next?</h2>

- Explore the list of available <a href="../actions/" target="_blank">Actions</a>                                   

- See the <a href="../events/" target="_blank">Events</a> list the actions can be bound to                                  

- Find out the list of <a href="../placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching                                         

- Read how to integrate your <a href="../custom-scripts/" target="_blank">Custom Scripts</a>                                 

- Learn how to customize <a href="../visual-settings/" target="_blank">Visual Settings</a>                            
