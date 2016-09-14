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

- `prepopulate` *[optional]* - link to get default field values 
- `fields`
    - `showIf` - show/hide field by condition. Only for `radio-fieldset` field
    - `type` *[optional]* - input field type (defaults to `string`). Possible values:
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
    - `inputType` *[optional]* - The type attribute for input fields - e.g. radio, text, password, file (defaults to 'text'). [More info](https://www.w3.org/wiki/HTML/Elements/input#Point)        
    - `name` - input field name that could be used to get a parameter value through `${settings.your_input_name}` placeholder inside of your scripts or a manifest. 
    - `default` *[optional]* - the default input field value
    - `caption` *[optional]*
    - `placeholder` *[optional]*
    - `required` *[optional]*
    - `vtype` *[optional]* - A validation type name. Possible values:
        - `alpha` - The keystroke filter mask to be applied on alpha input. Defaults to: /[a-z_]/i
        - `alphanum` - The keystroke filter mask to be applied on alphanumeric input. Defaults to: /[a-z0-9_]/i
        - `email` - The keystroke filter mask to be applied on email input. See the email method for information about more complex email validation. Defaults to: /[a-z0-9_.-+\'@]/i
        - `url` - The keystroke filter mask to be applied on URL input.                      
    - `vtypeText` *[optional]* - A custom error message to display in place of the default message provided for the `vtype` currently set for this field (defaults to ''). Note: only applies if `vtype` is set, else ignored.
    - `regex` *[optional]* - A constructor for the JavaScript RegExp object to be tested against the field value during validation (defaults to null). If the test fails, the field will be marked invalid using regexText.
    - `regexText` *[optional]* - The error text to display if regex is used and the test fails during validation (defaults to '')                               

##Custom buttons
Custom buttons can be implemented in add-ons. They will execute procedures which are predefined in manifest.  

![traffic-manager](/img/traffic-manager.jpg)  

Add-ons tab button here:
![addon tab](/img/add-on_tab.jpg)

!!! note
> JPS should include required field `targetNodes`. In opposite case add-on will be hidden in add-ons tab after installation.  

Button creating template:
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
- `buttons` - buttons array 
- `confirmText` - user custom confirm text. Default value *"Are you sure?"*. Optional   
It will display firstly after button click action:  
![confirm](/img/confirm.jpg)      
- `loadingText` - user custom text while loading and applying actions. Default is *"Applying..."*. Optional    
![loadingText](/img/loadingText.jpg)      
- `procedure` - procedure name which will be executed. Procerude's body describes in [*procedure* section](/reference/procedures/). Type is String. Required.   
- `caption` - button title.  
![caption](/img/caption.jpg)   
- `successText` - success message when action was performed successfull  
![successText](/img/successText.jpg)     
- `href` - external link, will open in new browser tab. It will execute if `settings` field is absent.  
In this case `procedure` wont be executed. Optional.
- `settings` - custom form id. Default - *main*. More details [here](/creating-templates/user-input-parameters/#custom-settings)    

Fields bellow can be enabled in case when field `settings` presents:
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
- `title` - custom dialog title. If `title` is absent `caption` will be applied.    
Also same value is a dialog title when option `settings` is available.
- `submitButtonText` - button text in opened dialog. Default *Apply*   
![submitButtonText](/img/submitButtonText.jpg)
- `logsPath` - visible button for showing logs in defined path  
![logsPath](/img/logsPath.jpg)
- `logsNodeGroup` - [nodeGroup](/reference/container-types/#containers-by-groups-nodegroup) layer where logging path will be opened   

##Custom menus  
Menu is a custom action list where every action can execute different procedures by name.   
![menu](/img/menu.jpg)   
There is one default menu - Uninstall. It will call procedures from [application lavel](/reference/events/#application-level-events) if they are.  
There are same properties list as in [Custom buttons](/creating-templates/user-input-parameters/#custom-buttons).  

##Custom settings
Settings section can include few custom forms. Default settings form id - *main*.   
For example:  
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
While installation *main* `settings` form will show.   
![settingMain](/img/settingsMain.jpg)   
After click button *Configure* from add-ons tab settings form *config* will show.   
![settingCustom](/img/settingsCustom.jpg)   


##Supported fields:
###string     
Basic text field.
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
- `caption` - field Label. Optional
- `hideLabel` - boolean, hide field Label. Optional. Default *false*.
###text   
Multiline text field.
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
- `caption` - field Label. Optional
- `hideLabel` - boolean, hide field Label. Optional. Default *false*.
###list   
Dron-down list and single-line non editable textbox.
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
- `caption` - field Label. Optional
- `values` - values object ("key":"value").
- `hideLabel` - boolean, hide field Label. Optional. Default *false*.
###checkbox   
Single checkbox field.
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
- `caption` - field Label. Optional
- `value` - boolean, denides enabling/disabling checkbox.
- `hideLabel` - boolean, hide field Label. Optional. Default *false*.
###checkboxlist   
Groupping `checkbox`.
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
- `caption` - field Label. Optional
- `values` - checkboxes ("key":"value")
- `hideLabel` - boolean, hide field Label (optional). Default *false*.
###radiolist   
Groupping `radio` elements.
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
- `caption` - field Label. Optional
- `values` - checkboxes ("key":"value")
- `hideLabel` - boolean, hide field Label (optional). Default *false*.
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
- `default` - enabled field when form has opened. Optional.
- `values` - checkboxes ("key":"value")
- `showIf` - conditions object for showing predefined elements by clicking to `radio-fieldset` elemets. Predefined elemets can be different.
- `hideLabel` - boolean, hide field Label (optional). Default *false*.
- `caption` - field Label. Optional
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