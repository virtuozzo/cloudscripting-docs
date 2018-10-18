# Placeholders
Cloud Scripting supports a set of placeholders that can be used in any section of a manifest file, if the section isn't strictly limited with its content. The Cloud Scripting engine makes an attempt to resolve all placeholders on the package installation stage. If it's not possible, the placeholder will be unresolved and displayed in the text as is (e.g. *${placeholder}*).                           

!!! note
    To output all available placeholders, use a special <b>${placeholders}</b> placeholder. For more information, see the <a href="/troubleshooting/" target ="_blank">*Troubleshooting*</a> guide.                                                                                                   

The following specific groups of placeholders are singled out: 

- [Environment Placeholders](/creating-manifest/placeholders/#environment-placeholders)           

- [Node Placeholders](/creating-manifest/placeholders/#node-placeholders)                 

- [Event Placeholders](/creating-manifest/placeholders/#event-placeholders)                    

- [Account Information](/creating-manifest/placeholders/#account-information)                 

- [Input Parameters](/creating-manifest/placeholders/#input-parameters)                          

- [Action Placeholders](/creating-manifest/placeholders/#action-placeholders)                  

- [UI Placeholders](/creating-manifest/placeholders/#ui-placeholders)                     

- [Custom Global Placeholders](/creating-manifest/placeholders/#custom-global-placeholders)                               

- [Function Placeholders](/creating-manifest/placeholders/#function-placeholders)                             

- [Array Placeholders](/creating-manifest/placeholders/#array-placeholders)                                       

- [File Path Placeholders](/creating-manifest/placeholders/#file-path-placeholders)                                 

Placeholders like `env`, `nodes`, `targetNodes`, `response` are dynamically updated. They could be updated by their requests if they are required to be updated.

## Environment Placeholders

This is the list of placeholders that you can use within the environment section (*{env.}*) of your manifest.                               

- `{env.}`
    - `appid` *[string]* - application appid 
    - `domain` *[string]* - application domain
    - `protocol` *[string]* - protocol
    - `url` *[string]* - link to application (environment)
    - `region` *[string]* - a region name where environment has been installed
    - `displayName` *[string]* - application display name
    - `envName` *[string]* - short domain name (without hosting provider URL)
    - `shortdomain` *[string]* - short domain name (alias to `envName`)
    - `name` *[string]* - alias to `envName`
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
    - `contexts.length` *[number]* - number of contexts that are deployed to an environment
    - `extdomains.length` *[number]* - number of external domains that are bound to an environment

## Node Placeholders    

This is the list of placeholders that you can use within the nodes section (*{nodes.}*) of your manifest.                                   

- `${nodes.}`
    - `{nodes.(group)[(i)].(key)}`
    - `{nodes.(group).first.(key)}`
    - `{nodes.(group).last.(key)}`   
    - `{nodes.(group).master.(key)}`   
    where:
    - `(group)` - node group (<a href="/1.6/creating-manifest/selecting-containers/#all-containers-by-group" target="_blank">nodeGroup</a> or <a href="/1.6/creating-manifest/selecting-containers/#all-containers-by-type" target="_blank">nodeType</a>)           
    - `(i)` - node index, starting from *'0'*
    - `(key)` - name of the applied parameter, according to the following list:
        - `address` - internal or external IP address                               
        - `adminUrl` - full URL address with protocol   
        - `canBeExported` *[boolean]* - Jelastic <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Export</a> feature       
        - `bandwidthLimit` - node bandwidth limit   
        - `contextValidatorRegex` - validation for context names    
        - `diskIopsLimit` - IOPS limitation quota   
        - `addons.length` - number of available add-ons at the selected node
        - `diskLimit` - hardware node disk space quota in MB 
        - `endpoints` [*array indexes*] - <a href="https://docs.jelastic.com/endpoints" target="_blank">endpoints</a> functionality                              
            - `domain` - full domain name of the node the endpoint is being set for                  
            - `id` - node ID  
            - `name` - title for the new endpoint (can be either custom or <a href="https://docs.jelastic.com/endpoints#preconfigured" target="_blank">predefined</a>)                         
            - `privatePort` - preferred local node port              
            - `publicPort` - private (dynamic) port used for mapping                                         
            - `protocol` - protocol type (currently, only TCP is provided)             
            - `length` - number of available endpoints within the selected node               
        - `fixedCloudlets` - fixed cloudlets number                        
        - `flexibleCloudlets` - flexible cloudlets number                                   
        - `id` - node ID   
        - `intIP` - internal IP address   
        - `extIPs` - external IP address array (`extips` is an alias)                                
        - `isClusterSupport`    
        - `isExternalIpRequired` - status, indicating that node requires the external IP address       
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
            - `vcsSupport` - supporting VCS in a container  
            - `version` - engine version  
            - `length` - number of available engines for the selected compute layer     
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
- `{nodes.(group).master.(key)}` - main node in the *nodeGroup* (i.e. layer)

## Event Placeholders

Event placeholders represent a set of dynamic parameters that are executed as a result of a certain event occurrence. The event placeholders have their custom set of parameters and begin with the default keywords:
                         
- `${event.params.(key)}` - where *key* is a name of the event parameter                     
- `${event.response.(key)}` -where *key* is a name of the event response parameter             

Learn more about the event placeholders within the <a href="/1.6/creating-manifest/events" target="_blank">*Events*</a> page.         

## Account Information  

This is the list of placeholders that you can use to specify account information.                                                                       

- `${user.uid}` - user ID at the Jelastic Platform               
- `${user.email}` - user email address      
- `${user.appPassword}` - random value that can be used to set application passwords       
- `${user.name}` - email address value (same as `${user.email}`)       

## Input Parameters

This is the list of placeholders that you can use to specify input parameters.                        

- `${settings.jelastic_email}` - user email that is always predefined       
- `${settings.key}` - where *key* is a name of the application's setting. The placeholder is defined, if user input parameters are specified within a manifest. So, after preparing a custom user form, the placeholder is defined by the field’s name.              

**Example**
@@@
```yaml
type: update

settings:
  fields:
  - type: string
    name: customName
    caption: String field
```
``` json
{
  "type": "update",
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
@@!
Here, the name of the placeholder is `${settings.customName}`. See the list of <a href="/1.6/creating-manifest/visual-settings/" target="_blank">fields</a> that are defined by users.       

## Action Placeholders

Action placeholders form a set of placeholders that can be used within the actions by means of a <b>*\${this.*}*</b> namespace. So, in <b>*${this.param}*</b> the *param* is a name of the action parameter.

**Example**
@@@
```yaml
script: "return greeting;"

params:
  greeting: Hello World
```
``` json
{
  "script": "return greeting;",
  "params": {
    "greeting": "Hello World!"
  }
}
```
@@!
Passing custom parameters to the action is performed in the following way.                  
@@@
```yaml
type: update
name: example

onInstall:
  customAction:
    first: 1
    second: 2

actions:
  customAction:
    log: ${this.first}
```
``` json
{
	"type": "update",
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
@@!
As a result, console will display the *first* (1) custom parameter from the <b>*${this.first}*</b> placeholder.

Also custom actions can receive as a parameter a string or an array or strings. In this case a new placeholder *\${this}* will be defined within executed action.

For example:
@@@
```yaml
type: update
name: this placeholder
onInstall:
  customAction:  custom string
actions:
  customAction:
    log: ${this}
```
```json
{
  "type": "update",
  "name": "this placeholder",
  "onInstall": {
    "customAction": "custom string"
  },
  "actions": {
    "customAction": {
      "log": "${this}"
    }
  }
}
```
@@!

The result message of \${this} placeholder is on the screen below:
![this-placeholder](/img/this-placeholder.png)

In case if an argument is an array of strings the executed custom action will be executed so many times how many arguments are in an array.

## UI Placeholders

This is the list of placeholders that you can use to specify UI parameters.                              

- `${user.uid}` - user ID at the Jelastic Platform
- `${user.email}` - user email address
- `${env.domain}` - full domain name without protocol
- `${env.appid}` - unique environment appid at the Jelastic Platform
- `${baseUrl}` - user custom relative URL. More details about <a href="/1.6/creating-manifest/basic-configs/#relative-links">Relative Links here</a>
- `${platformUrl}` - hoster dashboard URL.

**Example**
@@@
```yaml
type: update

settings:
  fields:
    - type: string
      name: email
      caption: Email
      default: ${user.email}
```
``` json
{
  "type": "update",
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
@@!

## Custom Global Placeholders

Placeholders that are managed by users can be predefined via <b>*globals declaration*</b>. The corresponding declaration is performed in advance of the manifest installation.  

**Example**
@@@
```yaml
type: update
name: Global declaration

globals:
  value1: 1
  value2: 2
```
``` json
{
  "type": "update",
  "name": "Global declaration",
  "globals": {
    "value1": 1,
    "value2": 2
  }
}
```
@@!

As a result, you can use <b>*${globals.value1}*</b> and <b>*${globals.value2}*</b>  within the entire manifest.

Values are global placeholders (<i>value1</i> and <i>value2</i> in example above) could consist of like simple text or/and placeholders in it. There are the list of placeholders which are predefined in `globals` block:

- `${settings.*}` - <a href="/1.6/creating-manifest/placeholders/#input-parameters" target="_blank">input parameters</a> from `settings` block, where custom forms are described
- `${env.*}` - all <a href="/1.6/creating-manifest/placeholders/#environment-placeholders" target="_balnk">environment placeholders</a>. Placeholders are available only in JPS manifests with `type` *install* -  `globals` block will be updated after an environment is created.
- `${nodes.*}` - all <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_balnk">node placeholders</a>. Node values in global placeholders will be available only after environment is created.
- `${user.*}` - <a href="/1.6/creating-manifest/placeholders/#account-information" target="-blank">account placeholders</a> are available during all JPS installation process.
- `${fn.*}` - <a href="/1.6/creating-manifest/placeholders/#function-placeholders" target="_blank">functional placeholders</a>  are available during all JPS installation process.

## Function Placeholders

These are the functions integrated inside Cloud Scripting:                               

- `${fn.password}` - random value within the upper and lower cases. The default length value is *'10'*. 
    The length can be passed as `${fn.password(max value)}`.   
- `${fn.base64}` - *base64* encoding                   
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


The function parameter can be passed from existing placeholders, for example:                         

- `${fn.md5([fn.random])}` - *md5* encoding random password   
- `${fn.base64([user.email])}` - *base64* encoding user email address  

You can easily define function placeholders within the [custom global placeholders](#custom-global-placeholders), for example:
@@@
```yaml
globals:
  pass: ${fn.password}
```
``` json
{
  "globals": {
    "pass": "${fn.password}"
  }
}
```
@@!
Now, you can use <b>*${globals.pass}*</b> within the entire manifest.

## Array Placeholders

Any array has a list of specific placeholders: array *length*, element by *ID*, the *first* and the *last* array elements.   

**Array Length**

Any array length placeholder can be defined within a manifest. 

**Example**

```
${nodes.cp.length},
${nodes.bl.extips.length}
```

**Element by ID**    

Each element has an index in the array. 

**Example**                         

`{nodes.cp[(i)].(key)}`   

where:

- `(i)` - array index, starting from *'0'*                     
- `(key)` - node <a href="/1.6/creating-manifest/placeholders/#node-placeholders" target="_blank">parameters</a>                            

**The First and the Last Array Elements** 

- `{nodes.cp.first.(key)}` - array element with the *'0'* index              
- `{nodes.sqldb.last.(key)}` - array element with the last ID in the array                      

Here, <b>*key*</b> is the node parameter.                         

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

You can use the following placeholders, as well, with the definite *nodeType*:                               

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

Explore the full list of available <a href="/1.6/creating-manifest/selecting-containers/#all-containers-by-type" target="_blank">*nodeType*</a> values within the linked page.                                                         

The list of single placeholders:

- `${nginxphp.NGINX_CONF}` - */etc/nginx/nginx.conf*   
- `${postgresql.POSTGRES_CONF}` - */var/lib/pgsql/data*   
- `${mysql5.MYSQL_CONF}` - */etc*   
- `${mariadb.MARIADB_CONF}` - */etc*             
- `${nginxphp.PHP_CONF}` - */etc/php.ini*   
- `${nginxphp.PHPFPM_CONF}` - */etc/php-fpm.conf*   
- `${nginxphp.PHP_MODULES}` - */usr/lib64/php/modules*   
- `${nginxphp.WEBROOT}` - */var/www/webroot*   


## Default Values of Placeholders

All placeholders which are spelled out in manifest and are not defined in Cloud Scripting during manifest execution will be displayed like a simple texts. <br>
In the example below the **action** `assert` is executed where values are compared.

@@@
```yaml
type: update
name: Default values of placeholders
onInstall:
  assert:
  - "'${unknown:defaultValue}' === 'defaultValue'"
  - "'${noName:[fn.password(7)]}'.length === 7"
  - "'${unknown:}' === ''"
```
```json
{
    "type": "update",
    "name": "Default values of placeholders",
    "onInstall": {
        "assert": [
            "'${unknown:defaultValue}' === 'defaultValue'",
            "'${noName:[fn.password(7)]}'.length === 7",
            "'${unknown:}' === ''"
        ]
    }
}
```
@@!

The first comparing in `assert` action is **"'\${unknown:defaultValue}' === 'defaultValue'"**, where placeholder *\${unknown:defaultValue}* in Cloud Scripting engine isn't defined. So the simple string will be displayed in console. The same behaviour will be with another comparisons.<br>
The executed results on the screen below:
![simple-comparison](/img/simple-comparison.png)

Default placeholder values can be replaced in placeholders if they were defined before they are spelled out in manifest. For example, custom placeholders can be defined in action `set`.

@@@
```yaml
type: update
name: Default values of placeholders
onInstall:
- set:
    custom: test
    length: 7
    'null':
    'false': false
    empty: ''
- assert:
  - "'${unknown:defaultValue}' === 'defaultValue'"
  - "'${unknown:[fn.password(7)]}'.length === 7"
  - "'${unknown:[this.custom]:[this.custom]}' === 'test'"
  - "'${unknown:[fn.password([this.length])]}'.length === 7"
  - "'${unknown:[this.custom]}' === 'test'"
  - "'${unknown:[this.empty]}' === ''"
  - "'${unknown:[this.false]}' === 'false'"
  - "'${unknown:[this.null]}' === 'null'"
  - "'${unknown:}' === ''"
```
```json
{
  "type": "update",
  "name": "Default values of placeholders",
  "onInstall": [
    {
      "set": {
        "custom": "test",
        "length": 7,
        "null": null,
        "false": false,
        "empty": ""
      }
    },
    {
      "assert": [
        "'${unknown:defaultValue}' === 'defaultValue'",
        "'${unknown:[fn.password(7)]}'.length === 7",
        "'${unknown:[this.custom]:[this.custom]}' === 'test'",
        "'${unknown:[fn.password([this.length])]}'.length === 7",
        "'${unknown:[this.custom]}' === 'test'",
        "'${unknown:[this.empty]}' === ''",
        "'${unknown:[this.false]}' === 'false'",
        "'${unknown:[this.null]}' === 'null'",
        "'${unknown:}' === ''"
      ]
    }
  ]
}
```
@@!
The results on the screen below:
![comparison](/img/comparison.png)

<br>       
<h2> What’s next?</h2>                    

- See how to use <a href="/1.6/creating-manifest/conditions-and-iterations/">Conditions and Iterations</a>                                

- Read how to integrate your <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a>                      

- Check how to create your custom <a href="/1.6/creating-manifest/addons/" target="_blank">Add-Ons</a>                                         

- Find out how to handle <a href="/1.6/creating-manifest/handling-custom-responses/" target="_blank">Custom Responses</a>      

- Learn how to customize <a href="/1.6/creating-manifest/visual-settings/" target="_blank">Visual Settings</a>

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples
