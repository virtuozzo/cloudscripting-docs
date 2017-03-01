#Handling Custom Errors

The Cloud Scripting engine provides functionality to handle custom errors. These possible errors should be described within a separate `errorHandlers` block. The errors handling is related to the action result codes. You can locate these codes within the <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Jelastic Console Log Panel</a> upon a corresponding action execution. Therefore, you can predefine a message text that will be displayed in case of an error occurrence.         

There is a number of predefined pop-up windows, which emerge while custom errors are being handled:  

- `info` - *information* pop-up window                

<center>![SuccessText](/img/SuccessText.jpg)</center>          

- `warning` - *warning* pop-up window with a custom message                
 
<center>![warningType](/img/warningType.jpg)</center>        

- `error` - *error* pop-up window          

<center>![errorType](/img/errorType.jpg)</center>          

- `success` - *success* window when the action will be executed with expected result code. This code can be described in `responses` block

<center>![success](/img/successResponse.jpg)</center>

The result message text can be localized according to the languages, available within the Jelastic Platform:

``` json
{
  "type": "warning",
  "message": {
    "en": "Localized text",
    "es": "Texto localizado"
  }
}
```

##Examples

**File creation error**

The example below describes a creation of the same file twice and handling an error, which occurs as a result of such action execution. Consequently, the result code of this error will be defined as *4036*.           

``` json
{
  "type": "update",
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

- `createFile` - predefined within the Cloud Scripting <a href="http://docs.cloudscripting.com/reference/actions/#createfile" target="_blank">action</a>              
- `errorHandlers` - object (array) to describe custom errors     
- `type` - type of a pop-up window, emerging upon the error occurrence. The available values are: *error*, *warning*, *info*.       

Thus, the example above sets all the actions with *4036* result to be displayed via *error* pop-up window with a custom error message text.      

The additional functionality is provided to display action errors using <a href="http://docs.cloudscripting.com/reference/actions" target="_blank">*return*</a> action.                         

``` json
{
  "type": "update",
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

- `script` - Cloud Scripting <a href= "/reference/actions/#script" target="__blank">action</a> for executing *Javascript* or *Java* code (*Javascript* is set by default)                     
- `1000` - custom predefined result code for error handling. It will be returned from the `script` action in the `onInstall` block.        

If the result code is delivered via *string*, then the default result code is *11039*. Therefore, `errorHandlers` can be handled by the following outcoming *string* text:            

``` json
{
	"type": "update",
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

In all the other cases, i.e. when a custom error is not predefined within the `errorHandler` block, the default pop-up window type is *error* with an output message.          
