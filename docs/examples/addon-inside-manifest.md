#Install Add-on inside Manifest

This manifest installs environment consisting of Apache PHP node with the PHP 7 engine version and attached external IP address. External IP address can be detached with the help of the add-on button.
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

As a result, environment with the above mentioned configurations is successfully installed. In order to disable external IP feature, click the Uninstall button located within the add-ons section.   
![addoninstall](/img/addon-install.jpg)
