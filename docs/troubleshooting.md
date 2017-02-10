# Troubleshooting

- Choose a hosting provider from the <a href="https://jelastic.cloud" target="_blank">Jelastic Cloud Union</a>, log in to your Jelastic account and open the link of the following type in a new browser tab: 

    <http://appstore.{HOSTER_URL}/console/> 

    Here, substitute a *{HOSTER_URL}* with the platform domain of the chosen hosting provider (see the last column of the table within the <a href="https://docs.jelastic.com/jelastic-hoster-info" target="_blank">Hosters Info</a> page).     

- In the opened browser tab you will see the Cloud Scripting execution log.              

<center>![Console](https://download.jelastic.com/public.php?service=files&t=a662aacb111575cf3d37b1d94fe59af9&download)</center>   

!!! note
    The maximum log size is 1 MB. The log will be truncated or overwritten, if this limit exceeded.

Below, some examples are provided on how to edit custom information to the log.        

Output single placeholder value:
```
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "log": [
      "Hello",
      "${user.email}"
    ]
  }
}
```

Output all placeholders:
```
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "log": "${placeholders}"
  }
}
```                                                                                      

Output from the script:
```
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "executeScript": {
      "type": "js",
      "script": "http://example.com/script.js"
    }
  },
  "actions": [
    {
      "myaction": {
        "log": "${this.message}"
      }
    }
  ]
}
```

`script.js` body:

```                                                
var message = 'Hello';

return { 
    result: 0, 
    onAfterReturn: {
        call: [{
            action: 'log', 
            params: {
                message: message
            } 
        }, {
            action: 'log',
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