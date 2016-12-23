# Troubleshooting

- Choose hoster provider at ![Jelastic site](https://jelastic.cloud), log into your Jelastic account and open the following link in a new browser tab: <http://appstore.{HOSTER_URL}/console/>  
- In the opened browser tab you will see the Cloud Scripting execution log

![Console](https://download.jelastic.com/public.php?service=files&t=a662aacb111575cf3d37b1d94fe59af9&download)

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

`script.js` body:

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