# Actions

Actions are the building blocks that can perform arbitrary automation tasks in your environments.
For example:

- increase/decrease CPU or RAM amount  
- adjust configs according to specific environment parameters
- restart a service
- restart a container
- apply a database patch according to specific environment parameters  
...     

Default workflow for any action:

- replace [Placeholders](placeholders/)
- get target containers list *[optional]* (see the [Selecting Containers For Your Actions](#selecting-containers-for-your-actions) section) 
- check rights
- execute the action itself

Actions can be executed when an [Event](events/) with a matching filter is triggered. 
Multiple Actions can be combined together into a [Procedure](procedures/). 
Each Procedure could be executed with different input parameters using [Call](#call) action. 

## Container Operations
Actions that performs some operations inside of a container. See [Selecting Containers For Your Actions](creating-templates/selecting-containers/).

Any container operation could be done using [ExecuteShellCommands](#executeshellcommands) action. 
Nevertheless, there are also a several actions provided for convenience.
All of them could be separated in three groups:

- SSH commands ([ExecuteShellCommands](#executeshellcommands))
- Predefined modules ([Deploy](#deploy), [Upload](#upload), [Unpack](#unpack))
- File operations ([CreateFile](#createfile), [CreateDirectory](#createdirectory), [WriteFile](#writefile), [AppendFile](#appendfile), [ReplaceInFile](#replaceinfile))   
 
!!! note 
    > To perform any Container Operation except [ExecuteShellCommands](#executeshellcommands) Cloud Scripting executor will use a default system user with restricted permissions.    
   
### ExecuteShellCommands
Execute a several SSH commands.

**Definition**

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

```no-highlight
sudo /etc/init.d/jetty start  
sudo /etc/init.d/mysql stop
sudo /etc/init.d/tomcat restart  
sudo /etc/init.d/memcached status  
sudo /etc/init.d/mongod reload  
sudo /etc/init.d/nginx upgrade  
sudo /etc/init.d/httpd help;  
```                                                        
     
**Examples**  

Execute bash script from URL for all Tomcat 6 nodes:

```example
{
  "executeShellCommands": [
    {
      "nodeType": "tomcat6",
      "commands": [
        "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
      ]
    }
  ]
}

```
                             
Download and unzip a WordPress plugin on all compute nodes: 
```example
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

```example
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
        
### Deploy
```
{
  "deploy": [
    {
      "archive": "URL",
      "name": "string",
      "context": "string"
    }
  ]
}
```

### Upload
```
{
  "upload": [
    {
      "nodeId": "number",
      "nodeType": "string",
      "nodeMission": "string",
      
      "sourcePath" : "URL",
      "destPath" : "string"
    }
  ]
}
```
### Unpack
### CreateFile
### CreateDirectory
### WriteFile
### AppendFile
### ReplaceInFile
<!-- DeletePath -->
<!-- RenamePath --> 

## Topology Nodes Management

### AddNodes
### SetCloudletsCount
### SetNodeDisplayName
### RestartNodes
### AddContext

## Database Operations

### PrepareSqlDatabase
### RestoreSqlDump
### ApplySqlPatch

## Performing User-Defined Operations

### Call
Call arbitrary [Procedure](procedures/)

### ExecuteScript
paste examples link
### InstallAddon