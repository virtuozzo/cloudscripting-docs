#Operation Examples

## Automatic Vertical Scaling

Adjust Nginx Balancer workers count depending on CPU cores amount:
``` json
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

## Automatic Horizontal Scaling

Create two Nginx PHP nodes with Nginx balancer and automatic horizontal scaling with the following rules:

- add 1 node if CPU > 70% up to 10 nodes
- remove 1 node if CPU < 5% down to 1 nodes
   
``` json
{
  "type": "install",
  "name": "Nginx PHP Auto Scaling",
  "engine": "php5.4",
  "nodes": [
    {
      "extip": true,
      "count": 2,
      "cloudlets": 16,
      "nodeType": "nginx"
    },
    {
      "count": 2,
      "cloudlets": 64,
      "nodeType": "nginxphp"
    }
  ],
  "onInstall": {
    "description": "Enable Auto Scaling Triggers",
    "script": "https://download.jelastic.com/public.php?service=files&t=adbf9389fa03afd1a559ec022e1e3a7c&download"
  }
}
```


**Enable Auto Scaling Triggers script:**
      
```
var APPID = getParam("TARGET_APPID"),
    oRespTurnOn,
    oData;

oData = {
  "isEnabled": true,
  "name": "hs-add-nginx",
  "nodeGroup": "cp",
  "period": 5,
  "condition": {
    "type": "GREATER",
    "value": 80,
    "resourceType": "CPU",
    "valueType": "PERCENTAGES"
  },
  "actions": [
    {
      "type": "ADD_NODE",
      "customData": {
        "limit": 3,
        "count": 1,
        "notify": false
      }
    }
  ]
};

oRespTurnOn = jelastic.env.trigger.AddTrigger(APPID, session, oData);

if (oRespTurnOn.result != 0) {
    return oRespTurnOn;
}

oData = {
  "isEnabled": true,
  "name": "hs-remove-nginx",
  "nodeGroup": "cp",
  "period": 15,
  "condition": {
    "type": "LESS",
    "value": 5,
    "resourceType": "CPU",
    "valueType": "PERCENTAGES"
  },
  "actions": [
    {
      "type": "REMOVE_NODE",
      "customData": {
        "limit": 2,
        "count": 1,
        "notify": false
      }
    }
  ]
};

oRespTurnOff = jelastic.env.trigger.AddTrigger(APPID, session, oData);

return oRespTurnOff;
```

## Using Dockers

Create and link WordPress Web and WordPress DB containers: 

``` json
{
  "type": "install",
  "name": "Wordpress",
  "homepage": "http://wordpress.org/",
  "description": "WordPress is web software you can use to create a beautiful website or blog. We like to say that WordPress is both free and priceless at the same time.",
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

## Wordpress Cluster
``` json
{
  "type": "install",
  "name": "WordPress Cluster",
  "appVersion": "4.0",
  "type": "php",
  "homepage": "http://www.wordpress.org/",
  "logo": "https://download.jelastic.com/public.php?service=files&t=3da2215839f82aa50d3d961271cd1cb9&download",
  "description": "Get your highly available and scalable clustered solution for WordPress, the extremely popular open source CMS and blogging tool. This package is designed to ensure the load tracking and distribution, as well as automatic adjusting the amount of allocated resources according to it.",
  "engine": "php5.3",
  "nodes": [
    {
      "extip": true,
      "count": 2,
      "cloudlets": 16,
      "nodeType": "nginx"
    },
    {
      "count": 2,
      "cloudlets": 16,
      "nodeType": "nginxphp"
    },
    {
      "nodeType": "mysql5",
      "count": 2,
      "cloudlets": 16
    }
  ],
  "onAfterCloneNodes": [
    "installRsyncDaemon",
    "startLsyncDaemon",
    "applyNewCPNode"
  ],
  "onBeforeLinkNode": "stopEvent",
  "onAfterRemoveNode": [
    "ConfigCPAddress",
    "installRsyncDaemon",
    "startLsyncDaemon"
  ],
  "onInstall": [
    "deployWordpress",
    "enableAutoScaling",
    "configureBalancers",
    "installRsyncDaemon",
    "configureReplication",
    "startLsyncDaemon"
  ],
  "actions": [
    {
      "deployWordpress": {
        "deploy": {
          "archive": "https://download.jelastic.com/public.php?service=files&t=c34ba789a018267bc931a7865e1e8de2&download",
          "name": "WordPress-4.1.zip",
          "context": "ROOT"
        },
        "upload [cp]": [
          {
            "destPath": "${SERVER_WEBROOT}/ROOT/db-config.php",
            "sourcePath": "https://download.jelastic.com/public.php?service=files&t=d90fd50c63fe018273db1ee9923caeb4&download"
          },
          {
            "destPath": "${SERVER_WEBROOT}/ROOT/wp-content/db.php",
            "sourcePath": "https://download.jelastic.com/public.php?service=files&t=c6a3c4018c8465bfb75c99f7ac4c2192&download"
          }
        ],
        "description": "Configuring Db connections at cp nodes by pairs",
        "script": "https://download.jelastic.com/public.php?service=files&t=849165f775c84ab40b15c385e905a360&download",
        "replaceInFile [cp]": [
          {
            "path": "${SERVER_WEBROOT}/ROOT/db-config.php",
            "replacements": [
              {
                "pattern": "{DB_USER}",
                "replacement": "root"
              },
              {
                "pattern": "{DB_PASSWORD}",
                "replacement": "${nodes.sqldb.password}"
              },
              {
                "pattern": "{DB_NAME}",
                "replacement": "wordpress"
              }
            ]
          },
          {
            "path": "${SERVER_WEBROOT}/ROOT/wp-config.php",
            "replacements": [
              {
                "pattern": "<?php",
                "replacement": "<?php\nif (!session_id())\n  session_start();"
              }
            ]
          },
          {
            "path": "/etc/nginx/nginx.conf",
            "replacements": [
              {
                "pattern": "index  index.html index.htm index.php;",
                "replacement": "index  index.html index.htm index.php; \n \n if (!-e $request_filename ) {\nrewrite ^(.*)$ /index.php?q=$1;\n}"
              }
            ]
          },
          {
            "path": "/etc/nginx/nginx.conf",
            "replacements": [
              {
                "pattern": "worker_processes  1;",
                "replacement": "worker_processes  8;"
              },
              {
                "pattern": "#tcp_nopush   on;",
                "replacement": "tcp_nopush on;\n  tcp_nodelay on;\n  types_hash_max_size 2048;\n  gzip    on;\n  gzip_disable  \"msie6\";\n  gzip_vary     on;\n  gzip_proxied  any;\n  gzip_comp_level   5;\n  gzip_buffers  16 8k;\n  keepalive_timeout  2;\n  gzip_http_version   1.0;\n  gzip_types    image/svg+xml text/plain text/js text/svg text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/png image/gif image/jpeg;\n\n  open_file_cache    max=5000  inactive=20s;\n  open_file_cache_valid  30s;\n  open_file_cache_min_uses 2;\n  open_file_cache_errors   on;"
              },
              {
                "pattern": "keepalive_timeout  2;",
                "replacement": "#keepalive_timeout  2;"
              },
              {
                "pattern": "location ~ \\.php$ {",
                "replacement": "location ~*  \\.(jpg|jpeg|png|gif|ico|css|js)$ {\\  nexpires 365d;\n  }\nlocation ~*  \\.(pdf)$ {\n  expires 30d;\n  }\n\nlocation ~ \\.php$ {"
              }
            ]
          },
          {
            "path": "/etc/php.ini",
            "replacements": [
              {
                "pattern": "session.save_handler = files",
                "replacement": "session.save_handler = files \nsession.save_path = ${SERVER_WEBROOT}/ROOT/sessions/"
              },
              {
                "pattern": "; extension=apc.so",
                "replacement": "extension=apc.so"
              },
              {
                "pattern": ";extension=mysql.so",
                "replacement": "extension=mysql.so"
              },
              {
                "pattern": "session.gc_maxlifetime = 1440",
                "replacement": "session.gc_maxlifetime = 300"
              },
              {
                "pattern": "session.gc_divisor = 1000",
                "replacement": "session.gc_divisor = 100"
              }
            ]
          }
        ],
        "upload [sqldb]": {
          "destPath": "/var/lib/jelastic/keys/DbCreation.sh",
          "sourcePath": "https://download.jelastic.com/public.php?service=files&t=78ae5e3ad1aefe25b13685fee7520e22&download"
        },
        "cmd [sqldb]": [
          "/bin/bash /var/lib/jelastic/keys/DbCreation.sh '${nodes.sqldb.password}' 'https://download.jelastic.com/public.php?service=files&t=7271e1a44982fe78025d4a98be84111e&download' '${env.url}' '${env.protocol}' '${env.domain}' '${user.email}'  '${user.appPassword}' 2>&1",
          "rm -rf /var/lib/jelastic/keys/DbCreation.sh"
        ],
        "cmd [cp]": [
          "rm -rf ${SERVER_WEBROOT}/ROOT/sessions",
          "mkdir ${SERVER_WEBROOT}/ROOT/sessions"
        ],
        "restartNodes": {
          "nodeGroup": "cp"
        }
      }
    },
    {
      "enableAutoScaling": {
        "description": "Enable AutoScaling trigger",
        "script": "https://download.jelastic.com/public.php?service=files&t=adbf9389fa03afd1a559ec022e1e3a7c&download"
      }
    },
    {
      "configureBalancers": {
        "replaceInFile [bl]": [
          {
            "path": "/etc/nginx/conf.d/cache.conf",
            "replacements": {
              "pattern": "#proxy",
              "replacement": "proxy"
            }
          }
        ],
        "cmd [cp]": "sudo /etc/init.d/nginx reload 2>&1"
      }
    },
    {
      "applyNewCPNode": {
        "cmd [${nodes.bl[0].id}]": [
          "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${event.response.array.address};|g\" ${HOME}/nginx-jelastic.conf",
          "sudo /etc/init.d/nginx reload 2>&1"
        ],
        "cmd [${nodes.bl[1].id}]": [
          "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${event.response.array.address};|g\" ${HOME}/nginx-jelastic.conf",
          "sudo /etc/init.d/nginx reload 2>&1"
        ],
        "user": "root",
        "description": "Configuring db's address on new compute nodes",
        "script": "https://download.jelastic.com/public.php?service=files&t=1dbb2213905dfbe4696813e218af1362&download"
      }
    },
    {
      "configureReplication": {
        "replaceInFile [sqldb]": {
          "path": "${MYSQL_CONF}/my.cnf",
          "replacements": [
            {
              "pattern": "#log-bin=mysql-bin",
              "replacement": "log-bin=mysql-bin"
            }
          ]
        },
        "replaceInFile [${nodes.sqldb[0].id}]": {
          "path": "${MYSQL_CONF}/my.cnf",
          "replacements": [
            {
              "pattern": "server-id\\s*= 1",
              "replacement": "server-id = 2"
            }
          ]
        },
        "cmd [${nodes.sqldb[0].id}]": [
          "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[1].address} IDENTIFIED BY 'rpl';\" 2>&1",
          "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port} 2>&1"
        ],
        "cmd [${nodes.sqldb[1].id}]": [
          "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[0].address} IDENTIFIED BY 'rpl';\" 2>&1",
          "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} 2>&1"
        ],
        "restartNodes": {
          "nodeGroup": "sqldb"
        }
      }
    },
    {
      "installRsyncDaemon": {
        "description": "Get compute nodes Ids and mirrors compute node's address for rsync",
        "script": "https://download.jelastic.com/public.php?service=files&t=b55b2cb809638c3643cbb448adb375c7&download"
      }
    },
    {
      "installLsync": {
        "cmd [${this.nodeId}]": "rm -rf ${SERVER_WEBROOT}/lsyncd",
        "createDirectory [${this.nodeId}]": "${SERVER_WEBROOT}/lsyncd",
        "upload [${this.nodeId}]": {
          "destPath": "${SERVER_WEBROOT}/lsyncd/sync.tar",
          "sourcePath": "https://download.jelastic.com/public.php?service=files&t=6d780367c8a6a290f3ecdcace7e4087e&download"
        },
        "unpack [${this.nodeId}]": {
          "sourcePath": "${SERVER_WEBROOT}/lsyncd/sync.tar",
          "destPath": "${SERVER_WEBROOT}/lsyncd/"
        },
        "replaceInFile [${this.nodeId}]": [
          {
            "path": "${SERVER_WEBROOT}/lsyncd/etc/lsyncd.conf",
            "replacements": [
              {
                "pattern": "_MIRROR_SERVER_IP",
                "replacement": "${this.mirrorServerIp}"
              },
              {
                "pattern": "_USER",
                "replacement": "admin"
              },
              {
                "pattern": "{SERVER_WEBROOT}",
                "replacement": "${SERVER_WEBROOT}"
              },
              {
                "pattern": "_INSTALL_DIRECTORY",
                "replacement": "${SERVER_WEBROOT}/lsyncd"
              },
              {
                "pattern": "name",
                "replacement": "varwwwwebroot"
              }
            ]
          },
          {
            "path": "${SERVER_WEBROOT}/lsyncd/etc/rsync.conf",
            "replacements": [
              {
                "pattern": "_NAME",
                "replacement": "varwwwwebroot"
              },
              {
                "pattern": "_USER",
                "replacement": "admin"
              },
              {
                "pattern": "_INSTALL_DIRECTORY",
                "replacement": "${SERVER_WEBROOT}/lsyncd"
              },
              {
                "pattern": "{SERVER_WEBROOT}",
                "replacement": "${SERVER_WEBROOT}"
              }
            ]
          },
          {
            "path": "${SERVER_WEBROOT}/lsyncd/etc/rsyncd.pass",
            "replacements": {
              "pattern": "_PASSWORD",
              "replacement": "${user.appPassword}"
            }
          },
          {
            "path": "${SERVER_WEBROOT}/lsyncd/etc/rsyncd.secrets",
            "replacements": [
              {
                "pattern": "_PASSWORD",
                "replacement": "${user.appPassword}"
              },
              {
                "pattern": "_USER",
                "replacement": "admin"
              }
            ]
          },
          {
            "path": "${SERVER_WEBROOT}/lsyncd/init.sh",
            "replacements": {
              "pattern": "_INSTALL_DIRECTORY",
              "replacement": "${SERVER_WEBROOT}/lsyncd/"
            }
          }
        ],
        "cmd": {
          "nodeId": "${this.nodeId}",
          "commands": [
            "cd ${SERVER_WEBROOT}/lsyncd/",
            "chmod 600 etc/rsyncd.pass",
            "chmod 600 etc/rsyncd.secrets",
            "chmod 755 usr/bin/lsyncd",
            "killall -9 lsyncd 2>/dev/null 1>/dev/null",
            "killall -9 rsync 2>/dev/null 1>/dev/null",
            "/usr/bin/rsync --daemon --config=${SERVER_WEBROOT}/lsyncd/etc/rsync.conf --port=7755 &>>${SERVER_WEBROOT}/lsyncd/var/log/rsyncd_start.log"
          ]
        }
      }
    },
    {
      "startLsyncDaemon": {
        "cmd [${nodes.bl[0].id}]": "sudo /etc/init.d/nginx reload",
        "cmd [cp]": "${SERVER_WEBROOT}/lsyncd/usr/bin/lsyncd ${SERVER_WEBROOT}/lsyncd/etc/lsyncd.conf &>> ${SERVER_WEBROOT}/lsyncd/var/log/lsyncd_start.log",
        "appendFile [cp]": {
          "path": "/var/spool/cron/nginx",
          "body": "*/5 * * * * /bin/bash ${SERVER_WEBROOT}/lsyncd/init.sh"
        }
      }
    },
    {
      "ConfigCPAddress": {
        "description": "Configure balancers after remove compute node",
        "script": "https://download.jelastic.com/public.php?service=files&t=26f66db839c9bd3d0c7e13131750c5bc&download"
      }
    },
    {
      "BLConfiguring": {
        "cmd [${nodes.bl[1].id}]": [
          "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${this.replacement};|g\" ${HOME}/nginx-jelastic.conf",
          "sudo /etc/init.d/nginx reload"
        ],
        "cmd [${nodes.bl[0].id}]": [
          "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${this.replacement};|g\" ${HOME}/nginx-jelastic.conf",
          "sudo /etc/init.d/nginx reload"
        ],
        "user": "root"
      }
    },
    {
      "replace": {
        "replaceInFile [${this.nodeid}]": {
          "path": "${this.path}",
          "replacements": {
            "pattern": "${this.pattern}",
            "replacement": "${this.replacement}"
          }
        }
      }
    }
  ],
  "success": "Below you will find your admin panel link, username and password.</br></br> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/wp-admin/' target='_blank'>${env.protocol}://${env.domain}/wp-admin/</a></td></tr>  <tr><td>Admin name:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>${user.appPassword}</td></tr></table></br>To add custom domain name for your Wordpress installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>"
}
```

**Configuring DB connections at compute nodes by pairs**
```
import com.hivext.api.environment.Environment;
  
var NODE_MISSION_COMPUTE = "cp",
    sPath = "${nginxphp.SERVER_WEBROOT}/ROOT/db-config.php",
    PROCEDURE_PROCESS_NODE = "replace",
    APPID = getParam("TARGET_APPID"),
    SESSION = getParam("session"),
    callArgs = [],
    aActions = [],
    item,
    env,
    isEvenNode,
    envInfoResponse;

envInfoResponse = jelastic.env.control.getEnvInfo();

if (envInfoResponse.result != 0) {
    return envInfoResponse;
}

var nodes = envInfoResponse.getNodes();
var iterator = nodes.iterator();
  
while(iterator.hasNext()) {
    var softNode = iterator.next();
    var softNodeProperties = softNode.getProperties();
      
    if (NODE_MISSION_COMPUTE.equals(softNodeProperties.getNodeGroup())) {
        callArgs.push(softNode);
    }
}

for (var i = 0, n = callArgs.length; i < n; i+=1) {
    isEventNode = (i % 2 === 0);
    aActions.push({
        procedure : PROCEDURE_PROCESS_NODE,
        params : {
            nodeid : callArgs[i].id,
            path : sPath,
            pattern : isEventNode ? "{DB_HOST1}" : "{DB_HOST2}",
            replacement : "{TMP}"
        }
    },{
        procedure : PROCEDURE_PROCESS_NODE,
        params : {
            nodeid : callArgs[i].id,
            path : sPath,
            pattern : isEventNode ? "{DB_HOST2}" : "{DB_HOST1}",
            replacement : "${nodes.sqldb[0].address}"
        }
    },{
        procedure : PROCEDURE_PROCESS_NODE,
        params : {
            nodeid : callArgs[i].id,
            path : sPath,
            pattern : "{TMP}",
            replacement : "${nodes.sqldb[1].address}"
        }
    });
}

return {
    result: 0,
    onAfterReturn : {
      call : aActions
    }
};
```

**Create database and restore dump**
```bash
#!/bin/bash
curl -fs $2 -o /var/lib/mysql/wordpress.sql 2>&1

mysql -uroot -p$1 << END 
    CREATE DATABASE wordpress;
    GRANT USAGE ON *.* TO wordpress@localhost  identified by 'password';
    grant all privileges on wordpress.* to wordpress@localhost;
    use wordpress;

\. /var/lib/mysql/wordpress.sql

    UPDATE wordpress.wp_posts SET guid='$3?p=1';
    UPDATE wordpress.wp_posts SET guid='$3?p=2';
    UPDATE wordpress.wp_posts SET guid='$3?p=3';
    UPDATE wordpress.wp_posts SET post_date_gmt=CURRENT_TIMESTAMP, post_date=CURRENT_TIMESTAMP, post_modified=CURRENT_TIMESTAMP;
    UPDATE wordpress.wp_options SET option_value='$4://$5' WHERE option_name='home'; 
    UPDATE wordpress.wp_options SET option_value='$4://$5' WHERE option_name='siteurl'; 
    UPDATE wordpress.wp_options SET option_value='$6' WHERE option_name='admin_email'; 
    UPDATE wordpress.wp_users SET user_email='$6' WHERE user_login='admin';
    UPDATE wordpress.wp_users SET user_pass=MD5('$7') WHERE user_login='admin';
END
```


**Configuring DB's address on new compute nodes**
```
var sPath = "${nginxphp.SERVER_WEBROOT}/ROOT/db-config.php",
    NODE_MISSION_COMPUTE = "cp",
    PROCEDURE_PROCESS_NODE = "replace",
    APPID = getParam("TARGET_APPID"),
    SESSION = getParam("session"),
    aComputeNodes = [],
    aActions = [],
    item,
    lastCoNode,
    envInfoResponse,
    isEventNode;

envInfoResponse = jelastic.env.control.getEnvInfo();

if (!envInfoResponse.isOK()) {
    return envInfoResponse;
}

var nodes = envInfoResponse.getNodes();
var iterator = nodes.iterator();
  
while(iterator.hasNext()) {
    var softNode = iterator.next();
    var softNodeProperties = softNode.getProperties();
      
    if (NODE_MISSION_COMPUTE.equals(softNodeProperties.getNodeGroup())) {
        aComputeNodes.push(softNode);
    }
}

lastCoNode = aComputeNodes[aComputeNodes.length -1].id;

if (aComputeNodes.length %2 == 1) {

  aActions.push({
      procedure : PROCEDURE_PROCESS_NODE,
      params : {
	  nodeId : lastCoNode,
	  path : sPath,
	  pattern : "${nodes.sqldb[1].address}",
	  replacement : "{ONE_DB}"
      }
  },{
      procedure : PROCEDURE_PROCESS_NODE,
      params : {
	  nodeId : lastCoNode,
	  path : sPath,
	  pattern : "${nodes.sqldb[0].address}",
	  replacement : "${nodes.sqldb[1].address}"
      }
  },{
      procedure : PROCEDURE_PROCESS_NODE,
      params : {
	  nodeId : lastCoNode,
	  path : sPath,
	  pattern : "{ONE_DB}",
	  replacement : "${nodes.sqldb[0].address}"
      }
  });
}

return {
    result: 0,
    onAfterReturn : {
        call : aActions
    }
};
```

**Get compute nodes Ids and mirrors compute node's address for rsync**
```  
var NODE_MISSION_COMPUTE = "cp",
    PROCEDURE_PROCESS_NODE = "installLsync",
    APPID = getParam("TARGET_APPID"),
    SESSION = getParam("session"),
    callArgs,
    env,
    envInfoResponse;

envInfoResponse = jelastic.env.control.getEnvInfo();

if (!envInfoResponse.isOK()) {
    return envInfoResponse;
}

var nodes = envInfoResponse.getNodes();
var iterator = nodes.iterator();
var computeNodes = [];
  
while(iterator.hasNext()) {
    var softNode = iterator.next();
    var softNodeProperties = softNode.getProperties();
      
    if (NODE_MISSION_COMPUTE.equals(softNodeProperties.getNodeGroup())) {
        computeNodes.push(softNode);
    }
}

callArgs = [];
for (var i = 0, n = computeNodes.length; i < n; i += 1) {
    var mirrorServerIp = computeNodes[(i + 1) === computeNodes.length ? 0 : i + 1].getAddress();

    callArgs.push({
        procedure : PROCEDURE_PROCESS_NODE,
        params : {
            nodeId : computeNodes[i].getId(),
            mirrorServerIp : mirrorServerIp
        }
    });

} 

return {
    result : 0,
    onAfterReturn : {
        call : callArgs
    }
}; 
```

**Configure balancers after remove compute node**
```  
var NODE_MISSION_COMPUTE = "cp",
    PROCEDURE_PROCESS_NODE = "BLConfiguring,
    APPID = getParam("TARGET_APPID"),
    SESSION = getParam("session"),
    envInfoResponse,
    callArgs,
    lenghtCP,
    env;

envInfoResponse = jelastic.env.control.getEnvInfo();

if (!envInfoResponse.isOK()) {
    return envInfoResponse;
}

var nodes = envInfoResponse.getNodes();
var iterator = nodes.iterator();
var computeNodes = [];
  
while(iterator.hasNext()) {
    var softNode = iterator.next();
    var softNodeProperties = softNode.getProperties();
      
    if (NODE_MISSION_COMPUTE.equals(softNodeProperties.getNodeGroup())) {
        computeNodes.push(softNode);
    }
}

callArgs = [];
lenghtCP = computeNodes.length;

if (lenghtCP > 2) {
  for (var i = 2, n = computeNodes.length; i < n; i += 1) {
	callArgs.push({
	  procedure : PROCEDURE_PROCESS_NODE,
	  params : {
	      replacement : computeNodes[i].getAddress()
	  }
      });
  }
}

return {
    result : 0,
    onAfterReturn : {
        call : callArgs
    }
};
```


## Automated Environment Migration after Cloning
``` json
{
  "type": "install",
  "name": "cloneEnv",
  "nodes": [
    {
      "cloudlets": 16,
      "nodeType": "tomcat7"
    },
    {
      "cloudlets": 16,
      "nodeType": "mysql5"
    }
  ],
  "onAfterClone": {
    "script": "https://download.jelastic.com/public.php?service=files&t=a6a659b4fcb85f4289559747b5568e4e&download"
  },
  "onInstall": {
    "call": [
      "deployApp",
      "uploadFiles",
      "createDb",
      "replaceInFiles",
      "bindDomain"
    ]
  },
  "actions": [
    {
      "deployApp": {
        "deploy": [
          {
            "archive": "https://download.jelastic.com/public.php?service=files&t=c3afe9748a679a132d47c0148978e3b2&download",
            "name": "share-5.0.war",
            "context": "share"
          },
          {
            "archive": "https://download.jelastic.com/public.php?service=files&t=91924607b72d9211c38cfe111d424263&download",
            "name": "alfresco-5.0.war",
            "context": "alfresco"
          }
        ]
      }
    },
    {
      "uploadFiles": {
        "upload [nodeGroup:cp]": [
          {
            "sourcePath": "http://app.jelastic.com/xssu/cross/download/RTYYHA81VwNaVlRAYAw4TUMVCRBUShURWBZsHH8iIlYQQktYDwIBQmNTTEBI",
            "destPath": "${WEBAPPS}/alfresco/WEB-INF/classes/alfresco-global.properties"
          },
          {
            "sourcePath": "http://app.jelastic.com/xssu/cross/download/QjYYHA81VwNaVlRAYAw4TUMVCRBUShURWBZsHH8iIlYQQktYDwIBQmNTTEBI",
            "destPath": "${JAVA_LIB}/mysql-connector-java-5.0.8-bin.jar"
          }
        ]
      }
    },
    {
      "createDb": {
        "execCmd [nodeGroup:sqldb]": [
          "curl \"https://download.jelastic.com/public.php?service=files&t=0f65b115eb5b9cdb889d135579414321&download\" -o /tmp/script.sh 2>&1",
          "bash /tmp/script.sh \"${nodes.sqldb.password}\" 2>&1"
        ]
      }
    },
    {
      "replaceInFiles": {
        "replaceInFile [nodeGroup:cp]": [
          {
            "path": "${WEBAPPS}/alfresco/WEB-INF/classes/alfresco-global.properties",
            "replacements": [
              {
                "pattern": "{DB_HOST}",
                "replacement": "${nodes.mysql5.address}"
              },
              {
                "pattern": "{DB_USER}",
                "replacement": "root"
              },
              {
                "pattern": "{DB_PASSWORD}",
                "replacement": "${nodes.mysql5.password}"
              },
              {
                "pattern": "{DB_NAME}",
                "replacement": "alfresco"
              }
            ]
          },
          {
            "path": "/opt/tomcat/webapps/alfresco/index.jsp",
            "replacements": [
              {
                "pattern": "{HOSTNAME}",
                "replacement": "${env.url}"
              }
            ]
          }
        ]
      }
    },
    {
      "bindDomain": {
        "script": "https://download.jelastic.com/public.php?service=files&t=6f5ccac2b011cbc1d6239464ea0a4c97&download"
      }
    }
  ],
  "success": "Below you will find your admin panel link, username and password.</br></br> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/share/' target='_blank'>${env.protocol}://${env.domain}/share/</a></td></tr>  <tr><td>Admin name:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>admin</td></tr></table></br>To bind a custom domain name with your Alfresco please refer to the steps described in Jelastic <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>"
}

```

/**
 * JS script for executing actions with the newly cloned environment.
 * The script is subscribed on the onAfterClone event and will be executed after old environment cloning.
 */
var APPID = getParam("TARGET_APPID"),
    CLONED_ENV_APPID = "${event.response.env.appid}", // placeholder for the cloned environment AppID

    APP_CONFIG_FILE_PATH = "/opt/tomcat/webapps/alfresco/WEB-INF/classes/alfresco-global.properties", // path to Alfresco config, where the database connection string should be replaced
    APP_INDEX_FILE_PATH = "/opt/tomcat/webapps/alfresco/index.jsp", // path to the Alfresco index.jsp file for the new environment URL substitution
    SOURCE_ENV_URL = "${env.url}", // placeholder for the old environment URL; will be substituted during the script execution

    NODE_TYPE_CP = "tomcat7", // keyword of the compute node's software stack.
    NODE_TYPE_DB = "mysql5", // keyword of the DB node's software stack

    HN_GROUP_PROFIT_BRICKS = "pbricks-de"; // second hardware node group's identifier

/**
 * Adjust application settings according to a new database connection string
 * @param {Object} oClonedEnvInfo - meta information of the cloned environment
 * @returns {Response}
 */
function configureAppSettings(oClonedEnvInfo) {
    var oFileService,
        oResp,
        sDbAddress;

    // fetch internal IP address of a new database node
    oClonedEnvInfo.nodes.some(function (oNode) {

        if (oNode.nodeType == NODE_TYPE_DB) {
            sDbAddress =  oNode.address;
        }
    });

    // adjust old database connection string with parameters of the cloned one
    oResp = jelastic.env.file.ReplaceInBody(CLONED_ENV_APPID, session, APP_CONFIG_FILE_PATH, "db.url=jdbc:mysql://.*", "db.url=jdbc:mysql://" + sDbAddress + "/alfresco?useUnicode=yes\\&characterEncoding=UTF-8", "", NODE_TYPE_CP);

    // replace environment URL with the cloned one
return jelastic.env.file.ReplaceInBody(CLONED_ENV_APPID, session, APP_INDEX_FILE_PATH, SOURCE_ENV_URL, oClonedEnvInfo.url, "", NODE_TYPE_CP);
}

/**
 * Method for migrating new environment to another hardware node group
 * @param {object} oEnvService - new environment service
 * @param {object} oClonedEnvInfo - meta information about the cloned environment
 * @returns {Response}
 */
function migrateEnv(oClonedEnvInfo) {
    // migrate environment API to another hardware node group
    return jelastic.env.control.Migrate(CLONED_ENV_APPID, session, HN_GROUP_PROFIT_BRICKS, true);
}

/**
 * Main method for executing actions with cloned environment
 * @returns {Response}
 */
function processEnvironment() {
    var oClonedEnvInfo,
        oEnvService,
        oResp;

    // Get meta information of the new environment.
    // Meta information includes all the data about environment, comprised nodes and their properties
     oClonedEnvInfo = jelastic.env.control.GetEnvInfo(CLONED_ENV_APPID, session);

    if (oClonedEnvInfo.result !== 0) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the cloned environment properties
    oResp = configureAppSettings(oClonedEnvInfo);

    if (oResp.result !== 0) {
        return oResp;
    }

    // migrate cloned environment to a new hardware node group, located in another region
/*    oResp = migrateEnv(oClonedEnvInfo);

    if (oResp.result !== 0) {
        return oResp;
    }
*/
    // Get meta information of the new environment after migrating into new region.
    oClonedEnvInfo = jelastic.env.control.GetEnvInfo(CLONED_ENV_APPID, session);

    if (oClonedEnvInfo.result !== 0) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the migrated environment properties
    oResp =  configureAppSettings(oClonedEnvInfo);

    return jelastic.env.binder.SwapExtDomains(APPID, session, CLONED_ENV_APPID);
}

return processEnvironment();

##Create two environments from one JPS in different regions

``` json
{
  "type": "install",
  "name": "2Envs",
  "nodes": [
    {
      "cloudlets": 16,
      "nodeType": "nginxphp"
    }
  ],
  "engine": "php5.3",
  "region": "default_hn_group",
  "onInstall": {
    "script": "https://download.jelastic.com/public.php?service=files&t=169362776e246cbf756eb7aad325f676&download"
  }
}
```

```example
var sAppid = getParam("TARGET_APPID"),
    sSession = hivext.local.getParam("session"),
    sRegion = "windows1",
    sEnvGeneratedName = generateEnvName(),
    oNodes = [{
        "nodeType": "nginxphp",
        "flexibleCloudlets": 10,
        "engine": "php5.4"
    }],
    oEnv = {
        "region": sRegion,
        "engine": "php5.4",
        "shortdomain": sEnvGeneratedName
    },
    sActionkey = "createenv;" + sEnvGeneratedName;

function generateEnvName(sPrefix) {
    sPrefix = sPrefix || "env-";

    return sPrefix + parseInt(Math.random() * 100000, 10);
}

return jelastic.env.control.CreateEnvironment(sAppid, sSession, sActionkey, oEnv, oNodes);
```

##Install Add-on inside Manifest

This manifest provides an environment, that is handled with the help of **Apache PHP** application server, is powered by **PHP 7** engine version and has external IP address attached. Subsequently, Public IP address can be detached with the help of the **Add-on** button.
``` json
{
  "type": "install",
  "name": "example",
  "nodes": [
    {
      "nodeType": "apache2",
      "cloudlets": "16",
      "addons": [
        "setExtIp"
      ]
    }
  ],
  "engine": "php7.0",
  "addons": {
    "id": "setExtIp",
    "onInstall": "attacheIp",
    "onUnInstall": "deAttacheIp",
    "actions": {
      "attacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": true
        }
      },
      "deAttacheIp": {
        "setExtIpEnabled": {
          "nodeType": "apache2",
          "enabled": false
        }
      }
    }
  },
  "success": "Environment with add-on installed successfully!"
}
```
   
As a result, environment with the above-specified topology is successfully created. In order to disable the external IP feature, click the **Uninstall** button located within the **Add-ons** section.   

![addoninstall](/img/addon-install.jpg)

##Mount Data Storage

Mount `data` directory from `storage` node to application server node:

``` json
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

