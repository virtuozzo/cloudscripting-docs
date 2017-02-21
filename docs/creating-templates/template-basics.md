<h1>Template Basics</h1>

<p dir="ltr" style="text-align: justify;">The above two units display the outer side of a JPS usage and now let’s have a closer look at the inner side - a code of a package with all required configurations.</p>

<p dir="ltr" style="text-align: justify;">The JPS manifest is a file with <b>.json</b> extension, which contains an appropriate code written in JSON format. This manifest file includes the links to the web only dependencies. This file can be named as you require.</p> 

<p dir="ltr" style="text-align: justify;">The code should contain a set of strings needed for a successful installation of an application. The basis of the code is represented by the following string:</p>

```
{
    "type": "string",
    "name": "any require name"
}
```

- `type`
    - <em>install</em> - application    
    - <em>update</em> - extension    
- `name` - JPS custom name           

<p dir="ltr" style="text-align: justify;">This is a mandatory body part of the application package, which includes the information about JPS name and the type of the application installation (the <b>*'install'*</b> mode initiates a new environment creation required for a deployment, the <b>*'update'*</b> mode performs actions on the existing environment).
This basic string should be extended with the settings required by the application you are packing. The following configuration details are included beside the <b>*'type': { }*</b> parameter:</p>

# Application Workflow

**Basic Template**
```
{
  "type": "string",
  "name": "string",
  "baseUrl": "string",
  "settings": "object",
  "version": "string",
  "appVersion": "string",
  "nodes": "array",
  "engine": "string",
  "region": "string",
  "displayName": "string",
  "ssl": "boolean",
  "ha": "boolean",
  "description": "object/string",
  "categories": "array",
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
- `version` - *[optional]* - JPS type supported by the Jelastic Platform. See the <a href="http://docs.cloudscripting.com/jelastic-cs-correspondence/" target="_blank">correspondence between version</a> page.
- `appVersion` *[optional]* - custom version of an application            
- `nodes` - object to describe information about nodes for an installation. Required option for **type** `install`.               
- `engine` *[optional]* - engine <a href="http://docs.cloudscripting.com/reference/container-types/#engine-versions-engine" target="_blank">version</a>, by **default** `java6`            
- `region` *[optional]* - region, where an environment will be installed. Required option for **type** `install`.             
- `displayName` *[optional]* - display name for an environment. Required option for **type** `install`.          
- `ssl` *[optional]* - Jelastic SSL status for an environment, by **default** `false`             
- `ha` *[optional]* - high availability for Java stacks, by **default** `false`                                
- `description` - text string that describes a template. This section should always follow the template format version section.            
- `categories` - categories available for manifests filtering                                        
- `logo` *[optional]* - JPS image that will be displayed within custom add-ons                    
- `homepage` *[optional]* - link to any external application source            
- `type` *[optional]* - language type of an application                
- `success` *[optional]* - success text that will be sent via email and will be displayed at the dashboard after installation          
- `startPage` *[optional]* - path to be opened via the **Open in browser** button through a successful installation message                                        
- `actions` *[optional]* - objects to describe all <a href="http://docs.cloudscripting.com/reference/actions/#custom-actions" target="_blank">custom actions</a>             
- `addons` *[optional]* - includes JPS manifests with the **type** `update` as a new JPS installation      
- `onInstall` *[optional]* - <a href="http://docs.cloudscripting.com/reference/events/#oninstall" target="_blank">event</a> that is an entry point for actions execution                               
