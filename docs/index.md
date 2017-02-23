# Cloud Scripting Overview
Jelastic <b>Cloud Scripting (CS)</b> is a tool, designed to program the cloud platform behaviour related to your application lifecycle for automating frequent tasks, complex CI/CD flows and clustering configurations.                                                                           
<br>
<center>![newoverview](/img/newoverview.png)</center>
<br>
There are three main pillars of cloud scripting:
<b>Application Dynamic Behaviour Control:</b> With Cloud Scripting it becomes possible to set a paradigm for application dynamic workflow, which is subject to change depending on the occurring events during its lifecycle. Keeping in mind factors that most likely going to vary from time to time (e.g. big load spikes), CS allows to automatically adjust the proper application functioning according to the changed conditions.                                          
<b>Jelastic API Methods Interconnection:</b> In confines of CS, you can also run your <a href="/creating-templates/writing-scripts/" target="_blank">custom scripts</a>, written in *Java* or *JavaScript*. You can use them to interconnect different <a href="https://docs.jelastic.com/api/" target="_blank">API methods</a> and build kind of action chains. Thus, any action performed by means of API (including running custom user scripts) should be bound to some <a href="http://docs.cloudscripting.com/reference/events/" target="_blank">event</a>. Herewith, an appropriate API action will be executed as a result of this event occurrence.                                             
<b>Placeholders Support:</b> Use of special automatically substituted parameters within your package manifest allows to fetch the required data right during solution installation. In such a way, you get rid of the necessity to hardcode and change the specific user or environment settings upon each package deployment. Such <a href ="http://docs.cloudscripting.com/reference/placeholders/"target="_blank">placeholders</a> can be called within any manifest section (unless its content is strictly limited).                                  

Cloud Scripting output is delivered through Jelastic Packaging Standard (<a href="https://docs.jelastic.com/jps" target="_blank">JPS</a>). In this way, JPS is used to prepare a template (i.e. *manifest.jps* file) declared in <a href="http://www.json.org/" target="_blank">JSON</a> format, that contains data accumulated with the help of CS practices. Eventually, any packaged application can be effortlessly deployed to the Platform by means of <a href="https://docs.jelastic.com/environment-import" target="_blank">import</a> functionality.                             

<h3>What’s next?</h3>

- Build a simple automation with <a href="/quick-start/" target="_blank">Quick Start</a> Guide                           
- Learn how to <a href="/creating-templates/basic-configs/" target="_blank">Create Manifest</a>                    
- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples                            
- Read how to integrate your <a href="/creating-templates/custom-scripts/" target="_blank">Custom Scripts</a>                              
- Explore the list of available <a href="/reference/actions/" target="_blank">Actions</a>                
- See the <a href="/reference/events/" target="_blank">Events</a> list the actions can be bound to                                     
- Find out the list of <a href="/reference/placeholders/" target="_blank">Placeholders</a> for automatic parameters fetching                    