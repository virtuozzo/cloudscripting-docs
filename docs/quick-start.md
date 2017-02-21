<h1>Quick Start</h1> 
<p dir="ltr" style="text-align: justify;">This guide will walk you through the Cloud Scripting basics and will help you to build and run such simple automation processes like creating new environments and deploying applications.</p>

<p dir="ltr" style="text-align: justify;">The required operations should be declared within the appropriate Cloud Scripting manifest, written in <a href="http://www.json.org/" target="_blank">JSON</a> format. You can name this file with manifest as you need. The only requirement is that it should have the <b>.json</b> extension. The manifest file can be composed via any text editor, using a modern code editor with the support of JSON syntax highlighting is recommended (e.g. <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>).</p>        

Below you can see two simple examples of how to: 

- Create a new environment and deploy a simple HelloWorld application to it: 

```
{
  "type": "install",
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

<p dir="ltr" style="text-align: justify;">In order to test the manifest examples presented above, you need to register at any Jelastic hosting provider from the <a href="https://jelastic.cloud" target="_blank">Jelastic Cloud Union</a> first.</p>       

Then, log in to your Jelastic account and perform the following operations: 

<ul><li>Copy an appropriate example and save it as a file with <b>.json</b> extension.</li>   
<li>Click the <b>Import</b> button at the top of your dashboard and select one of the options it contains.</li>        

<center>![import](img/import.jpg)</center>          

<li>Depending on the `type` stated at the beginning of the manifest, in the opened <b>Confirm installation</b> window, you should either select the existing environment or type the preferable name (or leave the default one) for a new one you'd like to create for your application deployment. After that click <b>Install</b>.</li>
<li>The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.</li>
<li>Once these operations are finished, you will see a message about the successful installation completion. It can also contain <a href="http://docs.cloudscripting.com/creating-templates/relative-links/#success-text-customization" target="blank">custom text</a> from the `success` manifest section (if it's declared).</li></ul>

<h2>Best Practices</h2>

While preparing your own manifest file, we recommend to:
<ul><li>use JSON formatter and validator (such as <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a>)</li>         
<li>use <a href="https://github.com/" target="_blank">GitHub</a> to store your manifest, scripts and files together</li></ul>  
   

<h2>What's next?</h2>

<h3>Explore More Complex Examples:</h3>    

<p dir="ltr" style="text-align: justify;">Visit the <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> page to find a set of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions.</p>                      

<h3>Learn Template Basics</h3> 
<p dir="ltr" style="text-align: justify;">See the <a href="http://docs.cloudscripting.com/creating-templates/template-basics/" target="_blank">Template Basics </a> section to learn the required basis of any JSON manifest and find out the differences between <em>Application</em> and <em>Extension</em>.</p>     

<h3>Write Cloud Scripts</h3>  
<p dir="ltr" style="text-align: justify;">Cloud Scripting comes with several generic actions out of the box - see the <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a> section to find out the list of them.</p>      

<p dir="ltr" style="text-align: justify;">In addition, you have the possibility to prepare and use your own actions within manifest. Such Custom Actions can be scripted either using Java, Javascript or PHP if you need to manage your whole environment or using any intercontainer language, if you need to script something inside of a container.
See the <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">Writing Scripts</a> section.</p>                                 
 
<h3>Build Actions Chain and Reuse Code</h3>    
<p dir="ltr" style="text-align: justify;">Reuse your code and the chain of actions using <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a></p>                                

<h3>Automate Workflows</h3>
<p dir="ltr" style="text-align: justify;">Automate workflows using <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">Events</a></p>

<h3>Define User Input Parameters</h3> 
<p dir="ltr" style="text-align: justify;">Customize your app's input parameters that should be specified by a user before the installation. For that, see the <a href="http://docs.cloudscripting.com/creating-templates/user-input-parameters/" target="_blank">Getting User Input</a> documentation page.</p>            

<h3>Use Placeholders</h3> 
<p dir="ltr" style="text-align: justify;">Learn how to use <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for:</p>                   
<ul><li>options and parameters which are user-defined or are often changed</li>     
<li>filtering events</li>   
<li>selecting containers for your actions</li></ul>     

<h3>Explore Troubleshooting</h3>   
<p dir="ltr" style="text-align: justify;">Follow the <a href="http://docs.cloudscripting.com/troubleshooting/" target="_blank">Troubleshooting</a> guide if you experience any issues.</p>              