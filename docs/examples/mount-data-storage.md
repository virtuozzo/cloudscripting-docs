#Mount Data Storage

Mount `data` directory from `storage` node to application server node:

```
{
  "jpsType": "install",
  "application": {
    "name": "mount Data Storage",
    "env": {
      "topology": {
        "nodes": [
          {
            "docker": {
              "volumeMounts": {
                "/var/www/webroot/ROOT": {
                  "readOnly": false,
                  "sourcePath": "/data",
                  "sourceNodeGroup": "storage"
                }
              },
              "image": "jelastic/magento2-nginxphp:1.8.0-php5.6.20",
              "volumes": [
                "/var/www/webroot/ROOT"
              ]
            },
            "cloudlets": 8,
            "count": 2,
            "nodeGroup": "cp",
            "displayName": "AppServer"
          },
          {
            "docker": {
              "image": "jelastic/magento2-storage-sample"
            },
            "cloudlets": 8,
            "nodeGroup": "storage",
            "displayName": "Storage"
          }
        ]
      }
    }
  }
}
```

