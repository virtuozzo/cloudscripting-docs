# Getting User Input

```
{
    "type" : "string",
    "name" : "string",
    "default" : "string or localization object",
    "caption" : "string or localization object",
    "placeholder" : "string or localization object",
    "required" : "boolean",
    "vtype" : "string",
    
    "hideLabel" : "boolean",
    "id" : "string",    
    "cls" : "string",
    "itemId" : "string",
    
}
```

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

 
