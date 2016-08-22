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