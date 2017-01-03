# Getting User Input

```
{
  "jpsType": "update",
  "application": {
    "settings": {
      "prepopulate": "URL",
      "fields": [{
        "showIf": "object",

        "type": "string",
        "inputType" : "string",
        "name": "string",
        "default": "string or localization object",
        "caption": "string or localization object",
        "placeholder": "string or localization object",
        "required": "boolean",
        "vtype": "string",
        "vtypeText" : "string or localization object", 
        "regex" : "string for RegExp constructor",
        "regexText" : "string or localization object", 

        "hideLabel": "boolean",
        "id": "string",
        "cls": "string",
        "itemId": "string"
      }]
    }
  }
}
```   
where:

- `prepopulate` *[optional]* - link to the script, that will fetch the default fields values  
- `fields` - an array of fields which will be displayed in custom form     
    - `showIf` - show/hide field by condition (is applicable only to the *radio-fieldset* field)   
    - `type` *[optional]* - input field type. The default value is *“string”*. Possible values:   
        * `string` - the basic [text field](/creating-templates/user-input-parameters/#string).      
        * `text`  - Multiline [`string` field](/creating-templates/user-input-parameters/#text).                                                                             
        * `list` - drop-dowm menu with non-editable textboxes. More info with example is [here](/creating-templates/user-input-parameters/#list). 
        * `checkbox` - simgle checkbox field. More info [here.](/creating-templates/user-input-parameters/#checkbox) 
        * `checkboxlist` - [the checkbox grouping](/creating-templates/user-input-parameters/#checkboxlist) 
        * `radiolist` - [the radio field grouping](/creating-templates/user-input-parameters/#radiolist)    
        * `radio-fieldset` - an alias to `radiolist`  
        * `dockertags` drop-down menu with list of docker tags. [More info.](/creating-templates/user-input-parameters/#dockertag)        
        * `compositefield` - a component with any available fields in it. [More info](/creating-templates/user-input-parameters/#compositefield)  
        * `slider` - the slider element as a form field. [More info](/creating-templates/user-input-parameters/#slider)  
        * `envlist` - [the account environments list](/creating-templates/user-input-parameters/#envlist)   
        * `popupselector` - new popup window via POST request. Posibility to pass additional parameters. [More info](/creating-templates/user-input-parameters/#popupselector)      
        * `popup-selector` - an alias for `popupselector` 
        * `displayfield` - text field intended for displaying text. [More info.](/creating-templates/user-input-parameters/#displayfield) 
        * `spacer` - an alias for `displayfield`   
        * `spinner` - input field for entering numeric values. [More info](/creating-templates/user-input-parameters/#spinner)  
        * `numberpicker` - text field within number validation within range. [More info](/creating-templates/user-input-parameters/#numberpicker)  
        * `number-picker` - an alias for `numberpicker`  
        * `hostpicker` - the drop-doown menu with environment hosts. [More info](/creating-templates/user-input-parameters/#hostpicker)  
        * `host-picher` - an alias for `hostpicker`   
        * `toggle` - the switcher between two values. [More info](/creating-templates/user-input-parameters/#toggle) 
    - `inputType` *[optional]* - type attribute of the input field (e.g. *radio*, *text*, *password*, *file*, etc.). The default value is *"text"*. More info [here](https://www.w3.org/wiki/HTML/Elements/input#Point).        
    - `name` - input field name, that could be used to get a parameter value through the `${settings.your_input_name}` placeholder within scripts or manifests   
    - `default` *[optional]* - default value for the input field  
    - `caption` *[optional]* - field label  
    - `placeholder` *[optional]* -  text, that describes the expected value of the input field  
    - `required` *[optional]* - possible values are *"true"* & *"false"*. If left empty, the default value is *"true"*.  
    - `regex` *[optional]* - constructor for testing the JavaScript RegExp object, that refers to the stated the field value, during validation. If test fails, the field will be marked invalid using *regexText*. The default value is *"null"*.                                                        
    - `regexText` *[optional]* - displays error message in case of the *regex* test failure during validation. The default value is *' '* (blank space).     
    - `vtype` *[optional]* - validation type name. Possible values:      
        - `alpha` - keystroke filter mask applied to alpha input. The default value is *"/[a-z_]/i"*.  
        - `alphanum` - keystroke filter mask applied to alphanumeric input. The default value is *"/[a-z0-9_]/i"*.  
        - `email` - keystroke filter mask applied to email input. The default value is *"/[a-z0-9_.-+\'@]/i"*. See the [appropriate method](http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.VTypes-method-email) for more information about complex email validation.  
        - `URL` - keystroke filter mask applied to URL input                        
    - `vtypeText` *[optional]* - custom error message to be displayed instead of the default one, provided by *vtype* for this field. The default value is *' '* (blank space).     
    
!!! note
    > `vtypeText` is applied only in case the *vtype* value is set; otherwise, it is ignored.  

##Target Nodes
`Target Nodes` is an optional method which allows to define environments, that are suitable for JPS installation. Herewith, this option is available only for *JpsType*: *update* procedure.   

Filtering for `targetNodes` can be performed by `nodeType`, `nodeGroup`, `dockerOs`, `dockerName` or `dockerTag`.   
```
{
	"jpsType": "update",
	"application": {
		"name": "targetNodes",
		"env": {},
		"targetNodes": {
			"nodeType": ["..."],
			"nodeGroup": ["..."],
			"dockerOs": ["..."],
			"dockerName": ["..."],
			"dockerTag": ["..."]
		},
		"onInstall": {
			"createFile": {
				"nodeGroup": "cp",
				"path": "/tmp/newFile"
			}
		}
	}
}
```
There are two possible ways to define a nodeType:  
```
"nodeType": ["..."] - to set the required nodeTypes in array

"nodeType": "..., ..." - to set the required nodeTypes being separated with commas
```
<b>Example</b> 

Let’s suppose you have three environments with different topology:     

![targetNodes](/img/targetNodes.jpg)  

Within these environments, the `targetNodes` filtering for JPS installation can be performed with the next example:
```
{
	"jpsType": "update",
	"application": {
		"name": "targetNodes",
		"env": {},
		"targetNodes": {
			"nodeType": "nginx, mysql5"
		},
		"onInstall": {
			"createFile": {
				"nodeGroup": "cp",
				"path": "/tmp/newFile"
			}
		}
	}
}
```
In this case, the filtering result will be the following:   

![TargetNodesFilter](/img/TargetNodesFilter.jpg)
  
##Custom Buttons
The custom buttons settings are intended for extending and adjusting functionality of planks within <b>Add-ons</b> section. It can be accessed upon clicking the same-named button next to the required node:      

![Addontab](/img/Addontab.jpg)    

Such buttons execute operations that are predefined within JPS manifest.   

![TrafficManager](/img/TrafficManager.jpg)

!!! note
    > JPS manifest should include the [*targetNodes*](http://docs.cloudscripting.com/creating-templates/user-input-parameters/#target-nodes) field in order to be displayed within the Add-ons section after installation. Otherwise, it will be hidden.  

<b>Templates</b>   

Sample to set buttons within add-on plank:
```
{
  "jpsType": "update",
  "application": {
    "name": "Custom buttons",
    "env": {},
    "targetNodes": {
      "nodeGroup": "bl"
    },
    "procedures": ["..."],
    "buttons": [
      {
        "confirmText": "Custom confirm text",
        "loadingText": "Load text while waiting",
        "procedure": "{String}",
        "caption": "Configure",
        "successText": "Configuration saved successfully!",
        "href": "http://google.com"
      }
    ]
  }
}
```
Here: 

- `buttons` - button parameters array   
- `confirmText` *[optional]* - custom confirmation text for users. The default value is *"Are you sure?"*.   

It will be displayed after clicking on the appropriate button for an add-on. According to the code above, the text will be:  

![Confirm](/img/Confirm.jpg)      

- `loadingText` *[optional]* - UI text to be displayed during loading and applying changes. The default value is *"Applying..."*.    

![LoadingText](/img/LoadingText.jpg)      

- `procedure` *[required] [string]* - name of the procedure that will be executed. Procedure body structure is described in the [*procedure*](/reference/procedures/) section.        
- `caption` - title of the button  

![Caption](/img/Caption.jpg)   

- `successText` -  message, that appears once action is successfully performed  

![SuccessText](/img/SuccessText.jpg)     

- `href` *[optional]* - external link that is opened in a new browser tab; is considered only if the *settings* field is absent. In this case *procedure* will not be executed.      
- `settings` - custom form ID. The default is *"main"*. For more details see [*custom settings*](/creating-templates/user-input-parameters/#custom-settings) section.                  

Another sample with additional configurations: the next parameters can be enabled only if the `settings` field is present:
```
{
  "jpsType": "update",
  "application": {
    "name": "Custom buttons",
    "env": {},
    "targetNodes": {
      "nodeGroup": "bl"
    },
    "procedures": [
      "..."
    ],
    "buttons": [
      {
        "confirmText": "Custom confirm text",
        "loadingText": "Load text while waiting",
        "procedure": "{String}",
        "caption": "Configure",
        "successText": "Configuration saved successfully!",
        "settings": "config",
        "title": "Title",
        "submitButtonText": "Button Text",
        "logsPath": "/var/log/add-on-action.log",
        "logsNodeGroup": "cp"
      }
    ]
  }
}
```
where:

- `title` - custom dialog title. If absent, than `caption` will be applied.    
- `submitButtonText` - text for submission button in the opened dialog. The default value is *"Apply"*.   

![SubmitButtonText](/img/SubmitButtonText.jpg)  

- `logsPath` - button for showing logs in the defined path  

![LogsPath](/img/LogsPath.jpg)  

- `logsNodeGroup` - [nodeGroup](/reference/container-types/#containers-by-groups-nodegroup) layer the logging path should be opened for      

##Custom Menus    
Menu is an expandable list within the <b>Add-ons</b> section comprising custom actions, that execute corresponding operations.  

![menu](/img/menu.jpg)     

Menu list contains the <b>Uninstall</b> option by default. Listed actions execute the operations from [application level](/reference/events/#application-level-events) if there are any. Custom menus use the same properties as [custom buttons](/creating-templates/user-input-parameters/#custom-buttons).    

##Custom Settings
The settings section can include a few custom forms. The default settings form ID is *"main"*.    

For instance:  
```
{
  "jpsType": "update",
  "application": {
    "name": "Custom buttons",
    "env": {},
    "targetNodes": {
      "nodeGroup": "bl"
    },
    "procedures": [
      "..."
    ],
    "settings": {
      "main": {
        "fields": [
          {
            "type": "text",
            "caption": "Main form"
          }
        ]
      },
      "config": {
        "fields": [
          {
            "type": "text",
            "caption": "Custom form from button action"
          }
        ]
      }
    },
    "buttons": [
      {
        "settings": "config",
        "procedure": "customProc",
        "caption": "Configure",
        "submitButtonText": "Button Text",
        "logsPath": "/var/lib/jelastic/keys/111"
      }
    ]
  }
}
```
Here, the *main settings* form appears during installation process.   

![settingMain](/img/SettingsMain.jpg)   

The *config settings* form appears after clicking the <b>Configure</b> button within the add-ons section.   

![settingCustom](/img/SettingsCustom.jpg)     

##Supported Fields
###string     
The basic text field.  

![string](/img/string.jpg)  
```
{
  "fields": [
    {
      "hideLabel": false,
      "type": "string",
      "caption": "String",
      "name": "customString"
    }
  ]
}
```
where:  
- `caption` *[optional]* - field label  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  
###text   
The multiline text field.

![text](/img/text.jpg)  
```
{
  "fields": [
    {
      "type": "text",
      "caption": "Text",
      "hideLabel": false
    }
  ]
}
```
where:   
- `caption` *[optional]* - field label  
- `hideLabel`*[optional] [boolean]* - hide field Label. The default value is *'false'*.  
###list   
The drop-down list and a single-line non-editable textbox.  

![list](/img/list.jpg)  
```
{
  "fields": [
    {
      "type": "list",
      "caption": "List",
      "values": {
        "value1": "hello",
        "value2": "world"
      },
      "hideLabel": false
    }
  ]
}
```
where:      
- `caption` *[optional]* - field label                                  
- `values` - objects' values (*"key"*:*"value"*)                            
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.          
###checkbox   
The single checkbox field.

![text](/img/checkbox.jpg)  
```
{
  "fields": [
    {
      "type": "checkbox",
      "caption": "Checkbox",
      "value": true,
      "hideLabel": false
    }
  ]
}
```
where:  
- `caption` *[optional]* - field label           
- `value` - enables or disables checkbox                         
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *'false'*.                      
###checkboxlist   
The *checkbox* grouping.  

![text](/img/checkboxlist.jpg)  
```
{
  "fields": [
    {
      "type": "checkboxlist",
      "caption": "Checkbox List",
      "values": {
        "value1": "hello",
        "value2": "world"
      },
      "hideLabel": false
    }
  ]
}
```
where:     
- `caption` *[optional]* - field label  
- `values` - checkboxes (*"key"*:*"value"*)  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  
###radiolist   
The *radio* elements grouping.  

![text](/img/radiolist.jpg)  
```
{
  "fields": [
    {
      "type": "radiolist",
      "caption": "Radio List",
      "values": {
        "value1": "hello",
        "value2": "world"
      },
      "hideLabel": false
    }
  ]
}
```
where:  
- `caption` *[optional]* - field label   
- `values` - checkboxes (*"key"*:*"value"*)  
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *'false'*.  
###radio-fieldset    
The groupping of the *radio* elements with the `showIf` function.     

!!! note
    The *hideLabel* boolean value is always *true* for this field   

![text](/img/radio-fieldset.jpg)   
```
{
  "fields": [
    {
      "type": "radio-fieldset",
      "name": "customName",
      "default": "1",
      "values": {
        "1": "hello",
        "2": "world"
      },
      "showIf": {
        "1": [
          {
            "hideLabel": false,
            "type": "string",
            "caption": "First String",
            "name": "first"
          }
        ],
        "2": [
          {
            "hideLabel": false,
            "type": "string",
            "caption": "Second String",
            "name": "second"
          }
        ]
      }
    }
  ]
}
```
where:   
- `name` *[required]* - name of the `radio-fieldset` element (for other elements it’s not required)                       
- `default` *[optional]* - selected field upon opening the form  
- `values` - checkboxes (*"key"*:*"value"*)  
- `showIf` - conditional object that shows predefined elements by clicking on the `radio-fieldset` elements. Predefined elements can be vary.  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  
- `caption` *[optional]* - field label
###dockertag   
Displaying Docker tags within the `list` element.  

![text](/img/dockertag.jpg)  
```
{
  "name": "Cloud Scripting",
  "settings": {
    "fields": [
      {
        "type": "dockertags",
        "name": "tag",
        "values": [
          {
            "name": "latest"
          },
          {
            "name": "first"
          }
        ]
      }
    ]
  },
  "dockerImage": {
    "name": "sych74/pokemongo-map",
    "registry": "",
    "username": "",
    "password": ""
  },
  "env": {}
}
```
where:   
- `name` *[required]* - should have the *'tag'* value  
- `values` *[required]* - Docker tag values (*name*: *"tag_name"* is required). By default Docker image is pulled from the Docker Hub registry.  
- `dockerImage` - Docker image details   
   - `name`: *repository* is required   
   - `registry`, `username`, `password` are optional   
- `env` - required object (can be empty)  
###compositefield
The `compositefield` is a container with specific functionality and structural components that constitute it as the block for application-oriented custom user interfaces.  

![compositefield](/img/compositefield.jpg)  
```
{
  "fields": [
    {
      "pack": "",
      "align": "",
      "defaultMargins": {
        "top": 0,
        "right": 0,
        "bottom": 0,
        "left": 10
      },
      "defaultPadding": "0",
      "defaultFlex": "",
      "caption": "Compositefield",
      "type": "compositefield",
      "name": "compositefield",
      "items": [
        {
          "name": "checkbox",
          "value": true,
          "type": "checkbox"
        },
        {
          "width": "50px",
          "name": "first",
          "type": "string"
        },
        {
          "width": "100px",
          "name": "latest",
          "type": "string"
        }
      ]
    }
  ]
}
```
where:   
- `pack` *[optional]* - manages the way items are packed together. The default value is *'start'*. Possible values: *'start'*, *'center'* and *'end'*.  
- `align` *[optional]* - manages the way items are aligned. The default value is *'top'*. Possible values: *'top'*, *'middle'*, *'stretch'*, *'stretchmax'*.  
- `defaultMargins` *[optional]* - default margins for items. The default value is *'0'*.  
- `defaultPadding` *[optional]* - default paddings for items. The default value is *'0'*.  
- `defaultFlex` *[optional]* - horizontal flex for items.   
- `items` - elements  
###slider
The slider element as a form field.

![slider](/img/slider.jpg)
```
{
  "fields": [
    {
      "min": "0",
      "max": "10",
      "increment": 1,
      "useTips": true,
      "caption": "Slider",
      "type": "slider",
      "name": "slider"
    }
  ]
}
```
where:   
- `min` - minimum slider value  
- `max` - maximum slider value  
- `useTips` - displaying tips for the value. The default value is *'true'*.  
- `caption` *[optional]* - field label  
- `name` *[optional]* - name of the field    
###envlist
The account environments list within a drop-down element.  

![envlist](/img/envlist.jpg)  
```
{
  "fields": [
    {
      "caption": "Envlist",
      "editable": true,
      "valueField": "appid",
      "type": "envlist",
      "name": "envlist"
    }
  ]
}
```
where:  

- `caption` *[optional]* - field label    
- `name` *[optional]* - name of the field  
- `editable` *[optional][boolean]* - enables/disables the `envlist` field editing. The default value is *'false'*.    
- `valueField` *[optional][string]* - The value from environment information which will be sent to server. The default value is **domain**. Available values are:    
    - **iconCls** - css class     
    - **isRunning** - check if environment status is *running*  
    - **shortdomain** - short environment domain name (without platform URL)  
    - **displayName** - environment *displayName*  
    - **appid** - unique environment id     
###popupselector
(`popup-selector` is an alias)     

Opens popup window via the POST request to any external service. Functionality provides the possibility to pass additional parameters.  

![popupselector](/img/popupselector.jpg)  
```
{
  "fields": [
    {
      "caption": "Popupselector",
      "type": "popupselector",
      "name": "popupselector",
      "buttonText": "Open",
      "url": "http://{external url}",
      "popupWidth": "300px",
      "popupHeight": "300px",
      "popupCallbackEvent": "handler",
      "params": {
        "first": 1,
        "second": 2
      }
    }
  ]
}
```
where:  
- `caption` *[optional]* - field label                      
- `name` *[optional]* - name of the field                  
- `buttonText` *[optional]* - button label              
- `url` *[optional]* - external source URL. The default link is to the Jelastic platform.         
- `popupWidth` *[optional]* - width in pixels          
- `popupHeight` *[optional]* - height in pixels   
- `popupCallbackEvent` - event handler   
- `params` - parameters for sending in POST request to `URL` source.     
###displayfield
(`spacer` is an alias)    

The text field intended only for display, which is not validated and not submitted.  

![displayfield](/img/displayfield.jpg)  
```
{
  "fields": [
    {
      "caption": "Displayfield",
      "type": "displayfield",
      "name": "displayfield",
      "markup": "display"
    }
  ]
}
```
where:  
- `caption` *[optional]* - field label                   
- `name` *[optional]* - name of the field                
- `markup` - value to initialize the field's display. The default value is "*'undefined'*".                 
###spinner
Enhanced input field for entering numeric values, with up/down buttons and arrow keys handling.  

![spinner](/img/spinner.jpg)  
```
{
  "fields": [
    {
      "type": "spinner",
      "name": "spinner",
      "caption": "Spinner",
      "min": 1,
      "max": 10,
      "increment": 2,
      "decimanPrecision": ""
    }
  ]
}
```
where:  
- `name` *[optional]* - name of the field  
- `caption` *[optional]* - field label  
- `min` - minimum spinner value  
- `max` - maximum spinner value  
- `increment` - increment value  
- `decimanPrecision` - precision value  
###numberpicker
(`number-picker` is an alias)  

The text field with a number validation within range.   

![numberpicker](/img/numberpicker.jpg)  
```
{
  "fields": [
    {
      "type": "numberpicker",
      "name": "numberpicker",
      "caption": "Numberpicker",
      "min": 3,
      "max": 10,
      "editable": true
    }
  ]
}
```
where:  
- `name` *[optional]* - name of the field  
- `caption` *[optional]* - field label    
- `min` - minimum spinner value  
- `max` - maximum spinner value  
- `editable` *[optional] [boolean]* - enables/disables editing the `numberpicker` field. The default value is *'false'*.  
###hostpicker
(`host-picker` is an alias)  

The drop-down menu with the environments hosts.  

![hostpicker](/img/hostpicker.jpg)  
```
{
  "fields": [
    {
      "type": "hostpicker",
      "name": "hostpicker",
      "caption": "Hostpicker",
      "editable": true,
      "valueField": "host"
    }
  ]
}
```
where:  
- `name` *[optional]* - name of the field   
- `caption` *[optional]* - field label   
- `editable` *[optional] [boolean]* - enables/disables editing the `envlist` field. The default value is *'false'*.  
- `valueField` *[optional]*   
###toggle
The toggle element is a switch between two values.

![toggle](/img/toggle.jpg)
```
{
  "fields": [
    {
      "type": "toggle",
      "name": "toggle",
      "caption": "Toggle",
      "value": true
    }
  ]
}
```
where:  
- `name` *[optional]* - name of the field  
- `caption` *[optional]* - field label    
- `value` *[boolean]* - enables/disables toggle value. The default value is *'false'*.   