# Cloud Scripting Overview
<p dir="ltr" style="text-align: justify;">Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour related to your application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.</p>                                         
    
<center>![newoverview](/img/newoverview.png)</center>
  
There are three main pillars of cloud scripting:   
<ul><li><p dir="ltr" style="text-align: justify;">- <b>Actions</b> - scripted logic for executing a set of commands to automate the tasks. The system provides a default list of actions and possibility to <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">script custom actions</a> using <a href="https://docs.jelastic.com/api/" target="_blank">API calls</a>, Linux bash shell command, JS and Java scripts</p></li>                                                           
<li><p dir="ltr" style="text-align: justify;">- <b>Events</b> - specific <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">triggers</a> for executing actions on a required application lifecycle stage</p></li>                                                                        
<li><p dir="ltr" style="text-align: justify;">- <b>Injection</b> - supplying default actions, <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">placeholders</a>, platform API methods, environment variables, request parameters and input settings in custom scripts by default</p></li></ul>                                                             
  
<p dir="ltr" style="text-align: justify;">The developed Cloud Scripting solutions are wrapped into packages and distributed with Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). This is accomplished through preparing a manifest file in JSON format. Such packaged solutions can be effortlessly deployed to the platform via <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.</p>                                   

## What’s next?


- Build a simple automation with <a href="http://docs.cloudscripting.com/quick-start/" target="_blank">Quick Start</a> Guide                            
- Learn how to <a href="http://docs.cloudscripting.com/creating-templates/template-basics/" target="_blank">Create Manifest</a>                           
- Explore the list of available <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">Actions</a>                               
- See the <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">Events</a> list the actions can be bound to                        
- Find out the list of <a href="http://docs.cloudscripting.com/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching                   
- Read how to integrate your <a href="http://docs.cloudscripting.com/creating-templates/writing-scripts/" target="_blank">Custom Scripts</a>                          
- Examine a bunch of <a href="http://docs.cloudscripting.com/samples/" target="_blank">Samples</a> with operation and package examples                   
                    