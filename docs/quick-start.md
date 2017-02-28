<h1>Quick Start</h1> 
<p dir="ltr" style="text-align: justify;">This guide will walk you through the Cloud Scripting basics and will help you to build and run such simple automation processes like creating new environments and deploying applications.</p>

<p dir="ltr" style="text-align: justify;">The required operations should be declared within the appropriate Cloud Scripting manifest, written in <a href="http://www.json.org/" target="_blank">JSON</a> format. You can name this file with manifest as you need. The only requirement is that it should have the <b>.json</b> extension. The manifest file can be composed via any text editor, using a modern code editor with the support of JSON syntax highlighting is recommended (e.g. <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>).</p>
The required operations should be declared within the appropriate Cloud Scripting manifest, written in <a href="http://www.json.org/" target="_blank">JSON</a> or <a href="http://www.yaml.org/" target="_blank">YAML</a> format. You can name this file with manifest as you need. The only requirement is that it should have the <b>*.jps*</b> extension. The manifest file can be composed via any text editor, using a modern code editor with the support of JSON or YAML syntax highlighting are recommended (e.g. <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a> or <a href="http://yaml-online-parser.appspot.com/" target="_blank">YAML</a>).        

Below you can see two simple examples of how to: 

- Create a new environment and deploy a simple HelloWorld application to it: 

``` json
{
  "type": "install",
  "name": "Hello World!",
  "engine": "php5.4",
  "nodes": {
    "nodeType": "apache2",
    "cloudlets": 16
  },
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

``` json
{
  "type": "update",
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

<h2>Running Examples</h2>

In order to test the manifest examples presented above, you need to register at any Jelastic hosting provider from the <a href="https://jelastic.cloud" target="_blank">Jelastic Cloud Union</a> first.       

Then, log in to your Jelastic account and perform the following operations: 

- Copy an appropriate example and save it as a file with <b>.json</b> extension.   
- Click the ***Import*** button at the top of your dashboard and select one of the options it contains.        

<center>![newimport](img/newimport.png)</center>          

- Depending on the `type` stated at the beginning of the manifest, in the opened <b>Confirm installation</b> window, you should either select the existing environment or type the preferable name (or leave the default one) for a new one you'd like to create for your application deployment. After that click <b>Install</b>.
- The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.
- Once these operations are finished, you will see a message about the successful installation completion. It can also contain <a href="http://docs.cloudscripting.com/creating-templates/relative-links/#success-text-customization" target="blank">custom text</a> from the `success` manifest section (if it's declared).

## Best Practices</h2>
While preparing your own manifest file, we recommend to:

- use JSON formatter and validator (such as <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>)         
- use <a href="https://github.com/" target="_blank">GitHub</a> to store your manifest, scripts and files together  

## What's next?

### Learn Template Basics

See the <a href="http://docs.cloudscripting.com/creating-templates/template-basics/" target="_blank">Basic Configs </a> section to learn the required basis of any JSON manifest and find out the differences between <em>Application</em> and <em>Extension</em>.    

### Write Cloud Scripts  

In addition, you have the possibility to prepare and use your own actions within manifest. Such Custom Actions can be scripted either using Java, Javascript or PHP if you need to manage your whole environment or using any intercontainer language, if you need to script something inside of a container.
See the <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">Writing Scripts</a> section.

### Build Actions Chain and Reuse Code        

Reuse your code and the chain of actions using <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a>.

### Automate Workflows

Automate workflows using <a href="/reference/events/" target="_blank">Events</a>                

### Define User Input Parameters

Customize your app's input parameters that should be specified by a user before the installation. For that, see the <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">Getting User Input</a> documentation page.            

### Use Placeholders

Learn how to use <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for:                         

- options and parameters which are user-defined or are often changed</li>     
- filtering events</li>   
- selecting containers for your actions</li></ul>     

### Explore Complex Examples

Visit the <a href="/samples/" target="_blank">Samples</a> page to find a set of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions.                    

### Explore Troubleshooting   

Follow the <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Troubleshooting</a> guide if you experience any issues. See the <a href="/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a> section.                                 
 
     