# Visual Settings

Cloud Scripting enables you to create a personalized solution by customizing the visual appearance and textual content of such elements as:              

* [Fields](#string)                                      
 
* [Menus](#custom-menus)                            

* [Buttons](#custom-buttons)                   

* [Forms](#custom-settings)                   

* [Messages](#success-text-customization)                           
      

## Supported Fields                               

You can use the parameters from the following example to fetch your input data.
@@@
```yaml
type: update

settings:
  prepopulate: URL
  fields:
    - showIf: object
      type: string
      inputType: string
      name: string
      default: string or localization object
      caption: string or localization object
      placeholder: string or localization object
      required: boolean
      vtype: string
      vtypeText: string or localization object
      regex: string for RegExp constructor
      regexText: string or localization object
      hideLabel: string
      id: string
      cls: string
      itemId: string     
      
```
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
@@!

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
@@@
```yaml
fields:
  - hideLabel: false
    type: string
    caption: string
    name: customString
```
```json
{
  "fields": [
    {
      "hideLabel": false,
      "type": "string",
      "caption": "string",
      "name": "customString"
    }
  ]
}
```
@@!

where:          
 
- `caption` *[optional]* - field label   
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  

### text
The multiline text field.

<center>![text](/img/text.jpg)</center>  
@@@
```yaml
fields:
  - type: text
    caption: string
    hideLabel: false
```
```json
{
  "fields": [
    {
      "type": "string",
      "caption": "string",
      "hideLabel": false
    }
  ]
}
```
@@!

where:   

- `caption` *[optional]* - field label  
- `hideLabel`*[optional] [boolean]* - hides field label. The default value is *'false'*. 

### list   
The drop-down list and a single-line textbox.  

<center>![list](/img/list.jpg)</center>  
@@@
```yaml
fields:
  - type: list
    caption: string
    values:
      value1: hello
      value2: world
    hideLabel: false
    editable: true
```
``` json
{
  "fields": [
    {
      "type": "list",
      "caption": "string",
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
@@!

where:      

- `caption` *[optional]* - field label         
- `values` - objects values (*"key"*:*"value"*)                            
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.
- `editable` [optional][boolean] - allows to input custom values. The default value is *'false'*.

### checkbox
The single checkbox field.

<center>![text](/img/checkbox.jpg)</center>  
@@@
```yaml
fields:
  - type: checkbox
    caption: string
    value: true
    hideLabel: false
```
``` json
{
  "fields": [
    {
      "type": "checkbox",
      "caption": "string",
      "value": true,
      "hideLabel": false
    }
  ]
}
```
@@!

where:  

- `caption` *[optional]* - field label           
- `value` - enables or disables checkbox                         
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *'false'*. 

### checkboxlist
The checkbox grouping.  

<center>![text](/img/checkboxlist.jpg)</center>  
@@@
```yaml
fields:
  - type: checkboxlist
    caption: Checkbox List
    values:
      value1: hello
      value2: world
    hideLabel: false
```
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
@@!

where:     

- `caption` *[optional]* - field label  
- `values` - checkboxes (*"key"*:*"value"*)  
- `hideLabel` *[optional] [boolean]* - shows/hides field label. The default value is *'false'*.  

### radiolist
The radio elements grouping.  

<center>![text](/img/radiolist.jpg)</center>  
@@@
```yaml
fields:
  - type: radiolist
    caption: Radio List
    values:
      value1: hello
      value2: world
    hideLabel: false
```
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
@@!

where:  

- `caption` *[optional]* - field label   
- `values` - checkboxes (*"key"*:*"value"*)  
- `hideLabel` *[optional][boolean]* - shows/hides field label. The default value is *'false'*.  

### radio-fieldset
The grouping of the radio elements with the <b>*showIf*</b> function.     

!!! note
    The *hideLabel* boolean is always *true* for this field.   

<center>![text](/img/radio-fieldset.jpg)</center>   
@@@
```yaml
fields:
  - type: radio-fieldset
    name: customName
    default: '1'
    values:
      1: hello
      2: world
    showIf:
      1:
        - hideLabel: false
          type: string
          caption: First String
          name: first
      2:
        - hideLabel: false
          type: string
          caption: Second String
          name: second
```
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
@@!

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
@@@
```yaml
name: Cloud Scripting

settings:
  fields:
  - type: dockertags
    name: tag
    values:
    - name: latest
    - name: first

dockerImage:
  name: sych74/pokemongo-map
  registry: ''
  username: ''
  password: ''

env: {}
```
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
@@!

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
@@@
```yaml
fields:
  - pack: ''
    align: ''
    defaultMargins:
      top: 0
      right: 0
      bottom: 0
      left: 10
    defaultPadding: 0
    defaultFlex: 0
    caption: Compositefield
    type: compositefield
    name: compositefield
    items:
      - name: checkbox
        value: true
        type: checkbox
      - width: 50px
        name: first
        type: string
      - width: 100px
        name: latest
        type: string
```
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
@@!

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
@@@
```yaml
fields:
  - min: '0'
    max: '10'
    increment: 1
    useTips: true
    caption: Slider
    type: slider
    name: slider
```
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
@@!

where:   

- `min` - minimum slider value  
- `max` - maximum slider value  
- `useTips` - displaying tips for the value. The default value is *'true'*.  
- `caption` *[optional]* - field label  
- `name` *[optional]* - name of the field 

### envlist
The account environments list expanded within a drop-down element.  

<center>![envlist](/img/envlist.jpg)</center>  
@@@
```yaml
fields:
  - caption: Envlist
    editable: true
    valueField: appid
    type: envlist
    name: envlist
```
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
@@!
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
@@@
```yaml
fields:
  - caption: Popupselector
    type: popupselector
    name: popupselector
    buttonText: Open
    url: http://{external url}
    popupWidth: 300px
    popupHeight: 300px
    popupCallbackEvent: handler
    params:
      first: 1
      second: 2
```
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
@@!

where:  

- `caption` *[optional]* - field label                      
- `name` *[optional]* - name of the field                  
- `buttonText` *[optional]* - button label              
- `url` *[optional]* - external source URL. The default link is to the current Jelastic Dashboard. New popup window is opened only via POST request.        
- `popupWidth` *[optional]* - width in pixels          
- `popupHeight` *[optional]* - height in pixels   
- `popupCallbackEvent` - event handler   
- `params` - parameters for sending in POST request to URL source     
- `value` - defined value which is filled in text field

The `textfield` value in `popupselector` element can be replaced by parameter from external `url` source. This parameter should be passed with `popupCallbackEvent` value.  
For example:
@@@
```yaml
type: update
name: Return Action

settings:
  fields:
    caption: Popupselector
    type: popupselector
    name: popupselector
    buttonText: Open
    value: '3'
    url: https://{external_source}/example
    popupWidth: 300px
    popupHeight: 300px
    popupCallbackEvent: click
    params:
      first: 1
      second: 2
```
```json
{
  "type": "update",
  "name": "Return Action",
  "settings": {
    "fields": {
      "caption": "Popupselector",
      "type": "popupselector",
      "name": "popupselector",
      "buttonText": "Open",
      "value": "3",
      "url": "https://{external_source}/example",
      "popupWidth": "300px",
      "popupHeight": "300px",
      "popupCallbackEvent": "click",
      "params": {
        "first": 1,
        "second": 2
      }
    }
  }
}
```
@@!

In example above the external source should returns a URL with such parameters as `value` and `event`. The `event` name is the same name as `popupCallbackEvent` in field description in manifest.  

A full external resource link should be like in example below:
```
http://{Jelastic_Platform_URL} + "fireevent?event=click&value=hello"
``` 
where:

- `Jelastic_Platform_URL` - Jelastic Dashboard URL where manifest is executed
- `click` - event namewhich is handled in manifest in `popupCallbackEvent` parameter
- `value` - type is **string**. The `textfield` will be filled by it when button "Open" will be applied.

### displayfield
(*spacer* is an alias)    

The text field intended only for display that is not validated and not submitted.  

<center>![displayfield](/img/displayfield.jpg)</center>  
@@@
```yaml
fields:
  - caption: Displayfield
    type: displayfield
    name: displayfield
    markup: display
```
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
@@!

where:  

- `caption` *[optional]* - field label                   
- `name` *[optional]* - name of the field                
- `markup` - value to initialize the field's display. The default value is *'undefined'*.                                

### spinner
The enhanced input field for entering numeric values, with up/down buttons and arrow keys handling.  

<center>![spinner](/img/spinner.jpg)</center>  
@@@
```yaml
fields:
  - type: spinner
    name: spinner
    caption: Spinner
    min: 1
    max: 10
    increment: 2
    decimanPrecision: ''
```
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
@@!

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
@@@
```yaml
fields:
  - type: numberpicker
    name: numberpicker
    caption: Numberpicker
    min: 3
    max: 10
    editable: true
```
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
@@!

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
@@@
```yaml
fields:
  - type: hostpicker
    name: hostpicker
    caption: Hostpicker
    editable: true
    valueField: host
```
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
@@!

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
@@@
```yaml
fields:
  - type: toggle
    name: toggle
    caption: Toggle
    value: true
```
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
@@!
where:    

- `name` *[optional]* - name of the field  
- `caption` *[optional]* - field label    
- `value` *[boolean]* - enables/disables toggle value. The default value is *'false'*.   

##Target Nodes
Target Nodes is an optional method that allows to define environments suitable for JPS installation. This method is available only for the *update* installation type.                                

Filtering for *targetNodes* can be performed by *nodeType*, *nodeGroup*, *dockerOs*, *dockerName* or *dockerTag*.                         
@@@
```yaml
type: update
name: targetNodes

targetNodes:
  nodeType:
  - "..."
  nodeGroup:
  - "..."
  dockerOs:
  - "..."
  dockerName:
  - "..."
  dockerTag:
  - "..."

onInstall:
  createFile:
    nodeGroup: cp
    path: "/tmp/newFile"
```
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
@@!
There are two possible ways to define *targetNodes*.                                  
```
"nodeType": ["..."] - to set the required nodeTypes in an array

"nodeType": "..., ..." - to set the required nodeTypes being separated with commas
```
  
<b>Example</b>   
 
Let’s suppose you have three environments with different topology.                              

<center>![target-nodes](/img/target-nodes.png)</center>                                       

Within these environments, the *targetNodes* filtering for JPS installation can be performed with the next example.                           
@@@
```yaml
type: update
name: targetNodes

targetNodes:
  nodeType: nginx, mysql5

onInstall:
  createFile:
    nodeGroup: cp
    path: "/tmp/newFile"
```
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
@@!
In this case, the filtering result will be the following.                                                 

<center>![TargetNodesFilter](/img/TargetNodesFilter.jpg)</center>
  
## Custom Menus    
Menu is an expandable list within the <b>Add-ons</b> section, comprising operations that can be extended and adjusted by means of [custom buttons](#custom-buttons).                                         

<center>![new-menu](/img/new-menu.png)</center>         

By default, this menu contains the <b>Uninstall</b> button. The rest of listed actions, if there are any, execute operations from the <a href="/reference/events/" target="_blank">events</a> settings.           

The properties used for custom menus are the same as for custom buttons. However, the appropriate *menu* field (instead of *buttons*) should be specified to adjust functionality exactly within the menu list of the Add-ons plank.           

The sample to set custom buttons within the menu list of the Add-ons plank.                       
@@@
```yaml
type: update
name: Custom buttons

targetNodes:
  nodeGroup: bl

actions:
  - "..."

menu:
  confirmText: Custom confirm text
  loadingText: Load text while waiting
  action: "{String}"
  caption: Configure
  successText: Configuration saved successfully!
  settings: config
  title: Title
  submitButtonText: Button Text
  logsPath: "/var/log/add-on-action.log"
  logsNodeGroup: cp
```
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
@@!
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
@@@
```yaml
type: update
name: Custom buttons

targetNodes:
  nodeGroup: bl

actions:
  - "..."

buttons:
  - confirmText: Custom confirm text
    loadingText: Load text while waiting
    action: "{String}"
    caption: Configure
    successText: Configuration saved successfully!
    href: http://google.com
```
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
@@!
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
@@@
```yaml
type: update
name: Custom buttons

targetNodes:
  nodeGroup: bl

actions:
  - "..."

buttons:
  - confirmText: Custom confirm text
    loadingText: Load text while waiting
    action: "{String}"
    caption: Configure
    successText: Configuration saved successfully!
    settings: config
    title: Title
    submitButtonText: Button Text
    logsPath: "/var/log/add-on-action.log"
    logsNodeGroup: cp
```
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
@@!
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
@@@
```yaml
type: update
name: Custom buttons

targetNodes:
  nodeGroup: bl
  
actions:
  - "..."

settings:
  main:
    fields:
    - type: text
      caption: Main form
  config:
    fields:
    - type: text
      caption: Custom form from button action

buttons:
  - settings: config
    action: customAction
    caption: Configure
    submitButtonText: Button Text
    logsPath: "/var/lib/jelastic/keys/111"
```
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
@@!
Here, the *main settings* form appears during installation process.   

<center>![settingMain](/img/SettingsMain.jpg)</center>   

The *config settings* form appears after clicking the <b>Configure</b> button within the Add-ons section.   

<center>![settingCustom](/img/SettingsCustom.jpg)</center>     

## Success Text Customization

It is possible to customize the *success* text that is displayed upon successful installation either at the dashboard, or via email notification.          
A success text can be defined like plain text or like Markdown syntax. More details about Markdown syntax in Cloud Scripting [here](/creating-manifest/visual-settings/#markdown-description) 

- Setting relative to the *baseUrl* link that points path to the <b>*README.md*</b> file for its content to be displayed within the *success* response.                                               
@@@
```yaml
type: update
name: Success Text first example
baseUrl: https://github.com/jelastic-jps/minio

onInstall:
  log: success text first example

success: README.md
```
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
@@!

- Customizing the *success* response text by means of the external link.                                     
@@@
```yaml
type: update
name: Success Text Second Example

onInstall:
  log: success Text Second Example

success: https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md
```
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
@@!

As it was mentioned above, the success response is distinguished between two values:                        

 - text displayed at the dashboard after installation is successfully conducted                         
 
@@@
```yaml
type: update
name: Success Text Second Example

onInstall:
  log: success Text Second Example

success:
  text: https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md
```
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
@@! 
 - message delivered via email notifying about the successful installation                                                  
@@@
```yaml
type: update
name: Success Text Test 4
baseUrl: https://github.com/jelastic-jps/lets-encrypt

onInstall:
  log: success text test 4

success:
  email: README.md
  text:
    en: README.md
    ru: https://github.com/jelastic-jps/lets-encrypt/blob/master/README.md
```
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
    "text": {
      "en": "README.md",
      "ru": "https://github.com/jelastic-jps/lets-encrypt/blob/master/README.md"
    }
  }
}
```
@@!

A email notification also can be customized in <a href="/creating-manifest/handling-custom-responses/">custom responses</a>. In this case an `email` value from handle custom response has a highier priority. For example:
@@@
```yaml
type: update
name: Success Text Customization

onInstall:
  return:
    result: success
    email: Custom email response text

success: success!!
```
```json
{
  "type": "update",
  "name": "Success Text Customization",
  "onInstall": {
    "return": {
      "result": "success",
      "email": "Custom email response text"
    }
  },
  "success": "success!!"
}
```
@@!

In the last example above, the localization functionality is applied, which depends upon the Jelastic Platform selected language.

A custom responses can be return within <a href="/creating-manifest/actions/#return" target="_blank">`return`</a> or <a href="/creating-manifest/actions/#script" target="_blank">`script`</a> actions. More details about <a href="/creating-manifest/handling-custom-responses/" target="_blank">custom responses here</a>. 

## Markdown description

Markdown is a light language with plain text formatting syntax. This language is supported by Cloud Scripting technology to describe a `description`, `success texts` or showing [`custom response` texts](/creating-manifest/visual-settings/#success-text-customization).

### Emphasis

Markdown treats underscores and asterisks to emphase text. Wrapped text with one `*` or `_` will be wrapperd with HTML `<em>` tag and double `*`'s or `_`'s will be wrapped with HTML `<strong>` tag.

<center>![emphasis](/img/emphasis.jpg)</center>
@@@
```yaml
type: update
name: Emphasis
description: |
  *Italic* or _Italic_
  
  **Bolt** or __Bolt__
```
```json
{
	"type": "update",
	"name": "Emphasis",
	"description": "*Italic* or _Italic_\n\n**Bolt** or __Bolt__\n"
}
```
@@!

### Headers
Cloud Scripting Markdown supports two styles headers: 
  
* setex-style headers are two headers (first and second levels) using "underlined" signs like in examples below:  
```
This is a H1 
============
This is a H2
------------
```

* atx-style headers support 1-6 levels
```
# This is H1
## This is H2
##### This is H6
```

### Links

Markdown supports two link styles - *inline* and *reference*. Both styles use [square brackets].

<center>![markdown_links](/img/markdown_links.jpg)</center>
For example:
@@@
```yaml
type: update
name: Emphasis
description: |
  [jelastic.com URL](https://jelastic.com)
  
  or
  
  [jelastic.com URL][1]
  
  [1]: https://jelastic.com
```
```json
{
	"type": "update",
	"name": "Emphasis",
	"description": "[jelastic.com URL](https://jelastic.com)\n\nor\n\n[jelastic.com URL][1]\n\n[1]: https://jelastic.com\n"
}
```
@@!

### Images

Markdown `image` syntax is resemble a `link` and also allowing in two styles: inline and reference. A difference between them is a symbol `!`.
For example:
@@@
```yaml
type: update
name: Emphasis
description: |
  ![Jelastic](https://jelastic.com/assets/img/favicon-32x32.ico)
  
  ![Jelastic][1]
  
  [1]: https://jelastic.com/assets/img/favicon-32x32.ico
```
```json
{
	"type": "update",
	"name": "Emphasis",
	"description": "![Jelastic](https://jelastic.com/assets/img/favicon-32x32.ico)\n\n![Jelastic][1]\n\n[1]: https://jelastic.com/assets/img/favicon-32x32.ico\n"
}
```
@@!

### Blockquotes 

This is an email-style characters `>`. Blockquotes can be inserted at the beginning of each line or can wrapped a full paragraph.  
<center>![blockquote](/img/blockquote.jpg)</center>  
For example:
@@@
```yaml
type: update
name: Markdown blockquote
description: |
    > Blockquote
```
```json
{
	"type": "update",
	"name": "Markdown blockquote",
	"description": "> Blockquote\n"
}
```
@@!

@@@
```yaml
type: update
name: Markdown blockquote
description: |
    > multiline 
    blockquote
```
```json
{
	"type": "update",
	"name": "Markdown blockquote",
	"description": "> multiline \nblockquote\n"
}
```
@@!

<br>
<h2>What's next?</h2>

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples                                

- See <a href="/troubleshooting/" target="_blank">Troubleshooting</a> for helpful tips and specific suggestions                            

- Read <a href="/releasenotes/" target="_blank">Realese Notes</a> to find out about the recent CS improvements                      

- Find out the correspondence between <a href="/jelastic-cs-correspondence/" target="_blank">CS & Jelastic Versions</a>                    
  