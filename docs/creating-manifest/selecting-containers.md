# Specifying Target Container

Running a specific <a href="/1.2/creating-manifest/actions/" target="_blank">action</a> requires to specify a target container, in confines of which this action is executed. Thus, it is possible to specify a [particular container](#particular-container), all containers within a layer by the [*nodeGroup*](#all-containers-by-group) value, or all containers of the same type by the [*nodeType*](#all-containers-by-type) value.                                 

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
For more information, visit the <a href="/1.2/creating-manifest/placeholders/" target="_blank"><em>Placeholders</em></a> documentation page.                               

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

Using the *nodeType* parameter while performing the <a href="/1.2/creating-manifest/actions/#writefile" target="_blank">**writeFile**</a> action.                         
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
- specifying a target container next to the performed action                                       

Through the following example, the <a href="/1.2/creating-manifest/actions/#createfile" target="_blank">**createFile**</a> and <a href="/1.2/creating-manifest/actions/#createdirectory" target="_blank">**createDirectory**</a> actions are applied to the specified <em>nodeGroup</em>, namely the compute layer (<em>[cp]</em>).
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

Learn more on this parameter within the <a href="/1.2/creating-manifest/actions/#custom-actions" target="_blank"><em>Custom Actions</em></a> documentation page.                                      

!!! note 
    <b>Node selectors</b> have higher priority than containers specified next to the action, but lower than parameters set in the *actions* object.   
    If you specify all three parameters (*nodeId*, *nodeGroup*, and *nodeType*), actions for indicated containers are executed in the following order: <b>*_nodeId -> nodeGroup -> nodeType_*</b>.   

## Supported Stacks                                  

Below you can find data about supported software stacks in confines of the *nodeGroup*, *nodeType*, and *engine* values.                             

### Predefined *nodeGroup* Values                   

The Jelastic Platform supports the following predefined *nodeGroup* values:                           

- **bl** (for load balancers) - *nginx, varnish, haproxy, apache-lb*                     

- **cp** (for compute nodes) - *tomcat6, tomcat7, tomcat8, tomee, glassfish3, glassfish4, jetty6, jetty8, jetty9, jboss7, smartfox-server, powerdns, railo4, wildfly, wildfly9, wildfly10, springboot, apache2, nginxphp, apache2-python, apache2-ruby, nginx-ruby, nodejs, iis8*                         

- **sqldb** (for SQL databases) - *mysql5, mysql5-6, mariadb, mariadb10, postgres8, postgres9, mssql, mssqlweb, mssqlstd*                             

- **nosqldb** (for NoSQL databases) - *mongodb, mongodb2, couchdb, redis, redis3, cassandra, cassandra2, cassandra3, neo4j, neo4j2-1, neo4j3, orientDB, orientDB2, Percona*                   

- **vds** (for virtual private servers, VPS) - *centos6, centos7, ubuntu16-04, windows2008, windows2012*                          

- **cache** (for a cache server) - *memcached*                         

- **build** (for a build node) - *maven3*                                   

- **storage** (for a storage container) - *storage*                                                          

### Predefined *nodeType* Values   

The Jelastic Platform supports the following software stacks:         

- **Compute Nodes (cp):**                  
    - *Java*                
        - `tomcat6` - *Tomcat 6*                
        - `tomcat7` - *Tomcat 7*               
        - `tomcat8` - *Tomcat 8*                       
        - `tomee` - *TomEE*              
        - `glassfish3` - *GlassFish 3*             
        - `glassfish4` - *GlassFish 4*                      
        - `jetty6` - *Jetty 6*                                      
        - `jetty8` - *Jetty 8*                  
        - `jetty9` - *Jetty 9*        
        - `jboss7` - *Jbossas 7*                
        - `smartfox-server` - *SmartFoxServer 2X*                     
        - `powerdns` - *Powerdns 3*             
        - `railo4` - *Railo4 9*          
        - `wildfly` - *Wildfly 8*         
        - `wildfly9` - *Wildfly 9*                       
        - `wildfly10` - *Wildfly 10* 
        - `springboot` - *SpringBoot 1.x-2.x* 
    - *PHP*              
        - `apache2` - *Apache 2*                
        - `nginxphp` - *Nginx PHP*          
    - *Python*                     
        - `apache2-python` - *Apache 2 + Python*                       
    - *Ruby*            
        - `apache2-ruby` - *Apache 2 + Ruby*                    
        - `nginx-ruby` - *Nginx Ruby*                    
    - *Node.js*                  
        - `nodejs` - *Node.js*       
    - *Web Server (IIS)*
        - `iis8` - *Web Server (IIS)*
- **SQL Databases (sqldb):**
     - `mysql5` - *MySQL*
     - `mariadb` - *MariaDB 5*
     - `mariadb10` - *MariaDB 10*
     - `postgres8` - *PostgreSQL 8*
     - `postgres9` - *PostgreSQL 9*
     - `mssql` - *MSSQL 2012*
     - `mssqlweb` - *MSSQL Web*
     - `mssqlstd` - *MSSQL std*
- **NoSQL Databases (nosqldb):**   
     - `mongodb` - *MongoDB*
     - `mongodb2` - *MongoDB 2*
     - `couchdb` - *CouchDB*
     - `redis` - *Redis 2.8*
     - `redis3` - *Redis 3.2*
     - `cassandra2` - *Cassandra 2*
     - `cassandra3` - *Cassandra 3*
     - `neo4j` - *Neo4j*
     - `neo4j2-1` - *Neo4j2-1*
     - `neo4j3` - *Neo4j3*
     - `orientDB` - *OrientDB*
     - `orientDB2` - *OrientDB 2*
     - `Percona` - *Percona 5*
- **Balancers (bl):**
     - `nginx` - *Nginx* balancer
     - `haproxy` - *HAProxy* balancer
     - `apache-lb` - *Apache* balancer
     - `varnish` - *Varnish 4*
- **Build Node (build):**
     - `maven3` - *Мaven*
- **Cache Node (cache):**
     - `memcached` - *Мemcached*
- **Virtual Private Servers (vps):**
     - `centos6` - *CentOS 6*
     - `centos7` - *CentOS 7*
     - `ubuntu16-04` - *Ubuntu16-04*
     - `windows2008` - *Windows2008*
     - `windows2012` - *Windows2012*
- **Storage (storage):**
     - `storage` - *Shared storage*
- **Docker Containers (docker):**
     - `docker`

###Dokerized Template Tags

There is a list of `dokerized` supported Jelastic templates with their tags:

|nodeType|`tomcat`|`tomee`|`apache2`|`nginxphp`|`nginx(lb)`|`mysql5`|
|--------|--------|-------|---------|----------|-----------|--------|
|**tag**|*6.0.45-jdk-1.6.0_45*<br>*6.0.45-jdk-1.7.0_79*<br>*6.0.45-jdk-1.8.0_102*<br>*7.0.73-jdk-1.8.0_102*<br>*7.0.73-jdk-1.6.0_45*<br>*7.0.73-jdk-1.7.0_79*<br>*8.5.5-jdk-1.7.0_79*<br>*8.5.5-jdk-1.8.0_102*|*7.0.1-jdk-1.7.0_79*<br>*7.0.1-jdk-1.8.0_102*|*2.4.6-php-5.3.29*<br>*2.4.6-php-5.4.45*<br>*2.4.6-php-5.5.38*<br>*2.4.6-php-5.6.28*<br>*2.4.6-php-7.0.13*<br>*2.4.6-php-7.1.0*|*1.10.1-php-5.3.29*<br>*1.10.1-php-5.4.45*<br>*1.10.1-php-5.5.38*<br>*1.10.1-php-5.6.28*<br>*1.10.1-php-7.0.10*<br>*1.10.1-php-7.0.13*<br>*1.10.1-php-7.1.0*|*1.10.1*|*5.7.14*|


|nodeType|`mysql5-6`|`mariadb`|`mariadb10`|`memcached`|`maven3`|`varnish`|
|--------|----------|---------|-----------|-----------|--------|---------|
|**tag**|*5.6.32*|*5.5.51*|*10.1.20*|*memcached*|*3.3.9-jdk-1.7.0_79*<br>*3.3.9-jdk-1.8.0_102*|*4.1.5*

### Engine Versions

The following section deals with the supported engine versions and their availability for a corresponding *nodeType* (in confines of the compute nodes).                                  

**Java Stacks**

|nodeType|`tomcat6`|`tomcat7`|`tomcat8`|`tomee`|`glassfish3`|`glassfish4`|`jetty6`|`jetty8`|`jetty9`|
|------------|------|---------|---------|-------|------------|------------|--------|--------|--------|
|engine|*java6*<br>*java7*<br>*java8*|*java6*<br>*java7*<br>*java8*|*java7*<br>*java8*|*java7*<br>*java8*|*java6*<br>*java7*|*java7*<br>*java8*|*java6*<br>*java7*<br>*java8*|*java6*<br>*java7*<br>*java8*|*java8*|

|nodeType|`jboss7`|`smartfox-server`|`powerdns`|`railo4`|`wildfly`|`wildfly9`|`wildfly10`|
|--------|--------|---------------- |----------|--------|---------|----------|-----------|
|engine  |*java7*|*java6*<br>*java7*<br>*java8*|*java6*|*java7*<br>*java8*|*java7*<br>*java8*|*java7*<br>*java8*|*java8*|

**PHP Stacks**

|nodeType|`apache2`                                   |`nginxphp`                                  |
|--------|--------------------------------------------|--------------------------------------------|
|engine  |*php5.3*<br>*php5.4*<br>*php5.5*<br>*php5.6*<br>*php7*|*php5.3*<br>*php5.4*<br>*php5.5*<br>*php5.6*<br>*php7*|

**Ruby Stacks**

|nodeType|`apache2-ruby`                                     |`nginx-ruby`                                       |
|--------|---------------------------------------------------|---------------------------------------------------|
|engine  |*ruby1.9*<br>*ruby2.0*<br>*ruby2.1*<br>*ruby2.2*<br>*ruby2.3*|*ruby1.9*<br>*ruby2.0*<br>*ruby2.1*<br>*ruby2.2*<br>*ruby2.3*|

**Python Stacks**

|nodeType|`apache2-python`                                |
|--------|------------------------------------------------|
|engine  |*python2.7*<br>*python3.3*<br>*python3.4*<br>*python3.5*|

**Nodejs Stacks**

|nodeType|`nodejs`            |
|--------|--------------------|
|engine  |*nodejs0.10*<br>*nodejs0.12*<br>*nodejs4.3*<br>*nodejs5.6*|

**.Net**

|nodeType|`iis8`            |
|--------|--------------------|
|engine  |*.NET 4*|

!!! note
    The list of supported <a href="https://docs.jelastic.com/software-stacks-versions" target="_blank">software stacks</a> can vary depending on your Jelastic Platform version - it can be checked at your dashboard.              

<h2>What’s next?</h2>

- Explore the list of available <a href="/1.2/creating-manifest/actions/" target="_blank">Actions</a>                                   

- See the <a href="/1.2/creating-manifest/events/" target="_blank">Events</a> list the actions can be bound to                                  

- Find out the list of <a href="/1.2/creating-manifest/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching                                         

- Read how to integrate your <a href="/1.2/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>                                 

- Learn how to customize <a href="/1.2/creating-manifest/visual-settings/" target="_blank">Visual Settings</a>                            
