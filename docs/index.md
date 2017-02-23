# Cloud Scripting Overview
Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour related to your application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.                                                                           
<br>
<center>![newoverview](/img/newoverview.png)</center>
<br>
There are three main pillars of cloud scripting:                     
<br>
<ul><li><b>Actions</b> - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">script custom actions</a> using <a href="https://docs.jelastic.com/api/" target="_blank">API calls</a>, Linux bash shell command, JS and Java scripts</li>                

<li><b>Events</b> - specific <a href="http://docs.cloudscripting.com/reference/events/">triggers</a> for executing actions on a required application lifecycle stage</li>                              

<li><b>Injection</b> - supplying default actions, <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">placeholders</a>, platform API methods, environment variables, request parameters and input settings in custom scripts by default</li></ul>                                  
<br>
The developed Cloud Scripting solutions are wrapped into packages and distributed with Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). This is accomplished through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.         
<br>
```
{
  "type": "update",
  "name": "overview",
  "onInstall": [
    {
      "script": "return {result: 0, response: 'test'}"
    },
    {
      "cmd [cp]": "echo 'test' >> /var/log/run.log"
    },
    {
      "api[bl]": "jelastic.environment.control.RestartNodesByGroup"
    },
   {
"createFile [cp]": "/tmp/example.txt"
    },
    "myAction"
  ],
  "onAfterScaleOut [cp]": {
    "myAction": "/tmp/firstFile.txt"
  },
  "actions": {
    "myAction": {
      "forEach(nodes)"...
    }
  }
}

```
<br>
## What’s next?
<br>
<ul><li>Build a simple automation with <a href="/quick-start/" target="_blank">Quick Start</a> Guide</li>                               
<li>Learn how to <a href="/creating-templates/basic-configs/" target="_blank">Create Manifest</a></li>   
<li>Explore the list of available <a href="/reference/actions/" target="_blank">Actions</a></li>     
<li>See the <a href="/reference/events/" target="_blank">Events</a> list the actions can be bound to</li>     
<li>Find out the list of <a href="/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching</li>    
<li>Read how to integrate your <a href="/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a></li>           
<li>Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples</li></ul>                                                    
