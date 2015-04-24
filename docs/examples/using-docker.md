# Using Docker&reg;

```
{
  "jpsVersion": "0.3",
  "jpsType": "install",
  "application": {
    "name": "Wordpress",
    "version": "latest",
    "logo": "https://download.jelastic.com/public.php?service=files&t=3da2215839f82aa50d3d961271cd1cb9&download",
    "type": "php",
    "homepage": "http://wordpress.org/",
    "description": {
      "text": "WordPress is web software you can use to create a beautiful website or blog. We like to say that WordPress is both free and priceless at the same time."
    },
    "env": {
      "topology": {
        "ha": false,
        "ssl": false,
        "nodes": [
          {
            "nodeType": "docker",
            "extip": false,
            "count": 1,
            "fixedCloudlets": 1,
            "flexibleCloudlets": 16,
            "fakeId": -1,
            "dockerName": "jelastic/wordpress-web",
            "dockerTag": "latest",
            "dockerLinks": [
              {
                "sourceNodeId": -1,
                "targetNodeId": "-2",
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
            "extip": false,
            "count": 1,
            "fixedCloudlets": 1,
            "flexibleCloudlets": 16,
            "fakeId": -2,
            "dockerName": "jelastic/wordpress-db",
            "dockerTag": "latest",
            "dockerEnvVars": {
              "MYVAR_EXAMPLE2": "example2"
            },
            "displayName": "jelastic/wordpress-db:latest",
            "metadata": {
              "layer": "storage"
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