# Quick Start 
This guide will walk you through the Cloud Scripting basics and will help you to build and run such simple automation processes like creating new environments and deploying applications.

The required operations should be declared within the appropriate Cloud Scripting manifest, written in [JSON](http://ru.wikipedia.org/wiki/JSON) format.
You can name this file with manifest as you need. The only requirement is that it should have the **.json** extension.
A manifest file can be composed via any text editor; using a modern code editor with the support of JSON syntax highlighting is recommended
(e.g. [JSON Editor Online](http://jsoneditoronline.org/)).

Below you can see two simple examples of how to: 

- Create a new environment and deploy a simple HelloWorld application to it:  

```
{
  "jpsType": "install",
  "application": {
    "name": "Hello World!",
    "env": {
      "topology": {
        "engine": "php5.4",
        "nodes": [
          {
            "nodeType": "apache2",
            "cloudlets": 16
          }
        ]
      }
    },
    "onInstall": {
      "deploy": {
        "archive": "http://app.demo.jelastic.com/HelloWorld.zip",
        "name": "Hello World",
        "context": "ROOT"
      }
    }
  }
}
```

- Deploy a simple HelloWorld application into the already existing environment: 

```
{
  "jpsType": "update",
  "application": {
    "name": "Hello World!",
    "onInstall": {
      "deploy": {
        "archive": "http://app.demo.jelastic.com/HelloWorld.zip",
        "name": "Hello World",
        "context": "ROOT"
      }
    }
  }
}
```

## Running Examples

In order to test the manifest examples presented above, you need to register at any Jelastic hosting providers at [https://jelastic.cloud//](https://jelastic.cloud//) first. 
Then, log in to your Jelastic account and perform the following operations:

1. Copy an appropriate example and save it as a file with **.json** extension.

2. Expand the **New environment** drop-down list at the top left of your dashboard and select the ***Import*** option it contains.

![Import](https://download.jelastic.com/index.php/apps/files_sharing/publicpreview?file=%2F%2Fimport.png&x=1904&a=true&t=0a79155f0039614d04c71840117b9d86&scalingup=0)

3. Depending on the `jpsType` stated at the beginning of the manifest, in the opened **Confirm installation** window you should either select the existing environment or type the preferable name (or leave the default one) for a new one you'd like to create for your application deployment. After that click **Install**.

4. The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.

5. Once these operations are finished, you will see a message about the successful installation completion. It can also contain the text from the `success` manifest section (if it's declared).

## Best Practices

While preparing your own manifest file, we recommend to:

- use JSON formatter and validator (such as [JSON Editor Online](http://jsoneditoronline.org/))
- use [GitHub](https://github.com/) to store your manifest, scripts and files together
   

## What's next?

### Explore more complex examples:

- [Vertical Scaling](/examples/vertical-scaling/)
- [Horizontal Scaling](/examples/horizontal-scaling/)
- [Using Docker&reg;](/examples/using-docker/)
- [WordPress Cluster](/examples/wordpress-cluster/)

### Learn Template Basics
See the [Template Basics](creating-templates/template-basics/) section to learn the required basis of any JSON manifest and find out the differences between *Application* and *Extension*. 

### Write Cloud Scripts  
Cloud Scripting comes with several generic actions out of the box - see the [Actions](/reference/actions/) section to find out the list of them.

In addition, you have the possibility to prepare and use your own actions within manifest. Such Custom Actions can be scripted either using Java, Javascript or PHP if you need to manage your whole environment or using any intercontainer language, if you need to script something inside of a container.
See [Writing Scripts](creating-templates/writing-scripts/).

### Build Actions Chain and reuse your code    
Reuse your code and the chain of actions using [Procedures](/reference/procedures/)

### Automate workflows
Automate workflows using [Events](/reference/events/)

### Define user input parameters 
Customize your app's input parameters that should be specified by a user before the installation. See [Getting User Input](creating-templates/user-input-parameters/) 

### Use Placeholders 
Learn how to use [Placeholders](/reference/placeholders/) for:

- options / parameters which are user-defined or are changed often
- filtering events 
- selecting containers for your actions

### Explore Troubleshooting
Follow the [Troubleshooting](troubleshooting/) guide if you experience any issues.