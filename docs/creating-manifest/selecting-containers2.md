# Specifying Target Container

Running a specific <a href="../actions/" target="_blank">action</a> requires to specify a target container, in confines of which this action is executed. Thus, it is possible to specify a [particular container](#particular-container), all containers within a layer by the [*nodeGroup*](#all-containers-by-group) value, or all containers of the same type by the [*nodeType*](#all-containers-by-type) value.                                 

### Particular Container

The <em>nodeId</em> parameter is used to specify a particular container for the action execution. If you know the Node ID of your container (displayed at the Jelastic dashboard next to the required node), you can set it statically as follows.                                           

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

The Jelastic Platform supports the following predefined *nodeGroup* values:     

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
| bl                                   | nginx-dockerized (nginx), varnish-dockerized (varnish), haproxy(haproxy2), apache-lb (apache-balancer), litespeedadc (litespeedadc2, litespeedadc3)                                                                                                                                                                                           | [Load-Balancers](https://docs.jelastic.com/software-stacks-versions#lb)      |
| cp                                   | tomcat (tomcat10, tomcat7, tomcat85, tomcat9), tomee-dockerized(tomee), glassfish (glassfish6, glassfish3, glassfish5), payara (payara5, payara3), jetty (jetty9, jetty10, jetty11), wildfly (wildfly21, wildfly22, wildfly23), springboot, apache (apache2), nginxphp-dockerized (nginxphp), apache-python (apache2-python), apache-ruby (apache2-ruby), nginxruby (nginx-ruby), nodejs, iis8, litespeedphp(litespeedphp5, litespeedphp6), lemp, llsmp, golang | [Application Servers](https://docs.jelastic.com/software-stacks-versions#app-servers) |
| sqldb, nosqldb                       | mysql (mysql5, mysql5-6), mariadb-dockerized (mariadb10), postgresql (postgres9, postgres10, postgres11, postgres12, postgres13), perconadb (percona5.5, percona5.6, percona5.7, percona8), mssql, mongodb-dockerized(mongodb), couchbase, redis (redis4, redis5, redis6)        | [Databases](https://docs.jelastic.com/software-stacks-versions#databases)           |
| vps, cache, build, proxysql, storage | centos-vps(centos7), ubuntu-vps(ubuntu16, ubuntu18, ubuntu20), memcached-dockerized(memcached), maven(maven3), proxysql, storage, windows2012                                                                                                                                | [Additional Stacks](https://docs.jelastic.com/software-stacks-versions#additional)   |

!!! note
    In case the root privileges are required within the certified template, it should be created as custom docker via [image](basic-configs/#environment-installation) parameter. If so, take into account that some functionality/automation won’t be available such as Custom SSL, Managed Firewall, etc. To create custom docker follow the **Supported Tags Link** column to get the proper name of certified Jelastic docker images.

<a href="https://docs.jelastic.com/software-stacks-versions#engines">Engine versions</a>

|Stacks|Java|PHP|Ruby|Python|Nodejs|ii8|Go|
|--------|----------|-----------|-----------|--------|---------|---------|---------|
|engine|graalvm8<br>dragonwell8<br>java8<br>java11<br>openj98<br>openj911<br>openj916<br>openjdk7<br>openjdk8<br>openjdk11<br>openjdk14<br>openjdk15<br>openjdk16<br>openjdk17<br>adoptopenjdk8<br>adoptopenjdk11<br>adoptopenjdk16<br>correttojdk8<br>correttojdk11<br>correttojdk15<br>correttojdk16<br>libericajdk8<br>libericajdk11<br>libericajdk14<br>libericajdk15<br>libericajdk16<br>zulujdk7<br>zulujdk8<br>zulujdk11<br>zulujdk13<br>zulujdk14<br>zulujdk15<br>zulujdk16<br>|php7.3<br>php7.4<br>php8.0|ruby2.5<br>ruby2.6<br>ruby2.7<br>ruby3.0|python3.6<br>python3.7<br>python3.8<br>python3.9|nodejs12-supervisor<br>nodejs14-supervisor<br>nodejs15-supervisor<br>nodejs16-supervisor|dotnet3<br>dotnet5|go|

!!! note
    The list of supported <a href="https://docs.jelastic.com/software-stacks-versions" target="_blank">software stacks</a> can vary depending on your Jelastic Platform version - it can be checked at your dashboard.    
    
## Selecting Hardware Hosts

There is an ability in Jelastic PaaS to select the hardware for the user's application with the help of the [multi zones](https://ops-docs.jelastic.com/multi-zones) approach. If a user is aware all of the [labels](https://ops-docs.jelastic.com/multi-zones#host-labels) assigned for the hardware hosts within the platform he can decide which hosts across all of the available regions can be used to install the user's environment.  
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
