# Specifying Target Container

## Selector Types

Running a specific <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">action</a> requires to specify a target container, in confines of which this action will be executed. Thus, it is possible to specify a [particular container](#particular-container), all containers within a layer by their [*nodeGroup*](#all-containers-by-group) value (e.g. <em>sql</em>) or all containers of the same type by their [*nodeType*](#all-containers-by-type) value (e.g. <em>MySQL</em>).                                 

### Particular Container

The <em>nodeId</em> parameter is used to set a particular container for an action to be executed at it. If you know the Node ID of a container (displayed at the Jelastic dashboard next to the required node), you can set it statically.                     
  
For example:
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
If you don't know the Node ID or a container is not created yet, you can set a dynamic value, using special placeholders.       

For example:  
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
Visit the <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank"><em>Placeholders</em></a> documentation page for more information.      

### All Containers By Group        
 
The *nodeGroup* value is used to point out all containers within a specific layer.            

The Jelastic Platform supports the following predefined *nodeGroup* values:     

- *bl*             
- *cp*                 
- *cache*                 
- *sqldb*            
- *nosqldb*            
- *storage*                  
- *vps*                
- *build*        

Actions for the specified <em>nodeGroup</em> are executed successively one by one. For Docker containers the <em>nodeGroup</em> value is not predefined, therefore, it can be stated to any value above or your custom one.                              

!!! note
    Upon stating non-predefined (i.e. custom) <em>nodeGroup</em> value for Docker containers, the corresponding container will be placed to the <em>Extra</em> layer. Subsequently, this <em>nodeGroup</em> value can be used within the same-named <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">actions</a> field to point to a particular <em>Extra</em> layer.
    <center>![dockerextra](/img/dockerextra.png)</center>         

### All Containers By Type

The <em>nodeType</em> parameter is applied to specify all containers that are built upon the same software [stacks](#supported-stacks ).                                   	  

<b>Examples</b>     

Using the *nodeType* field while performing the <a href="http://docs.cloudscripting.com/reference/actions/#writefile" target="blank">**writeFile**</a> action.
``` json
{
  "writeFile": {
    "nodeType": "apache2",
    "path": "/tmp/example.txt",
    "body": "Hello World"
  }
} 
```
where:                

- `writeFile` - action to write data to a file    
- `nodeType` - parameter to specify node(s) by type    
- `path` - parameter specifying path to a file    
- `body` - data that is being written to a file     

Creating an environment with topology specifics, set by the *engine* and *nodeType* values.   
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
where:          

- `engine` - parameter that specifies engine version (*java7* in our example)        
- `nodeType` - parameter that specifies node type (*tomcat7*  in our example)       

### Types of Selectors 

There are three alternative approaches, provided to specify target container(s) in a manifest.                          

- specifying a target node within a name of an action (**node selectors**)     

For example: 
``` json
[
  {
    "createFile [cp]": {
      "path": "/tmp/test.txt"
    }
  },
  {
    "createDirectory [cp,bl,123]": {
      "path": "/tmp/test.txt"
    }
  }
]
```
In the example above, a new file will be created in the compute node (<em>[cp]</em>) and a new directory will be created in the compute (<em>[cp]</em>) and balancer (<em>[bl]</em>) layers and container with Node ID <em>123</em>. Actions for the specified nodes are executed in the declared order.                 

- setting a target node next to the performed action     

For example:   
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
Here, the <em>createFile</em> and <em>createDirectory</em> actions are applied to the specified <em>nodeGroup</em>, namely the compute (<em>[cp]</em>) layer.                      
 
- specifying a required node as a parameter in the action object     

Learn more on this parameter within the <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank"><em>Custom Actions</em></a> documentation page.                                      

!!! note 
    <b>Node selectors</b> have higher priority than nodes, specified next to the action, but lower than parameters set in the action object.   
    If you set all three parameters (i.e *nodeId*, *nodeGroup* and *nodeType*), actions for indicated containers would be executed in the following order: <b>*_nodeId -> nodeGroup -> nodeType_*</b>.   

Below you can find data on supported software stacks in confines of the *nodeGroup*, *nodeType* and *engine* values.

## Supported Stacks

### Predefined nodeGroup Values                   

The Jelastic Platform supports the following predefined *nodeGroup* values:                           

- **lb** (for load balancers) - *nginx, varnish, haproxy, apache-lb*                     
- **cp** (for compute nodes) - *tomcat6, tomcat7, tomcat8, tomee, glassfish3, glassfish4, jetty6, jetty8, jetty9, jboss7, smartfox-server, powerdns, railo4, wildfly, wildfly9, wildfly10, apache2, nginxphp, apache2-python, apache2-ruby, nginx-ruby, nodejs, iis8*                     
- **sql** (for *sql* databases) - *mysql5, mysql5-6, mariadb, mariadb10, postgres8, postgres9, mssql, mssqlweb, mssqlstd*                          
- **nosql** (for *nosql* databases) - *mongodb, mongodb2, couchdb, redis, redis3, cassandra, cassandra2, cassandra3, neo4j, neo4j2-1, neo4j3, orientDB, orientDB2, Percona*                   
- **vds** (for virtual private servers) - *centos6, centos7, ubuntu16-04, windows2008, windows2012*                        
- **cache** (for a cache server) - *memcached*                       
- **build** (for a build node) - *maven3*                     
- **storage** (for a storage container) - *storage*  

### Predefined *nodeType* Values   

The Jelastic Platform supports the following software stacks:         

- **Compute Nodes:**                  
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
- **SQL Databases:**
     - `mysql5` - *MySQL*
     - `mariadb` - *MariaDB 5*
     - `mariadb10` - *MariaDB 10*
     - `postgres8` - *PostgreSQL 8*
     - `postgres9` - *PostgreSQL 9*
     - `mssql` - *MSSQL 2012*
     - `mssqlweb` - *MSSQL Web*
     - `mssqlstd` - *MSSQL std*
- **NoSQL Databases:**   
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
- **Balancers:**
     - `nginx` - *Nginx* balancer
     - `haproxy` - *HAProxy* balancer
     - `apache-lb` - *Apache* balancer
     - `varnish` - *Varnish 4*
- **Build Node:**
     - `maven3` - *Мaven*
- **Cache Node:**
     - `memcached` - *Мemcached*
- **Virtual Private Server nodes:**
     - `centos6` - *CentOS 6*
     - `centos7` - *CentOS 7*
     - `ubuntu16-04` - *Ubuntu16-04*
     - `windows2008` - *Windows2008*
     - `windows2012` - *Windows2012*
- **Storage:**
     - `storage` - *Shared storage*
- **Docker Containers:**
     - `docker`
         

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
<br>       
<h3> What’s next?</h3>                    

- Explore the list of available <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a>             
- See the <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">Events</a> list the actions can be bound to            
- Find out the list of <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching        
- Read how to integrate your <a href="http://docs.cloudscripting.com/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a>   
- Learn how to customize <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">Visual Settings</a>              
- Examine a bunch of <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> with operation and package examples    