#Control Flows: Conditions and Iterations

##Conditions
The main condition statement is *“if”*. Within this parameter, all available [Placeholders](http://docs.cloudscripting.com/reference/placeholders/) and their objective JavaScript  mappings can be used. For example:
```
if ('${env.protocol}' == 'http')
```
or 
```
if (env.protocol == 'http')
```

Both *If* and *ForEach* can be of any nesting level.

- In case a condition is specified incorrectly, the actions inside *if* statement won't be executed. Herewith, [Cloud Scripting Console](http://docs.cloudscripting.com/troubleshooting/) will return the <b>*‘invalid condition’*</b> message with the root cause explanation. The application installer will proceed to the next action.
- If condition is valid but hasn’t being executed, the <b>*'condition is not met'*</b> message will be logged.

<b>Examples:</b>     
Comparing global variables:
```
{
  "jpsType": "update",
  "application": {
    "name": "Comparing global variables",
    "globals": {
      "p1": 1,
      "p2": 2
    },
    "onInstall": [
      {
        "if (globals.p1 < globals.p2)": {
          "if (user.uid > 1)": {
            "log": "## p1 < p2 and ${user.email} is not a platform owner"
          }
        }
      }
    ]
  }
}
```

Checking environment status:
```
{
  "onInstall": {
    "if (env.status == 1)": {
      "log": "## Environment is running"
    }
  }
}
```
     
Checking Jelastic SSL status: 
```
{
  "onInstall": {
    "if(!${env.ssl})": {
      "log": "## SSL Disabled"
    }
  }
}
```

Environment domain validation:
```
{
  "onInstall": {
    "if (/^env-/.test(env.domain))": {
      "log": "## Env domain begins with env-: ${env.domain}"
    }
  }
}
```


Checking compute node OS type and balancer presence: 
```
{
  "onInstall": {
    "if (nodes.cp && nodes.cp[0].osType == 'LINUX')": [
      {
        "log": "## Environment has compute node based on Linux"
      },
      {
        "if (nodes.bl && nodes.bl[0].nodeType == 'nginx' && nodes.cp.length > 1)": {
          "log": "## Environment has Nginx balancer and more than one compute node"
        }
      }
    ]
  }
}
```

Nested conditions:   
  
Nesting of two *If* condition statements - the first one is checking an environment for two compute nodes presence. In case the nodes are available, the second one is checking the presence of external IP address on the first balancer node and logging the correspondent messages.
```
{
  "jpsType": "update",
  "name": "Nesting example",
  "onInstall": {
    "if (${nodes.cp[1].id})": [
      {
        "cmd [${nodes.cp[1].id}]": "echo \"Environment consists of two compute nodes\" >> /tmp/result.txt "
      },
      {
        "if (/^[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}/.test(\"${nodes.bl[0].extips}\"))": {
          "cmd [${nodes.cp[0].id}]": "echo \"Balancer node with external IP address!\" >> /tmp/result.txt "
        }
      }
    ]
  }
}
```

The operation result can be located within a *result.txt* file automatically created in the master node (i.e. the first *cp* node) *<b>tmp</b>* directory:
```
Environment consists of two compute nodes
Balancer node with external IP address!
```

Checking balancer stack type:
```
{
  "jpsType": "update",
  "name": "Nginx stack",
  "onInstall": {
    "if (nodes.bl[0].nodeType == 'nginx')": [
      {
        "script": "return { result: 0, error: \"Environment balancer node is NGINX stack\"};"
      }
    ]
  }
}
```

##Iterations
<b>ForEach.</b>
The main iterable object is *ForEach*. Its map:

```
{
  "env": {
    "nodes": [],
    "contexts": [],
    "extdomains": []
  },
  "nodes": {},
  "settings": {},
  "license": {},
  "event": {
    "params": {},
    "response": {}
  },
  "this": {}
}
```
where:    

- `settings [optional]` - fields values predefined within a [user setting form](http://docs.cloudscripting.com/creating-templates/user-input-parameters/)   
- `license [optional]` - link to fetch parameters specified within [prepopulate](http://docs.cloudscripting.com/creating-templates/user-input-parameters/) custom script. It enables to customize default field values and can be further initialized through [placeholders](http://docs.cloudscripting.com/reference/placeholders/) `$(license.{any_name}` within a manifest.   
- `event [optional]` - object entity with [event](http://docs.cloudscripting.com/reference/events/) parameters.  Can be of two types that allows initiation of a particular [action](http://docs.cloudscripting.com/reference/actions/) before and after event execution   
- `this [optional]` - parameters object to be transmitted within the procedure body. See the [full list of available placeholders](http://docs.cloudscripting.com/reference/placeholders/#procedure-placeholders) on this parameter.   

Iteration can be executed by `env.nodes`, `nodes`, `env.contexts` and `env.extdomains` objects:

```
{
  "forEach(env.extdomains)": [
    {
      "writeFile": {
        "nodeGroup": "cp",
        "path": "/var/lib/jelastic/keys/${@i}.txt",
        "body": "hello"
      }
    }
  ]
}
```
where:    

- `@i` - default iterator name

```
{
  "forEach(env.contexts)": [
    {
      "writeFile": {
        "nodeGroup": "cp",
        "path": "/var/lib/jelastic/keys/${@i.context}.txt",
        "body": "1"
      }
    }
  ]
}
```
where:  

- `env.contexts` -  list of contexts (applications) deployed to environment    
- `env.extdomains` - bound external domains 

See the [full list of available placeholders](/reference/placeholders/).

Scaling nodes example:
```
{
  "jpsType": "update",
  "name": "Scaling Example",
  "onAfterScaleIn[nodeGroup:cp]": {
    "call": "ScaleNodes"
  },
  "onAfterScaleOut[nodeGroup:cp]": {
    "call": "ScaleNodes"
  },
  "actions": [
    {
      "ScaleNodes": [
        {
          "forEach(nodes.cp)": {
            "cmd [bl]": [
              "{commands to rewrite all Compute nodes internal IP addresses in balancer configs. Here balancer node is NGINX}",
              "/etc/init.d/nginx reload"
            ]
          }
        }
      ]
    }
  ]
}
```
As a result of *execCmd*, compute nodes internal IP addresses are rewritten within balancer configs and *NGINX* balancer node is reloaded. `onAfterScaleIn` and `onAfterScaleOut` events are executed immediately after adding or removing a compute node.

###Iteration by all nodes in environment

```
{
  "forEach(env.nodes)": [
    {
      "cmd [${@i.id}]": "echo ${@i.address} > /tmp/example.txt"
    }
  ]
}
```

###Iteration by compute nodes with custom iterator name
```
{
  "forEach(cp:nodes.cp)": {
    "execCmd" : {
      "nodeId": "${@cp.id}",
      "nodeGroup": "${@cp.nodeGroup}",
      "nodeType": "${@cp.nodeType}",
      "commands": [
        "echo ${@cp.address} > /tmp/example.txt"
      ]
    }
  }
}
```
where:   
- `@cp [optional]` - custom iterator name

Custom iterator name can be used for nesting cycles one into another:
```
{
  "forEach(item:env.nodes)": [
    {
      "forEach(env.nodes)": [
        {
          "execCmd": {
            "nodeId": "${@i.id}",
            "commands": "[[ '${@i.id}' -eq '${@item.id}' ]] && touch /tmp/${@}.txt || touch /tmp/${@}${@}.txt"
          }
        }
      ]
    }
  ]
}
```
where:   
- `@` iterator number

In this case every environment node will have only one conjunction by node ID.