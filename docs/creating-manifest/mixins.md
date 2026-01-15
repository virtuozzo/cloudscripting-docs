# Mixins

The **mixins** provide agility in Cloud Scripting allowing to include(mix) pieces of code from one manifest into another.
The following sections can be mixed:

- `globals`
- `actions`
- `addons`
- `responses`

The *mixins* section in JPS manifest can contain a description of both a single and an array of *mixins*.

!!! note
    If there are included identical *mixins* or recursive ones, only the first occurrence will be taken into action. Names defined in the main manifest have higher priority than those in the *mixins*.

**main.jps**

@@@
```yaml
type: install
name: Mixins Example
baseUrl: https://example.com/mixins

mixins:
  - mixin1.jps
  - mixin2.jps

actions:
  mainAction:
    log: mainTest

onInstall:
  - mainAction
  - mixin1Action
  - mixin2Action
```
```json
{
  "type": "install",
  "name": "Mixins Example",
  "baseUrl": "https://example.com/mixins",
  "mixins": [
    "mixin1.jps",
    "mixin2.jps"
  ],
  "actions": {
    "mainAction": {
      "log": "mainTest"
    }
  },
  "onInstall": [
    "mainAction",
    "mixin1Action",
    "mixin2Action"
  ]
}
```
@@!

Where the Included mixins' code looks as follows:

**mixin1.jps**

@@@
```yaml
mixins:
- https://example.com/mixins/mixin1.yaml

actions:
  mixin1Action:
    log: mixin1Action
```
```json
{
  "mixins": [
    "https://example.com/mixins/mixin1.yaml"
  ],
  "actions": {
    "mixin1Action": {
      "log": "mixin1Action"
    }
  }
}
```
@@!

**mixin2.jps**

@@@
```yaml
actions:
  mixin2Action:
    log: mixin2Action
```
```json
{
  "actions": {
    "mixin2Action": {
      "log": "mixin2Action"
    }
  }
}
```
@@!

While performing the example above, the result of mixins include will be displayed in the log before executing onInstall event:

![mixins-log](/img/creating-manifest/mixins/mixins-log.png)

!!! warning
    If the mixin could not be loaded, an ERROR will be displayed in the CS log indicating the reason (for example, file not found), and the response from the server will contain error code 11042.

Once the *mixins* are loaded, you can use any action which is in *mixins*.

The mixin's baseURL is always overridden by the baseURL from the main manifest the mixin is included into.


## What's next?

- Learn how to define [Actions](/creating-manifest/actions/)
- Explore [Add-Ons](/creating-manifest/addons/)
- See [Custom Scripts](/creating-manifest/custom-scripts/)
- Examine a bunch of [Samples](/samples/) with operation and package examples
- See the [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions
