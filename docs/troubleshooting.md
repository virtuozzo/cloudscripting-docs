# Troubleshooting

Run into trouble with Cloud Scripting? Here are some helpful tips and specific suggestions for troubleshooting as follows.                     

* Log in to your Jelastic dashboard and open the link of the following type in a new browser tab:              

    *http://appstore.{HOSTER_URL}/console/*                       
    
    Here, substitute <b>*{HOSTER_URL}*</b>  with the platform domain of your hosting provider (see the last column of the table within the <a href="https://docs.jelastic.com/jelastic-hoster-info" target="_blank">Hosters Info</a> page).                                           

* In the opened browser tab, you will see the Cloud Scripting execution log.                                                               
    
<center>![troubleshooting](img/troubleshooting.jpg)</center>          

!!! note
    The maximum size of the log is 1 MB. The log will be truncated or overwritten, if this limit is exceeded.

Below, you can find some samples of editing custom information to the log:                      

* outputting a single <a href="http://docs.cloudscripting.com/reference/placeholders/" target="blank">placeholder</a> value                     

``` json
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

* outputting all the placeholders              

``` json
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "log": "${placeholders}"
  }
}
```  

* outputting from a script             

``` json  
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

``` javascript                                               
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