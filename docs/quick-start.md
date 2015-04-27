# Quick Start 
This guide will walk you through Cloud Scripting basics and help you build and run a simple automation: create new environment and deploy application.

To create an appropriate Cloud Scripting manifest [JSON](http://ru.wikipedia.org/wiki/JSON) format should be used.
You can name the file with manifest as you need. The only requirement is that it should be saved in **.json** extension.
A manifest file can be composed in any text editor, using a modern code editor with support for JSON syntax highlighting is recommended
(e.g. [JSON Editor Online](htp://jsoneditoronline.org/)).

The following are a two simple examples of how to create new environment and deploy a simple HelloWorld application. 

Create new environment and deploy HelloWorld example:  

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
        "archive": "http://app.cloudscripting.com/HelloWorld.zip",
        "name": "Hello World",
        "context": "ROOT"
      }
    }
  }
}
```

Deploy HelloWorld example in an existing environment: 

```
{
  "jpsType": "update",
  "application": {
    "name": "Hello World!",
    "onInstall": {
      "deploy": {
        "archive": "http://app.cloudscripting.com/HelloWorld.zip",
        "name": "Hello World",
        "context": "ROOT"
      }
    }
  }
}
```

## Runing Examples

Log in to your Jelastic account and follow the instruction below.

1. Copy an appropriate example and save it as a file with **.json** extension.
2. Expand the New environment list at the top left of your dashboard and choose the Import option it contains.
![Import](https://download.jelastic.com/index.php/apps/files_sharing/publicpreview?file=%2F%2Fimport.png&x=1904&a=true&t=0a79155f0039614d04c71840117b9d86&scalingup=0)
3. In the opened **Confirm installation** of application window, depending on `jpsType` select environment or type the preferable name (or leave the default one) for the environment you would like to create for your application deployment and click Install.
4. The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.
5. After these operations are completed, you will see a success message that could contain information from manifest's `success` section.

## Best Practices

- use JSON formatter and validator (such as [JSON Editor Online](htp://jsoneditoronline.org/))
- use [GitHub](https://github.com/) to keep your manifest, scripts and files together
   

## What's next?

### Explore more complex examples:

- [Vertical Scaling](/examples/vertical-scaling/)
- [Horizontal Scaling](/examples/horizontal-scaling/)
- [Using Docker&reg;](/examples/using-docker/)
- [WordPress Cluster](/examples/wordpress-cluster/)

### Learn Template Basics
Learn template basics and the differences between Application and Extension. See [Template Basics](creating-templates/template-basics/) section.  

### Write Cloud Scripts  
Cloud Scripting comes with a several generic actions out of the box. See [Actions](/reference/actions/) section.

Custom Actions could be scripted using Java, Javascript or PHP if you need to manage the whole your environment and any intercontainer language if you need to script something inside of a container.
See [Writing Scripts](creating-templates/writing-scripts/).

### Build Actions Chain and reuse your code    
Reuse your code and actions chain using [Procedures](/reference/procedures/)

### Automate workflows
Automate workflows using [Events](/reference/events/)

### Define user input parameters 
Customize your app input parameters. See [Getting User Input](creating-templates/user-input-parameters/) 

### Use Placeholders 
Learn how to use [Placeholders](/reference/placeholders/) for:

- options / parameters which are user defined or change often
- events filtering
- selecting containers for your actions

### Explore Troubleshooting guide
Follow [Troubleshooting](troubleshooting/) guide if something goes wrong.