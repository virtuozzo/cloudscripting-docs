#Docker Actions

Specific Cloud Scripting actions for Docker containers include operations of *volumes*, *links* and *environment variables* management.
<br>
##Volumes

There are three available parameters to set Docker `volumes`:  
- `volumes` - list of volume paths   
- `volumeMounts` - mount configurations  
- `volumesFrom` - list of nodes the volumes are imported from    

All of the fields are set within the Docker object:
```
{
  "env": {
    "topology": {
      "nodes": [
        {
          "nodeGroup": "sqldb",
          "docker": {
            "image": "centos:7",
            "volumes": [...],
            "volumeMounts": {...},
            "volumesFrom": [...]
          }
        }
      ]
    }
  }
}
```
###Volumes  
This field represents a string array:  
```
[
  {
    "volumes": [
      "/external",
      "/data",
      "/master",
      "/local"
    ]
  }
]
```

###VolumeMounts   
This parameter is an object. It can be set like within the example below:    
```
{
  "volumeMounts": {
    "/example-path": {
      "sourcePath": "",
      "sourceNodeId": 0,
      "sourceNodeGroup": "",
      "sourceHost": "",
      "readOnly": true
    }
  }
}
```
Here:  
- `/example-path` - path to place the volume at a target node  
- `sourcePath [optional]` - the default value repeats volume path (*/example-path* in our sample)   
- `sourceNodeId` -  node identifier the volume should be mounted from (optional in case of the `sourceNodeGroup` parameter using)  
- `sourceHost [optional]` - parameter for <u>[external mounts](https://docs.jelastic.com/configure-external-nfs-server)</u> usage  
- `readOnly` - defines write data permissions at source node; the default value is `false`   
- `sourceNodeGroup` - any available *nodeGroup* within source environment (ignored if the `sourceNodeId` parameter is specified). The list of mounted volumes is defined by a master node.    

In case not all source node volumes are required to be mounted, the particular ones can be specified:
```
[
  {
    "sourceNodeGroup": "storage",
    "volumes": [
      "/master",
      "/local"
    ]
  }
]
```

####*VolumeMounts* examples   
 
**Master Node Mount:**   
Samples to mount a particular volume by exact node identifier & path (*/master*), and to mount all volumes from the layer master node by *nodeGroup* (*/master-1*)
```
{
  "volumeMounts": {
    "/master": {
      "sourcePath": "/master",
      "sourceNodeId": 81725,
      "readOnly": true
    },
    "/master-1": {
      "sourceNodeGroup": "current-node-group"
    }
  }
}
```

Here, *sourcePath* and *readOnly* parameters are optional.

**Mount Data Container:**
<br>
Samples to mount all volumes from a particular node by exact node identifier & path (*/node*) and to mount master node volumes by *nodeGroup* type (*/data*)

```
{
  "volumeMounts": {
    "/node": {
      "sourceNodeId": 45
    },
    "/data": {
      "sourceNodeGroup": "storage"
    }
  }
}
```

**External Server Mounts:**
<br>
Sample to mount a volume (*/external*) from external server by indicating its host (`sourceHost`), path (`sourcePath`) and access permissions (`readOnly`).
```
{
  "volumeMounts": {
    "/external": {
      "sourceHost": "external.com",
      "sourcePath": "/remote-path",
      "readOnly": true
    }
  }
}
```
**Short Set for External Server:**
<br>
Sample to mount a number of volumes from external server by specifying the required parameters (i.e. volume path, `sourceHost`, `sourcePath`, access permissions) for each of them within a one string.   
```
{
  "volumeMounts": {
    "/ext-domain": "aws.com",
    "/ext-domain/ro": "aws.com:ro",
    "/ext-domain/path": "aws.com:/121233",
    "/ext-domain/path/ro": "aws.com:/121233:ro"
  }
}
```

Here, "*ro*" stands for *readOnly* permissions.

<!--
##volumesFrom

`volumesFrom` is an list object.    
There are two ways to select the volume source container:
```
[
  {
    "sourceNodeId": "49",
    "readOnly": true
  },{
    "sourceNodeGroup": "storage",
    "readOnly": true
  }
]
```

In case to import not full source node volumes list You can set like below:
```
[
  {
    "sourceNodeGroup": "storage",
    "volumes": [
      "/master",
      "/local"
    ]
  }
]
```

Simple set examples above:
```
[
  49,
  "storage",
  "storage:ro"
]
```
where:   
- *49* - like { sourceNodeId : 49, readOnly : false }  
- *"storage"* - like { sourceNodeGroup : "storage", readOnly : false }  
- *"storage:ro"* - like { sourceNodeGroup : "storage", readOnly : true }
-->

##Docker Environment Variables

[Docker environment variable](https://docs.jelastic.com/docker-variables) is an optional topology object. The *env* instruction allows to set the required environment variables to specified values. 

```
{
  "env": {
    "topology": {
      "nodes": [
        {
          "nodeGroup": "cp",
          "docker": {
            "image": "wordpress:latest",
            "env": {
              "WORDPRESS_VERSION": "4.6.1",
              "PHP_INI_DIR": "/usr/local/etc/php"
            }
          }
        }
      ]
    }
  }
}
```

##Docker Links

[Docker links](https://docs.jelastic.com/docker-links) option allows to set up interaction between Docker containers, without having to expose internal ports to the outside world.
<br>
The example below illustrates the way to link *sql* and *memcached* nodes to *cp* container.
```
[
  {
    "docker": {
      "image": "wordpress:latest",
      "links": [
        "db:DB",
        "memcached:MEMCACHED"
      ]
    },
    "cloudlets": 8,
    "nodeGroup": "cp",
    "displayName": "AppServer"
  },
  {
    "docker": {
      "image": "mysql5:latest"
    },
    "cloudlets": 8,
    "nodeGroup": "db",
    "displayName": "Database"
  },
  {
    "docker": {
      "image": "memcached:latest"
    },
    "cloudlets": 4,
    "nodeGroup": "memcached",
    "displayName": "Memcached"
  }
]
```
where:   
- `links` - an object that defines nodes to be linked to *cp* node by their *nodeGroup* and these links names.    
- `db` - MYSQL server `nodeGroup` (environment layer)  
- `memcached` - Memcached server `nodeGroup` (environment layer)   

As a result, all the environment variables within *db* and *memcached* nodes will be also available at *cp* container.  
 
Here, environment variables of linked nodes will have the names, predefined within `links` array.   
For example:  
- variable *MYSQL_ROOT_PASSWORD* from *sql* node is *DB_MYSQL_ROOT_PASSWORD* in *cp* node   
- variable *IP_ADDRESS* from *memcached* node is *MEMCACHED_IP_ADDRESS* in *cp* node