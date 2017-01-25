#Relative Links

The relative links functionality is intended to specify the JPS file’s base URL, in relation to which the subsequent links can be set throughout the manifest. This source destination (URL) can point either to the text of the file or its raw code. Therefore, it is passed in the manifest through the <b>*baseUrl*</b> parameter or specified while <a href="https://docs.jelastic.com/environment-export-import" target="_blank">importing</a> a corresponding JPS file via the Jelastic dashboard.          

!!! note
    > The <b>*baseUrl*</b> value declared within the manifest has higher priority than installation via URL (i.e. <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Import</a>).                

**Example:**
```
{
    "jpsType" : "update",
    "name" : "Base URL test",
    "baseUrl" : "https://github.com/jelastic-jps/minio/blob/master",
    "onInstall" : {
        "log" : "Base URL test"
    },
    "onAfterRestartNode[nodeGroup:cp]" : {
        "script" : "build-cluster.js"
    },
    "success" : "README.md"
}
```

In case of the manifest installation via URL by means of the Jelastic **Import** functionality, the `baseUrl` placeholder will be defined if the specified path is set like in the example below:      
  
```
{protocol}://{domain}/myfile.extension
```
where:                

- <b>*{protocol}*</b> - *http* or *https* protocols              
- <b>*{domain}*</b> - domain name of the website, where the manifest is stored                     
- <b>*myfile.extension*</b> - name of the file with indicated extension (i.e. *jps*) at the end                     

There are the following Cloud Scripting rules applied while parsing a relative path to a file:                         
  - `baseUrl` parameter is being defined                            
  - verification that the linked file’s text doesn't contain whitespaces (including tabs and line breaks)                                     
  - verification that the linked file’s text doesn't contain semicolons and round brackets                                  

If installation is being run from <a href="https://github.com/jelastic-jps" target="_blank">*GitHub*</a> and URL includes <b>*‘/blob/’*</b>, it will be replaced with <b>*‘/raw/’*</b>. In case the `baseUrl` parameter is defined without a slash at the end, it will be added automatically.              

 
The Cloud Scripting engine also supports a `${baseUrl}` placeholder. It can be used throughout the users’ customs scripts (within the [*cmd*](reference/actions/#cmd) and [*script*](reference/actions/#script) actions).              

For example:

```
{
  "jpsType" : "update",
  "name" : "Test Base URL",
  "baseUrl" : "http://example.com/",
  "onInstall" : {
    "cmd [cp]" : {
      "curl -fSs '${baseUrl}script.sh'"
    }
  }
}
```

##Success Text Customization

It is possible to customize the *success* text, which is displayed upon successful application installation either at the dashboard or via email notification, in confines of a manifest.         

- Setting a relative to `baseUrl` link, which points path to the <b>*README.md*</b> file for its content to be displayed within the *success* response.                  
```
{
    "jpsType" : "update",
    "name" : "Success Text first example",
    "baseUrl" : "https://github.com/jelastic-jps/minio",
    "onInstall" : {
        "log" : "success text first example"
    },
    "success" : "README.md"
}
```

- Customizing the *success* return text by means of the external link.                    
```
{
  "jpsType": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
}
```

As it was mentioned above, the success response is distinguished between two values:                        

 - text displayed at the dashboard after application installation is successfully conducted                       
 
```
{
  "jpsType": "update",
  "name": "Success Text Second Example",
  "onInstall": {
    "log": "success Text Second Example"
  },
  "success": {
    "text": "https://github.com/jelastic-jps/lets-encrypt/raw/master/README.md"
  }
}
```
 
 - message delivered via email notifying about the successful application setup                             
 
```
{
  "jpsType": "update",
  "name": "Success Text Test 4",
  "baseUrl": "https://git.jelastic.com/sk/jps-test/raw/master/",
  "onInstall": {
    "log": "success text test 4"
  },
  "success": {
    "email": "README.md",
    "en": "README.md",
    "ru": "https://github.com/jelastic-jps/git-push-deploy/blob/master/README.md"
  }
}
```

In the last example above, the localization functionality is applied, which depends upon the Jelastic Platform selected language.                        