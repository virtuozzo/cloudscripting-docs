# Placeholders
Cloud Scripting supports a list of placeholders that can be used in any section of the manifest file (if the section isn't strictly limited with its content). 
The executor makes an attempt to resolve all placeholders on the package installation stage.
If it's not possible, the placeholder will be unresolved and displayed in the text as is (e.g. *${placeholder}*).

!!! note
    To output all available placeholders you can use the special placeholder: `${placeholders}`. See [Troubleshooting](/troubleshooting/) for more info.                                                                                         

## Environment Placeholders

- `{env.}`
    - `appid` *[string]* - application appid 
    - `domain` *[string]* - application domain
    - `protocol` *[string]* - protocol
    - `url` *[string]* - link to application (env)
    - `displayName` *[string]* - application display name
    - `envName` *[string]* - short domain name (without hoster *URL*)
    - `shortdomain` *[string]* - short domain name (alias to `envName`)
    - `hardwareNodeGroup` *[string]* - hardware node node group
    - `ssl` *[boolean]* - env SSL status
    - `sslstate` *[boolean]* - env SSL state
    - `status` *[number]* - environment status. The available statuses are: 1 - *running*, 2 - *down*, 3 - *launching*, 4 - *sleep*, 5 - *creating*, 6 - *cloning*, 7 - *exists*. 
    - `uid` *[number]* - user ID
    - `ishaenabled` *[boolean]* - high availability status 
    - `ha` *[boolean]* - alias to `${env.ishaenabled}`
    - `isTransferring` *[boolean]* - transferring status
    - `creatorUid` *[number]* - env creator ID 
    - `engine.id` *[number]* - engine ID
    - `engine.keyword` *[string]* - engine keyword
    - `engine.name` *[string]* - engine name
    - `engine.type` *[string]* - engine type
    - `engine.vcsSupport` *[boolean]* - VCS support status
    - `engine.version` *[string]* - engine version 
    - `contexts.type` *[string]* - env context type
    - `contexts.context` *[string]* - context name
    - `contexts.archivename` *[string]* - context display name
    
## Node Placeholders    
- `${nodes.}`
    - `{nodes.(group)[(i)].(key)}`
    - `{nodes.(group).first.(key)}`
    - `{nodes.(group).last.(key)}`   
    where:
    - `(group)` - node group ([nodeGroup](/creating-templates/selecting-containers/#all-containers-by-group) or [nodeType](/creating-templates/selecting-containers/#all-containers-by-type))
    - `(i)` - node's index, starting from *'0'*
    - `(key)` - name of the applied parameter, according to the following list:
        - `address` - internal or external IP address                               
        - `adminUrl` - full *URL* address with protocol   
        - `canBeExported` *[boolean]* - Jelastic [Export](https://docs.jelastic.com/environment-export-import) feature    
        - `bandwidthLimit` - node's bandwidth limit   
        - `contextValidatorRegex` - validation for context names    
        - `diskIopsLimit` - IOPS limitation quota   
        - `diskLimit` - hardware node disk space quota  
        - `endpoints` [*array indexes*] - setting [endpoints](https://docs.jelastic.com/endpoints) functionality                         
            - `domain` - full domain name of the node the endpoint is being set for                  
            - `id` - node ID  
            - `name` - title for the new endpoint (can be either custom or [predefined](https://docs.jelastic.com/endpoints#preconfigured))                
            - `privatePort` - preferred local node’s port              
            - `publicPort` - private (dynamic) port used for mapping                                         
            - `protocol` - protocol type (currently, only TCP is provided)                     
        - `fixedCloudlets` - fixed cloudlets amount     
        - `flexibleCloudlets` - flexible cloudlets amount      
        - `id` - node ID   
        - `intIP` - internal IP address   
        - `extIPs` - external IP address array (`extips` is an alias)                                
        - `isClusterSupport`    
        - `isExternalIpRequired` - status, indicating that node requires external IP address       
        - `isResetPassword` - enables to reset a service password    
        - `isWebAccess`   
        - `ismaster` - master node's status in the [`nodeGroup`](/reference/container-types/#containers-by-group)(i.e. layer)   
        - `maxchanks`   
        - `name` - stack name   
        - `nodeGroup` - node's layer, e.g. *lb*, *cp*, *sqldb*, *nosqldb*, *cache*, *storage*, *extra* (for *Docker* containers)   
        - `nodeType` -  stacks [nodeType](/reference/container-types/#nodetype-values) list  
        - `nodemission` - deprecated value (same as `nodeGroup`)  
        - `osType` - OS type (e.g. LINUX)   
        - `password` - container's password   
        - `port` - service port   
        - `type` - container's compatibility (native)   
        - `url` - full *URL* address with protocol   
        - `version` - stack version   
        - `engines`(for compute nodes):  
            - `id` - engine's ID at the platform  
            - `keyword` - engine's keyword (e.g. *java7*, *php7.0*)  
            - `name` - full engine's name (e.g. *Java 8*, *PHP 7*)  
            - `type` - engine's type (e.g. *java*, *php*, *ruby*, *python*, *nodejs*)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine's version  
        - `activeEngine`(current engine in container):  
            - `id` - engine's ID at the platform   
            - `keyword` - engine's keyword (e.g. *java7*, *php7.0*)  
            - `name` - full engine's name (e.g. *Java 8*, *PHP 7*)  
            - `type` - engine's type (e.g. *java*, *php*, *ruby*, *python*, *nodejs*)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine's version   
        - `packages` [*array*] - packages with add-ons installed over the appropriate node (e.g. [FTP add-on](https://docs.jelastic.com/ftp-ftps-support))                  
            - `description` - package's description                                       
            - `documentationurl` - redirect to page(s) with more info on the corresponding add-on                          
            - `iconurl` - add-on's logo                                               
            - `id` - ID of the installed package                       
            - `isInstalled` - installation status, the possible values are *"true"* & *"false"*.                       
    
In case a few nodes are available within `nodeGroup`, you can execute actions in one of them.
For example:    
- `{nodes.cp[1].address}` - IP address of the second compute node  
- `{nodes.bl.first.address}` - first IP address of a balancer node in the `nodeGroup` array  
- `{nodes.db.last.address}` - last IP address of a compute node     
  
## Event Placeholders
Event placeholders represent a set of dynamic parameters, which are executed as a result of a certain [event](/reference/events/) occurrence.                   
Herewith, all event placeholders have their custom set of parameters and begin with the default keywords:                       
- `${event.params.(key)}` - where *key* is a name of event parameter                     
- `${event.response.(key)}` -where *key* is a name of event response parameter             

Learn more about the event placeholders within the above-linked *Events* page. 

## Account Information                                                                                                                                       
- `${user.uid}` - user's ID at the Jelastic platform    
- `${user.email}` - user's email address    
- `${user.appPassword}` - random value that can be used to set application's passwords    
- `${user.name}` - email address value (same as `${user.email}`)    

## Input Parameters
- `${settings.jelastic_email}` - user's email, which is always predefined    
- `${settings.key}` - (where *key* is a name of the application setting) - the placeholder is defined in case user input parameters are specified within a manifest. So, after preparing custom user form, the placeholder is defined by the field’s name.     

For example:
```example
{
  "jpsType": "update",
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
```
The placeholder's name here is `${settings.customName}`. Check the list of [fields defined by a user](/creating-templates/user-input-parameters/).

 
## Procedure Placeholders
- `${this.param}` - where *param* is a name of the procedure parameter

For example:
```
{
  "script": "return greeting;",
  "params": {
    "greeting": "Hello World!"
  }
}
```
Passing custom params to the procedure is performed in the following way:
```
{
	"jpsType": "update",
	"name": "example",
	"onInstall": {
		"customProcedure": {
			"first": 1,
			"second": 2
		}
	},
	"actions": {
		"customProcedure": {
			"log": "${this.first}"
		}
	}
}
```
As a result, console will display the *first* (1) custom parameter from `${this.first}` placeholder.

## UI Placeholders
- `${user.uid}` - user's ID at the Jelastic platform
- `${user.email}` - user's email address
- `${env.domain}` - a full domain name without protocol
- `${env.appid}` - a unique environment appid at the Jelastic platform

For instance: 

```example
{
  "jpsType": "update",
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
```

##Custom Global Placeholders
Placeholders managed by users can be predefined via <b>*globals declaration*</b>. The corresponding declaration is performed in advance of the manifest installation.  

For example:
```
{
  "jpsType": "update",
  "name": "Global declaration",
  "globals": {
    "value1": 1,
    "value2": 2
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

- `${fn.password}` - random value within the upper and lower cases. The default length value is *'10'*. The length can be passed as `${fn.password(max value)}`.   
- `${fn.base64}` - *base64* encoding passed value  
```
${fn.base64(value)}
```
- `${fn.md5}` - *md5* encoding  
```
${fn.md5(value)}
```
- `${fn.uuid}` - generates new Universally Unique Identifier     
- `${fn.random}` - random value within the default length comprising 7 digits.  
Herewith, either one or two values can be passed optionally:
    - `${fn.random(max)}` - random value to maximum value inclusively
    - `${fn.random(min,max)}` - random value between minimum and maximum values inclusively 

Functions without required parameters have two input forms:

- `${fn.password}` or `${fn.password()}`   
- `${fn.random}` or `${fn.random()}`


Function parameter can be passed from existing placeholders. For example:   

- `${fn.md5([fn.random])}` - *md5* encoding random password   
- `${fn.base64([user.email])}` - *base64* encoding user email address  

You can easily define function placeholders within the [cutom global placeholders](#/reference/placeholders/#global-variables).  

For example:
```
{
  "globals": {
    "pass": "${fn.password}"
  }
}
```
Now, you can use `${global.pass}` within the entire manifest.

##Array Placeholders

Any array has a list of specific placeholders: array *length*, element by *ID*, the *first* and the *last* array elements.   

**Array Length**

Any array length placeholder can be defined within a manifest. 

For example:
```
${nodes.cp.length},
${nodes.bl.extips.length}
```

**Element by ID**    

Each element has an index in the array. 

For example: 

`{nodes.cp[(i)].(key)}`   

where:   
- `i` - array's index   
- `key` - node's parameter. See the details on setting [node parameters](#/reference/placeholders/#node-placeholders).   

**The First and the Last Array Elements** 

`{nodes.cp.first.(key)}` - the array element with the the *'0'* index  
`{nodes.sqldb.last.(key)}` - the array element with the last ID in the array   

where:  
- `key` - node's parameter  

## File Path Placeholders
The values below can vary depending on the chosen [nodeType](/reference/container-types/#nodetype-values):    
- `${HOME}` - for *couchdb*, *glassfish3*, *jetty6*, *nginx-ruby*, *nginx*, *nginxphp*, *tomcat6*,*tomcat7*, *tomee*    
- `${WEBAPPS}` - for *apache2-ruby*, *apache2*, *jetty6*, *nginx-ruby*, *nginxphp*, *nodejs*, *tomcat6*, *tomcat7*, *tomee*    
- `${JAVA_HOME}` - for *glassfish3*, *jetty6*, *maven3*, *tomcat6*, *tomcat7*, *tomee*   
- `${JAVA_LIB}` - for *tomcat6*, *tomcat7*    
- `${SYSTEM_CRON}` - for all native *nodeType*               
- `${SYSTEM_ETC}`- for all *nodeType*    
- `${SYSTEM_KEYS}` - for all native *nodeType*   
- `${SERVER_CONF}` - for *apache2*, *glassfish3*, *jetty6*, *maven3*, *tomcat6*, *tomcat7*, *tomee*    
- `${SERVER_CONF_D}` - for *apache2*, *memcached*, *nginx*, *nginxphp*    
- `${SERVER_MODULES}` - for *apache2*, *glassfish3*, *jetty6*, *nginxphp*, *tomcat6*, *tomcat7*, *tomee*    
- `${SERVER_SCRIPTS}` - for *couchdb*, *mariadb*, *mariadb10*, *mongodb*, *mysql5*, *postgres8*, *postgres9*    
- `${SERVER_WEBROOT}` - for *apache2-ruby*, *apache2*, *jetty6*, *nginx-ruby*, *nginxphp*, *nodejs*, *tomcat6*, *tomcat7*, *tomee*    
- `${SERVER_BACKUP}` - for *couchdb*, *mariadb*, *mariadb10*, *mongodb*, *mysql5*, *postgres8*, *postgres9*    
- `${SERVER_LIBS}` - for *apache2*, *glassfish3*, *jetty6*, *nginxphp*, *tomcat6*, *tomcat7*, *tomee*    
- `${SERVER_DATA}` - for *postgres8*, *postgres9*         

You can use the following placeholders, as well, with the definite `nodeType`. For example:   
- `${glassfish3.HOME}` - */opt/glassfish3/temp*  
- `${jetty6.JAVA_HOME}` - */usr/java/latest*  
- `${mariadb10.SERVER_BACKUP}` - */var/lib/jelastic/backup*  
- `${maven3.SYSTEM_KEYS}` - */var/lib/jelastic/keys*  
- `${memcached.SERVER_CONF}` - */etc/sysconfig*  
- `${mongodb.SYSTEM_CRON}` - */var/spool/cron*  
- `${mysql5.SERVER_SCRIPTS}` - */var/lib/jelastic/bin*  
- `${mysql5.SYSTEM_ETC}` - */etc*  
- `${nginx-ruby.SERVER_WEBROOT}` - */var/www/webroot*  
- `${nginx.SERVER_CONF_D}` - */etc/nginx/conf.d*      

Explore the full list of the [Jelastic native container types](/reference/container-types/#jelastic-native-container-types).                  

The list of single placeholders:   
- `${nginxphp.NGINX_CONF}` - */etc/nginx/nginx.conf*   
- `${postgresql.POSTGRES_CONF}` - */var/lib/pgsql/data*   
- `${mysql5.MYSQL_CONF}` - */etc*   
- `${mariadb.MARIADB_CONF}` - */etc*             
- `${nginxphp.PHP_CONF}` - */etc/php.ini*   
- `${nginxphp.PHPFPM_CONF}` - */etc/php-fpm.conf*   
- `${nginxphp.PHP_MODULES}` - */usr/lib64/php/modules*   
- `${nginxphp.WEBROOT}` - */var/www/webroot*   