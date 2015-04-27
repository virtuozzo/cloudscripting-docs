# Template Basics

The above two units display the outer side of JPS usage and now let’s have a closer look at the inner side - the code of the package with all required configurations.

JPS manifest is a file with .json extension which contains an appropriate code written in JSON format (JSON Formatter & Validator). This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for successful installation of application. The basis of the code is represented by the following strings:

```
{
    "jpsType": "string",
    "jpsVersion": "string",
    "application": "object"
}
```

- `jpsType`
    - `install` - application 
    - `update` - extension
- `jpsVersion` **[optional]** - minimum engine version
- `application` - an object that contains your application configuration details   

This is a mandatory body part of the application package which includes the information about JPS version and the type of the application installation (“install” mode initiates a new environment creation required for deploy).
These basic strings should be extended with the settings required by the application you are packing. The following configuration details are included to the "application": { } parameter:

# Application Workflow

**Basic Template**
```
{
  "jpsType": "install",
  "jpsVersion": "0.3",
  "application": {
    "name": "string",
    "env": "object",
    
    "description": "object/string",
    "categories": "array",
    "version": "string",
    "logo": "string",
    "homepage": "string",
    "success": "object/string",
    "startPage": "string",
    
    "procedures": "array",
    "addons" : "array",

    "onInstall": "object/array"
  }
}
```

- `name`
- `env`
- `description` - A text string that describes the template. This section must always follow the template format version section.
- `version`
- `logo`
- `homepage`
- `type`
- `success`
- `startPage`
- `procedures`
- `addons`
- `onInstall`


# Extension Workflow

**Basic Template**
```
{
  "jpsType": "update",
  "jpsVersion": "0.3",
  "application": {    
    "name": "string",
    "env" : "object<set of environment events subscriptions>",
        
    "description": "object/string", 
    "categories" : "array",
    "version": "string",
    "logo": "string",
    "homepage": "string",
    "type": "string",         
    "success": "object/string",
    "startPage": "string",
    
    "procedures" : "array",

    "onInstall" : "object/array",
    "onUninstall" : "object/array"
  }
}
```

- `name`
- `env`
- `description` - A text string that describes the template. This section must always follow the template format version section.
- `version`
- `logo`
- `homepage`
- `type`
- `success`
- `startPage`
- `procedures`
- `onInstall`
- `onUninstall`

