# Visual Settings

## Supported Fields

``` json
{
  "type": "update",
  "settings": {
    "prepopulate": "URL",
    "fields": [
      {
        "showIf": "object",
        "type": "string",
        "inputType": "string",
        "name": "string",
        "default": "string or localization object",
        "caption": "string or localization object",
        "placeholder": "string or localization object",
        "required": "boolean",
        "vtype": "string",
        "vtypeText": "string or localization object",
        "regex": "string for RegExp constructor",
        "regexText": "string or localization object",
        "hideLabel": "boolean",
        "id": "string",
        "cls": "string",
        "itemId": "string"
      }
    ]
  }
}
```   
where:

- `prepopulate` *[optional]* - link to the script, that will fetch the default fields values  
- `fields` - array of fields that will be displayed in a custom form     
    - `showIf` - shows/hides field by condition (is applicable only to the *radio-fieldset* field)   
    - `type` *[optional]* - input field type. The default value is *'string'*. Possible values:   
        * `string` - [basic](/creating-templates/user-input-parameters/#string) text field                                  
        * `text`  - [multiline](/creating-templates/user-input-parameters/#text) text field                                                                                                         
        * `list` - drop-down menu with [textboxes](/creating-templates/user-input-parameters/#list))                                           
        * `checkbox` - single [checkbox field](/creating-templates/user-input-parameters/#checkbox)                     
        * `checkboxlist` - [checkbox](/creating-templates/user-input-parameters/#checkboxlist) grouping                             
        * `radiolist` - [radio field](/creating-templates/user-input-parameters/#radiolist) grouping                       
        * `radio-fieldset` - alias to `radiolist`              
        * `dockertags` - drop-down menu with a list of [docker tags](/creating-templates/user-input-parameters/#dockertag))                   
        * `compositefield` - [component](/creating-templates/user-input-parameters/#compositefield) that comprises any available field    
        * `slider` - [slider element](/creating-templates/user-input-parameters/#slider) as a form field
        * `envlist` - [list of environments](/creating-templates/user-input-parameters/#envlist) available for a corresponding account                  
        * `popupselector` - new [pop-up window](/creating-templates/user-input-parameters/#popupselector) via POST request with posibility to pass additional parameters
        * `popup-selector` - alias to `popupselector`                               
        * `displayfield` - [text field](/creating-templates/user-input-parameters/#displayfield) intended for displaying text                            
        * `spacer` - alias to `displayfield`                     
        * `spinner` - [input field](/creating-templates/user-input-parameters/#spinner) for entering numeric values                       
        * `numberpicker` - [text field within number validation](/creating-templates/user-input-parameters/#numberpicker) within a range                            
        * `number-picker` - alias to `numberpicker`  
        * `hostpicker` - drop-down menu with [environment hosts](/creating-templates/user-input-parameters/#hostpicker)                             
        * `host-picher` - alias to `hostpicker`                                      
        * `toggle` - [switcher](/creating-templates/user-input-parameters/#toggle) between two values                        
    - `inputType` *[optional]* - type attribute of the input field (e.g. *radio*, *text*, *password*, *file*, etc.). The default value is *'text'*. See more info on the <a href="https://www.w3.org/wiki/HTML/Elements/input#Point" target="_blank">type attribute</a>.                         
    - `name` - input field name, that could be used to get a parameter value through the `${settings.your_input_name}` placeholder within scripts or manifests   
    - `default` *[optional]* - default value for the input field  
    - `caption` *[optional]* - field label  
    - `placeholder` *[optional]* - used <a href="http://docs.cloudscripting.com/reference/placeholders/" target="blank">placeholders</a>                         
    - `required` *[optional]* - possible values are *'true'* & *'false'*. If left empty, the default value is *'true'*.  
    - `regex` *[optional]* - constructor for testing the JavaScript RegExp object, that refers to the stated the field value, during validation. If test fails, the field will be marked invalid using *regexText*. The default value is *'null'*.                                                        
    - `regexText` *[optional]* - displays error message in case of the *regex* test failure during validation. The default value is *' '* (blank space).     
    - `vtype` *[optional]* - validation type name. Possible values:      
        - `alpha` - keystroke filter mask applied to alpha input. The default value is *'/[a-z_]/i'*.  
        - `alphanum` - keystroke filter mask applied to alphanumeric input. The default value is *'/[a-z0-9_]/i'*.  
        - `email` - keystroke filter mask applied to email input. The default value is *'/[a-z0-9_.-+\'@]/i'*. See the <a href="http://docs.sencha.com/extjs/3.4.0/#!/api/Ext.form.VTypes-method-email" target="_blank">appropriate method</a> for more information about complex email validation.      
        - `URL` - keystroke filter mask applied to URL input                        
    - `vtypeText` *[optional]* - custom error message to be displayed instead of the default one, provided by *vtype* for this field. The default value is *' '* (blank space).     
    
!!! note
    *vtypeText* is applied only in case the *vtype* value is set, otherwise, it is ignored.

### string
The basic text field.  

<center>![string](/img/string.jpg)</center>  

``` json
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

<center>![text](/img/text.jpg)</center>  

``` json
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
- `hideLabel`*[optional] [boolean]* - hides field Label. The default value is *'false'*. 

###list   
The drop-down list and a single-line textbox.  

<center>![list](/img/list.jpg)</center>  

``` json
{
  "fields": [
    {
      "type": "list",
      "caption": "List",
      "values": {
        "value1": "hello",
        "value2": "world"
      },
      "hideLabel": false,
      "editable": true
    }
  ]
}
```

where:      

- `caption` *[optional]* - field label         
- `values` - objects values (*"key"*:*"value"*)                            
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.
- `editable` [optional][boolean] - allows to input custom values. The default value is *'false'*.

###checkbox
The single checkbox field.

<center>![text](/img/checkbox.jpg)</center>  

``` json
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
The checkbox grouping.  

<center>![text](/img/checkboxlist.jpg)</center>  

``` json
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
The radio elements grouping.  

<center>![text](/img/radiolist.jpg)</center>  

``` json
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
The grouping of the radio elements with the <b>*showIf*</b> function.     

!!! note
    The *hideLabel* boolean value is always *true* for this field.   

<center>![text](/img/radio-fieldset.jpg)</center>   

``` json
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

- `name` *[required]* - name of the *radio-fieldset* element (for other elements it’s not required)                       
- `default` *[optional]* - selected field upon opening the form  
- `values` - checkboxes (*"key"*:*"value"*)  
- `showIf` - conditional object that shows predefined elements by clicking on the *radio-fieldset* elements. Predefined elements can vary.  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  
- `caption` *[optional]* - field label

###dockertag
Displaying Docker tags within the list element.  

<center>![text](/img/dockertag.jpg)</center>  

``` json
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
- `values` *[required]* - Docker tag values (*name*: *"tag_name"* is required). By default Docker image is pulled from Docker Hub registry.  
- `dockerImage` - Docker image details   
   - `name` - *repository* is required   
   - `registry`, `username`, `password` [*optional*]   
- `env` - required object (can be empty) 

###compositefield
The compositefield is a container with specific functionality and structural components that constitute it as a block for application-oriented custom user interfaces.  

<center>![compositefield](/img/compositefield.jpg)</center>  

``` json
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
      "defaultPadding": 0,
      "defaultFlex": 0,
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
- `defaultFlex` *[optional]* - horizontal flex for items 
- `items` - elements  

###slider
The slider element as a form field.

<center>![slider](/img/slider.jpg)</center>

``` json
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
The account environments list expanded within a drop-down element.  

<center>![envlist](/img/envlist.jpg)</center>  

``` json
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
- `editable` *[optional][boolean]* - enables/disables the *envlist* field editing. The default value is *'false'*.    
- `valueField` *[optional][string]* - value from environment information, which will be sent to a server. The default value is *'domain'*. Available values are:      
    - *iconCls* - CSS class     
    - *isRunning* - checking whether environment status is *running*    
    - *shortdomain* - short environment domain name (without platform URL)  
    - *displayName* - environment *displayName*  
    - *appid* - unique environment ID       

###popupselector
(*popup-selector* is an alias)     

Opens a pop-up window via the POST request to any external service. It provides the possibility to pass additional parameters.  

<center>![popupselector](/img/popupselector.jpg)</center>  

``` json
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
- `url` *[optional]* - external source URL. The default link is to the Jelastic Platform.         
- `popupWidth` *[optional]* - width in pixels          
- `popupHeight` *[optional]* - height in pixels   
- `popupCallbackEvent` - event handler   
- `params` - parameters for sending in POST request to URL source     

###displayfield
(*spacer* is an alias)    

The text field intended only for display, which is not validated and not submitted.  

<center>![displayfield](/img/displayfield.jpg)</center>  

``` json
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

<center>![spinner](/img/spinner.jpg)</center>  

``` json
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
(*number-picker* is an alias)  

The text field with a number validation within a range.   

<center>![numberpicker](/img/numberpicker.jpg)</center>  

``` json
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
- `editable` *[optional] [boolean]* - enables/disables editing the *numberpicker* field. The default value is *'false'*.  

###hostpicker
(*host-picker* is an alias)  

The drop-down menu with the environments hosts.  

<center>![hostpicker](/img/hostpicker.jpg)</center>  

``` json
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
- `editable` *[optional] [boolean]* - enables/disables editing the *envlist* field. The default value is *'false'*.  
- `valueField` *[optional][string]* - value from environment information, which will be sent to a server. The default value is *'domain'*. Available values are:    
    - *iconCls* - CSS class     
    - *isRunning* - checking whether environment status is *running*    
    - *shortdomain* - short environment domain name (without platform URL)  
    - *displayName* - environment *displayName*  
    - *appid* - unique environment ID        

###toggle
The toggle element is a switch between two values.

<center>![toggle](/img/toggle.jpg)</center>

``` json
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

<h3>Target Nodes</h3>
Target Nodes is an optional method that allows to define environments suitable for JPS installation. Herewith, this option is available only for *update* installation type.      

Filtering for **targetNodes** can be performed by *nodeType*, *nodeGroup*, *dockerOs*, *dockerName* or *dockerTag*.                         
``` json
{
  "type": "update",
  "name": "targetNodes",
  "targetNodes": {
    "nodeType": [
      "..."
    ],
    "nodeGroup": [
      "..."
    ],
    "dockerOs": [
      "..."
    ],
    "dockerName": [
      "..."
    ],
    "dockerTag": [
      "..."
    ]
  },
  "onInstall": {
    "createFile": {
      "nodeGroup": "cp",
      "path": "/tmp/newFile"
    }
  }
}
```
There are two possible ways to define a *nodeType*:  
```
"nodeType": ["..."] - to set the required nodeTypes in array

"nodeType": "..., ..." - to set the required nodeTypes being separated with commas
```
  
<b>Example</b>   
 
Let’s suppose you have three environments with different topology:     

<center>![target-nodes](/img/target-nodes.png )</center>  

Within these environments, the *targetNodes* filtering for JPS installation can be performed with the next example:
``` json
{
  "type": "update",
  "name": "targetNodes",
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
```
In this case, the filtering result will be the following:   

<center>![TargetNodesFilter](/img/TargetNodesFilter.jpg)</center>
  
## Custom Menus    
Menu is an expandable list within the <b>Add-ons</b> section, comprising operations that can be extended and adjusted by means of [custom buttons](/creating-templates/user-input-parameters/#custom-buttons).                 

<center>![menu](/img/menu.jpg)</center>     

By default, this menu contains the <b>Uninstall</b> option. The rest of listed actions, if there are any, execute operations from the <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">events</a> settings.          

The used properties for custom menus are the same as for custom buttons. However, the appropriate *menu* field (instead of *buttons*) should be specified in order to adjust functionality exactly within the menu list of the Add-ons plank.           

Sample to set custom buttons within the menu list of the Add-ons plank:
``` json
{
  "type": "update",
  "name": "Custom buttons",
  "targetNodes": {
    "nodeGroup": "bl"
  },
  "actions": [
    "..."
  ],
  "menu": {
    "confirmText": "Custom confirm text",
    "loadingText": "Load text while waiting",
    "action": "{String}",
    "caption": "Configure",
    "successText": "Configuration saved successfully!",
    "settings": "config",
    "title": "Title",
    "submitButtonText": "Button Text",
    "logsPath": "/var/log/add-on-action.log",
    "logsNodeGroup": "cp"
  }
}
```
Refer to the *Custom Buttons* section below for a detailed description on the parameters that are set with the current sample.

## Custom Buttons
The custom buttons settings are intended for extending and adjusting functionality of planks within the <b>Add-ons</b> section. It can be accessed upon clicking the same-named button next to the required node:      

<center>![new-addon](/img/new-addon.png)</center>       

Such buttons execute operations that are predefined within a JPS manifest.   

<center>![TrafficManager](/img/TrafficManager.jpg)</center>    

!!! note
    The JPS manifest should include the [*targetNodes*](http://docs.cloudscripting.com/creating-templates/user-input-parameters/#target-nodes) field in order to be displayed within the Add-ons section after installation, otherwise, it will be hidden.     

<b>Templates</b>   

Sample to set buttons within the Add-ons plank:
``` json
{
  "type": "update",
  "name": "Custom buttons",
  "targetNodes": {
    "nodeGroup": "bl"
  },
  "actions": [
    "..."
  ],
  "buttons": [
    {
      "confirmText": "Custom confirm text",
      "loadingText": "Load text while waiting",
      "action": "{String}",
      "caption": "Configure",
      "successText": "Configuration saved successfully!",
      "href": "http://google.com"
    }
  ]
}
```

where: 

- `buttons` - button parameters array   
- `confirmText` *[optional]* - custom confirmation text for users. The default value is *'Are you sure?'*.             
    It will be displayed after clicking on the appropriate button for an add-on. According to the code above, the text will be:          

<center>![Confirm](/img/Confirm.jpg)</center>      

- `loadingText` *[optional]* - UI text to be displayed during loading and applying changes. The default value is *'Applying...'*.    

<center>![LoadingText](/img/LoadingText.jpg)</center>      

- `action` *[required] [string]* - name of the custom action that will be executed. Custom action body structure is described in the <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank">*actions*</a> section.          
- `caption` - title of the button  

<center>![Caption](/img/Caption.jpg)</center>   

- `successText` -  message, that appears once action is successfully performed  

<center>![SuccessText](/img/SuccessText.jpg)</center>     

- `href` *[optional]* - external link that is opened in a new browser tab that is executed only if the *settings* field is absent. In case of *href* execution, *action* will not be carried out.     

Another sample with additional configurations - the next parameters can be enabled only if the [*settings*](/creating-templates/user-input-parameters/#custom-settings) field is present:     
``` json
{
  "type": "update",
  "name": "Custom buttons",
  "targetNodes": {
    "nodeGroup": "bl"
  },
  "actions": [
    "..."
  ],
  "buttons": [
    {
      "confirmText": "Custom confirm text",
      "loadingText": "Load text while waiting",
      "action": "{String}",
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
```
where:

- `settings` - custom form ID. The default is *'main'*.
- `title` - custom dialog title. If absent, then *caption* will be applied.    
- `submitButtonText` - text for submission button in the opened dialog. The default value is *'Apply'*.   

<center>![SubmitButtonText](/img/SubmitButtonText.jpg)</center>  

- `logsPath` - specifying path to a definite log file for it to be accessible via the **Show Logs** button                          

<center>![LogsPath](/img/LogsPath.jpg)</center>  

- `logsNodeGroup` - <a href="http://docs.cloudscripting.com/creating-templates/selecting-containers/#all-containers-by-group" target="_blank">nodeGroup</a> layer the logging path should be opened for                     

## Custom Settings
The settings section can include a few custom forms. The default settings form ID is *'main'*.    

For example:  
``` json
{
  "type": "update",
  "name": "Custom buttons",
  "targetNodes": {
    "nodeGroup": "bl"
  },
  "actions": [
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
      "action": "customAction",
      "caption": "Configure",
      "submitButtonText": "Button Text",
      "logsPath": "/var/lib/jelastic/keys/111"
    }
  ]
}
```
Here, the *main settings* form appears during installation process.   

<center>![settingMain](/img/SettingsMain.jpg)</center>   

The *config settings* form appears after clicking the <b>Configure</b> button within the Add-ons section.   

<center>![settingCustom](/img/SettingsCustom.jpg)</center>     

##Handling Custom Errors

The Cloud Scripting engine provides functionality to handle custom errors. These possible errors should be described within a separate *errorHandlers* block. The errors handling is related to the action result codes that can be located within the <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Jelastic Console Log Panel</a> upon a corresponding action execution. Therefore, you can predefine a message text that will be displayed in case of an error occurrence.         

There are a number of predefined pop-up windows that emerge while custom errors are being handled:  

- `info` - *information* pop-up window                

<center>![SuccessText](/img/SuccessText.jpg)</center>          

- `warning` - *warning* pop-up window with a custom message                
 
<center>![warningType](/img/warningType.jpg)</center>        

- `error` - *error* pop-up window          

<center>![errorType](/img/errorType.jpg)</center>          

The result message text can be localized according to the languages that are available within the Jelastic Platform:

``` json
{
  "type": "warning",
  "message": {
    "en": "Localized text",
    "es": "Texto localizado"
  }
}
```

<h3>Examples</h3>

**File creation error**

The example below describes a creation of the same file twice and handling an error, which occurs as a result of such action execution. Consequently, the result code of this error will be defined as *4036*. The example presupposes that all the actions with *4036* result will be displayed via *error* pop-up window with a custom error message text. 
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

The additional functionality is provided to display action errors using return <a href="http://docs.cloudscripting.com/reference/actions" target="_blank">action</a>.                         

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
- `1000` - custom predefined result code for error handling. It will be returned from the *script* action in the *onInstall* block.        

If the result code is delivered via *string*, then the default result code is *11039*. Therefore, *errorHandlers* can be handled by the following outcoming *string* text:            

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

In all the other cases, i.e. when a custom error is not predefined within the *errorHandler* block, the default pop-up window type is *error* with an output message.          


# Success Text Customization
 
It is possible to customize the *success* text that is displayed upon successful application installation either at the dashboard or in the email notification.            

<b>Examples</b>             

- Setting a <a href="http://docs.cloudscripting.com/creating-templates/basic-configs/#relative-links" target="blank">relative link</a> to *baseUrl*, which points path to the <b>*README.md*</b> file for its content to be displayed within the *success* response.                    
``` json
{
    "type" : "update",
    "name" : "Success Text first example",
    "baseUrl" : "https://github.com/jelastic-jps/minio",
    "onInstall" : {
        "log" : "success text first example"
    },
    "success" : "README.md"
}
```

- Customizing the *success* return text by means of the external link.                    
``` json
{
  "type": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
}
```

As it was mentioned above, the success response is distinguished between two values:                        

 - text displayed at the dashboard after application installation is successfully conducted                       
 
``` json
{
  "type": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": {
    "text": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
  }
}
```
 
 - message delivered via email notifying about the successful application setup                             
 
``` json
{
  "type": "update",
  "name": "Success Text Test 4",
  "baseUrl": "https://github.com/jelastic-jps/lets-encrypt",
  "onInstall": {
    "log": "success text test 4"
  },
  "success": {
    "email": "README.md",
    "en": "README.md",
    "ru": "https://github.com/jelastic-jps/lets-encrypt/blob/master/README.md"
  }
}
```

In the last example above, the localization functionality is applied that depends upon the Jelastic Platform selected language.