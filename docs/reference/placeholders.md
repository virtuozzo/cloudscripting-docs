# Placeholders
Cloud Scripting supports a list of placeholders that can be used in any section of the manifest file (if the section isn't strictly limited with its content).
The executor makes attempt to resolve all placeholders on the package installation stage.
If it's not possible placeholder will be unresolved and displayed in the text as is (e.g. ${placeholder})

!!! note
    To output all available placeholders you can use the special placeholder: `${placeholders}`        
    See [Troubleshooting](/troubleshooting/) for more info.                                                                                         

## Environment Placeholders

- `{env.}`
    - `${env.appid}` *[string]* - application appid. 
    - `${env.domain}` *[string]* - application domain. 
    - `${env.protocol}` *[string]* - protocol. 
    - `${env.url}` *[string]* - link to application (env). 
    - `${env.displayName}` *[string]* - application display name. 
    - `${env.envName}` *[string]* - short domain name (without hoster URL).
    - `${env.shortdomain}` *[string]* - short domain name. Alias to `envName`.
    - `${env.hardwareNodeGroup}` *[string]* - hardware node node group.
    - `${env.ssl}` *[boolean]* - env SSL status.
    - `${env.sslstate}` *[boolean]* env SSL state.
    - `${env.status}` *[number]* environment status. Available statuses are: 1 - running, 2 - down, 3 - launching, 4 - sleep, 6 - creating, 7 - cloning, 8 - exists. 
    - `${env.uid}` *[number]* - user uid. 
    - `${env.ishaenabled}` *[boolean]* - High availability status. 
    - `${env.ha}` *[boolean]* - alias to `${env.ishaenabled}`. 
    - `${env.isTransferring}` *[boolean]* - transfering status. 
    - `${env.creatorUid}` *[number]* - env creator ID. 
    - `${env.engine.id}` *[number]* - engine ID. 
    - `${env.engine.keyword}` *[string]* - engine keyword. 
    - `${env.engine.name}` *[string]* - engine name. 
    - `${env.engine.type}` *[string]* - engine type. 
    - `${env.engine.vcsSupport}` *[boolean]* - vcs support status. 
    - `${env.engine.version}` *[string]* - engine version. 
    - `${env.contexts.type}` *[string]* - env context type. 
    - `${env.contexts.context}` *[string]* - context name
    - `${env.contexts.archivename}` *[string]* - context display name
    
## Node placeholders    
- `${nodes.}`
    - `{nodes.(group)[(i)].(key)}`
    - `{nodes.(group).first.(key)}`
    - `{nodes.(group).last.(key)}`   
    where:
    - `(group)` - nodes group ([nodeGroup](/creating-templates/selecting-containers/#all-containers-by-group) or [nodeType](/creating-templates/selecting-containers/#all-containers-by-type))
    - `(i)` - index of node, starting from 0
    - `(key)` - parameter name according to the following list:   
        - `address` - internal or external IP address     
        - `adminUrl` - full URL address with protocol   
        - `canBeExported [boolean]` - Jelastic [Export](https://docs.jelastic.com/environment-export-import)   
        - `diskIopsLimit` - IOPS limitation quota   
        - `diskLimit` - hardware node disk space quota   
        - `fixedCloudlets` - fixed cloudlets number   
        - `flexibleCloudlets` - flexible cloudlets number    
        - `id` - node ID   
        - `intIP` - internal IP address   
        - `isClusterSupport`    
        - `isExternalIpRequired` - status, that node require external IP address   
        - `isResetPassword` - enable to reset service password    
        - `isWebAccess`   
        - `ismaster` - master node's status in the [`nodeGroup`](/reference/container-types/#containers-by-group)(layer)   
        - `maxchanks`   
        - `name` - stack name   
        - `nodeGroup` - nodes layer, i.e. lb, cp, sqldb, nosqldb, cache, storage extra(for Docker container)   
        - `nodeType` -  stacks [nodeType](/reference/container-types/#nodetype-values) list  
        - `nodemission` - deprecated value. Same as `nodeGroup`   
        - `osType` - OS type (LINUX)   
        - `password` - container password   
        - `port` - service port   
        - `type` - container's compatibility (native)   
        - `url` - full URL address with protocol   
        - `version` - stack version   
        - `engines`(for compute nodes):  
            - `id` - engine ID at the platform  
            - `keyword` - engine keyword ( e.g. java7, php7.0)  
            - `name` - full engine name (e.g. Java 8, PHP 7)  
            - `type` - engine type  (e.g. java, php,ruby, python, nodejs)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine version  
        - `activeEngine`(current engine in container):  
            - `id` - engine ID at the platform   
            - `keyword` - engine keyword ( e.g. java7, php7.0)  
            - `name` - full engine name (e.g. Java 8, PHP 7)  
            - `type` - engine type  (e.g. java, php,ruby, python, nodejs)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine version   
    
In case a few nodes are available within `nodeGroup`, you can execute actions in one of them.
For example:    
- `{nodes.cp[1].address}` - IP address of the a second compute node  
- `{nodes.bl.first.address}` - first IP address of a balancer node in the `nodeGroup` array  
- `{nodes.db.last.address}` - last IP address of a compute node     
  
  
## File Path Placeholders
These values can be different depending on the chosen [nodeType](/reference/container-types/#nodetype-values):    
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

You can use the following placeholders, as well, with a defined `nodeType`. For example:   
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
Explore [the full list](/reference/container-types/#native-jelastic-nodetypes) of the native `nodeType`.

The single placeholders list:   
- `${nginxphp.NGINX_CONF}` - /etc/nginx/nginx.conf  
- `${postgresql.POSTGRES_CONF}` - /var/lib/pgsql/data  
- `${mysql5.MYSQL_CONF}` - /etc  
- `${mariadb.MARIADB_CONF}` - /etc  
- `${nginxphp.PHP_CONF}` - /etc/php.ini  
- `${nginxphp.PHPFPM_CONF}` - /etc/php-fpm.conf  
- `${nginxphp.PHP_MODULES}` - /usr/lib64/php/modules  
- `${nginxphp.WEBROOT}` - /var/www/webroot  

## Account Information                                                                                                                                       
- `${user.uid}` - user ID at the Jelastic platform    
- `${user.email}` - user email address    
- `${user.appPassword}` - random value that can be used to set application passwords    
- `${user.name}` - email address value. Same as `${user.email}`    

## Input Parameters
- `${settings.jelastic_email}` - user email that is always predefined.    
- `${settings.key}` - where key is a name of application setting. The placeholder is defined in case user input parameters are specified within a manifest.   
After preparing custom user form, the placeholder is defined by the field’s name.     

For instance:
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
Explore [the list of the fields](/creating-templates/user-input-parameters/) defined by a user.

 
## Procedure Placeholders
- `${this.param}` - where *param* is a name of the procedure parameter.
For example:
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
Passing custom params to the procedure is performed in the following way:
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
As a result, a console will display the first (1) custom parameter from `${this.first}` placeholder.
 
## Event Placeholders
- `${event.params.(key)}` - where key is an event name parameter
- `${event.response.(key)}` -where key is an event name response parameter. [See the full event placeholders list](/reference/events/).

## UI Placeholders
- `${user.uid}` - user ID at the Jelastic platform
- `${user.email}` - user email address
- `${env.domain}` - full domain name without protocol
- `${env.appid}` - unique environment appid at the Jelastic platform

For instance: 

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

##Custom Global Placeholders
User defined placeholders can be predefined via <b>globals declaration</b>. The corresponding declaration is performed in advance of the manifest installation.  
For example:
```
{
	"jpsType": "update",
	"application": {
		"name": "Global declaration",
		"env": {},
		"globals": {
			"value1": 1,
			"value2": 2
		}
	}
}
```

As a result, the new placeholders are created:
```
{
  "globals.value1": 1,
  "globals.value2": 2
}
```
##Function Placeholders
The integrated functions inside Cloud Scripting are listed below:   

- `${fn.password}` - random value consists within the upper and lower cases. The default length value is *10*.
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
- `${fn.random}` - random value within the default length comprising 7 digits.  
One or two values can be passed optionally:
    - `${fn.random(max)}` - random value to maximum value inclusively.
    - `${fn.random(min,max)}` - random value between minimum and maximum values inclusively 

Functions without required parameters have two input forms:

`${fn.password}` or `${fn.password()}`   
`${fn.random}` or `${fn.random()}`


Function parameter canbe passed from existing placeholders. For example:   
- `${fn.md5([fn.random])}` - md5 encoding random password   
- `${fn.base64([user.email])}` - base64 encoding user email address  

You can easily define function placeholders within the [cutom global placeholders](#/reference/placeholders/#global-variables).  
For example:
```
{
  "globals": {
    "pass": "${fn.password}"
  }
}
```
Now You can use `${global.pass}` within the entire manifest.

##Array Length

Any array has a list of specific placeholders, they are the array length, elements by index in the array and the first and the last array elements.   

**Array length**
Any array length placeholder can be defined within a manifest. For example:
```
${nodes.cp.length},
${nodes.bl.extips.length}
```

**Element by id in array**    
Every element has an index in the array. For example:   
`{nodes.cp[(i)].(key)}`   
where   
- `i` - array index   
- `key` - node parameter. See the details about [node parameters](#/reference/placeholders/#node-placeholders)   

**First or last array elements**   
`{nodes.cp.first.(key)}` -  array element with the index *0*   
`{nodes.sqldb.last.(key)}` - array element with last array index   
where   
- `key` - node parameter.   