# Troubleshooting

Run into trouble with Cloud Scripting? Here are some helpful tips and specific suggestions for troubleshooting as follows:                             

* Log in to your Jelastic dashboard and open the link of the following type in a new browser tab.                            

    *http://app.{HOSTER_URL}/console/*                       
    
    Here, substitute <b>*{HOSTER_URL}*</b>  with the platform domain of your hosting provider (see the last column of the table within the <a href="https://docs.jelastic.com/jelastic-hoster-info" target="_blank">Hosters Info</a> page).                                           

* In the opened browser tab, you will see the Cloud Scripting execution log.                                                               
    
![troubleshooting](img/troubleshooting.jpg)          

!!! note
    The maximum size of the log is 1 MB. The log will be truncated or overwritten, if this limit is exceeded.

Below, you can find some samples of editing custom information to the log:                      

- outputting a single <a href="/1.6/creating-manifest/placeholders/" target="blank">placeholder</a> value                     

@@@
```yaml
type: update
name: LogTest

onInstall:
  log:
    - Hello
    - ${user.email}
```
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
@@!

- outputting all the placeholders              

@@@
```yaml
type: update
name: LogTest

onInstall:
  log: ${placeholders}
```
``` json
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "log": "${placeholders}"
  }
}
```
@@!

All dynamic placeholders in *\${placeholders}* value are updated immediately after any action. Also placeholders will be updated automatically before displaying \${placeholders} value into console.

- outputting from a script             

@@@
```yaml
type: update
name: LogTest

onInstall:
  script:
    type: js
    script: "http://example.com/script.js"

actions:
  - myaction:
      log: ${this.message}
```
``` json  
{
  "type": "update",
  "name": "LogTest",
  "onInstall": {
    "script": {
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
@@!

`script.js` body:      

``` javascript                                               
var message = 'Hello';

return { 
    result: 0, 
    onAfterReturn: {
        call: [{
            action: 'myaction', 
            params: {
                message: message
            } 
        }, {
            action: 'myaction',
            params: {
                message: 'World !'
            }
        }] 
    } 
};
```
<br>
<h2> What's next?</h2>    

- Read <a href="/releasenotes/" target="_blank">Realese Notes</a> to find out about the recent CS improvements                    

- Find out the correspondence between <a href="/jelastic-cs-correspondence/" target="_blank">CS & Jelastic Versions</a>          


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