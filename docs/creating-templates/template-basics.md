# Template Basics

The above two units display the outer side of JPS usage and now let’s have a closer look at the inner side - the code of the package with all required configurations.

JPS manifest is a file with .json extension which contains an appropriate code written in JSON format. This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for successful installation of application. The basis of the code is represented by the following string:

```
{
    "jpsType": "string",
    "name": "any require name"
}
```

- `jpsType`
    - `install` - application 
    - `update` - extension  
- `name` - JPS custom name. 

This is a mandatory body part of the application package which includes the information about JPS name and the type of the application installation (“install” mode initiates a new environment creation required for deploy, "update" mode performs actions on the existing environment).
These basic string should be extended with the settings required by the application you are packing. The following configuration details are included beside "jpsType": { } parameter:

# Application Workflow

**Basic Template**
```
{
  "jpsType": "install(update)",
  "name": "string",
  "jpsVersion": "string",
  "nodes": "array",
  "engine": "string",
  "region": "string",
  "displayName": "string",
  "ssl": "boolean",
  "ha": "boolean",
  "description": "object/string",
  "categories": "array",
  "version": "string",
  "logo": "string",
  "homepage": "string",
  "type": "string",
  "success": "object/string",
  "startPage": "string",
  "actions": "array",
  "addons": "array",
  "onInstall": "object/array"
}
```

- `name` *[required]* - jps custom name.
- `jpsVersion` - *[optional]* - jps type supported by Jelastic platform. Correspondence between version [here](/jelastic-cs-correspondence/)  
- `nodes` - an object where describes nodes information for installation. Requered option for `jpsType` **install**.       
- `engine` *[optional]*. **Default**: `java6` 
- `region` *[optional]* - region where will be installed environment. Required option of `jpsType` **install**.   
- `displayName` *[optional]* - display name for environment. Required option of `jpsType` **install**.   
- `ssl` *[optional]*. **Default**: false - Jelastic ssl status for environment    
- `ha` *[optional]*. **Default**: false. High availability for java stacks     
- `description` - A text string that describes the template. This section must always follow the template format version section.
- `categories` - available categories for filter manifests   
- `version` *[optional]* - application custom version.
- `logo` *[optional]* - jps image. Will be displayed at custom add-ons    
- `homepage` *[optional]* - link for any external aplication source    
- `type` *[optional]* - application language type   
- `success` *[optional]* - success text. Will be sent to email and will be shown at the dashboard after installation
- `startPage` *[optional]* - path. Can be open via button in success form *Open in browser*    
- `actions` *[optional]* - objects where describe all [*custom actions*](/reference/actions/#custom-actions)    
- `addons` *[optional]* - included jps manifests with jpsType *update* as a new jps installation   
- `onInstall` *[optional]* - first action which will be executed   
