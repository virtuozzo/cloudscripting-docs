#Volumes

Docker actions include such actions as docker `volumes` `links` and `environment variables`.

##Volumes

There are three fields provided to set docker `volumes`:  
- `volumes` - volumes list  
- `volumeMounts` - mount configs  
- `volumesFrom` - node list where volumes will be imported  

All fields set in docker object:
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
where 
- field `volumes` is an string array:
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

In case to import not full source node volumes list You can set like bellow:
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
  
##volumeMounts
`volumeMounts` is an object. It can be set like example below:
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
where  
- */example-path* - volume path  
- `sourcePath` - optional parameter. Default value - volume path. (*/example-path* in this example)   
- `sourceNodeId` - any available user node. Optinal in case of using `sourceNodeGroup`    
- `sourceHost` - only for external mounts. Optional.   
- `readOnly` - default value *false*   
- `sourceNodeGroup` - any avaliable `nodeGroup` in environment. Volumes will be defined by master node. Optional in case of using `sourceNodeId`.   
In case using not full source node volumes list `volumes` can be added.
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

###volumeMounts examples   
 
**Master node mount:**
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

**Mount Data Container**
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

**External Server mounts**
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
**Short set for External Server**
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

#Docker environment variables

The `env` instruction sets the environment variable <key> to the value <value>. Optional object
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

##Docker links
Connect to any number of docker container without the need to expose container's internal ports to the outside world.
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
where   
- `links` - an object where discribes nodes to link between `cp` node by their `nodeGroup`. Links is an links array between nodes;    
- `db` - mysql5 node's' nodeGroup;   
- `memecached` - memecached node's  `nodeGroup`.   

So all environment variables from `db` and `memcached` nodes available in `cp` container.  
 
Environment variables in linked nodes have names as it has predefined in `links` array. 
For example,  
- variable *MYSQL_ROOT_PASSWORD* from `sql` node is *DB_MYSQL_ROOT_PASSWORD* in `cp` node.   
- variable *IP_ADDRESS* from `memcached` node is *MEMCACHED_IP_ADDRESS* in `cp` node.