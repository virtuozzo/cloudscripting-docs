#Handling Custom Errors

The Cloud Scripting engine provides functionality for handling custom errors. These possible errors should be described in separate block `errorHandlers`.
The handling errors relates to action result codes. These codes can be found at [Jelastic Console Log Panel](/troubleshooting/) after action was executed. 
Therefore, Jelastic customers can predefine possible messages for such errors.

There is a list of predefined popup windows which can be displayed while custom errors are handled:  

- `info` - information type popup   
![SuccessText](/img/SuccessText.jpg)    
- `warning` - warning popup type with custom message  
![warningType](/img/warningType.jpg)
- `error` - error popup type window  
![errorType](/img/errorType.jpg)

Result message text can be localized according to an available languages at Jelastic platform:

```example
{
  "type": "warning",
  "message": {
    "en": "Localized text",
    "es": "Texto localizado"
  }
}
```


##Examples

**File creating error**  
The example below describes a double creating the same file and handling it error. Jelastic defined the result code of such errors - *4036*.

```
{
  "jpsType": "update",
  "name": "Handling File Creation",
  "onInstall": [
    {
      "createFile [cp]": "/tmp/customDirectory"
    },
    {
      "createFile [cp]": "/tmp/customDirectory"
    }
  ],
  "errorHandlers": {
    "4036": {
      "type": "error",
      "message": "file path already exists"
    }
  }
}
```

where: 

- `createFile` - Cloud Scripting predefined [action](reference/actions/#createfile)
- `errorHandlers` - an object (array) of custom descripbed errors.  
- `type` - popup window type after the error has a place. Available values are: *error*, *warning*, *info*.    

Therefore, the example subscribed all actions with result *4036* for displaying error popup menu with custom error message.


An additional ability is provided to display action errors using [`return` action.](reference/actions/#handleErrors)

```
{
  "jpsType": "update",
  "name": "Custom Error Handlers",
  "onInstall": {
    "script": "return {result : 1000};"
  },
  "errorHandlers": {
    "1000": {
      "type": "warning",
      "message": "Custom Warning message!"
    }
  }
}
```

where:

- `script` - Cloud Scripting <a href= "/reference/actions/#script" target="__blank">action</a> for executing javascript or java code. Javascript type script is by default.  
- `1000` - custom predefined result code for handling. It will be returned from `script` action in `onInstall` block.

If the result code is a *string* type when the default result code is *11039*. Therefore, `errorHandlers` can be handling by this outcoming *string* text:
```
{
	"jpsType": "update",
	"name": "Custom Error Handlers",
	"onInstall": {
		"script": "return 'error'"
	},
	"errorHandlers": {
		"error": {
			"type": "info",
			"message": "Custom Warning message!"
		}
	}
}
```

All other cases when custom error is not predefined in the block `errorHandler` the default popup type is `error` with output message in it.
