# Specifying Target Container

##Selector Types
Running a specific <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">action</a> requires to set a target container, in confines of which this action will be executed. Thus, it is possible to specify a particular container, all containers within a layer by their <a href="http://docs.cloudscripting.com/reference/container-types/#containers-by-groups-nodegroup" target="_blank">*nodeGroup*</a> value (e.g. *sql*) or all containers of the same type by their <a href="http://docs.cloudscripting.com/reference/container-types/#containers-by-types-nodetype"target="_blank">*nodeType*</a> value (e.g. *MySQL*).          

Also, there are three alternative approaches to set containers filtering:       

* **Node Selectors** - specifying a target node within a name of an action     

For example:  
``` json
{
    "createFile [cp]" : {
          "path" : "/tmp/test.txt"
    }
}, {
    "createDirectory [cp,bl,123]" : {
          "path" : "/tmp/test.txt"
    }
}
```
In the example above, a new file will be created in the compute node (*[cp]*) and a new directory will be created in the compute node (*[cp]*) and balancer (*[bl]*) [layers](http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-group) and container with [Node ID](http://docs.cloudscripting.com/creating-templates/selecting-containers/#particular-container) *123*. Actions for the specified nodes are executed in the declared order.       

* setting a target node next to the performed action     

For example:     
``` json
{
  "createFile": {
    "path": "/tmp/test.txt"
  },
  "createDirectory": {
    "path": "/tmp/test"
  },
  "nodeGroup": "cp"
}
``` 
Here, the `createFile` and `createDirectory` actions are applied to the specified *nodeGroup*, namely compute node (*[cp]*) layer.         
 
* setting a required node as a parameter in the action object     

Learn more on this <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank">parameter</a> within the linked page.             

!!! note 
    > **Node Selectors** have higher priority than nodes specified next to the action but lower than parameters set in the action object.     

Have a look at more detailed descriptions on approaches available to set a target container:          
- [Particular Container](#particular-container)   
- [All Containers By Group](#all-containers-by-group)    
- [All Containers By Type](#all-containers-by-type)   

<h3>Particular Container</h3>   
The `nodeId` parameter is used to set a particular container for the action to be executed at it. If you know the **Node ID** of a container (displayed at the Jelastic dashboard next to the required node), you can set it statically.       
  
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

If you don't know the ID or a container hasn't been created yet, you can set a dynamic value using special placeholders.       

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

Visit the <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> documentation page for more information.      

<h3>All Containers By Group</h3>   
 
The `nodeGroup` value is used to point out all containers within a specific layer.   

Jelastic platform supports the following predefined *nodeGroup* values:     
- *bl*  
- *cp*  
- *sqldb*   
- *nosqldb*   
- *cache*  
- *build*   
- *vps*         

Actions for a specified *nodeGroup* are executed successively one by one. For Docker containers the *nodeGroup* value is not predefined, therefore, it can be stated to any value above or your custom one. Visit the <a href="http://docs.cloudscripting.com/reference/container-types/#containers-by-groups-nodegroup" target="_blank">Containers by Groups</a> documentation page for more information.        

<h3>All Containers By Type</h3>
The `nodeType` parameter is applied to set all containers built upon the same software stacks. Visit the <a href="http://docs.cloudscripting.com/reference/container-types/#containers-by-types-nodetype"target="_blank">Containers by Types</a> documentation page to explore the provided containers listed according to their type.    	  

For example:

Using the nodeType field while performing the writeFile action:

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
- `nodeType` - value to define a particular node, where file is located
- `path` - parameter specifying path to a file
- `body` - data that is being written to a file  

Creating an environment with topology specifics, set by the engine and nodeType values:

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

- `engine` - value that specifies engine version (java7 in our example)
- `nodeType` - value that specifies compute node type (tomcat7 in our example)

Below you can find data on supported software stacks in confines of the nodeGroup, nodeType and engine values.

!!! note
    > Upon stating non-predefined (i.e. custom) *nodeGroup* value for *Docker* containers, the corresponding container will be placed to the *Extra* layer:               
    <br><center>![extra](/img/extra_layer.jpg)</center>            
    Subsequently, this *nodeGroup* value can be used within the same-named <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">actions</a> field to point to a particular *Extra* layer.                 

!!! note
    > If you set all three parameters, actions for indicated containers would be executed in the following order: <b>*_nodeId -> nodeGroup -> nodeType_*</b>. 

##Supported Stacks
<b>Predefined *nodeGroup* values</b>                 

Jelastic platform supports the following predefined *nodeGroup* values:                         

- **lb** (for load balancers) - *nginx, varnish, haproxy*                     
- **cp** (for compute nodes) - *tomcat6, tomcat7, tomcat8, tomee, glassfish3, glassfish4, jetty6, jetty8, jetty9, jboss7, smartfox-server, powerdns, railo4, wildfly, wildfly9, wildfly10, apache2, nginxphp, apache2-python, apache2-ruby, nginx-ruby, nodejs*                     
- **sql** (for *sql* databases) - *mysql5, mariadb, mariadb10, postgres8, postgres9*                          
- **nosql** (for *nosql* databases) - *mongodb, couchdb, redis, redis3, cassandra2*                   
- **vps** (for virtual private servers) - *centos6, centos7*                        
- **cache** (for a cache server) - *memcached*                       
- **build** (for a build node) - *maven3*                     
- **storage** (for a storage container) - *storage*                        

**Containers by Types** (`nodeType`)

Jelastic Platform supports the following software stacks:         

- **Compute nodes:**                  
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
- **SQL Databases:**                     
     - `mysql5` - *MySQL*                       
     - `mariadb` - *MariaDB 5*                    
     - `mariadb10` - *MariaDB 10*                    
     - `postgres8` - *PostgreSQL 8*                  
     - `postgres9` - *PostgreSQL 9*                    
- **NoSQL Databases:**   
     - `mongodb` - *MongoDB*           
     - `couchdb` - *CouchDB*             
     - `redis` - *Redis 2.8*                 
     - `redis3` - *Redis 3.2*                
     - `cassandra2` - *Cassandra 2*             
- **Balancers:**   
     - `nginx` - *Nginx* balancer                        
     - `haproxy` - *HAProxy* balancer                     
     - `varnish` - *Varnish 4*                    
- **Build node:**   
     - `maven3` - *Мaven*                  
- **Cache node:**                    
     - `memcached` - *Мemcached*                     
- **Virtual Private Server nodes:**                         
     - `centos6` - *CentOS 6*                  
     - `centos7` - *CentOS 7*               
- **Storage:**                 
     - `storage` - *Shared storage*                 
- **Docker containers:**                               
     - `docker`                 
         
**Engine Versions** (`engine`)

The following section deals with supported engine versions and their availability for a corresponding *nodeType* (in confines of the compute nodes).                               

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

!!! note
    > The list of supported <a href="https://docs.jelastic.com/software-stacks-versions" target="_blank">software stacks</a> can vary depending on your Jelastic platform version - it can be checked at your dashboard.  
