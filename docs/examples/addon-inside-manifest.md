#Install Add-on inside Manifest

This manifest provides an environment, that is handled with the help of **Apache PHP** application server, is powered by **PHP 7** engine version and has external IP address attached. Subsequently, Public IP address can be detached with the help of the **Add-on** button.
``` json
{
  "type": "install",
  "name": "example",
  "nodes": [
    {
      "nodeType": "apache2",
      "cloudlets": "16",
      "addons": [
        "setExtIp"
      ]
    }
  ],
  "engine": "php7.0",
  "addons": {
    "id": "setExtIp",
    "onInstall": "attacheIp",
    "onUnInstall": "deAttacheIp",
    "actions": {
      "attacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": true
        }
      },
      "deAttacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": false
        }
      }
    }
  },
  "success": "Environment with add-on installed successfully!"
}
```
   
As a result, environment with the above-specified topology is successfully created. In order to disable the external IP feature, click the **Uninstall** button located within the **Add-ons** section.   

![addoninstall](/img/addon-install.jpg)
