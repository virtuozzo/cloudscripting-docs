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
    - `${env.envName}` - short domain name (without hoster url). String
    - `${env.shortdomain}` - short domain name. Alias to `envName`. String
    - `${env.hardwareNodeGroup}` - HW node group. String
    - `${env.ssl}` - env ssl status. Boolean
    - `${env.sslstate}` env ssl state. Boolean
    - `${env.status}` env status. Available statuses are: 1 - running, 2 - down, 3 - launching, 4 - sleep, 6 - creating, 7 - cloning, 8 - exists. Number
    - `${env.uid}` - user uid. Number
    - `${env.ishaenabled}` - HA status. Boolean
    - `${env.ha}` - alias to `${env.ishaenabled}`. Boolean
    - `${env.isTransferring}` - transfering status. Boolean
    - `${env.creatorUid}` - env creator id. Number
    - `${env.engine.id}` - engine id. Number
    - `${env.engine.keyword}` - engine keyword. String
    - `${env.engine.name}` - engine name. String
    - `${env.engine.type}` - engine type. String
    - `${env.engine.vcsSupport}` - vcs support status. Boolean
    - `${env.engine.version}` - engine version. String
    - `${env.contexts.type}` - env context type. String
    - `${env.contexts.context}` - context name
    - `${env.contexts.archivename}` - context display name
    
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
        - `adminUrl` - full url address with protocol   
        - `canBeExported` - boolean value. Jelastic [Export](https://docs.jelastic.com/environment-export-import) feature   
        - `diskIopsLimit` - iops limitation quota   
        - `diskLimit` - hw disk space quota   
        - `fixedCloudlets` - set fixed cloudlets   
        - `flexibleCloudlets` - set flexible cloudlets   
        - `id` - id node   
        - `intIP` - internal IP address   
        - `isClusterSupport`    
        - `isExternalIpRequired`   
        - `isResetPassword`    
        - `isWebAccess`   
        - `ismaster`   
        - `maxchanks`   
        - `name`   
        - `nodeGroup`   
        - `nodeType`   
        - `nodemission`   
        - `osType`   
        - `password`   
        - `port`   
        - `type`  
        - `url`   
        - `version`   
        - `engines`:  
            - `id`  
            - `keyword`  
            - `name`  
            - `type`  
            - `vcsSupport`  
            - `version`  
        - `activeEngine`:  
            - `id`  
            - `keyword`  
            - `name`  
            - `type`  
            - `vcsSupport`  
            - `version`  

For example:

```example
    `{nodes.cp[1].address}` - IP address of a second compute node
    `{nodes.bl.first.address}` - First IP address of balancer node
    `{nodes.db.last.address}` - Last IP address of compute node
```

## File path placeholders

- `${HOME}` (/opt/tomcat/temp)
- `${JAVA_HOME}` (/usr/java/latest)
- `${SERVER_BACKUP}` (/var/lib/jelastic/backup)
- `${SERVER_CONF}` (/opt/tomcat/conf)
- `${SERVER_CONF_D}` - Available for nginx, apache nodes (/etc/httpd/conf.d)
- `${SERVER_DATA}` (/var/lib/pgsql/data)
- `${SERVER_LIBS}` (/opt/tomcat/lib)
- `${JAVA_LIB}` (opt/tomcat/lib)
- `${SERVER_MODULES}` /opt/tomcat/lib
- `${SERVER_SCRIPTS}` (/var/lib/jelastic/bin)
- `${SERVER_WEBROOT}` (/opt/tomcat/webapps)
- `${WEBAPPS}` (/opt/tomcat/webapps)
- `${SYSTEM_CRON}` (/var/spool/cron)
- `${SYSTEM_ETC}` (/etc)
- `${SYSTEM_KEYS}` (/var/lib/jelastic/keys)

## Account information                                                                                                                                       
- `${user.uid}`
- `${user.email}`
- `${user.appPassword}`
- `${user.name}`

## Input parameters
- `${settings.jelastic_email}` - user email. Always is Predefined.
- `${settings.key}` - `key` - name of application setting. This placeholder will be resolved if you use user defined parameters in your manifest.

For Example:
```example
{
  "jpsType": "update",
  "application": {
    "settings": {
      "fields": [
        {
          "type": "string",
          "name": "key",
          "caption": "String field"
        }
      ]
    }
  }
}
```
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
- `${event.params.(key)}` - `key` - name of event parameter
- `${event.response.(key)}` - key` - name of event response parameter 
Detailed placeholders list [here](/reference/events/)

## UI placeholders
- `${user.uid}`
- `${user.email}`
- `${env.domain}`
- `${env.appid}`

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
