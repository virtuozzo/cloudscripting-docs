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
    - `showIf` - show/hide field by condition
    - `type` *[optional]* - input field type (defaults to `string`). Possible values:
        * `string`
        * `text`                                                                           
        * `list`
        * `checkbox`
        * `checkboxlist`
        * `radiolist` 
        * `radio-fieldset` - an alias for `radiolist`  
        * `dockertags`        
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

 
