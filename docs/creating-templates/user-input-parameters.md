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

where   
- `prepopulate` <b>[optional]</b> - link to the script, that will fetch the default fields values  
- `fields`   
    - `showIf` - show/hide field by condition (is applicable only to the radio-fieldset field)   
    - `type` <b>[optional]</b> - input field type. The default value is “string”. Possible values:   
        * `string`     
        * `text`                                                                              
        * `list`  
        * `checkbox`  
        * `checkboxlist`  
        * `radiolist`   
        * `radio-fieldset`  
        * `dockertags`        
        * `compositefield` 
        * `slider`  
        * `envlist`   
        * `popupselector`  
        * `popup-selector`  
        * `displayfield`  
        * `spinner`  
        * `numberpicker`  
        * `number-picker`  
        * `host-picher`  
        * `hostpicker`  
        * `toggle`  
        * `spacer`  
    - `inputType` *[optional]* - type attribute of the input field (e.g. radio, text, password, file, etc.).The default value is "text". More info [here](https://www.w3.org/wiki/HTML/Elements/input#Point)        
    - `name` - input field name that could be used to get a parameter value through the `${settings.your_input_name}` placeholder within scripts or manifests.   
    - `default` *[optional]* - default value for the input field  
    - `caption` *[optional]* - field label  
    - `placeholder` *[optional]* -  text that describes the expected value of an input field  
    - `required` *[optional]* possible values are "true" & "false". If left empty, the default value is "true".  
    - `regex` *[optional]* - constructor for testing the JavaScript RegExp object, that refers to the stated the field value, during validation. If test fails, the field will be marked invalid using regexText. The default value is "null"  
    - `regexText` *[optional]* - displays error message in case of the regex test failure during validation. The default value is ' ' (blank space)     
    - `vtype` *[optional]* - A validation type name. Possible values:  
        - `alpha` - The keystroke filter mask applied to alpha input. The default value is: /[a-z_]/i  
        - `alphanum` - The keystroke filter mask applied to alphanumeric input. The default value is: /[a-z0-9_]/i  
        - `email` - The keystroke filter mask applied to email input. See the email method for information about more complex email validation. The default value iso: /[a-z0-9_.-+\'@]/i. See the [appropriate method](http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.VTypes-method-email) for more information about complex email validation  
        - `url` - The keystroke filter mask applied to URL input.                        
    - `vtypeText` *[optional]* - custom error message to be displayed instead of the default one, provided by vtype for this field. The default value is ' ' (blank space).     
    
!!! note
    > `vtypeText` is applied only in case the vtype value is set; otherwise, it is ignored.  

##Target Nodes
`Target Nodes` is a optional section where environments can be defined or disable for JPS installation. `TargetNodes` are available only for `JpsType` *update*.   
Filtering for `targetNodes` is by `nodeType`, `nodeGroup`, `dockerOs`, `dockerName` or `dockerTag`.   
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
There are two input type available:  
```
"nodeType": ["..."]  //set all nodeTypes in array
and
"nodeType": "..., ..."    //set all nodeTypes via commas
```

For example, there are three environments with different topologies:  
![targetNodes](/img/targetNodes.jpg)  
`targetNodes` can filtered JPS installation with example below:
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
In this case the filter result will be the next:
![targetNodesFilter](/img/targetNodesFilter.jpg)
  
##Custom buttons
The custom buttons functionality is intended for planks within Add-ons section. It can be accessed upon clicking the same-named button next to the required node:  
![traffic-manager](/img/traffic-manager.jpg)    
Such buttons execute operations that are predefined within JPS manifest.

Add-ons tab button here:
![addon tab](/img/add-on_tab.jpg)

!!! note
    > JPS manifest should the [`targetNodes`](http://docs.cloudscripting.com/creating-templates/user-input-parameters/#target-nodes) field in order to be displayed within the add-ons section after installation. Otherwise, it will be hidden.  

<b>Template</b>
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
![confirm](/img/confirm.jpg)      
- `loadingText` *[optional]* - UI text to be displayed during loading and applying changes. The default value i *"Applying..."*.    
![loadingText](/img/loadingText.jpg)      
- `procedure` *[required] [string]* - name of the procedure that will be executed. Procedure body structure is described in the [*procedure* section](/reference/procedures/).   
- `caption` - title of a button.  
![caption](/img/caption.jpg)   
- `successText` -  message, that appears once action is successfully performed  
![successText](/img/successText.jpg)     
- `href` *[optional]* - external link that is opened in new browser tab; is considered only if the settings field is absent. In this case procedure will not be executed  
- `settings` - custom form ID. The default is "main". For more details see [custom settings section](/creating-templates/user-input-parameters/#custom-settings)      

The next parameters can be enabled only when the `settings` field is present:
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
where    
- `title` - custom dialog title. If absent, than `caption` will be applied.    
- `submitButtonText` - text for submission button in the opened dialog. The default value is *Apply*   
![submitButtonText](/img/submitButtonText.jpg)  
- `logsPath` - button for showing logs in the defined path  
![logsPath](/img/logsPath.jpg)  
- `logsNodeGroup` - [nodeGroup](/reference/container-types/#containers-by-groups-nodegroup) layer the logging path is opened for      

##Custom Menus    
Menu is an expandable list within the add-ons section comprising custom actions, that execute corresponding operations  
![menu](/img/menu.jpg)     
Menu list contains the Uninstall option by default. Listed actions execute the operations from [application lavel](/reference/events/#application-level-events) if there are any. Custom menus use the same properties as [custom buttons](/creating-templates/user-input-parameters/#custom-buttons).    

##Custom Settings
The settings section can include a few custom forms. The default settings form ID is - *main*.   
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
Here, the main settings form appears during installation process.   
![settingMain](/img/settingsMain.jpg)   
The config settings form appears after clicking the <b>Configure</b> button within the add-ons section.   
![settingCustom](/img/settingsCustom.jpg)     


##Supported Fields:
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
where  
- `caption` *[optional]* - field label.  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *false*.  
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
where   
- `caption` *[optional]* - field label .  
- `hideLabel`*[optional] [boolean]* - hide field Label. Optional. Default *false*.  
###list   
The drop-down list and a single-line non editable textbox.  
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
where      
- `caption` *[optional]* - field Label.  
- `values` - object's values ("key":"value").  
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *false*.  
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
where  
- `caption` *[optional]* - field label.    
- `value` - enables or disables checkbox.  
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *false*.  
###checkboxlist   
The `checkbox` groupping.  
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
where     
- `caption` *[optional]* - field Label.    
- `values` - checkboxes ("key":"value")  
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *false*.  
###radiolist   
The `radio` elements groupping.  
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
where  
- `caption` *[optional]* - field Label.   
- `values` - checkboxes ("key":"value")  
- `hideLabel` - shows/hides field label. The default value is *false*.  
###radio-fieldset   
Groupping `radio` elements with available function `showIf`.    
`hideLabel` is true always.  
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
- `name` - required field  at `radio-fieldset` element. Non required at other elements.   
- `default` *[optional]* - enabled field when form has opened.  
- `values` - checkboxes ("key":"value")  
- `showIf` - conditions object for showing predefined elements by clicking to `radio-fieldset` elemets. Predefined elemets can be different.  
- `hideLabel` - boolean, hide field Label (optional). Default *false*.  
- `caption` *[optional]* - field Label.  
###dockertag   
Show docker tags in `list` element.  
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
- `name` - 'tag' value. Required.  
- `values` - docker tags values. `name` is required. By default docker image will be pulled from Docker® Hub registry.  
- `dockerImage` - docker image name. Name is required.   
- `registry`, `username`, `password` are optional.  
- `env` - required object. It can be empty.  
###compositefield
`Compositefield` is a container that has specific functionality and structural components that make it the block for application-oriented custom user interfaces.  
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
- `pack` - controls how items packed together. Default - *start*. Available options are: *center*, *end*. Optional.  
- `align` - controls how items are aligned. Default - top. Available options are: *middle*, *stretch*, *stretchmax*. Optional.  
- `defaultMargins` - default margins for each item. Default is 0. Optional.  
- `defaultPadding` - sets paddings for all items. Default is 0. Optional.  
- `defaultFlex` - each item will be flexed horizontally according to each item's. Optional.  
- `items` - elements object  
###slider
Slider element as a form field.
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
- `min` - min slader value  
- `max` - max slider value  
- `useTips` - display tips for the value. Default to true.  
- `caption` - field Label caption. Optional.   
- `name` - field name. Optional.  
###envlist
Account environments list in drop-down element.  
![envlist](/img/envlist.jpg)  
```
{
  "fields": [
    {
      "caption": "Envlist",
      "editable": true,
      "valueField": "1",
      "type": "envlist",
      "name": "envlist"
    }
  ]
}
```
- `caption` - field Label caption. Optional.  
- `name` - field name. Optional.  
- `editable` - boolean. Enable editing `envlist` field. Default *false*. Optional.  
- `valueField` - Optional.  
###popupselector
(`popup-selector` an alias)     
Opening popup window via POST request to any external service.   
Functionality provides an opportunity to pass additional parameters.  
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
- `caption` - field Label caption. Optional.  
- `name` - field name. Optional.  
- `buttonText` - button label text. Optional  
- `url` - external source url. Optional. Default - Jelastic platform url.  
- `popupWidth` - width size in pixels. Optional  
- `popupHeight` - height zise. Optional  
- `popupCallbackEvent` - event handler  
- `params` - parameters for send in POST request to `url` source.  
###displayfield
(`spacer` an alias)   
A display-only text field which is not validated and not submitted.  
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
- `caption` - field Label caption. Optional.
- `name` - field name. Optional.
- `markup` - a value to initialize this field with (defaults to undefined).
###spinner
Enhance a text input for entering numeric values, with up/down buttons and arrow key handling.
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
- `name` - field name. Optional.  
- `caption` - field Label caption. Optional.  
- `min` - minimal spinner value  
- `max` - max spinner value  
- `increment` - increment value  
- `decimanPrecision` - precision value  
###numberpicker
(`number-picker` an alias)  
Textfield with number validation in a range.  
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
- `name` - field name. Optional.  
- `caption` - field Label caption. Optional.  
- `min` - minimal spinner value  
- `max` - max spinner value  
- `editable` - boolean. Enable editing `numberpicker` field. Default *false*. Optional.  
###hostpicker
(host-pickeran alias)  
Drop-down menu with environments hosts.  
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
- `name` - field name. Optional.
- `caption` - field Label caption. Optional.
- `editable` - boolean. Enable editing `envlist` field. Default *false*. Optional.
- `valueField` - Optional.
###toggle
Toggle element is a switch between two values
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
- `name` - field name. Optional.  
- `caption` - field Label caption. Optional.  
- `value` - enabling/disabling toggle value. Default is *false*  