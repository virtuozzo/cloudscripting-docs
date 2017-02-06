# Quick Start 
This guide will walk you through the Cloud Scripting basics and will help you to build and run such simple automation processes like creating new environments and deploying applications.

The required operations should be declared within the appropriate Cloud Scripting manifest, written in <a href="http://www.json.org/" target="_blank">JSON</a> format. You can name this file with manifest as you need. The only requirement is that it should have the **.json** extension.     
The manifest file can be composed via any text editor, using a modern code editor with the support of JSON syntax highlighting is recommended (e.g. <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>).    

Below you can see two simple examples of how to: 

- Create a new environment and deploy a simple HelloWorld application to it:  

```
{
  "jpsType": "install",
  "name": "Hello World!",
  "engine": "php5.4",
  "nodes": [
    {
      "nodeType": "apache2",
      "cloudlets": 16
    }
  ],
  "onInstall": {
    "deploy": {
      "archive": "http://app.demo.jelastic.com/HelloWorld.zip",
      "name": "Hello World",
      "context": "ROOT"
    }
  }
}
```

- Deploy a simple HelloWorld application into the already existing environment: 

```
{
  "jpsType": "update",
  "name": "Hello World!",
  "onInstall": {
    "deploy": {
      "archive": "http://app.demo.jelastic.com/HelloWorld.zip",
      "name": "Hello World",
      "context": "ROOT"
    }
  }
}
```

## Running Examples

In order to test the manifest examples presented above, you need to register at any Jelastic hosting provider from the <a href="https://jelastic.cloud" target="_blank">Jelastic Cloud Union</a> first.       
Then, log in to your Jelastic account and perform the following operations: 

1. Copy an appropriate example and save it as a file with **.json** extension.

2. Click the ***Import*** button at the top of your dashboard and select one of the options it contains.        

![import](img/import.jpg)          

3. Depending on the `jpsType` stated at the beginning of the manifest, in the opened **Confirm installation** window you should either select the existing environment or type the preferable name (or leave the default one) for a new one you'd like to create for your application deployment. After that click **Install**.

4. The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.

5. Once these operations are finished, you will see a message about the successful installation completion. It can also contain the text from the `success` manifest section (if it's declared).

## Best Practices

While preparing your own manifest file, we recommend to:

- use JSON formatter and validator (such as <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>)       
- use <a href="https://github.com/" target="_blank">GitHub</a> to store your manifest, scripts and files together
   

## What's next?

### Explore more complex examples:    

Visit the <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> page to find a set of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions.                  

### Learn Template Basics 
See the <a href="http://docs.cloudscripting.com/creating-templates/template-basics/" target="_blank">Template Basics </a> section to learn the required basis of any JSON manifest and find out the differences between *Application* and *Extension*.     

### Write Cloud Scripts  
Cloud Scripting comes with several generic actions out of the box - see the <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a> section to find out the list of them.      

In addition, you have the possibility to prepare and use your own actions within manifest. Such Custom Actions can be scripted either using Java, Javascript or PHP if you need to manage your whole environment or using any intercontainer language, if you need to script something inside of a container.
See the <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">Writing Scripts</a> section.                                 
 
### Build Actions Chain and reuse your code    
Reuse your code and the chain of actions using <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a>                                 

### Automate workflows
Automate workflows using <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">Events</a>

### Define user input parameters 
Customize your app's input parameters that should be specified by a user before the installation. For that, see the <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">Getting User Input</a> documentation page.       

### Use Placeholders 
Learn how to use <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for:                   

- options / parameters which are user-defined or are often changed     
- filtering events   
- selecting containers for your actions     

### Explore Troubleshooting  
Follow the <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Troubleshooting</a> guide if you experience any issues.              