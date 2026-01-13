````markdown
# Create two environments from one JPS in different regions

```json
{
	"type": "install",
	"application": {
		"name": "2Envs",
		"env": {
			"topology": {
				"engine": "php5.3",
				"region": "default_hn_group",
				"nodes": [{
						"cloudlets": 16,
						"nodeType": "nginxphp"
					}
				]
			}
		},
		"onInstall": {
			"executeScript": {
				"type": "javascript",
				"script": "https://download.jelastic.com/public.php?service=files&t=169362776e246cbf756eb7aad325f676&download"
			}
		}
	}
}
```
````
