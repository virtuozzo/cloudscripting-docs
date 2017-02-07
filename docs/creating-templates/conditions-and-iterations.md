#Control Flows: Conditions and Iterations

##Conditions
The main condition statement is *'if'*. Within this parameter, all available <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">placeholders</a> and their objective JavaScript  mappings can be used. 

For example:
```
if ('${env.protocol}' == 'http')
```
or 
```
if (env.protocol == 'http')
```

Both *If* and *ForEach* can be of any nesting level.

- In case a condition is specified incorrectly, the actions inside *if* statement won't be executed. Herewith, <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Cloud Scripting Console</a> will return the <b>*‘invalid condition’*</b> message with the root cause explanation. The application installer will proceed to the next action.
- If condition is valid but hasn’t being executed, the <b>*'condition is not met'*</b> message will be logged.

<b>Examples</b>    

Comparing global variables:
```
{
  "jpsType": "update",
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
<b>ForEach</b>

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

- `settings` *[optional]* - fields values predefined within a <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">user setting form</a>          
- `license [optional]` - link to fetch parameters specified within <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">prepopulate</a> custom script. It enables to customize default field values and can be further initialized through <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">placeholders</a> `$(license.{any_name}` within a manifest.    
- `event [optional]` - object entity with <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">events</a> parameters; can be of two types that allow initiation of a particular <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank"> action</a>before and after event execution       
- `this [optional]` - parameters object to be transmitted within the procedure body. See the <a href="http://docs.cloudscripting.com/reference/placeholders/#procedure-placeholders" target="_blank">full list of available placeholders</a> on this parameter.     

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
- `env.extdomains` - bound external domains 

```
{
  "forEach(env.contexts)": {
    "writeFile [cp]": {
      "path": "/var/lib/jelastic/keys/${@i.context}.txt",
      "body": "1"
    }
  }
}
```
where:  

- `env.contexts` -  list of contexts (applications) deployed to an environment    

See the <a href="http://docs.cloudscripting.com/reference/placeholders/#procedure-placeholders" target="_blank">full list of available placeholders</a>.             

Scaling nodes example:
```
{
  "jpsType": "update",
  "name": "Scaling Example",
  "onAfterScaleIn[nodeGroup:cp]": "ScaleNodes",
  "onAfterScaleOut[nodeGroup:cp]": "ScaleNodes",
  "actions": {
    "ScaleNodes": {
      "forEach(nodes.cp)": {
        "cmd [bl]": [
          "{commands to rewrite all Compute nodes internal IP addresses in balancer configs. Here balancer node is NGINX}",
          "/etc/init.d/nginx reload"
        ]
      }
    }
  }
}
```
As a result of *cmd*, compute nodes internal IP addresses are rewritten within balancer configs and *NGINX* balancer node is reloaded. <b>*onAfterScaleIn*</b> and <b>*onAfterScaleOut*</b> events are executed immediately after adding or removing a compute node.   

###Iteration by all nodes in environment

```
{
  "forEach(env.nodes)": {
    "cmd [${@i.id}]": "echo ${@i.address} > /tmp/example.txt"
  }
}
```

###Iteration by compute nodes with custom iterator name
```
{
  "forEach(cp:nodes.cp)": {
    "cmd [${@cp.id}]": "echo ${@cp.address} > /tmp/example.txt"
  }
}
```
where:   
- `@cp [optional]` - custom iterator name. Target nodes also can be set by type -`${@cp.nodeType}` or group - `${@cp.nodeGroup}` 

Custom iterator name can be used for nesting cycles one into another:
```
{
  "jpsType": "update",
  "name": "execution actions",
  "onInstall": {
    "forEach(item:env.nodes)": {
      "forEach(secondItem:env.nodes)": {
        "log": "${@@item} - ${@@secondItem} - ${@}"
      }
    }
  }
}
```
where:   

- `${@}` - iterator number current loop  
- `${@@item}` - iterator number of the first loop 
- `${@@secondItem}` - iterator number of the second loop 

In this case, every environment node will have only one conjunction by <b>Node ID</b>.

`ForEach` **count** execution is printed in a <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">user console log</a> for usefull debugging code execution.     

<center>![forEachCount](/img/forEachCount.jpg)</center>