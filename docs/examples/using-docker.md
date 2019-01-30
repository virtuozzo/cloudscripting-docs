# Using Docker&reg;

Create and link WordPress Web and WordPress DB containers: 

```example
{
  "type": "install",
  "application": {
    "name": "Wordpress",            
    "homepage": "http://wordpress.org/",
    "description": "WordPress is web software you can use to create a beautiful website or blog. We like to say that WordPress is both free and priceless at the same time.",
    "env": {
      "topology": {
        "nodes": [
          {
            "nodeType": "docker",            
            "cloudlets" : 16,
            "displayName": "App Server",
            
            "docker" : {
              "nodeGroup" : "cp",
              "image" : "jelastic/wordpress-web:latest",
              "links" : "db:DB"
            }
          },
          {
            "nodeType": "docker",            
            "cloudlets" : 16,
            "displayName": "Database",
            
            "docker" : {
              "nodeGroup" : "db",
              "image" : "jelastic/wordpress-db:latest"
            }
          }
        ]
      }
    },                     
    "onInstall" : {
      "restartContainers" : {
          "nodeGroup" : "cp"
      }
    }
  }
}
```
