---
draft: false
title: "Mount Data Storage"
aliases: "/mount-data-storage/"
seoindex: "index, follow"
seotitle: "Mount Data Storage"
seokeywords: "cloud scripting, mount data storage"
seodesc: "Mount data directory from storage node to application server node:"
menu:
    docs:
        title: "Mount Data Storage"
        url: "/mount-data-storage/"
        identifier: "mount-data-storage"
---

# Mount Data Storage

Mount `data` directory from `storage` node to application server node:

```json
{
  "type": "install",
  "name": "mount Data Storage",
  "nodes": [
    {
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
      ],
      "cloudlets": 8,
      "count": 2,
      "nodeGroup": "cp",
      "displayName": "AppServer"
    },
    {
      "image": "jelastic/magento2-storage-sample",
      "cloudlets": 8,
      "nodeGroup": "storage",
      "displayName": "Storage"
    }
  ]
}
```
