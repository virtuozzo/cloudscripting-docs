# Placeholders
Cloud Scripting supports a set of placeholders that can be used in any section of a manifest file (if the section isn't strictly limited with its content). 
The executor makes an attempt to resolve all placeholders on the package installation stage.
If it's not possible, the placeholder will be unresolved and displayed in the text as is (e.g. *${placeholder}*).

!!! note
    To output all available placeholders, use a special <b>${placeholders}</b> placeholder. For more information, see the <a href="http://docs.cloudscripting.com/troubleshooting/" target ="_blank">Troubleshooting</a> guide.                                                                                                   

The following specific groups of placeholders are singled out: 

- [Environment Placeholders](http://docs.cloudscripting.com/reference/placeholders/#environment-placeholders)           
- [Node Placeholders](http://docs.cloudscripting.com/reference/placeholders/#node-placeholders)                 
- [Event Placeholders](http://docs.cloudscripting.com/reference/placeholders/#event-placeholders)                    
- [Account Information](http://docs.cloudscripting.com/reference/placeholders/#account-information)                 
- [Input Parameters](http://docs.cloudscripting.com/reference/placeholders/#input-parameters)                          
- [Action Placeholders](http://docs.cloudscripting.com/reference/placeholders/#action-placeholders)                  
- [UI Placeholders](http://docs.cloudscripting.com/reference/placeholders/#ui-placeholders)                     
- [Custom Global Placeholders](http://docs.cloudscripting.com/reference/placeholders/#custom-global-placeholders)                                
- [Function Placeholders](http://docs.cloudscripting.com/reference/placeholders/#function-placeholders)                             
- [Array Placeholders](http://docs.cloudscripting.com/reference/placeholders/#array-placeholders)                                       
- [File Path Placeholders](http://docs.cloudscripting.com/reference/placeholders/#file-path-placeholders)                                 

## Environment Placeholders

- `{env.}`
    - `appid` *[string]* - application appid 
    - `domain` *[string]* - application domain
    - `protocol` *[string]* - protocol
    - `url` *[string]* - link to application (environment)
    - `displayName` *[string]* - application display name
    - `envName` *[string]* - short domain name (without hosting provider URL)
    - `shortdomain` *[string]* - short domain name (alias to `envName`)
    - `hardwareNodeGroup` *[string]* - hardware node group
    - `ssl` *[boolean]* - environment SSL status
    - `sslstate` *[boolean]* - environment SSL state
    - `status` *[number]* - environment status. The available statuses are:                    
        - *running*              
        - *down*               
        - *launching*                 
        - *sleep*               
        - *creating*                 
        - *cloning*                
        - *exists*                        
    - `uid` *[number]* - user ID
    - `ishaenabled` *[boolean]* - high availability status 
    - `ha` *[boolean]* - alias to `${env.ishaenabled}`
    - `isTransferring` *[boolean]* - transferring status
    - `creatorUid` *[number]* - environment creator ID 
    - `engine.id` *[number]* - engine ID
    - `engine.keyword` *[string]* - engine keyword
    - `engine.name` *[string]* - engine name
    - `engine.type` *[string]* - engine type
    - `engine.vcsSupport` *[boolean]* - VCS support status
    - `engine.version` *[string]* - engine version 
    - `contexts.type` *[string]* - environment context type
    - `contexts.context` *[string]* - context name
    - `contexts.archivename` *[string]* - context display name
    - `contexts.length` *[number]* - number of contexts which are deployed to environment
    - `extdomains.length` *[number]* - number of external domains which are binded to environment
    
## Node Placeholders    
- `${nodes.}`
    - `{nodes.(group)[(i)].(key)}`
    - `{nodes.(group).first.(key)}`
    - `{nodes.(group).last.(key)}`   
    where:
    - `(group)` - node group (<a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-group" target="_blank">nodeGroup</a> or <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-type" target="_blank">nodeType</a>)           
    - `(i)` - node index, starting from *'0'*
    - `(key)` - name of the applied parameter, according to the following list:
        - `address` - internal or external IP address                               
        - `adminUrl` - full URL address with protocol   
        - `canBeExported` *[boolean]* - Jelastic <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Export</a> feature       
        - `bandwidthLimit` - node bandwidth limit   
        - `contextValidatorRegex` - validation for context names    
        - `diskIopsLimit` - IOPS limitation quota   
        - `addons.length` - number of available addons at the selected node
        - `diskLimit` - hardware node disk space quota  
        - `endpoints` [*array indexes*] - <a href="https://docs.jelastic.com/endpoints" target="_blank">endpoints</a> functionality                              
            - `domain` - full domain name of the node the endpoint is being set for                  
            - `id` - node ID  
            - `name` - title for the new endpoint (can be either custom or <a href="https://docs.jelastic.com/endpoints#preconfigured" target="_blank">predefined</a>)                         
            - `privatePort` - preferred local node port              
            - `publicPort` - private (dynamic) port used for mapping                                         
            - `protocol` - protocol type (currently, only **TCP** is provided)             
            - `length` - number of available endpoints within the selected node               
        - `fixedCloudlets` - fixed cloudlets number                        
        - `flexibleCloudlets` - flexible cloudlets number                                   
        - `id` - node ID   
        - `intIP` - internal IP address   
        - `extIPs` - external IP address array (`extips` is an alias)                                
        - `isClusterSupport`    
        - `isExternalIpRequired` - status, indicating that node requires external IP address       
        - `isResetPassword` - enables to reset a service password    
        - `isWebAccess`   
        - `ismaster` - master node status in the *nodeGroup* (i.e. layer)   
        - `maxchanks`   
        - `length` - number of nodes available in an environment             
        - `name` - stack name   
        - `nodeGroup` - node layer, e.g. *lb*, *cp*, *sqldb*, *nosqldb*, *cache*, *storage*, (*extra* for Docker containers)     
        - `nodeType` -  stacks *nodeType*                        
        - `nodemission` - deprecated value (same as `nodeGroup`)  
        - `osType` - OS type (e.g. Linux)   
        - `password` - container password   
        - `port` - service port   
        - `type` - container compatibility (native)     
        - `url` - full URL address with protocol      
        - `version` - stack version   
        - `engines`(for compute nodes):  
            - `id` - engine ID at the platform  
            - `keyword` - engine keyword (e.g. *java7*, *php7.0*)  
            - `name` - full engine name (e.g. *Java 8*, *PHP 7*)  
            - `type` - engine type (e.g. *java*, *php*, *ruby*, *python*, *nodejs*)  
            - `vcsSupport` - supporting VCS in container  
            - `version` - engine version  
            - `length` - number of available engines for selected compute layer     
        - `activeEngine`(current engine in a container):  
            - `id` - engine ID at the platform   
            - `keyword` - engine keyword (e.g. *java7*, *php7.0*)  
            - `name` - full engine name (e.g. *Java 8*, *PHP 7*)  
            - `type` - engine type (e.g. *java*, *php*, *ruby*, *python*, *nodejs*)  
            - `vcsSupport` - supporting VCS in a container  
            - `version` - engine version   
        - `packages` [*array*] - packages with add-ons installed over the corresponding nodes (e.g. <a href="https://docs.jelastic.com/ftp-ftps-support" target="_blank">FTP</a> add-on)                              
            - `description` - package description                                       
            - `documentationurl` - redirect to page(s) with more info on the particular add-on                          
            - `iconurl` - add-on logo                                               
            - `id` - ID of the installed package
            - `length` - number of packages installed to a node
            - `isInstalled` - installation status, the possible values are *'true'* & *'false'*                      
    
In case a few nodes are available within a single *nodeGroup*, you can execute actions in one of them by specifying: 

- `{nodes.cp[1].address}` - IP address of the second compute node  
- `{nodes.bl.first.address}` - first IP address of a balancer node in the *nodeGroup* array            
- `{nodes.db.last.address}` - last IP address of a batabase node     

## Event Placeholders
Event placeholders represent a set of dynamic parameters that are executed as a result of a certain event occurrence. The event placeholders have their custom set of parameters and begin with the default keywords:
                         
- `${event.params.(key)}` - where *key* is a name of event parameter                     
- `${event.response.(key)}` -where *key* is a name of event response parameter             

Learn more about the event placeholders within the <a href="http://docs.cloudscripting.com/reference/events" target="_blank">*Events*</a> page.         

## Account Information                                                                                                                                       
- `${user.uid}` - user ID at the Jelastic Platform              
- `${user.email}` - user email address      
- `${user.appPassword}` - random value that can be used to set application passwords       
- `${user.name}` - email address value (same as `${user.email}`)       

## Input Parameters
- `${settings.jelastic_email}` - user email that is always predefined       
- `${settings.key}` - (where *key* is a name of the application setting) 
    The placeholder is defined in case user input parameters are specified within a manifest. So, after preparing custom user form, the placeholder is defined by the field’s name.     

For example:
``` json
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
The name of the placeholder here is `${settings.customName}`. Check the list of <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">fields defined by users</a>.       

 
## Action Placeholders

Action placeholders are a set of placeholders that can be used within the appropriate actions by means of `${this}` namespace.                            

- `${this.param}` - where *param* is a name of the action parameter                         

For example:
``` json
{
  "script": "return greeting;",
  "params": {
    "greeting": "Hello World!"
  }
}
```
Passing custom parameters to the action is performed in the following way:                       
``` json
{
	"jpsType": "update",
	"name": "example",
	"onInstall": {
		"customAction": {
			"first": 1,
			"second": 2
		}
	},
	"actions": {
		"customAction": {
			"log": "${this.first}"
		}
	}
}
```
As a result, console will display the *first* (1) custom parameter from `${this.first}` placeholder.

## UI Placeholders
- `${user.uid}` - user ID at the Jelastic Platform
- `${user.email}` - user email address
- `${env.domain}` - full domain name without protocol
- `${env.appid}` - unique environment appid at the Jelastic Platform

For example: 
``` json
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

## Custom Global Placeholders
Placeholders managed by users can be predefined via <b>*globals declaration*</b>. The corresponding declaration is performed in advance of the manifest installation.  

For example:
``` json
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
``` json
{
  "globals.value1": 1,
  "globals.value2": 2
}
```  

## Function Placeholders
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
- `${fn.random}` - random value within the default length, comprising 7 digits  
Here, either one or two values can be passed optionally:
    - `${fn.random(max)}` - random value to maximum value inclusively
    - `${fn.random(min,max)}` - random value between minimum and maximum values inclusively 

Functions without required parameters have two input forms:

- `${fn.password}` or `${fn.password()}`   
- `${fn.random}` or `${fn.random()}`


Function parameter can be passed from existing placeholders. For example:   

- `${fn.md5([fn.random])}` - *md5* encoding random password   
- `${fn.base64([user.email])}` - *base64* encoding user email address  

You can easily define function placeholders within the [cutom global placeholders](#custom-global-placeholders).  

For example:
``` json
{
  "globals": {
    "pass": "${fn.password}"
  }
}
```
Now, you can use `${global.pass}` within the entire manifest.

## Array Placeholders

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

- `(i)` - array index. Indexes of array start from *'0'*                     
- `(key)` - node <a href="http://docs.cloudscripting.com/reference/placeholders/#node-placeholders" target="_blank">parameters</a>                            

**The First and the Last Array Elements** 

- `{nodes.cp.first.(key)}` - array element with the the *'0'* index              
- `{nodes.sqldb.last.(key)}` - array element with the last ID in the array                      

Here, `key` is the node parameter.                         

## File Path Placeholders

The values below can vary depending on a particular *nodeType*:              

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

You can use the following placeholders, as well, with the definite *nodeType*.                
For example:     

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

Explore the full list of available <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-type" target="_blank">nodeType</a>.                                              

The list of single placeholders:

- `${nginxphp.NGINX_CONF}` - */etc/nginx/nginx.conf*   
- `${postgresql.POSTGRES_CONF}` - */var/lib/pgsql/data*   
- `${mysql5.MYSQL_CONF}` - */etc*   
- `${mariadb.MARIADB_CONF}` - */etc*             
- `${nginxphp.PHP_CONF}` - */etc/php.ini*   
- `${nginxphp.PHPFPM_CONF}` - */etc/php-fpm.conf*   
- `${nginxphp.PHP_MODULES}` - */usr/lib64/php/modules*   
- `${nginxphp.WEBROOT}` - */var/www/webroot*   

<br>       
## What’s next?                    

- See how to use <a href="http://docs.cloudscripting.com/creating-templates/conditions-and-iterations/">Conditions and Iterations</a>                               
- Read how to integrate your <a href="http://docs.cloudscripting.com/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a>       
- Learn how to customize the <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">Visual Settings</a>                
- Examine a bunch of <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> with operation and package examples           