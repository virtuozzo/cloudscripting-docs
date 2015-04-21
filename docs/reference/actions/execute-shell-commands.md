# ExecuteShellCommands

## Definition

```json
{
  "executeShellCommands": [
    {
      "nodeId": "int or string",
      "nodeType" : "string",
      "nodeMission" : "string",
            
      "commands": [
        "cmd1",
        "cmd2"
      ],
      
      "sayYes" : "boolean"
    }
  ]
}
```

- `nodeId`, `nodeType`, `nodeMission` - parameters that determines containers on which the action should be executed. 
One of these parameters is required. See [Selecting containers for your actions](#selecting-containers-for-your-actions).
- `commands` - a set of commands that gets executed. 
    Its value is wrapped by the underlying Cloud Scripting executor via **echo cmd | base64 -d | su user**. 
    Where:
    - **cmd** equals a Base64 encoded string: **yes | (cmd1;cmd2)**. 
        It means that if your commands requires interactive input, by default the Cloud Scripting executor will always try to give a positive answer using **yes** utility.        
    - **user** - default system user with restricted permissions.
- `sayYes` - optional parameter that enables or disables using of **yes** utility. Defaults to: **true**.    

!!! note 
    The **ExecuteShellCommands** method will fail if any of your commands write something in standard error stream  (**stderr**).
    For example,` wget` and `curl` utils will write their output to _stderr_ by default.   
    To avoid this:
          
    - you can use special flags for _curl_ : `curl -fsS http://example.com/ -o example.txt`
    - or just redirect standard error stream (_stdout_) to standard output stream (_stderr_) if it fits your needs: `curl http://example.com/ -o example.txt 2>&1` 

While accessing containers via **executeShellCommands**, a user receives all required permissions and additionally can manage the main services with sudo commands of the following kind (and others):

```
sudo /etc/init.d/jetty start  
sudo /etc/init.d/mysql stop
sudo /etc/init.d/tomcat restart  
sudo /etc/init.d/memcached status  
sudo /etc/init.d/mongod reload  
sudo /etc/init.d/nginx upgrade  
sudo /etc/init.d/httpd help  
```
     
Examples

Download and unzip a WordPress plugin on all compute nodes:
 
```
{
  "executeShellCommands": [
    {
      "nodeMission": "cp",
      "commands": [
        "cd /var/www/webroot/ROOT/wp-content/plugins/",
        "curl -fsS \"http://example.com/plugin.zip\" -o plugin.zip",
        "unzip plugin.zip"
      ]
    }
  ]
}
```
The same could be done by unpack method: --link--


Using **sudo** to reload **Nginx** balancer:
```
{
  "executeShellCommands": [
    {
      "nodeType": "nginx",
      "commands": [
        "sudo /etc/init.d/nginx reload"
      ]
    }
  ]
}
```