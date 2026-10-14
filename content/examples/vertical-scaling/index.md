---
draft: false
title: "Automatic Vertical Scaling"
aliases: "/vertical-scaling/"
seoindex: "index, follow"
seotitle: "Automatic Vertical Scaling"
seokeywords: "cloud scripting, automatic vertical scaling"
seodesc: "Adjust Nginx Balancer workers count depending on CPU cores amount: example { \"type\": \"update\", \"name\": \"Nginx Balancer Vertical Scaling\", \"onInstall\""
menu:
    docs:
        title: "Automatic Vertical Scaling"
        url: "/vertical-scaling/"
        identifier: "vertical-scaling"
---

# Automatic Vertical Scaling

Adjust Nginx Balancer workers count depending on CPU cores amount:
```example
{
  "type": "update",
  "name": "Nginx Balancer Vertical Scaling",
  "onInstall": "adjustWorkersCount",
  "onAfterSetCloudletCount[nodeType:nginx]": "adjustWorkersCount",
  "actions": {
    "adjustWorkersCount": {
      "execmCmd [nodeType:nginx]": "sed -i \"s|worker_processes.*|worker_processes $(cat /proc/cpuinfo | grep -c 'cpu cores');|g\" /etc/nginx/nginx.conf; sudo /etc/init.d/nginx reload 2>&1"
    }
  }
}
```
