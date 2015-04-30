# Troubleshooting

- Log in to your Jelastic account and open the following link in a new browser tab: <http://appstore.cloudscripting.com/console/>  
- In the opened browser tab you will see the Cloud Scripting execution log

![Console](http://77047754c838ee6badea32b5afab1882.app.cart.jelastic.com/xssu/cross/download/RDYYHFRvUwRZAQ8fYlJqFBNHARcBTURBChNqHyt5clNCF0RRDwYAQmNTTEBI)

!!! note
    Maximum log size is 1 MB. The log will be truncated or overwritten if this limit exceeded.

Below you can see an examples of how to write custom information to the log.

Output single placeholder value:
```
{
  "jpsType": "update",
  "application": {
    "name": "LogTest",                                      
    "onInstall": {
      "log": [
        "Hello", 
        "${user.email}"
      ]
    }
  }
}
```

Output all placeholders:
```
{
  "jpsType": "update",
  "application": {
    "name": "LogTest",
    "onInstall": {
      "log": "${placeholders}"
    }
  }
}
```                                                                                      

Output from the script:
```
{
  "jpsType": "update",
  "application": {
    "name": "LogTest",
    "onInstall": {
      "executeScript": {
        "type": "js",
        "script": "http://example.com/script.js"
      }
    },
    "procedures": [
      {
        "id": "log",
        "onCall": {
          "log": "${this.message}"
        }
      }
    ]
  }
}
```

script.js body:

```
var message = 'Hello';

return { 
    result: 0, 
    onAfterReturn: {
        call: [{
            procedure: 'log', 
            params: {
                message: message
            } 
        }, {
            procedure: 'log',
            params: {
                message: 'World !'
            }
        }] 
    } 
};
```
<!--## Logging-->
<!--Work in progress...-->
<!--
add example 
2 procedures:
- log - public_html/cs.txt (do not forget to limit log) 
- getLogLink 
-->


<!--## Checking event subscribers list-->
<!--Work in progress...-->
<!-- think how to do that -->