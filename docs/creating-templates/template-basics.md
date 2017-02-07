# Template Basics

The above two units display the outer side of a JPS usage and now let’s have a closer look at the inner side - a code of a package with all required configurations.

The JPS manifest is a file with <b>*.json*</b> extension, which contains an appropriate code written in JSON format. This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for a successful installation of an application. The basis of the code is represented by the following string:

```
{
    "jpsType": "string",
    "name": "any require name"
}
```

- *jpsType*
    - `install` - application    
    - `update` - extension    
- *name* - JPS custom name           

This is a mandatory body part of the application package, which includes the information about JPS name and the type of the application installation (the <b>*'install'*</b> mode initiates a new environment creation required for a deployment, the <b>*'update'*</b> mode performs actions on the existing environment).
This basic string should be extended with the settings required by the application you are packing. The following configuration details are included beside the <b>*'jpsType': { }*</b> parameter:

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
- `baseUrl` *[optional]* - custom <a href="http://docs.cloudscripting.com/creating-templates/relative-links/" target="_blank">relative links</a>                                       
- `settings` *[optional]* - custom form with <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">predefined user input elements</a>                        
- `jpsVersion` - *[optional]* - JPS type supported by the Jelastic Platform. See the <a href="http://docs.cloudscripting.com/jelastic-cs-correspondence/" target="_blank">correspondence between version page.</a>                          
- `nodes` - object to describe information about nodes for an installation. Required option for **jpsType** `install`.               
- `engine` *[optional]* - engine <a href="http://docs.cloudscripting.com/reference/container-types/#engine-versions-engine" target="_blank">version</a>, **default**: `java6`            
- `region` *[optional]* - region, where an environment will be installed. Required option for **jpsType** `install`.             
- `displayName` *[optional]* - display name for an environment. Required option for **jpsType** `install`.          
- `ssl` *[optional]* - Jelastic SSL status for an environment, **default**: `false`             
- `ha` *[optional]* - high availability for Java stacks, **default**: `false`                              
- `description` - text string that describes a template. This section should always follow the template format version section.            
- `categories` - categories available for manifests filtering                         
- `version` *[optional]* - custom version of an application                           
- `logo` *[optional]* - JPS image that will be displayed within custom add-ons                    
- `homepage` *[optional]* - link to any external aplication source            
- `type` *[optional]* - language type of an application                
- `success` *[optional]* - success text that will be sent via email and will be displayed at the dashboard after installation          
- `startPage` *[optional]* - path to be opened via the **Open in browser** button through a successful installation message                                        
- `actions` *[optional]* - objects to describe all <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank">custom actions</a>             
- `addons` *[optional]* - includes JPS manifests with the **jpsType** `update` as a new JPS installation      
- `onInstall` *[optional]* - [event](http://docs.cloudscripting.com/reference/events/#oninstall) that is an entry point for actions execution                               
