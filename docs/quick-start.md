# Quick Start                                      
    
This guide is designed to assist you with the first steps towards implementing the Cloud Scripting solutions.                                     

To give a try to Cloud Scripting right away, use a basic [Hello World](#hello-world-manifest-example) application sample provided in the section below.                                                                     

And to get up and ready with your own project, fulfill the following requirements:                                   

- decide upon a <a href="/samples/" target="blank">scenario</a> that will be delivered by means of CS                      
- define a set of <a href="/creating-templates/basic-configs/" target="blank">properties</a> essential for the proper application workflow                     
- declare the required properties within a <a href="/creating-templates/basic-configs/" target="blank">JPS manifest</a> file                     
- deploy the prepared manifest to a Platform via [import](#how-to-deploy-cs-solution-to-jelastic ) functionality               

## Hello World Manifest Example                      

Hello World is a simple ready-to-go application that you can use as a start point for exploring Cloud Scripting.                          

```json
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

The current manifest states to create a new environment, handled with **Apache 2** application server on top of **PHP 5.4** engine. After that, the platform will fetch the archive with Hello World app from the specified URL and deploy it to the Apache **ROOT** context.                                   

## How to Deploy CS Solution to Jelastic 

In order to give a try to *Hello World* sample from above (or deploy your own application), enter your <a href="https://jelastic.cloud/" target="blank">Jelastic Platform</a> account and perform the following steps.                    

1.Click the **Import** button at the top pane of the dashboard.                                             

<center>![import-button.png](img/import-button.png)</center>                        

2.Within the opened frame, switch to the **JPS** tab and paste the code provided above (for Hello World app).                      

<center>![import-manifest.png](img/import-manifest.png)</center>               

!!! note
    **Tip:** Within the **Import** frame, two more options are available for JPS deployment:                    
- <b>*Local File*</b> - to upload the locally stored manifest                              
- <b>*URL*</b> - to specify direct link to the required file                                           
Clicking on the **Examples** string nearby will redirect you to <a href="https://github.com/jelastic-jps" target="blank">Jelastic JPS Collection</a> with numerous ready-to-go solutions (just import the link to the appropriate *manifest.jps* file to fetch the required one).                        

To proceed, click on **Import** in the bottom-right corner.                   

3.Within the installation confirmation window, specify domain name for a new **Environment**, set **Display Name** (i.e. <a href="https://docs.jelastic.com/environment-aliases">alias</a>) for it and select the preferred <a href="https://docs.jelastic.com/environment-regions">region</a> (if available).                  

<center>![hello-world.png](img/hello-world.png)</center>                                        

4.Once the import is completed, you’ll be shown the successful installation window.                                      

<center>![open-in-browser.png](img/open-in-browser.png)</center>               

Here, **Open** your new environmental **in browser** to check the result.                     

<center>![hello-world-startpage.png](img/hello-world-startpage.png)</center>                                   

Just in the same way, you can build and run the solution you need - from frequent tasks automation to implementing complex CI/CD flows and clustering configurations.                               

!!! note
    **Tip:** Consider using a repository hosting service (for example, <a href="https://github.com/" target="blank">GitHub</a>) to comfortably store and manage your projects, manifests and scripts all together.                               
<br>    
## Best Practises               

- Use <a href="http://jsoneditoronline.org/" target="blank">JSON Editor Online</a> with the automatic formatting and syntax highlighting                    
- Use <a href="http://www.yaml.org/" target="blank">YAML</a> parser to edit manifest code in YAML format                         
- Use <a href="https://github.com/" target="blank">GitHub</a> to store and manage your projects, manifests and scripts all together                           
- Use <a href="/samples/" target="blank">Jelastic Samples</a> to explore operation and package examples                       

<br> 
## What’s next?              

- <a href="/creating-templates/basic-configs/" target="blank">Template Basics</a> - learn the required basis of any JSP manifest and find out about differences between *Install* and *Update* installation types.                             

- <a href="/reference/actions/" target="blank">Actions</a> - define the required configuration properties and declare expected application behavior with the help of appropriate actions that Cloud Scripting offers out of the box.                     

- <a href="/creating-templates/custom-scripts/" target="blank">Custom Scripts</a> - prepare and use your own custom actions within a manifest. Such actions can be scripted either using *Java*, *Javascript* or *PHP* in order to manage the whole environment. To execute scripts inside of a container, use any intercontainer language.                         

- <a href="/reference/events/" target="blank">Events</a> - automate application workflow by bounding actions to a particular application lifecycle event.                        

- <a href="/creating-templates/user-input-parameters/" target="blank">Visual Settings</a> - customize your application visual layout before the installation.                     

- <a href="/reference/placeholders/" target="blank">Placeholders</a> - specify automatically substituted parameters within your manifest that are fetched during installation.                          

- <a href="/samples/" target="blank">Samples</a> - find a set of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions.                        

- <a href="/troubleshooting/" target="blank">Troubleshooting</a> - appeal to this guide, if you face any issue, while working with Cloud Scripting.                                     
