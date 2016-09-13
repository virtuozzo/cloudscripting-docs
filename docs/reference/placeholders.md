# Placeholders
Cloud Scripting supports a list of placeholders that can be used in any section of manifest file (if the section isn't strictly limited with its content).
The executor will try to resolve all placeholders on the package installation stage.
If it's not possible placeholder will be unresolved and displayed in the text as is (e.g. ${placeholder})

!!! note
    To output all available placeholders you can use special placeholder: `${placeholders}`        
    See [Troubleshooting](/troubleshooting/) for more info.                                                                                         

## Environment placeholders

- `{env.}`
    - `${env.appid}` - application appid. String
    - `${env.domain}` - application domain. String
    - `${env.protocol}` - protocol. String
    - `${env.url}` - link to application (env). String
    - `${env.displayName}` - application display name. String
    - `${env.envName}` - short domain name (without hoster URL). String
    - `${env.shortdomain}` - short domain name. Alias to `envName`. String
    - `${env.hardwareNodeGroup}` - hardware node node group. String
    - `${env.ssl}` - env SSL status. Boolean
    - `${env.sslstate}` env SSL state. Boolean
    - `${env.status}` environment status. Available statuses are: 1 - running, 2 - down, 3 - launching, 4 - sleep, 6 - creating, 7 - cloning, 8 - exists. Number
    - `${env.uid}` - user uid. Number
    - `${env.ishaenabled}` - High availability status. Boolean
    - `${env.ha}` - alias to `${env.ishaenabled}`. Boolean
    - `${env.isTransferring}` - transfering status. Boolean
    - `${env.creatorUid}` - env creator ID. Number
    - `${env.engine.id}` - engine ID. Number
    - `${env.engine.keyword}` - engine keyword. String
    - `${env.engine.name}` - engine name. String
    - `${env.engine.type}` - engine type. String
    - `${env.engine.vcsSupport}` - vcs support status. Boolean
    - `${env.engine.version}` - engine version. String
    - `${env.contexts.type}` - env context type. String
    - `${env.contexts.context}` - context name
    - `${env.contexts.archivename}` - context display name
    
## Node placeholders    
- `${nodes.}`
    - `{nodes.(group)[(i)].(key)}`
    - `{nodes.(group).first.(key)}`
    - `{nodes.(group).last.(key)}`   
    Where:
    - `(group)` - nodes group ([nodeGroup](/creating-templates/selecting-containers/#all-containers-by-group) or [nodeType](/creating-templates/selecting-containers/#all-containers-by-type))
    - `(i)` - an index of node, starting from 0
    - `(key)` - parameter name   
    ...  
    **`key` available values**:    
        - `address` - internal(external) IP address     
        - `adminUrl` - full URL address with protocol   
        - `canBeExported` - boolean value. Jelastic [Export](https://docs.jelastic.com/environment-export-import) feature   
        - `diskIopsLimit` - IOPS limitation quota   
        - `diskLimit` - hardware node disk space quota   
        - `fixedCloudlets` - set fixed cloudlets   
        - `flexibleCloudlets` - set flexible cloudlets   
        - `id` - ID node   
        - `intIP` - internal IP address   
        - `isClusterSupport`    
        - `isExternalIpRequired` - status requiring external IP address   
        - `isResetPassword` - enable to reset service password    
        - `isWebAccess`   
        - `ismaster` - master node's status in the [`nodeGroup`](/reference/container-types/#containers-by-group)(layer)   
        - `maxchanks`   
        - `name` - stack name   
        - `nodeGroup` - nodes layer (lb, cp, sqldb, nosqldb, cache, extra(for docker-based))   
        - `nodeType` -  stacks [nodeType](/reference/container-types/#nodetype-values) list  
        - `nodemission` - deprecated value. Same as `nodeGroup`   
        - `osType` - OS type (LINUX)   
        - `password` - container password   
        - `port` - service port   
        - `type` - container's compatibility (native)   
        - `url` - full URL address with protocol   
        - `version` - stack version   
        - `engines`(for compute nodes):  
            - `id` - engine ID at platform  
            - `keyword` - engine keyword (java7, php7.0)  
            - `name` - full engine name (Java 8, PHP 7)  
            - `type` - engine type  (java, php,ruby, python, nodejs)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine version  
        - `activeEngine`(current engine in container):  
            - `id` - engine ID at platform   
            - `keyword` - engine keyword (java7, php7.0)  
            - `name` - full engine name (Java 8, PHP 7)  
            - `type` - engine type  (java, php,ruby, python, nodejs)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine version   
    
In case when few nodes are available in one `nodeGroup` you can execute actions in one of them.
For example:    
- `{nodes.cp[1].address}` - IP address of a second compute node  
- `{nodes.bl.first.address}` - First IP address of balancer node in `nodeGroup` array  
- `{nodes.db.last.address}` - Last IP address of compute node     
  
  
## File path placeholders

- `${HOME}` - for `couchdb`, `glassfish3`, `jetty6`, `nginx-ruby`, `nginx`, `nginxphp`, `tomcat6`,`tomcat7`, `tomee`
- `${WEBAPPS}` - for `apache2-ruby`, `apache2`, `jetty6`,`nginx-ruby`, `nginxphp`,`nodejs`,`tomcat6`, `tomcat7`,`tomee`
- `${JAVA_HOME}` - for `glassfish3`, `jetty6`, `maven3`,`tomcat6`,`tomcat7`,`tomee`
- `${JAVA_LIB}` - for `tomcat6`,`tomcat7`
- `${SYSTEM_CRON}` - for all native `nodeType`   
- `${SYSTEM_ETC}`- for all `nodeType`
- `${SYSTEM_KEYS}` - for all native `nodeType`   
- `${SERVER_CONF}` - for `apache2`, `glassfish3`, `jetty6`,`maven3`,`tomcat6`, `tomcat7`, `tomee`
- `${SERVER_CONF_D}` - for `apache2`, `memcached`,`nginx`, `nginxphp`
- `${SERVER_MODULES}` - for `apache2`, `glassfish3`, `jetty6`,`nginxphp`,`tomcat6`,`tomcat7`,`tomee`
- `${SERVER_SCRIPTS}` - for `couchdb`, `mariadb`, `mariadb10`, `mongodb`, `mysql5`,`postgres8`, `postgres9`
- `${SERVER_WEBROOT}` - for `apache2-ruby`, `apache2`, `jetty6`,`nginx-ruby`,`nginxphp`, `nodejs`,`tomcat6`,`tomcat7`, `tomee`
- `${SERVER_BACKUP}` - for `couchdb`, `mariadb`, `mariadb10`, `mongodb`, `mysql5`, `postgres8`, `postgres9`
- `${SERVER_LIBS}` - for `apache2`, `glassfish3`, `jetty6`, `nginxphp`,`tomcat6`,`tomcat7`, `tomee`
- `${SERVER_DATA}` - for `postgres8`, `postgres9`     
This values can be different depending to chosen [nodeType](/reference/container-types/#nodetype-values).

Also you can use this placeholders with defined `nodeType`. Examples:   
- `${glassfish3.HOME}` - /opt/glassfish3/temp  
- `${jetty6.JAVA_HOME}` - /usr/java/latest  
- `${mariadb10.SERVER_BACKUP}` - /var/lib/jelastic/backup  
- `${maven3.SYSTEM_KEYS}` - /var/lib/jelastic/keys  
- `${memcached.SERVER_CONF}` - /etc/sysconfig  
- `${mongodb.SYSTEM_CRON}` - /var/spool/cron  
- `${mysql5.SERVER_SCRIPTS}` - /var/lib/jelastic/bin  
- `${mysql5.SYSTEM_ETC}` - /etc  
- `${nginx-ruby.SERVER_WEBROOT}` - /var/www/webroot  
- `${nginx.SERVER_CONF_D}` - /etc/nginx/conf.d      
Full list native `nodeType` [here](/reference/container-types/#native-jelastic-nodetypes).

**Single placeholders list**:   
- `${nginxphp.NGINX_CONF}` - /etc/nginx/nginx.conf  
- `${postgresql.POSTGRES_CONF}` - /var/lib/pgsql/data  
- `${mysql5.MYSQL_CONF}` - /etc  
- `${mariadb.MARIADB_CONF}` - /etc  
- `${nginxphp.PHP_CONF}` - /etc/php.ini  
- `${nginxphp.PHPFPM_CONF}` - /etc/php-fpm.conf  
- `${nginxphp.PHP_MODULES}` - /usr/lib64/php/modules  
- `${nginxphp.WEBROOT}` - /var/www/webroot  

## Account information                                                                                                                                       
- `${user.uid}` - user ID at Jelastic platform
- `${user.email}` - user email address
- `${user.appPassword}` - random value. Can be used to set application passwords
- `${user.name}` - email address value. Same as `${user.email}`

## Input parameters
- `${settings.jelastic_email}` - user email. Always is predefined.
- `${settings.key}` - `key` - name of application setting. This placeholder will be defined if you use user input parameters in your manifest.
After preparing custom user form placeholders will be defined by fields name. 

For Example:
```example
{
  "jpsType": "update",
  "application": {
    "settings": {
      "fields": [
        {
          "type": "string",
          "name": "customName",
          "caption": "String field"
        }
      ]
    }
  }
}
```
Placeholder's name is `${settings.customName}`.   
User defined fields list [here](/creating-templates/user-input-parameters/).

 
## Procedure placeholders
- `${this.param}` - `param` - name of a procedure parameter.
Examples:
```
{
  "executeScript": [
    {
      "type": "js",
      "script": "return '${this.greeting}';",
      "params": {
        "greeting": "Hello World!"
      }
    }
  ]
}
```
Passing custom params in procedure:
```
{
	"jpsType": "update",
	"application": {
		"name": "example",
		"env": {},
		"onInstall": {
            "call": {"procedure": "customProcedure",
            "params": {
            	"first": 1,
                "second": 2
            }}
		},
        "procedures": [
            {
            	"id": "customProcedure",
                "onCall": {
                	"log": "${this.first}"
                }
            }
        ]
	}
}
```
As a result, in console will be printed `1` - custom parameter from `${this.first}` placeholder.
 
## Event placeholders
- `${event.params.(key)}` - `key` - event name parameter
- `${event.response.(key)}` - key` - event name response parameter 
Detailed placeholders list [here](/reference/events/)

## UI placeholders
- `${user.uid}` - user ID at Jelastic platform
- `${user.email}` - user email address
- `${env.domain}` - full domain name without protocol
- `${env.appid}` - unique enviroment appid at Jelastic platform

Example: 

```example
{
  "jpsType": "update",
  "application": {
    "settings": {
      "fields": [
        {
          "type": "string",
          "name": "email",
          "caption": "Email",
          "default": "${user.email}"
        }
      ]
    }
  }
}
```

##Global variables
Globals variables can be defined before install manifest. It will be as placeholder values. Optional value, only object.  
For example:
```
{
	"jpsType": "update",
	"application": {
		"name": "Global variables",
		"env": {},
		"globals": {
			"value1": 1,
			"value2": 2
		}
	}
}
```

The result is created new placeholders:
```
{
  "globals.value1": 1,
  "globals.value2": 2
}
```
##Function placeholders
Injected functions inside Cloud Scripting. There are a list of available functions:   
- `${fn.password}` - random value consists in upper and lower cases. Default length is 10. `${fn.password()}` is an alias.
Length can be passed as `${fn.password(max value)}`.   
- `${fn.base64}` - base64 encoding passed value.
```
${fn.base64(value)}
```
- `${fn.md5}` - md5 encoding.
```
${fn.md5(value)}
```
- `${fn.uuid}` - generates new Universally Unique Identifier.
- `${fn.random}` - random value. Default length - 7 digits. `${fn.random()}` is an alias.
 One or two values can be passed optionally:
    - `${fn.random(max)}` - random value to max.
    - `${fn.random(min,max)}` - random value between min and max values

Functions without required parameters have two input forms:

`${fn.password}` or `${fn.password()}`   
`${fn.random}` or `${fn.random()}`


Function parameter canbe passed from existing placeholders. For example:   
- `${fn.md5([fn.random])}` - md5 encoding random password   
- `${fn.base64([user.email])}` - base64 encoding user email address  

In conveniance, function placeholders can be defined in [global variables](#/reference/placeholders/#global-variables).
For example:
```
{
  "globals": {
    "pass": "${fn.password}"
  }
}
```
Now placeholder `${global.password}` also as `${fn.password}` available in manifest.

##Placeholder length
Any placeholder array length can be defined in manifest. For example:
```
${nodes.cp.length},
${node.bl.extips.length}
```