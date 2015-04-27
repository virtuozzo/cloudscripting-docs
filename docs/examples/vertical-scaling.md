# Automatic Vertical Scaling

Adjust Nginx Balancer workers count depending on CPU cores amount:
```example
{
  "jpsType": "update",
  "application": {
    "name": "Nginx Balancer Vertical Scaling",
    "onInstall": {
      "call": "adjustWorkersCount"
    },
    "env": {
      "onAfterSetCloudletCount[nodeType:nginx]": {
        "call": "adjustWorkersCount"
      }
    },
    "procedures": [{
      "id": "adjustWorkersCount",
      "onCall": [{
        "executeShellCommands": {
          "nodeType": "nginx",
          "user" : "root",
          "commands": [
            "sed -i \"s|worker_processes.*|worker_processes $(cat /proc/cpuinfo | grep -c 'cpu cores');|g\" /etc/nginx/nginx.conf",
            "sudo /etc/init.d/nginx reload 2>&1"
          ]
        }
      }]
    }]
  }
}
```

