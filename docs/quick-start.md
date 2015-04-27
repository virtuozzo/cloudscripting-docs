# Quick Start 
This guide will walk you through Cloud Scripting basics and help you build and run a simple automation: a rule that triggers an action on external event.

To create an appropriate Cloud Scripting manifest [JSON](http://ru.wikipedia.org/wiki/JSON) format should be used.
You can name the file with manifest as you need. The only requirement is that it should be saved in **.json** extension.
A manifest file can be composed in any text editor, using a modern code editor with support for JSON syntax highlighting is recommended
(e.g. [JSON Eitor Online](htp://jsoneditoronline.org/)).

The following are a two simple examples to give you an idea of how Cloud Scripting is structured.

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


## Runing Examples
Log in to your Jelastic account and follow the instruction below.

1. Copy an appropriate example and save it as a file with **.json** extension.
2. Expand the New environment list at the top left of your dashboard and choose the Import option it contains.
![Import](https://download.jelastic.com/index.php/apps/files_sharing/publicpreview?file=%2F%2Fimport.png&x=1904&a=true&t=0a79155f0039614d04c71840117b9d86&scalingup=0)
3. In the opened **Confirm installation** of application window, type the preferable name (or leave the default one) for the environment you would like to create for your application deployment and click Install.
4. The process of installation will be started. Wait a minute for Preparing, Deploying and Configuring to be finished.
5. After these operations are completed, you will see a success message that could contain information from manifest's `success` section.

1. Choose what you would like to create. An Application or an Extention?
2. editor [JSON Eitor Online](htp://jsoneditoronline.org/)


3. scripts storage (GitHub!)
4. bind installation event
5.
5. explore actions

Cloud Scripting comes with a several generic actions out of the box.
Custom Actions could be scripted using Java, Javascript or PHP.  See [Writing Scripts](writing-scripts/).

reuse your code and actions chain using [Procedures](/reference/procedures/)
automate workflows using [Events](/reference/events/)
customize your app input parameters
use placeholders for
    options / parameters which are user defined or change often
    events filtering
    selecting containers for your actions

hello world tutorial 

## Troubleshooting
Follow [Troubleshooting](troubleshooting/) guide
