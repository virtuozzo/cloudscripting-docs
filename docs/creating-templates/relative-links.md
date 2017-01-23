#Relative Links

A relative link takes advantage of the fact that the server knows where the current manifest is loaded.  
Relative link specifies the external link which contains a text of file. It can be used in case when manifest contains parameter `baseUrl` or manifest installation is defined via URL in <a href="https://docs.jelastic.com/environment-export-import" target="_blank">Import feature</a>.  

`baseUrl` inside manifest has higher priority than installation by URL.

Simple example:
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

In case manifest is installing by URL via Import Jelastic feature than `baseUrl` placeholder will defined if URL like example bellow:
  
```
{protocol}://{domain}/myfile.extension
```
In the end of URL should be file name with extension. 

Cloud Scriptiong rules for parsing relative path for file:

  - `baseUrl` parameter is defined;
  - text doesn't contain whitespaces (includes tabs, line breaks);
  - text doesn't contain semicolons and round brackets.

If installation is going from <a href="https://github.com/jelastic-jps" target="_blank">*GitHub*</a> and URL is consists */blob/* - it will replaced to */raw/* word.
if `baseUrl` parameter is defined without slash in the end, it will be added automatically.
 
Cloud Scripting engine supports placeholder `${baseUrl}`. Every customer can use it in their customs scripts (in [`cmd`](actions/#cmd), [`script`](actions/#script) actions).

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

##Success Text Customize

Ability to customize `success` text inside manifest. See examples bellow:

- set [`baseUrl`](creating-templates/relative-links/) relative URL which is based path for README.md file in success text:
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

- customizing `success` text by external link:
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

`Success` text can be divided on two values:

 - text on dashboard when application will be installed
 
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
 
 - text to notify user about successfull application installation by email
 
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

Last example also shows localization functionality depends on Jelastic platform selected language. 