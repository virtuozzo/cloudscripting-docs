#Addons

A Cloud Scripting technology provides an ability to install a custom addons within new environment or in an existing environment. A custom addon is an insertion with manifest `type` *update* within a parent JPS.  
It is described in `addons` section.
   
These addons can be called in two options - an install addon within one `nodeGroup` or to call `installAddon` action.

The first one case is a installation in `nodeGroup` layer:

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
      "api [cp]": "environment.control.RestartNodesByGroup"
    }
  }
}
```

In the example above, Jelastic API method **RestartNodesByGroup** will be executed after the environment creation completion. A compute node will be restarted at the end of manifest installation procedure. 
In this case, the addons instalation can be executed only if manifest `type` is **install**.  
The **Add-ons** tab will be available after manifest installation.
<center>![add-ons-tab.jpg](/img/add-on_tab.jpg)</center>
  
A another case for install addons is to call the `installAddon` action. This action can be called while manifest `type` is **update** or **install**.

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

In this example, a new file *test.log* will be created during `onInstall` action. The addon behaviour should be described in `addons` section, `installAddon` action need to take only addon's identifier.

<br>       
<h2> What’s next?</h2>                    

- Find out the list of <a href="/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching   
- See how to use <a href="/creating-templates/conditions-and-iterations/">Conditions and Iterations</a>                              
- Read how to integrate your <a href="/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a>   
- Learn how to customize <a href="/creating-templates/user-input-parameters/" target="_blank">Visual Settings</a>              
- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples   