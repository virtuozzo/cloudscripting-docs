<h1>Troubleshooting</h1>
Run into trouble with Cloud Scripting? Here are some helpful tips and specific suggestions for troubleshooting as follows:      
<ul><li><p dir="ltr" style="text-align: justify;">Log in to your Jelastic dashboard and open the link of the following type in a new browser tab:</p></li>          

    <p dir="ltr" style="text-align: justify;">http://appstore.{HOSTER_URL}/console/</p>                   

    <p dir="ltr" style="text-align: justify;">Here, substitute *{HOSTER_URL}* with the platform domain of your hosting provider (see the last column of the table within the <a href="https://docs.jelastic.com/jelastic-hoster-info" target="_blank">Hosters Info</a> page).</p>               

<li><p dir="ltr" style="text-align: justify;">In the opened browser tab, you will see the Cloud Scripting execution log.</p></li></ul>                                 

<center>![troubleshooting](img/troubleshooting.jpg)</center>      

!!! note
> The maximum log size is 1 MB. The log will be truncated or overwritten, if this limit is exceeded.

Below, some tips are provided on how to edit custom information to the log.        

Output a single placeholder value:
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

Output all the placeholders:
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