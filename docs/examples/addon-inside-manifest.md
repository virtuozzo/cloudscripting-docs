#Install Add-on inside Manifest

This manifest provides an environment, that is handled with the help of <b>Apache PHP</b> aplication server, is powered by <b>PHP 7</b> engine version and has external IP address attached. Subsequently, Public IP address can be detached with the help of the <b>Add-on</b> button.
```example
{
	"jpsType": "install",
	"application": {
		"name": "example",
		"env": {
			"topology": {
				"engine": "php7.0",
				"nodes": [{
					"nodeType": "apache2",
					"cloudlets": "16",
					"addons": [
						"setExtIp"
					]
				}]
			}
		},
		"addons": [{
			"id": "setExtIp",
			"onInstall": {
				"call": "attacheIp"
			},
			"onUnInstall": {
				"call": "deAttacheIp"
			},
			"procedures": [{
				"id": "attacheIp",
				"onCall": [{
					"setExtIpEnabled": {
						"nodeType": "apache2",
						"enabled": true
					}
				}]
			}, {
				"id": "deAttacheIp",
				"onCall": [{
					"setExtIpEnabled": {
						"nodeType": "apache2",
						"enabled": false
					}
				}]
			}]
		}],
		"success": "Environment with add-on installed successfully!"
	}
}
```
   
As a result, environment with the above-specified topology is successfully created. In order to disable the external IP feature, click the <b>Uninstall</b> button located within the <b>Add-ons</b> section.   

![addoninstall](/img/addon-install.jpg)