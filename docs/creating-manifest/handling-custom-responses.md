##Handling Custom Responses

The Cloud Scripting engine provides functionality to handle custom responses. The responses handling is related to the action result codes. You can locate these codes within the <a href="/troubleshooting/" target="_blank">Jelastic Console Log Panel</a> upon a corresponding action execution. Therefore, you can predefine a message text that will be displayed in case of an error occurrence.         

There are a types of predefined pop-up windows, which emerge while custom responses are being handled:  

- `info` - *information* pop-up window                

<center>![SuccessText](/img/SuccessText.jpg)</center>          

- `warning` - *warning* pop-up window with a custom message                
 
<center>![new-warning](/img/new-warning.png)</center>        

- `error` - *error* pop-up window          

<center>![new-error](/img/new-error.png)</center>          

The text of the messages in these windows can be localized according to the languages that are available within the Jelastic Platform.                
- `success` - *success* window when the action will be executed with expected result code. The manifest installation will be finished immediately if an any action will return the result code from `script` or `return` actions or which is predefined in `responses` block.

<center>![success](/img/successResponse.jpg)</center>

The types `info`, `error` and `warning` are unsuccessful installation results. Therefore, the install process will be marked by red cross like on the screen below:

<center>![success](/img/redCross.jpg)</center>

The simplest custom response message can be returned in one string via actions `return` or `script`. The examples below provide this ability:
 
```json
{
  "type": "update",
  "name": "response handlers",
  "onInstall": {
    "return": "Warning!"
  }
}
```

```json
{
  "type": "update",
  "name": "response handlers",
  "onInstall": {
    "script": "return 'Warning!'"
  }
}
```

In this case the default response `type` is `error` and response `message` is returned string.

There is an ability to return a response with a defined result type and with a custom message via `script` or `return` actions. 
`Return` action: 

```json
{
    "type": "update",
    "name": "response handlers",
    "onInstall": {
        "return": {
          "result": "warning",
          "message": "Warning!",
          "email": "string"
        }
    }
}
```
!!! note
    `email` parameter is available only for `success` response type. This text will be sent after an any action will be finished with **success** response code.

`Script` action:

```json
{
    "type": "update",
    "name": "response handlers",
    "onInstall": {
        "script": "return {result: 'warning', message: 'Warning!','email': 'string'}"
    }
}
```

Parameters `message` and `email` support all <a href="/creating-manifest/placeholders/" target="_blank">available placeholders</a>. Either, they could be uploaded from an any external source via direct link or according to <a href="/creating-manifest/basic-configs/#relative-links">baseUrl ability</a>.  

In case, when is returned a response code with a type `success` two response objects impose one to another. 
But the `success` text from response object has a higher priority than a <a href="/creating-manifest/visual-settings/#success-text-customization" target="_blank">**success**</a> text from main manifest block.    
A examples below display the difference:

```json
{
    "type": "update",
    "name": "response handlers",
    "onInstall": {
        "script": "return {'result': 'success','message': 'Hello!!'}"
    },
    "success": "success!!"
}
```

The result code with `success` type, message - '*Hello!!*' and sent email text - '*success!!*'

```json
{
    "type": "update",
    "name": "response handlers",
    "onInstall": {
        "script": "return {'result': 'success','message': 'Hello!!', 'email': 'Hello!!'}"
    },
    "success": "success!!"
}
```

The result code with `success` type, message - '*Hello!!*' and sent email text - '*Hello!!*'

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

In necessity to display the same response codes a `response` object can be added where a custom responses can be defined. The examples below show how to use it.

<h3>Examples</h3>

**File creation error**

The example below describes a creation of the same file twice and handling an response, which occurs as a result of such action execution. Consequently, the result code of this response will be defined as *4036*.           

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
  "responses": {
    "4036": {
      "type": "error",
      "message": "file path already exists"
    }
  }
}
```

where: 

- `createFile` - predefined within the Cloud Scripting <a href="/creating-manifest/actions/#createfile" target="_blank">action</a>              
- `responses` - object (array) to describe custom responses     
- `type` - type of a pop-up window, emerging upon the response occurrence. The available values are: *error*, *warning*, *info*, *success*.       

Thus, the example above sets all the actions with *4036* result to be displayed via *error* pop-up window with a custom response message text.      

The additional functionality is provided to display action responses using <a href="/creating-manifest/actions" target="_blank">*return*</a> action.                         

``` json
{
  "type": "update",
  "name": "Custom Response Handlers",
  "onInstall": {
    "script": "return {result : 1000};"
  },
  "responses": {
    "1000": {
      "type": "warning",
      "message": "Custom Warning message!"
    }
  }
}
```

where:

- `script` - Cloud Scripting <a href= "/creating-manifest/actions/#script" target="__blank">action</a> for executing *Javascript* or *Java* code (*Javascript* is set by default)                     
- `1000` - custom predefined result code for responses handling. It will be returned from the `script` action in the `onInstall` block.        

If the result code is delivered via *string*, then the default result code is *11039*. Therefore, `responses` can be handled by the following outcoming *string* text:            

``` json
{
	"type": "update",
	"name": "Custom Response Handlers",
	"onInstall": {
		"script": "return 'error'"
	},
	"responses": {
		"error": {
			"type": "info",
			"message": "Custom Warning message!"
		}
	}
}
```

   
In all the other cases, i.e. when a custom response is not predefined within the `responses` block, the default pop-up window type is *error* with an output message.          

A response objects which are returned from custom scripts and predefined in `response` block are emposed one to another. A response object from custom scripts has a higher priority than responses in `response` object.  
For example:
```json
{
  "type": "update",
  "name": "Custom Response Handlers",
  "onInstall": {
    "script": "return {'result': '2308', 'message': 'Success from script with result 2308'}"
  },
  "responses": {
    "2308": {
      "type": "success",
      "message": "Custom Success message!"
    }
  }
}
```

The final success form will be same as on screen below:

<center>![redefinedSuccessResponseHandler](/img/redefinedSuccessResponseHandler.jpg)</center>