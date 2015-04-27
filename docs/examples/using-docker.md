# Using Docker&reg;

Create and link WordPress Web and WordPress DB containers: 
```example
{
  "jpsType": "install",
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
            "fakeId": "web",
            "dockerName": "jelastic/wordpress-web",
            "dockerTag": "latest",
            "dockerLinks": [
              {
                "sourceNodeId": "web",
                "targetNodeId": "db",
                "alias": "DB"
              }
            ],
            "dockerEnvVars": {
              "MYVAR_EXAMPLE1": "example1"
            },
            "displayName": "jelastic/wordpress-web:latest",
            "metadata": {
              "layer": "cp"
            }
          },
          {
            "nodeType": "docker",                                    
            "cloudlets": 16,
            "fakeId": "db",
            "dockerName": "jelastic/wordpress-db",
            "dockerTag": "latest",
            "dockerEnvVars": {
              "MYVAR_EXAMPLE2": "example2"
            },
            "displayName": "jelastic/wordpress-db:latest",
            "metadata": {
              "layer": "sqldb"
            }
          }
        ]
      }
    },
    "onInstall" : {
      "restartNodes" : [{
          "nodeType" : "docker"
      }
    }
  }
}
```