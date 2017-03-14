#Visual Settings

Cloud Scripting enables you to create a personalized solution by customizing the visual appearance and textual content of such elements as:              

* [Fields](#string)                                      
 
* [Menus](#custom-menus)                            

* [Buttons](#custom-buttons)                   

* [Forms](#custom-settings)                   

* [Responces](#handling-custom-responses)                                     

* [Messages](#success-text-customization)                           
      

##Supported Fields                               

You can use the parameters from the following example to fetch your input data.                        
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
        * `string` - [basic](#string) text field                                  
        * `text`  - [multiline](#text) text field                                                                                                         
        * `list` - drop-down menu with [textboxes](#list)                                                         
        * `checkbox` - [single checkbox](#checkbox) field                                                 
        * `checkboxlist` - [checkbox](#checkboxlist) grouping                             
        * `radiolist` - [radio field](#radiolist) grouping                       
        * `radio-fieldset` - alias to `radiolist`              
        * `dockertags` - drop-down menu with a list of [docker tags](#dockertag)                                         
        * `compositefield` - [component](#compositefield) that comprises any available field    
        * `slider` - [slider element](#slider) as a form field
        * `envlist` - [list of environments](#envlist) available for a corresponding account                  
        * `popupselector` - new [pop-up window](#popupselector) via POST request with posibility to pass additional parameters
        * `popup-selector` - alias to `popupselector`                               
        * `displayfield` - [text field](#displayfield) intended for displaying text                            
        * `spacer` - alias to `displayfield`                     
        * `spinner` - [input field](#spinner) for entering numeric values                       
        * `numberpicker` - [field to select a number](#numberpicker) within a range                            
        * `number-picker` - alias to `numberpicker`  
        * `hostpicker` - drop-down menu with [environment hosts](#hostpicker)                             
        * `host-picher` - alias to `hostpicker`                                      
        * `toggle` - [switcher](#toggle) between two values                        
    - `inputType` *[optional]* - type attribute of the input field (e.g. *radio*, *text*, *password*, *file*, etc.). The default value is *'text'*. See more info on the <a href="https://www.w3.org/wiki/HTML/Elements/input#Point" target="_blank">type attribute</a>.                         
    - `name` - input field name, that could be used to get a parameter value through the `${settings.your_input_name}` placeholder within scripts or manifests   
    - `default` *[optional]* - default value for the input field  
    - `caption` *[optional]* - field label  
    - `placeholder` *[optional]* - used <a href="/reference/placeholders/" target="blank">placeholders</a>                         
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
    The *vtypeText* parameter is applied only in case the *vtype* value is set, otherwise, it is ignored.                                       

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

### text
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
- `hideLabel`*[optional] [boolean]* - hides field label. The default value is *'false'*. 

### list   
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

### checkbox
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

### checkboxlist
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

### radiolist
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

### radio-fieldset
The grouping of the radio elements with the <b>*showIf*</b> function.     

!!! note
    The *hideLabel* boolean is always *true* for this field.   

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
- `default` *[optional]* - field selected upon opening the form  
- `values` - checkboxes (*"key"*:*"value"*)  
- `showIf` - conditional object that shows predefined elements by clicking on the *radio-fieldset* elements. Predefined elements can vary.  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  
- `caption` *[optional]* - field label

### dockertag
The field for displaying Docker tags within the list element.                             

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
- `values` *[required]* - Docker tag values (*name*: *"tag_name"* is required). By default, Docker image is pulled from the Docker Hub registry.  
- `dockerImage` - Docker image details   
   - `name` - *repository* is required   
   - `registry`, `username`, `password` [*optional*]   
- `env` - required object (can be empty) 

### compositefield
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

### slider
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

### envlist
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

### popupselector
(*popup-selector* is an alias)     

The field for opening a pop-up window via the POST request to any external service. It provides the possibility to pass additional parameters.                      

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

### displayfield
(*spacer* is an alias)    

The text field intended only for display that is not validated and not submitted.  

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
- `markup` - value to initialize the field's display. The default value is *'undefined'*.                                

### spinner
The enhanced input field for entering numeric values, with up/down buttons and arrow keys handling.  

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

### numberpicker
(*number-picker* is an alias)                                  

The field that enables to select a number from a predefined range.                    
 
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

### hostpicker
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

### toggle
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

##Target Nodes
Target Nodes is an optional method that allows to define environments suitable for JPS installation. This method is available only for the *update* installation type.                                

Filtering for *targetNodes* can be performed by *nodeType*, *nodeGroup*, *dockerOs*, *dockerName* or *dockerTag*.                         
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
There are two possible ways to define *targetNodes*.                                  
```
"nodeType": ["..."] - to set the required nodeTypes in an array

"nodeType": "..., ..." - to set the required nodeTypes being separated with commas
```
  
<b>Example</b>   
 
Let’s suppose you have three environments with different topology.                              

<center>![target-nodes](/img/target-nodes.png)</center>                                       

Within these environments, the *targetNodes* filtering for JPS installation can be performed with the next example.                           
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
In this case, the filtering result will be the following.                                                 

<center>![TargetNodesFilter](/img/TargetNodesFilter.jpg)</center>
  
## Custom Menus    
Menu is an expandable list within the <b>Add-ons</b> section, comprising operations that can be extended and adjusted by means of [custom buttons](#custom-buttons).                                         

<center>![new-menu](/img/new-menu.png)</center>         

By default, this menu contains the <b>Uninstall</b> button. The rest of listed actions, if there are any, execute operations from the <a href="/reference/events/" target="_blank">events</a> settings.           

The properties used for custom menus are the same as for custom buttons. However, the appropriate *menu* field (instead of *buttons*) should be specified to adjust functionality exactly within the menu list of the Add-ons plank.           

The sample to set custom buttons within the menu list of the Add-ons plank.                       
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
Refer to the *Custom Buttons* section below for a detailed description on the parameters set with the current sample.                          

## Custom Buttons
The custom buttons settings are intended for extending and adjusting functionality of planks within the <b>Add-ons</b> section. It can be accessed upon clicking the same-named button next to the required node.                                      

<center>![custom-addon](/img/custom-addon.png)</center>       

Such buttons execute operations that are predefined within a JPS manifest.   

<center>![traffic-distributor](/img/traffic-distributor.png)</center>    

!!! note
    > The JPS manifest should include the [*targetNodes*](#target-nodes) field in order to be displayed within the Add-ons section after installation, otherwise, it will be hidden.     

<b>Templates</b>   

The sample to set buttons within the Add-ons plank.                      
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

It will be displayed after clicking on the appropriate button for an add-on. According to the code above, the text will be the following.              

<center>![Confirm](/img/Confirm.jpg)</center>      

- `loadingText` *[optional]* - UI text to be displayed during loading and applying changes. The default value is *'Applying...'*.    

<center>![LoadingText](/img/LoadingText.jpg)</center>      

- `action` *[required] [string]* - name of the custom action that will be executed. The custom action body structure is described in the <a href="/reference/actions/#custom-actions" target="_blank">*actions*</a> section.          
- `caption` - title of the button  

<center>![Caption](/img/Caption.jpg)</center>   

- `successText` -  message that appears once action is successfully performed  

<center>![SuccessText](/img/SuccessText.jpg)</center>     

- `href` *[optional]* - external link that is opened in a new browser tab and is executed only if the *settings* field is absent. In case of *href* execution, an *action* will not be carried out.                      

Another sample with additional configurations where parameters can be enabled only if the [*settings*](/creating-manifest/user-input-parameters/#custom-settings) field is present.                           
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

- `logsPath` - path to a log file that is accessible via the **Show Logs** button                          

<center>![LogsPath](/img/LogsPath.jpg)</center>  

- `logsNodeGroup` - nodeGroup <a href="/creating-templates/selecting-containers/#predefined-nodegroup-values" target="_blank">layer</a> the logging path should be opened for                           

## Custom Settings
The settings section can include a few custom forms. The default settings form ID is *'main'*.    

**Example**  
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

## Handling Custom Responses

The Cloud Scripting engine provides functionality to handle custom responses. The responses handling is related to the action result codes that can be located within the <a href="/troubleshooting/" target="_blank">Jelastic Console Log Panel</a> upon a corresponding action execution. Therefore, you can predefine a response text that will be displayed in case of an error occurrence.           

There are the following types of pop-up windows that emerge while custom responses are being handled:                    

- `info` - *information* pop-up window                

<center>![SuccessText](/img/SuccessText.jpg)</center>          

- `warning` - *warning* pop-up window with a custom message                
 
<center>![new-warning](/img/new-warning.png)</center>        

- `error` - *error* pop-up window          

<center>![new-error](/img/new-error.png)</center>          

When the action is executed with the expected result code, the *success* window is displayed. The manifest installation is finished immediately after the result code is returned from the *script* or *return* actions or which is predefined in *responses* block.

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

Parameters `message` and `email` support all <a href="/reference/placeholders/" target="_blank">available placeholders</a>. Either, they could be uploaded from an any external source via direct link or according to <a href="/creating-manifest/basic-configs/#relative-links">baseUrl ability</a>.  

In case, when is returned a response code with a type `success` two response objects impose one to another. 
But the `success` text from response object has a higher priority than a <a href="/creating-manifest/user-input-parameters/#success-text-customization" target="_blank">**success**</a> text from main manifest block.    
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

- `createFile` - predefined within the Cloud Scripting <a href="/reference/actions/#createfile" target="_blank">action</a>              
- `responses` - object (array) to describe custom responses     
- `type` - type of a pop-up window, emerging upon the response occurrence. The available values are: *error*, *warning*, *info*, *success*.       

Thus, the example above sets all the actions with *4036* result to be displayed via *error* pop-up window with a custom response message text.      

The additional functionality is provided to display action responses using <a href="/reference/actions" target="_blank">*return*</a> action.                         

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

- `script` - Cloud Scripting <a href= "/reference/actions/#script" target="__blank">action</a> for executing *Javascript* or *Java* code (*Javascript* is set by default)                     
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

##Success Text Customization

It is possible to customize (in confines of a manifest) the *success* text, which is displayed upon successful application installation either at the dashboard or via email notification.         

- Setting a relative to `baseUrl` link, which points path to the <b>*README.md*</b> file for its content to be displayed within the *success* response.                    
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

In the last example above, the localization functionality is applied, which depends upon the Jelastic Platform selected language.
<br>
<h2> What's next?</h2>

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples      
- See <a href="/troubleshooting/" target="_blank">Troubleshooting</a> for helpful tips and specific suggestions            
- Read <a href="/releasenotes/" target="_blank">Realese Notes</a> to find out about the recent CS improvements                         
- Find out the correspondence between <a href="/jelastic-cs-correspondence/" target="_blank">CS & Jelastic Versions</a>
       
  