````markdown
# Swap domain between two environments

```json
{
	"type": "install",
	"application": {
		"name": "swapDomain",
		"env": {
			"topology": {
				"engine": "php5.3",
				"nodes": [{
						"cloudlets": 6,
						"nodeType": "nginxphp"
					}
				]
			}
		},
		"onInstall": {
			"call": ["secondEnvInstallation"]
		},
		"procedures": [{
				"id": "secondEnvInstallation",
				"onCall": [{
						"executeScript": {
							"type": "javascript",
							"script": "https://download.jelastic.com/public.php?service=files&t=6922fed7efb17261e038bfc6d8947924&download"
						}
					}
				]
			}
		]
	}
}
```
````
