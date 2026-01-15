# Troubleshooting

Having trouble with Cloud Scripting? Here are some helpful tips and specific troubleshooting suggestions:

- Log in to your Virtuozzo Application Platform dashboard and open the link of the following type in a new browser tab.

`http://app.{HOSTER_URL}/console/`

Here, substitute **{HOSTER_URL}**  with the platform domain of your hosting provider (see the last column of the table within the [Hosters Info](https://www.virtuozzo.com/application-platform-docs/hosting-providers/) page).

- In the opened browser tab, you will see the Cloud Scripting execution log.

![Cloud Scripting execution log](/img/troubleshooting/troubleshooting.jpg)

!!! note
    The maximum size of the log is 1 MB. The log will be truncated or overwritten, if this limit is exceeded.

Below, you can find some samples of editing custom information to the log:

- outputting a single [placeholder](/creating-manifest/placeholders/) value

@@@
```yaml
type: update
name: LogTest

onInstall:
  log:
    - Hello
    - ${user.email}
```
```json
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
```json
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
```json
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


## loggerName

When installing any JPS, the logger name is displayed next to the time in each line of the log.
By default, the name of the logger is determined by the parameter *name* inside the JPS manifest:

![Default logger name format](/img/troubleshooting/troubleshooting-default.png)

If the parameter *name* consists of more than two words, the name of the logger is formed by the first and last word with a dot as a delimiter:

![Multi-word logger name format](/img/troubleshooting/troubleshooting-name.png)

If you start the asynchronous installation of several identical JPSs, the name of logger may be overridden with **loggerName** parameter for each JPS in order to distinguish different JPS installation logs.

- inside *install* action:

Example 1:

```yaml
install:
  - jps: https://example.com/manifest.jps
    loggerName: Test 1

  - jps: https://example.com/manifest.jps
    loggerName: Test 2
```

Example 2:

```yaml
install:
  - loggerName: Test 1
    jps:
      type: install
      name: test
      onInstall:
        log: Test

  - loggerName: Test 2
    jps:
      type: install
      name: test
      onInstall:
        log: Test
```

![Logger name override examples](/img/troubleshooting/troubleshooting-loggername.png)

- with parameter of API request:

```javascript
api.marketplace.jps.Install({
  jps: "https://example.com/manifest.jps",
  loggerName: "Test 1"
});
```


## Current Step

To simplify debugging, the number of the current step is added to the logs. As you can see from the examples above, the step number follows the logger name and a colon.

![Step numbers in logs](/img/troubleshooting/troubleshooting-steps.png)


## separate log for each node in group

In case the engine splits action execution into separate requests, the logging is performed for each node separately. For example:

- asynchronous execution:

```yaml
cmd [cp, bl]: echo test
```

![Asynchronous execution logs](/img/troubleshooting/troubleshooting-async-nodesseparate.png)

- synchronous execution:

```yaml
sync: true
cmd [cp, bl]: echo test
```

![Synchronous execution logs](/img/troubleshooting/troubleshooting-sync-nodesseparate.png)


## warning

The warnings are highlighted with orange.

```yaml
onInstall:
  return:
    type: warning
    message: Warning message!
```

![Warning message display](/img/troubleshooting/troubleshooting-warning.png)


## What's next?

- Learn about [Creating Manifest](/creating-manifest/basic-configs/) and available configuration options
- Explore [Placeholders](/creating-manifest/placeholders/) for dynamic content in your scripts
- Review [Actions](/creating-manifest/actions/) to understand available operations
- Check out [Events](/creating-manifest/events/) for trigger-based automation
- Find out the correspondence between [CS & Virtuozzo Application Platform Versions](/virtuozzo-cs-correspondence/)
