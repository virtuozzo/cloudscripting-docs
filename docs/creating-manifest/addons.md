# Add-Ons

Cloud Scripting allows you to install a custom add-on to a new environment or to an existing one. You can develop your custom add-on within another - *parent* manifest. Therefore, you need to set the add-on's installation type to *update* and declare essential properties within the *addons* section.

You can install the developed add-on either by specifying a target [*nodeGroup*](/creating-manifest/selecting-containers/#all-containers-by-group), or by calling the [*installAddon*](/creating-manifest/actions/#installaddon) action.


## Examples

The following example illustrates the add-on's installation to a specific *nodeGroup* (layer).

@@@
```yaml
type: install
name: Addon installation

nodes:
  - nodeType: apache2
    addons: custom-addon-id
  - nodeType: mysql5

addons:
  - id: custom-addon-id
    name: Custom Addon
    onInstall:
      api [cp]: environment.control.RestartNodes
```
```json
{
  "type": "install",
  "name": "Addon installation",
  "nodes": [
    {
      "nodeType": "apache2",
      "addons": "custom-addon-id"
    },
    {
      "nodeType": "mysql5"
    }
  ],
  "addons": {
    "id": "custom-addon-id",
    "name": "Custom Addon",
    "onInstall": {
      "api [cp]": "environment.control.RestartNodes"
    }
  }
}
```
@@!

In the example above, the [Virtuozzo Application Platform API](https://www.virtuozzo.com/application-platform-api-docs/) ***RestartNodes*** method is executed after the environment creation is completed. The compute node is restarted at the end of the manifest installation procedure.

!!! note
    The add-on is installed only if the *parent* manifest's installation type is *install*. When the add-on is installed, the **Add-ons** tab for the corresponding compute node becomes available at the dashboard.

![new-addon](/img/creating-manifest/addons/new-addon.png)

The following example illustrates the add-on's installation by calling the *installAddon* action. You can call this action for both *update* and *install* installation types of a *parent* manifest.

@@@
```yaml
type: install
name: Addon installation

onInstall:
  installAddon:
    id: custom-addon-id

addons:
  - id: custom-addon-id
    name: Custom Addon
    onInstall:
      createFile [cp]: /var/log/test.log
```
```json
{
  "type": "install",
  "name": "Addon installation",
  "onInstall": {
    "installAddon": {
      "id": "custom-addon-id"
    }
  },
  "addons": {
    "id": "custom-addon-id",
    "name": "Custom Addon",
    "onInstall": {
      "createFile [cp]": "/var/log/test.log"
    }
  }
}
```
@@!

Through this example, a new *test.log* file is created during the *onInstall* action execution. You can declare the add-on's expected behavior within the *addons* section, while the *installAddon* action is needed to specify the appropriate add-on's identifier.


## What's next?

- Find out how to handle [Custom Responses](/creating-manifest/handling-custom-responses/)
- Explore how to customize [Visual Settings](/creating-manifest/visual-settings/)
- Examine a bunch of [Samples](/samples/) with operation and package examples
- See [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions
