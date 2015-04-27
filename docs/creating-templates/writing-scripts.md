# Writing Scripts

Custom users’ scripts can be written in Java, PHP or JavaScript. Inside these scripts, the set of client libraries for platform’s API methods calling is available. 
A script can be subscribed to the onAfterReturn event on its outlet for, for example, execution of the [Call](/reference/actions/#call) action.


    
## Intercontainer Scripts
Using `executeShellCommands` action.

```example
{
  "executeShellCommands": [
    {
      "nodeMission": "cp",
      "commands": [
        "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
      ]
    }
  ]
}
```

## Top level scripts
Using `executeScript` action.

### Java
```example
{
  "executeScript": [
    {
        "type" : "java",        
        "params" : {
            "greeting" : "Hello World!"
        },
        "script" : "return hivext.local.GetParam(\"greeting\");",
    }
  ]
}
```
### JavaScript
```example
{
  "executeScript": [
    {
        "type" : "js",        
        "params" : {
            "greeting" : "Hello World!"
        },
        "script" : "return getParam('greeting');",
    }
  ]
}
```

### PHP
```example
{
  "executeScript": [
    {
        "type" : "php",        
        "params" : {
            "greeting" : "Hello World!"
        },
        "script" : "return $hivext->local->getParam(\"greeting\")",
    }
  ]
}
```

## What's next?
Learn more about using [Jelastic Cloud API](http://docs.jelastic.com/api/)
