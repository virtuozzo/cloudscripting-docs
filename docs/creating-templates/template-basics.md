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
  "jpsType": "string",
  "name": "string",
  "baseUrl": "string",
  "settings": "object",
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

- `name` *[required]* - JPS custom name      
- `baseUrl` *[optional]* - custom [relative links](http://docs.cloudscripting.com/creating-templates/relative-links/)                 
- `settings` *[optional]* - custom form with [predefined user input elements](http://docs.cloudscripting.com/creating-templates/user-input-parameters/)          
- `jpsVersion` - *[optional]* - JPS type supported by the Jelastic platform. Correspondence between version is located [here](http://docs.cloudscripting.com/jelastic-cs-correspondence/).                  
- `nodes` - object to describe information about nodes for installation. Required option for `jpsType` **install**.          
- `engine` *[optional]* - engine [version](/reference/container-types/#engine-versions-engine), **default**: `java6`      
- `region` *[optional]* - region, where an environment will be installed . Required option of `jpsType` **install**.          
- `displayName` *[optional]* - display name for an environment. Required option of `jpsType` **install**.      
- `ssl` *[optional]* - Jelastic SSL status for an environment, **default**: false         
- `ha` *[optional]* - high availability for Java stacks, **default**: false                  
- `description` - text string that describes a template. This section should always follow the template format version section.          
- `categories` - available categories for manifests filtering                   
- `version` *[optional]* - custom version of application                        
- `logo` *[optional]* - JPS image that will be displayed within custom add-ons                
- `homepage` *[optional]* - link for any external aplication source        
- `type` *[optional]* - language type of application           
- `success` *[optional]* - success text that will be sent via email and will be shown at the dashboard after installation      
- `startPage` *[optional]* - path to be opened via the *Open in browser* button in a success form                          
- `actions` *[optional]* - objects to describe all [*custom actions*](/reference/actions/#custom-actions)             
- `addons` *[optional]* - includes JPS manifests with jpsType *update* as a new jps installation      
- `onInstall` *[optional]* - [even](http://docs.cloudscripting.com/reference/events/#oninstall) that is an entry point for the first action execution                        
