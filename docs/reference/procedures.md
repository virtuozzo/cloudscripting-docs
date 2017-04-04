# Procedures

The declarative code inside a manifest can be divided into a separate blocks, named procedures. Afterwards, the particular procedures can be run by means of appealing to Call actions with different parameters.
 
## Procedure Placeholders 
In order to access any required data or parameters of allocated resources inside the manifest, a special set of placeholders should be used. Sent to the Call method parameters are transformed in a separate kit of placeholders, that can be received inside the appropriate procedure with the help of ${this} namespace. Access to the nodes inside environment can be performed according to the node’s type, as well as according to its role in an environment.

## Examples

<h3>Code Reuse</h3>

Output `Hello World!` two times in `greeting.txt`:  
``` json
{
  "type": "update",
  "name": "Procedures Example",
  "onInstall": [
    {
      "createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
    },
    {
      "call": [
        "greeting",
        "greeting"
      ]
    }
  ],
  "actions": {
    "greeting": {
      "appendFile": [
        {
          "nodeGroup": "cp",
          "path": "${SERVER_WEBROOT}/greeting.txt",
          "body": "Hello World!"
        }
      ]
    }
  }
}
```

<h3>Call procedure with parameters</h3>

Write `Hello World!` and output first and second compute node IP address 
``` json
{
	"type": "update",
	"name": "Procedures Example",
	"onInstall": [{
		"createFile [cp]": "${SERVER_WEBROOT}/greeting.txt"
	}, {
		"call": [
			"greeting",
			"greeting", {
				"log": {
					"message": "${nodes.cp[0].address}"
				}
			}, {
				"log": {
					"message": "${nodes.cp[1].address}"
				}
			}
		]
	}],
	"actions": {
		"greeting": {
			"appendFile": [{
				"nodeGroup": "cp",
				"path": "${SERVER_WEBROOT}/greeting.txt",
				"body": "Hello World!"
			}]
		},
		"log": {
			"appendFile": [{
				"nodeGroup": "cp",
				"path": "${SERVER_WEBROOT}/greeting.txt",
				"body": "${this.message}"
			}]
		}
	}
}
```


