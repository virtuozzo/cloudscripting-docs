````markdown
# Using Docker&reg;

Create and link WordPress Web and WordPress DB containers:

```json
{
  "type": "install",
  "name": "Wordpress",
  "homepage": "http://wordpress.org/",
  "description": "WordPress is web software you can use to create a beautiful website or blog.",
  "nodes": [
    {
      "nodeType": "docker",
      "cloudlets": 16,
      "displayName": "App Server",
      "nodeGroup": "cp",
      "image": "jelastic/wordpress-web:latest",
      "links": "db:DB"
    },
    {
      "nodeType": "docker",
      "cloudlets": 16,
      "displayName": "Database",
      "nodeGroup": "db",
      "image": "jelastic/wordpress-db:latest"
    }
  ],
  "onInstall": {
    "restartContainers": {
      "nodeGroup": "cp"
    }
  }
}
```

````
