# Container by Groups and Types

Container nodeType defines software stack (among the supported ones) to be deployed within a node. Node type value is used in "nodeType" field for [Actions](/reference/actions/).

**Examples:**

Using `nodeType` field in [action](/reference/actions/#writefile) `writeFile`:
```
{
  "writeFile": {
    "nodeType": "apache2",
    "path": "/tmp/example.txt",
    "body": "Hello World"
  }
} 
```
Install `nodeType` tomcat7 with `java7` engine:
```
{
  "env": {
    "topology": {
      "engine": "java7",
      "nodes": [
        {
          "count": 1,
          "nodeType": "tomcat7"
        }
      ]
    }
  }
}
```
Below you can find the list of available [`nodeType`](/reference/container-types/#nodetype-values) and [`engine`](/reference/container-types/#engine-versions) values.

##Container by Groups (nodeGroup)

The nodeGroup parameter is used to define how to separate nodeType on groups, i.e. determines environment layer the container(s) should be placed to.
The nodeGroup value can be used within 'nodeType' field for [Actions](/reference/actions/) too.

For **Docker-based** containers, `nodeGroup` can be started to any value - either [predefined](/reference/container-types/#containers-by-group) or your custom one.    
For example:
```
{
  "env": {
    "topology": {
      "nodes": [
        {
          "docker": {
            "image": "dockerImage:latest"
          },
          "cloudlets": 8,
          "nodeGroup": "customGroup"
        }
      ]
    }
  }
}
```
- `customGroup` - custom NodeGroup. In [actions](/reference/actions/) it can be called via field `"nodeGroup":"customGroup"`
!!! note
    > If specified `nodeGroup` is not predefined at Jelastic platform, the container will be placed to *Extra* layer:    
    ![extra](https://download.jelastic.com/public.php?service=files&t=2bda4051062f413278b693d2898cdcbd&download)    
    Subsequently, this nodeGroup value can be used within the same-named field of [Actions](/reference/actions/) to address to a particular extra layer.

Jelastic platform supports the next predefined `nodeGroup` values:

- **bl** (for balancer nodes) - `nginx`, `varnish`, `haproxy`
- **cp** (for compute nodes) - `tomcat6`, `tomcat7`, `tomcat8`, `tomee`, `glassfish3`, `glassfish4`, `jetty6`, `jetty8`, `jetty9`, `jboss7`, `smartfox-server`, `powerdns`, `railo4`, `wildfly`, `wildfly9`, `wildfly10`, `apache2`, `nginxphp`, `apache2-python`, `apache2-ruby`, `nginx-ruby`, `nodejs`
- **sql** - `mysql5`, `mariadb`, `mariadb10`, `postgres8`, `postgres9`
- **nosql** - `mongodb`, `couchdb`, `redis`, `redis3`, `cassandra2` 
- **vps** - `centos6`, `centos7`
- **cache** - `memcached`
- **build** - `maven3`
- **storage** - `storage`

## Container by Types (nodeType)
- **Compute nodes:**
    - Java
        - `tomcat6` - Tomcat 6
        - `tomcat7` - Tomcat 7
        - `tomcat8` - Tomcat 8
        - `tomee` - TomEE
        - `glassfish3` - GlassFish 3
        - `glassfish4` - GlassFish 4
        - `jetty6` - Jetty 6
        - `jetty8` - Jetty 8
        - `jetty9` - Jetty 9
        - `jboss7` - Jbossas 7
        - `smartfox-server` - SmartFoxServer 2X
        - `powerdns` - Powerdns 3
        - `railo4` - Railo4 9
        - `wildfly` - Wildfly 8
        - `wildfly9` - Wildfly 9
        - `wildfly10` - Wildfly 10
    - PHP
        - `apache2` - Apache 2
        - `nginxphp` - Nginx PHP
    - Python
        - `apache2-python` - Apache 2 + Python
    - Ruby
        - `apache2-ruby` - Apache 2 + Ruby
        - `nginx-ruby` - Nginx Ruby
    - Node.js
        - `nodejs` - Node.js
- **SQL Databases:**
    - `mysql5` - MySQL
    - `mariadb` - MariaDB 5
    - `mariadb10` - MariaDB 10
    - `postgres8` - PostgreSQL 8
    - `postgres9` - PostgreSQL 9
- **NoSQL Databases:**
    - `mongodb` - MongoDB
    - `couchdb` - CouchDB
    - `redis` - Redis 2.8
    - `redis3` - Redis 3.2
    - `cassandra2` - Cassandra 2
- **Balancers:**
    - `nginx` - Nginx balancer
    - `haproxy` - HAProxy balancer
    - `varnish` - Varnish 4
- **Build node:**
    - `maven3` - Мaven
- **Cache node:**
    - `memcached` - Мemcached
- **Virtual Private Server nodes:**
    - `centos6` - CentOS 6
    - `centos7` - CentOS 7
- **Storage:**
    - `storage` - Shared storage
- **Docker-based nodes:**
    - `docker`

##Jelastic Native Container Types
- `apache2-ruby`
- `apache2`
- `couchdb`
- `glassfish3`
- `jetty6`
- `mariadb`
- `mariadb10`
- `maven3`
- `memcached`
- `mongodb`
- `mysql5`
- `nginx-ruby`
- `nginx`
- `nginxphp`
- `nodejs`
- `postgres8`
- `postgres9`
- `postgresql`
- `tomcat6`
- `tomcat7`
- `tomee`
- `storage`

## Engine versions (engine)

**Java Stacks**

|nodeType|`tomcat6`|`tomcat7`|`tomcat8`|`tomee`|`glassfish3`|`glassfish4`|`jetty6`|`jetty8`|`jetty9`|
|------------|------|---------|---------|-------|------------|------------|--------|--------|--------|
|engine|java6<br>java7<br>java8|java6<br>java7<br>java8|java7<br>java8|java7<br>java8|java6<br>java7|java7<br>java8|java6<br>java7<br>java8|java6<br>java7<br>java8|java8|

|nodeType|`jboss7`|`smartfox-server`|`powerdns`|`railo4`|`wildfly`|`wildfly9`|`wildfly10`|
|--------|--------|---------------- |----------|--------|---------|----------|-----------|
|engine  |java7|java6<br>java7<br>java8|java6|java7<br>java8|java7<br>java8|java7<br>java8|java8|

**PHP Stacks**

|nodeType|`apache2`                                   |`nginxphp`                                  |
|--------|--------------------------------------------|--------------------------------------------|
|engine  |php5.3<br>php5.4<br>php5.5<br>php5.6<br>php7|php5.3<br>php5.4<br>php5.5<br>php5.6<br>php7|

**Ruby Stacks**

|nodeType|`apache2-ruby`                                     |`nginx-ruby`                                       |
|--------|---------------------------------------------------|---------------------------------------------------|
|engine  |ruby1.9<br>ruby2.0<br>ruby2.1<br>ruby2.2<br>ruby2.3|ruby1.9<br>ruby2.0<br>ruby2.1<br>ruby2.2<br>ruby2.3|

**Python Stack**

|nodeType|`apache2-python`                                |
|--------|------------------------------------------------|
|engine  |python2.7<br>python3.3<br>python3.4<br>python3.5|

**Nodejs Stack**

|nodeType|`nodejs`            |
|--------|--------------------|
|engine  |nodejs0.10<br>nodejs0.12<br>nodejs4.3<br>nodejs5.6|

!!! note
    > List of supported [Jelastic Stack Versions](https://docs.jelastic.com/software-stacks-versions) can be vary for different platform versions.
