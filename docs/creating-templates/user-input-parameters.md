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
        "name": "string",
        "default": "string or localization object",
        "caption": "string or localization object",
        "placeholder": "string or localization object",
        "required": "boolean",
        "vtype": "string",

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
    - `type` *[optional]* - input field type. Possible values:
        * `string`
        * `text`                                                                           
        * `list`
        * `checkbox`
        * `checkboxlist`
        * `radiolist` 
        * `radio-fieldset` - an alias for `radiolist`  
        * `dockertags`
        
        **Default**: `string`             
       
    - `name` - input field name that could be used to get a parameter value through `${settings.your_input_name}` placeholder inside of your scripts or a manifest. 
    - `default` *[optional]* - the default input field value      

 
