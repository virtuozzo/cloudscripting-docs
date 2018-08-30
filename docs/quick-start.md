# Quick Start                                      
    
This guide is designed to assist you with the first steps towards implementing the Cloud Scripting solutions.                                     

To give a try to Cloud Scripting right away, use a basic [Hello World](#hello-world-manifest-example) application sample, provided below.                                                                     

And to get up and ready with your own project, fulfill the following requirements:                                    

- decide upon a <a href="/samples/" target="_blank">scenario</a> that will be delivered by means of CS                       

- define a set of <a href="/1.6/creating-manifest/basic-configs/" target="_blank">properties</a>, essential for the proper application workflow                  

- declare the required properties within your <a href="/1.6/creating-manifest/basic-configs/" target="_blank">JPS manifest</a> file                      

- deploy the prepared manifest to a Platform via [import](#how-to-deploy-cs-solution-to-jelastic ) functionality                 

## Hello World Manifest Example                      

Hello World is a simple ready-to-go application that you can use as a start point in exploring Cloud Scripting possibilities.                                              
@@@
```yaml
type: install
name: Hello World!
engine: php5.4

nodes:
  nodeType: apache2
  cloudlets: 16

onInstall:
  deploy:
    archive: http://app.demo.jelastic.com/HelloWorld.zip
    name: Hello World
    context: ROOT
```
```json
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
@@!

The current manifest states to create a new environment, handled with **Apache 2** application server on top of **PHP 5.4** engine. After that, the platform will fetch the archive with Hello World app from the specified URL and deploy it to the Apache **ROOT** context.                                   

## How to Deploy CS Solution to Jelastic 

In order to give a try to *Hello World* sample from above (or deploy your own application), enter your <a href="https://jelastic.cloud/" target="_blank">Jelastic Platform</a> account and perform the following steps.                    

1.&nbsp;Click the **Import** button at the top pane of the dashboard.                                             

![import-button.png](img/import-button.png)                        

2.&nbsp;Within the opened frame, switch to the **JPS** tab and paste the code provided above (for Hello World app).                      

![import-manifest.png](img/import-manifest.png)               

!!! note
    **Tip:** Subsequently, you can use this editor to adjust your manifest code on a fly. Clicking on the **Examples** string nearby will redirect you to <a href="https://github.com/jelastic-jps" target="_blank">Jelastic JPS Collection</a> with numerous ready-to-go solutions (just import the link to the appropriate *manifest.jps* file to fetch the required one). Also, two more options for JPS deployment are available here:<ul><li><b>*Local File*</b> - to upload the locally stored manifest</li><li><b>*URL*</b> - to specify direct link to the required file</li></ul>        

To proceed, click on **Import** in the bottom-right corner.                   

3.&nbsp;Within the installation confirmation window, specify domain name for a new **Environment**, set a **Display Name** (i.e. <a href="https://docs.jelastic.com/environment-aliases" target="_blank">alias</a>) for it and select the preferred <a href="https://docs.jelastic.com/environment-regions" target="_blank">region</a> (if available).                  

![hello-world.png](img/hello-world.png)                                        

4.&nbsp;Once the import is completed, you’ll get notification about successful package installation.                                                                              

![open-in-browser.png](img/open-in-browser.png)               

Now you can **Open** your new environment in a **browser** and check the result.                         

![hello-world-startpage.png](img/hello-world-startpage.png)                                   

Just in the same way, you can build and run the solution you need - from frequent tasks automation to implementing complex CI/CD flows and clustering configurations.                               
<br>    
## Best Practises                        

- For advanced coding possibilities, use either <a href="http://jsoneditoronline.org/" target="_blank">JSON Editor Online</a> with automatic formatting and syntax highlighting or <a href="http://www.yaml.org/" target="_blank">YAML</a> parser (depending on the syntax you prefer to work with)                               

- Leverage <a href="https://github.com/" target="_blank">GitHub</a> to store and manage your projects, manifests and scripts all together                              

- Explore <a href="/samples/" target="_blank">Jelastic Samples</a> to benefit on preliminary composed operation and package examples                            

<br> 
<h2> What’s next?</h2>                                     

- <a href="/1.6/creating-manifest/basic-configs/" target="_blank">Basic Configs</a> - learn the minimum basis of any JSP manifest and find out about the differences between *Install* and *Update* package types                                                         

- <a href="/1.6/creating-manifest/actions/" target="_blank">Actions</a> - define the required configurations and application behavior with a set of prescribed procedures                                                           

- <a href="/1.6/creating-manifest/custom-scripts/" target="_blank">Custom Scripts</a> - integrate your own scripts, written in either *Java*, *Javascript* or *PHP*, to subsequently execute them within containers                                                              

- <a href="/1.6/creating-manifest/events/" target="_blank">Events</a> - automate application workflow by binding actions to particular application lifecycle events                                                     

- <a href="/1.6/creating-manifest/visual-settings/" target="_blank">Visual Settings</a> - customize your package visual layout                                                             

- <a href="/1.6/creating-manifest/placeholders/" target="_blank">Placeholders</a> - specify automatically substituted parameters for the required data to be fetched during installation                 

- <a href="/troubleshooting/" target="_blank">Troubleshooting</a> - appeal to this guide if you face any issue while working with Cloud Scripting                                                                           
