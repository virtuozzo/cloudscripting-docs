# Specifying Target Container

Running a specific <a href="/1.6/creating-manifest/actions/" target="_blank">action</a> requires to specify a target container, in confines of which this action is executed. Thus, it is possible to specify a [particular container](#particular-container), all containers within a layer by the [*nodeGroup*](#all-containers-by-group) value, or all containers of the same type by the [*nodeType*](#all-containers-by-type) value.                                 

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
For more information, visit the <a href="/1.6/creating-manifest/placeholders/" target="_blank"><em>Placeholders</em></a> documentation page.                               

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

Using the *nodeType* parameter while performing the <a href="/1.6/creating-manifest/actions/#writefile" target="_blank">**writeFile**</a> action.                         
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

Through the following example, the <a href="/1.6/creating-manifest/actions/#createfile" target="_blank">**createFile**</a> and <a href="/1.6/creating-manifest/actions/#createdirectory" target="_blank">**createDirectory**</a> actions are applied to the specified <em>nodeGroup</em>, namely the compute layer (<em>[cp]</em>).
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

Learn more on this parameter within the <a href="/1.6/creating-manifest/actions/#custom-actions" target="_blank"><em>Custom Actions</em></a> documentation page.                                      

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


<table>
	<tr>
		<th>nodeGroup</th><th>Supported nodeType Values and Aliases</th><th>Supported Tags Link</th>
	</tr>
	<tr>
		<td>bl</td><td>nginx, varnish, haproxy, apache-lb</td><td><a href="https://docs.jelastic.com/software-stacks-versions#lb">Load-Balancers</a></td>
	</tr>
	<tr>
		<td>cp</td><td>tomcat7, tomcat8, tomee, glassfish, glassfish3, glassfish4, jetty, jetty6, jetty8, jetty9, smartfox-server, powerdns, railo4, wildfly, springboot, apache2, nginxphp, apache2-python, apache2-ruby, nginx-ruby, nodejs, iis8</td><td><a href="https://docs.jelastic.com/software-stacks-versions#app-servers">Application Servers</a></td>
	</tr>
	<tr>
		<td>sqldb, nosqldb</td><td>mysql, mysql5, mysql5-6, mariadb, mariadb10, postgres9, postgresql, percona, mssql,
mongodb, mongodb2, couchdb, redis, redis3, redis4, cassandra, cassandra2, cassandra3, neo4j, neo4j2-1, neo4j3, orientDB, orientDB2
</td><td><a href="https://docs.jelastic.com/software-stacks-versions#databases">Databases</a></td>
	</tr>
	<tr>
		<td>vps, cache, build, proxysql, storage</td><td>centos6, centos7, ubuntu16-04, memcached, maven3, proxysql, storage, windows2008, windows2012</td><td><a href="https://docs.jelastic.com/software-stacks-versions#additional">Additional Stacks</a></td>
	</tr>
</table>

<table>
	<tr>
		<td><strong>Note:</strong> In case the root privileges are required within the certified template, it should be created as custom docker via <a href="http://docs.cloudscripting.com/creating-manifest/basic-configs/#environment-installation">image</a> parameter. If so, take into account that some functionality/automation won’t be available such as Custom SSL, Managed Firewall, etc.
          To create custom docker follow the <strong>Supported Tags Link</strong> column to get the proper name of certified Jelastic docker images.</td>
	</tr>
</table>

<a href="https://docs.jelastic.com/software-stacks-versions#engines">Engine versions</a>

<table>
	<tr>
		<th>Stacks</th><th>Java</th><th>PHP</th><th>Ruby</th><th>Python</th><th>Nodejs</th><th>ii8</th>
	</tr>
	<tr>
		<td  valign=top>engine</td>
<td valign=top>
java6

java7

java8

jdk-9

jdk-10

jdk-1.8.0_144

jdk-1.8.0_152
</td>
<td valign=top>
php5.3

php5.4

php5.5

php5.6

php7

php7.1.13

php7.1.7

php7.2.1
</td>
<td valign=top>
ruby1.9

ruby2.0

ruby2.1

ruby2.2

ruby2.3

ruby2.4.1
</td>
<td valign=top>
python2.7

python3.3

python3.4

python3.5
</td>
<td valign=top>
nodejs6.11.5

nodejs6.12.3

nodejs8.9.0

nodejs8.9.4

nodejs9.0.0

nodejs9.4.0
</td>
<td valign=top>.NET 4</td>
	</tr>
</table>

!!! note
    The list of supported <a href="https://docs.jelastic.com/software-stacks-versions" target="_blank">software stacks</a> can vary depending on your Jelastic Platform version - it can be checked at your dashboard.              

<h2>What’s next?</h2>

- Explore the list of available <a href="/1.6/creating-manifest/actions/" target="_blank">Actions</a>                                   

- See the <a href="/1.6/creating-manifest/events/" target="_blank">Events</a> list the actions can be bound to                                  

- Find out the list of <a href="/1.6/creating-manifest/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching                                         

- Read how to integrate your <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>                                 

- Learn how to customize <a href="/1.6/creating-manifest/visual-settings/" target="_blank">Visual Settings</a>                            
