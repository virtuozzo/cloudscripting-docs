# Quick Start                                      
    
This guide is designed to assist you with the first steps towards implementing the Cloud Scripting solutions.                                     

To give a try to Cloud Scripting right away, use a basic [Hello World](#hello-world-manifest-example) application sample provided in the section below.                                                                     

And to get up and ready with your own project, fulfill the following requirements:                                   

- decide upon a <a href="http://docs.cloudscripting.com/samples/" target="blank">scenario</a> that will be delivered by means of CS                      
- define a set of <a href="http://docs.cloudscripting.com/creating-templates/template-basics/" target="blank">properties</a> essential for the proper application workflow                     
- declare the required properties within a <a href="http://docs.cloudscripting.com/creating-templates/basic-configs/" target="blank">JPS manifest</a> file                     
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

1. Click the **Import** button at the top pane of the dashboard.                                             

<center>![import-button.png](img/import-button.png)</center>                        

2. Within the opened frame, switch to the **JPS** tab and paste the code provided above (for Hello World app).                      

<center>![import-manifest.png](img/import-manifest.png)</center>               

!!! note
    **Tip:** Within the **Import** frame, two more options are available for JPS deployment:                    
    - <b>*Local File*</b> - to upload the locally stored manifest                             
    - <b>*URL*</b> - to specify direct link to the required file                                         
Clicking on the Examples string nearby will redirect you to Jelastic JPS Collection with numerous ready-to-go solutions (just import the link to the appropriate manifest.jps file to fetch the required one).

