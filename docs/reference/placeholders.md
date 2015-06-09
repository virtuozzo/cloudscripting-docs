# Placeholders
Cloud Scripting supports a list of placeholders that can be used in any section of manifest file (if the section isn't strictly limited with its content).
The executor will try to resolve all placeholders on the package installation stage.
If it's not possible placeholder will be unresolved and displayed in the text as is (e.g. ${placeholder})

## Environment placeholders

- `{env.}`
    - `${env.appid}` - application appid
    - `${env.domain}` - application domain
    - `${env.protocol}` - protocol
    - `${env.url}` - link to application (env)
- `${nodes.}`
    - `{nodes.cp[i].address}` - IP address of compute node, where `i` - equals an index of node      
...

## File path placeholders

- `${HOME}`
- `${JAVA_HOME}`
- `${SERVER_BACKUP}`
- `${SERVER_CONF}`
- `${SERVER_CONF_D}`
- `${SERVER_DATA}`
- `${SERVER_LIBS}`
- `${SERVER_MODULES}`
- `${SERVER_SCRIPTS}`
- `${SERVER_WEBROOT}`
- `${SYSTEM_CRON}`
- `${SYSTEM_ETC}`
- `${SYSTEM_KEYS}`


## Account information                                                                                                                                       
- `${user.uid}`
- `${user.email}`
- `${user.appPassword}`   
...

## Input parameters
- `${settings.key}` - `key` - name of application setting. This placeholder will be resolved if you use user defined parameters in your manifest.

For Example:
```example
${settings.user_email}
```
 
## Procedure placeholders
- `${this.param}` - `param` - name of a procedure parameter.
 
## Event placeholders
- `${event.params.key}` - `key` - name of event parameter
- `${event.response.key}` - key` - name of event response parameter 

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