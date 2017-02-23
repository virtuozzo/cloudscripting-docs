#Complex Ready to Go Solutions

##Minio Cluster

Highly reliable S3-compatible storage. S3 compatible object storage server in Docker containers.  

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https://raw.githubusercontent.com/jelastic-jps/minio/master/manifest.jps&min-version=4.6) 

[More details here.](https://github.com/jelastic-jps/minio)

``` json
{
  "type": "install",
  "name": "Minio",
  "homepage": "https://github.com/minio/minio",
  "description": "Minio is an object storage server, compatible with Amazon S3 cloud storage service, best suited for storing unstructured data such as photos, videos, log files and backups.",
  "logo": "https://github.com/jelastic-jps/minio/raw/master/images/minio-logo-70x70.png",
  "settings": {
    "fields": [
      {
        "name": "servers",
        "caption": "Servers",
        "type": "list",
        "inputType": "string",
        "values": {
          "1": "1 server",
          "4": "4 servers",
          "8": "8 servers",
          "16": "16 servers"
        },
        "default": 4,
        "required": true
      },
      {
        "name": "accessKey",
        "caption": "Access Key",
        "type": "string",
        "inputType": "string",
        "default": "AKIAIOSFODNN7EXAMPLE",
        "required": true
      },
      {
        "name": "secretKey",
        "caption": "Secret Key",
        "type": "string",
        "inputType": "string",
        "default": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "required": true
      }
    ]
  },
  "nodes": {
    "count": "${settings.servers}",
    "cloudlets": 16,
    "nodeGroup": "cp",
    "image": "minio/minio",
    "env": {
      "MINIO_ACCESS_KEY": "${settings.accessKey}",
      "MINIO_SECRET_KEY": "${settings.secretKey}",
      "PORT": "80"
    },
    "cmd": "--help"
  },
  "ssl": true,
  "onInstall": [
    "build-cluster",
    {
      "restartContainers": {
        "nodeGroup": "cp"
      }
    }
  ],
  "actions": {
    "build-cluster": {
      "script": "https://github.com/jelastic-jps/minio/raw/master/build-cluster.js",
      "params": {
        "nodeGroup": "cp",
        "volumePath": "/export"
      }
    }
  },
  "success": "Admin Panel: <a href='${env.url}' target='_blank'>${env.url}</a><br/><br/>To add custom domain name for your Minio installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>"
}
```

##Glassfish Cluster

Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount.  

To instantly host your own scalable GF cluster, click the **Deploy to Jelastic** button below. Within the opened frame, specify your email address, choose one of the [Jelastic Public Cloud providers] (https://jelastic.cloud/) and press **Install**.

Due to the native GlassFish clustering architecture, its topology includes three node groups:

- Load Balancer - intended to process all incoming requests, sent to the cluster, and distribute them between worker nodes
- Worker Node - application server to handle the required app and web services
- Domain Administration Server (DAS) - management instance which performs centralized control of the cluster nodes and configure communication between them via SSH

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https://raw.githubusercontent.com/jelastic-jps/glassfish/master/manifest.jps)

[More details here](https://github.com/jelastic-jps/glassfish)

``` json
{
  "type": "install",
  "name": "Auto Scaling GlassFish Cluster",
  "logo": "https://github.com/jelastic-jps/glassfish/raw/master/glassfish-cluster/img/glassfish-logo.png",
  "description": "Pre-configured and ready-to-work GlassFish Cluster with auto scaling triggers. The cluster consists of 1 DAS node, 1 Worker node and 1 HAProxy node as the load balancer. By default connection to the cluster is secured by Jelastic SSL.",
  "nodes": [
    {
      "cloudlets": 16,
      "displayName": "DAS",
      "nodeGroup": "das",
      "image": "jelastic/glassfish:latest",
      "env": {
        "DAS": "true"
      },
      "volumes": [
        "/home/glassfish/.ssh"
      ]
    },
    {
      "cloudlets": 16,
      "nodeGroup": "cp",
      "displayName": "Worker",
      "image": "jelastic/glassfish:latest",
      "links": [
        "das:das"
      ],
      "volumes": [
        "/home/glassfish/.ssh"
      ],
      "volumeMounts": {
        "/home/glassfish/.ssh": {
          "sourceNodeGroup": "das",
          "readOnly": false
        }
      }
    },
    {
      "cloudlets": 16,
      "displayName": "LoadBalancer",
      "nodeGroup": "bl",
      "image": "jelastic/haproxy-managed-lb",
      "volumes": [
        "/usr/local/etc/haproxy"
      ],
      "env": {
        "HOSTS_PORT": "28080"
      }
    }
  ],
  "ssl": true,
  "--": "---- Create Procedures ----",
  "onBeforeScaleIn[nodeGroup:cp]": {
    "forEach(event.response.nodes)": {
      "execCmd [nodeId:${@i.id}]": "sudo -i -u ${USER} bash -c 'bash glassfish.sh stop'"
    }
  },
  "onAfterScaleOut[nodeGroup:cp]": [
    "addWorkerToLB",
    {
      "forEach(event.response.nodes)": {
        "call": [
          {
            "action": "80->28080",
            "params": {
              "nodeId": "${@i.id}"
            }
          },
          {
            "action": "localhost:4848->das:4848",
            "params": {
              "nodeId": "${@i.id}"
            }
          }
        ]
      }
    }
  ],
  "onAfterSetCloudletCount[nodeGroup:cp]": {
    "restartContainers": {
      "nodeGroup": "${event.params.nodeGroup}"
    }
  },
  "onAfterSetCloudletCount[nodeGroup:das]": {
    "restartContainers": {
      "nodeGroup": "${event.params.nodeGroup}"
    }
  },
  "onInstall": [
    {
      "call": [
        "addWorkerToLB",
        "80->28080",
        {
          "action": "localhost:4848->das:4848",
          "params": {
            "nodeGroup": "cp"
          }
        },
        {
          "action": "localhost:4848->das:4848",
          "params": {
            "nodeGroup": "das"
          }
        },
        "addAutoScalingTriggers",
        "deployApp"
      ]
    }
  ],
  "actions": [
    {
      "deployApp": {
        "execCmd [nodeGroup:das]": [
          "sudo -u ${USER} wget -O ${HOME_DIR}/clusterjsp.ear https://github.com/jelastic-jps/glassfish/blob/master/glassfish-cluster/test-app/clusterjsp.ear?raw=1",
          "while (true); do fuser -n tcp 4848 && { sleep 20; sudo -u ${USER} ${HOME_DIR}/glassfish4/bin/asadmin --user=admin --passwordfile=${PSWD_FILE} deploy --target cluster1 ${HOME_DIR}/clusterjsp.ear; break; } || sleep 2s; done"
        ]
      }
    },
    {
      "addWorkerToLB": {
        "forEach(nodes.cp)": {
          "execCmd [nodeGroup:bl]": "/root/lb_manager.sh --addhosts ${@i.intIP}"
        }
      }
    },
    {
      "addAutoScalingTriggers": {
        "execScript": {
          "script": "https://github.com/jelastic-jps/glassfish/blob/master/glassfish-cluster/scripts/add-triggers.js?raw=1",
          "params": {
            "nodeGroup": "cp",
            "resourceType": "CPU",
            "scaleUpValue": 70,
            "scaleUpLimit": 10,
            "scaleUpLoadPeriod": 1,
            "scaleDownValue": 30,
            "scaleDownLimit": 1,
            "scaleDownLoadPeriod": 5,
            "cleanOldTriggers": true
          }
        }
      }
    },
    {
      "80->28080": {
        "execCmd [nodeId:${this.nodeId}]": "iptables -t nat -I PREROUTING -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 28080 && iptables-save > /etc/iptables.rules"
      }
    },
    {
      "localhost:4848->das:4848": {
        "execCmd [nodeId:${this.nodeId}]": "sed -i \"s/http:\\/\\/localhost:4848/https:\\/\\/${nodes.das.first.nodeType}${nodes.das.first.id}-${env.domain}:4848/g\" ${HOME_DIR}/glassfish4/glassfish/domains/domain1/docroot/index.html"
      }
    }
  ],
  "success": "<table style='font-size:14px'><tr><td>Admin Console:</td><td><a href='${nodes.das.first.adminUrl}:4848' target='_blank'>${nodes.das.first.adminUrl}:4848</a></td></tr><tr><td>Login:</td><td><b>admin</b></td></tr><tr><td>Password:</td><td><b>glassfish</b></td></tr></table>"
}
```

##Minecraft Server

Personal Docker-based Minecraft server with auto-deploy.  

Set up your own Minecraft server of the latest version inside the Cloud in one click. Being based on itzg/minecraft-server Docker image, this solution is provided with an automatically generated connection link, that allows to launch your server remotely without external IP address attachment.   

To get your personal Minecraft server inside the cloud, perform the following:

- if you don’t have Jelastic account yet - scroll down to the Deploy Now section and follow the provided instruction.
- if you have Jelastic account - copy link to the manifest.jps file above and import it to the required Jelastic installation.

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https://raw.githubusercontent.com/jelastic-jps/minecraft-server/master/manifest.jps&min-version=4.6&keys=app.mircloud.host;app.jelastic.dogado.eu;app.fi.cloudplatform.fi;app.appengine.flow.ch;app.jelasticlw.com.br;app.paas.datacenter.fi;app.whelastic.net) 

[More details here](https://github.com/jelastic-jps/minecraft-server)

``` json
{
  "type": "install",
  "name": "Minecraft Server",
  "description": "Minecraft server allows players to play online or via a local area network with other people.",
  "logo": "https://github.com/jelastic-jps/minecraft-server/raw/master/images/minecraft-logo-90px.png",
  "homepage": "https://github.com/jelastic-jps/minecraft-server",
  "nodes": {
    "image": "itzg/minecraft-server",
    "env": {
      "EULA": "TRUE"
    },
    "entryPoint": "/start-server.sh",
    "cloudlets": 16,
    "nodeGroup": "cp",
    "displayName": "Minecraft"
  },
  "license": {
    "terms": {
      "en": "I agree with <a href='https://account.mojang.com/documents/minecraft_eula' target='_blank'><u>terms of service</u></a>"
    }
  },
  "onInstall": [
    [
      "updateConfiguration",
      "addEndpoint"
    ],
    {
      "restartContainers": {
        "nodeGroup": "cp"
      }
    }
  ],
  "actions": [
    {
      "updateConfiguration": {
        "execCmd [nodeGroup:cp]": {
          "commands": [
            "echo \"eula=true\" > /data/eula.txt",
            "sed  -i \"/usermod\\|groupmod/d\" /start",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/properties/server.properties -O /data/server.properties",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/lib/jelastic-gc-agent.jar -O /data/jelastic-gc-agent.jar",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/scripts/memoryConfig.sh -O /data/memoryConfig.sh",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/scripts/start-server.sh -O /start-server.sh",
            "chmod +x /start-server.sh",
            "mkdir -p /data/web/",
            "chown -R minecraft:minecraft /data",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/web/index.html -O /data/web/index.html",
            "wget https://github.com/jelastic-jps/minecraft-server/raw/master/scripts/start-web.sh -O /data/start-web.sh",
            "bash /data/start-web.sh"
          ],
          "user": "minecraft"
        }
      }
    },
    {
      "addEndpoint": {
        "script": "https://github.com/jelastic-jps/minecraft-server/raw/master/scripts/addEndpoint.js",
        "params": {
          "nodeId": "${nodes.cp.first.id}",
          "port": 25565
        }
      }
    }
  ]
}
```

##CI from Git Repo
Automated CI from private GIT repository with authentication via private SSH key.

With a help of this JPS add-on, Git-Push-Deploy is installed on app server available in the environment to provide possibility to connect and update the project in automatic mode from Git repository after changes pushed.

In order to get this solution instantly deployed, click the "Deploy" button, specify your email address within the widget, choose one of the [Jelastic Public Cloud providers](https://jelastic.cloud) and press Install.

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fgit-push-deploy%2Fraw%2Fmaster%2Fmanifest.jps)

[More details here](https://github.com/jelastic-jps/git-push-deploy)
``` json
{
  "type": "install",
  "name": "Git-Push-Deploy Example",
  "homepage": "https://github.com/jelastic-jps/git-push-deploy",
  "description": "Example of continuous integration (CI) with git-push-deploy ",
  "nodes": {
    "cloudlets": 16,
    "nodeGroup": "cp",
    "nodeType": "apache2"
  },
  "engine": "php5.6",
  "onInstall": [
    {
      "script": "https://raw.githubusercontent.com/jelastic-jps/git-push-deploy/master/add-git-project.cs",
      "params": {
        "url": "github.com:jelastic-jps/test-private-repo.git",
        "branch": "master"
      }
    },
    "after-deploy-hook",
    {
      "log": "installed successfully"
    }
  ],
  "actions": [
    {
      "after-deploy-hook": {
        "execCmd [nodeGroup:cp]": [
          "mkdir -p /opt/repo/ROOT/.git/hooks/",
          "printf '#!/bin/bash\nsudo /etc/init.d/cartridge reload >> /var/log/reload.log\n' > /opt/repo/ROOT/.git/hooks/post-merge",
          "chmod +x /opt/repo/ROOT/.git/hooks/post-merge"
        ]
      }
    },
    {
      "log": {
        "log": "${this.message}"
      }
    }
  ]
}
```

##WildFly Continuous Deployment

Bundle of WildFly application server and Maven build node for CD from GIT.

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https://raw.githubusercontent.com/jelastic-jps/wildfly/master/manifest.jps) 

[More details here](https://github.com/jelastic-jps/wildfly)
``` json
{
  "type": "install",
  "logo": "https://github.com/jelastic-jps/wildfly/raw/master/images/wildfly-logo-70px.png",
  "name": "WildFly Continuous Deployment",
  "categories": [
    "apps/dev-and-admin-tools"
  ],
  "homepage": "https://github.com/jelastic-jps/wildfly",
  "description": {
    "text": "The package automatically installs WildFly 10 and Maven 3, connects them to each other and integrate public Git repo for continuous deployment. Additional automation options like triggered deployments, auto clustering and auto scaling are available at info@jelastic.com.",
    "short": "Continuous Deployment option for WildFly to automatically integrate projects from Git SVN."
  },
  "settings": {
    "fields": {
      "name": "repo",
      "caption": "Git Public Repo URL",
      "type": "string",
      "inputType": "string",
      "default": "https://github.com/jelastic/HelloWorld.git",
      "required": "true"
    }
  },
  "nodes": [
    {
      "cloudlets": 16,
      "nodeGroup": "cp",
      "nodeType": "wildfly10",
      "displayName": "App Server"
    },
    {
      "cloudlets": 32,
      "nodeGroup": "build",
      "nodeType": "maven3",
      "displayName": "Build Node"
    }
  ],
  "ssl": true,
  "engine": "java8",
  "onInstall": [
    {
      "script": "https://raw.githubusercontent.com/jelastic-jps/wildfly/master/scripts/add-public-git-repo.js",
      "params": {
        "name": "HelloWorld",
        "url": "${settings.repo}",
        "branch": "master"
      }
    },
    {
      "script": "return jelastic.env.control.ResetNodePasswordById('${env.envName}', session, ${nodes.cp.first.id}, '${nodes.cp.password}')"
    }
  ],
  "success": "Your WildFly Admin Console</br></br> <table style='font-size:13px; border: none;'><tr><td>URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}:4848/console/' target='_blank'>${env.protocol}://${env.domain}:4848/console/</a></td></tr>  <tr><td>Login:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>${nodes.cp.password}</td></tr></table></br>Please wait while we pull, build and deploy your project. The process may take several minutes before you get the application up and running."
}
```

##PostgreSQL Cluster

PostgreSQL Cluster with preconfigured Master-Slave replication.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fpostgresql-replication%2Fraw%2Fmaster%2Fmanifest.jps)

[More details here](https://github.com/jelastic-jps/postgresql-replication)
``` json
{
  "type": "install",
  "categories": [
    "apps/clustered-dbs",
    "apps/clusters"
  ],
  "homepage": "http://docs.jelastic.com/postgresql-database-replication",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/postgresql-replication/master/images/postgres9_logo.png",
  "description": "Master-slave replication is used to solve performance problems, to support the db backups, and to alleviate system failures. It enables data from one database server (master) to be replicated to another (slave)",
  "name": "PostgreSQL Database Replication",
  "nodes": {
    "cloudlets": 24,
    "count": 2,
    "nodeType": "postgres9"
  },
  "onInstall": "ConfigReplication",
  "actions": {
    "ConfigReplication": [
      {
        "execCmd [nodeMission:sqldb]": "wget \"https://raw.githubusercontent.com/jelastic-jps/postgresql-replication/master/scripts/execCmdScript.sh\" -O /var/lib/pgsql/script.sh 2>&1"
      },
      {
        "execCmd [nodeId:${nodes.sqldb[0].id}]": "bash -x /var/lib/pgsql/script.sh master ${nodes.sqldb[1].address} ${nodes.sqldb.password} ${nodes.sqldb[0].address} 1>> /var/lib/pgsql/log.log 2>>/var/lib/pgsql/log.log"
      },
      {
        "execCmd [nodeId:${nodes.sqldb[1].id}]": "bash -x /var/lib/pgsql/script.sh slave ${nodes.sqldb[1].address} ${nodes.sqldb.password} ${nodes.sqldb[0].address} 1>> /var/lib/pgsql/log.log 2>>/var/lib/pgsql/log.log"
      }
    ]
  },
  "success": "The environment with multiple databases has been successfully created. The login and password of your database servers are sent to your email.\nPlease wait a minute for the replication process to be completed. <br><br /> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${nodes.postgres9.url}' target='_blank'>${nodes.postgres9.url}/</a></td></tr></table>"
}
```

##MariaDB Cluster

MariaDB Cluster with preconfigured Master-Slave replication.

The JPS package deploys MariaDB Cluster with preconfigured replication that initially contains 2 database containers. The package provides the solution for solving performance problems, DB backups support, gives ability to alleviate system failures. It enables data from one database server (the master) to be replicated to another (the slave).

The target usage for replication in MariaDB databases includes:

  -  Data security
  -  Analytics
  -  Long-distance data distribution
  
[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fmariadb-replication%2Fraw%2Fmaster%2Fmanifest.jps)
  
[More details here](https://github.com/jelastic-jps/mariadb-replication)
  
``` json
{
  "type": "install",
  "categories": [
    "apps/clustered-dbs",
    "apps/clusters"
  ],
  "logo": "https://raw.githubusercontent.com/jelastic-jps/mariadb-replication/master/images/maria.png",
  "description": "Master-slave replication is used to solve performance problems, to support the db backups, and to alleviate system failures. It enables data from one database server (master) to be replicated to another (slave)",
  "name": "MariaDB Database Replication",
  "nodes": {
    "cloudlets": 16,
    "count": 2,
    "nodeType": "mariadb"
  },
  "onInstall": "configureReplication",
  "actions": {
    "configureReplication": [
      {
        "replaceInFile [nodeMission:sqldb]": {
          "path": "${SYSTEM_ETC}/my.cnf",
          "replacements": [
            {
              "pattern": ".*log-bin.*",
              "replacement": "log-bin=mysql-bin"
            },
            {
              "pattern": ".*autoconfiguration mark.*",
              "replacement": "\n"
            }
          ]
        }
      },
      {
        "replaceInFile [nodeId:${nodes.sqldb[0].id}]": {
          "path": "${SYSTEM_ETC}/my.cnf",
          "replacements": [
            {
              "pattern": "server-id\\s*= 1",
              "replacement": "server-id = 2"
            }
          ]
        }
      },
      {
        "restartNodes": {
          "nodeMission": "sqldb"
        }
      },
      {
        "execCmd [nodeId:${nodes.sqldb[0].id}]": [
          "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[1].address} IDENTIFIED BY 'rpl';\" 2>&1",
          "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port}  --rpl-user=rpl:rpl 2>&1"
        ]
      },
      {
        "restartNodes": {
          "nodeMission": "sqldb"
        }
      }
    ]
  },
  "homepage": "http://docs.jelastic.com/mariadb-master-slave-replication",
  "appVersion": "0.1",
  "success": "The environment with multiple databases has been successfully created. The login and password of your database servers are sent to your email.\nPlease wait a minute for the replication settings to be completed. The process can be monitored in the <b>cron > mysql</b> file of your database servers. This file becomes empty when the configurations are finished. <br><br /> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${nodes.mariadb.url}' target='_blank'>${nodes.mariadb.url}/</a></td></tr></table><br />To add custom domain name for your MariaDB installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation"
}
```

##MySQL Cluster

MySQL Cluster with preconfigured Master-Slave replication.

The JPS package deploys MySQL Cluster with preconfigured replication that initially contains 2 database containers. The package provides the solution for solving performance problems, DB backups support, gives ability to alleviate system failures. It enables data from one database server (the master) to be replicated to one or more database servers (the slaves).

The target usage for replication in MySQL databases includes:

  -  Data security
  -  Analytics
  -  Long-distance data distribution

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fmysql-replication%2Fraw%2Fmaster%2Fmanifest.jps)

[More details here](https://github.com/jelastic-jps/mysql-replication)

``` json
{
  "type": "install",
  "homepage": "http://docs.jelastic.com/database-master-slave-replication",
  "categories": [
    "apps/clustered-dbs",
    "apps/popular",
    "apps/clusters"
  ],
  "logo": "https://raw.githubusercontent.com/jelastic-jps/mysql-replication/master/images/mysql_new.png",
  "description": "Master-slave replication is used to solve performance problems, to support the db backups, and to alleviate system failures. It enables data from one database server (master) to be replicated to another (slave)",
  "name": "MySQL Database Replication",
  "nodes": [
    {
      "cloudlets": 16,
      "count": 2,
      "nodeType": "mysql5"
    }
  ],
  "onInstall": "configureReplication",
  "actions": {
    "configureReplication": [
      {
        "replaceInFile": {
          "nodeMission": "sqldb",
          "path": "${SYSTEM_ETC}/my.cnf",
          "replacements": [
            {
              "pattern": ".*log-bin.*",
              "replacement": "log-bin=mysql-bin"
            },
            {
              "pattern": ".*autoconfiguration mark.*",
              "replacement": "\n"
            }
          ]
        }
      },
      {
        "replaceInFile [nodeId:${nodes.sqldb[0].id}]": {
          "path": "${SYSTEM_ETC}/my.cnf",
          "replacements": {
            "pattern": "server-id\\s*= 1",
            "replacement": "server-id = 2"
          }
        }
      },
      {
        "restartNodes": [
          {
            "nodeMission": "sqldb"
          }
        ]
      },
      {
        "execCmd [nodeId:${nodes.sqldb[0].id}]": [
          "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[1].address} IDENTIFIED BY 'rpl';\" 2>&1",
          "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port}  --rpl-user=rpl:rpl 2>&1"
        ]
      },
      {
        "restartNodes": {
          "nodeMission": "sqldb"
        }
      }
    ]
  },
  "success": "The environment with multiple databases has been successfully created. The login and password of your database servers are sent to your email.\nPlease wait a minute for the replication settings to be completed. The process can be monitored in the <b>cron > mysql</b> file of your database servers. This file becomes empty when the configurations are finished. <br><br /> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${nodes.mysql5.url}' target='_blank'>${nodes.mysql5.url}/</a></td></tr></table><br />To add custom domain name for your MySQL installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation"
}
```

##Cyclos 4

Auto-deployed Cyclos 4 online bancking solution.
The JPS package deploys Cyclos 4 that initially contains 1 application server and 1 database container.
  
[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fcyclos%2Fraw%2Fmaster%2Fcyclos-4%2Fmanifest.jps)

[More details here](https://github.com/jelastic-jps/cyclos/tree/master/cyclos-4)

``` json
{
  "type": "install",
  "logo": "https://github.com/jelastic-jps/cyclos/raw/master/images/cyclos.png",
  "description": "Cyclos 4 PRO is our payment platform for large businesses and organisations. It is secure and reliable JAVA software that can be installed on your server. Both application server as the database server are fully clusterable. It offers mobile banking (Mobile app, SMS, USSD*, and IVR*), online banking and much more.",
  "name": "Cyclos4 Pro",
  "categories": [
    "apps/accounting",
    "apps/popular",
    "apps/sales-and-marketing"
  ],
  "homepage": "http://www.cyclos.org/",
  "appVersion": "4.5",
  "success": "Instance address: <a href='${env.url}' target='_blank'>${env.url}</a> </br></br>To add custom domain name for your Cyclos installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>",
  "engine": "java8",
  "nodes": [
    {
      "cloudlets": 16,
      "nodeType": "tomcat7"
    },
    {
      "cloudlets": 16,
      "nodeType": "postgres9"
    }
  ],
  "onInstall": [
    "deployment",
    "configuringApp"
  ],
  "actions": [
    {
      "deployment": {
        "deploy": {
          "name": "cyclos4.war",
          "context": "ROOT",
          "archive": "https://github.com/jelastic-jps/cyclos/raw/master/cyclos-4/dumps/cyclos.zip"
        }
      }
    },
    {
      "configuringApp": [
        {
          "execCmd [nodeType:postgres9]": {
            "user": "root",
            "commands": [
              "curl -sSfL \"https://github.com/jelastic-jps/cyclos/raw/master/cyclos-4/scripts/install.sh\" -o ${SERVER_SCRIPTS}/install.sh 2>&1",
              "/bin/bash ${SERVER_SCRIPTS}/install.sh \"cyclos\" \"cyclos4\" \"${user.appPassword}\" 2>>${SERVER_SCRIPTS}/install.log 1>>${SERVER_SCRIPTS}/install.log"
            ]
          }
        },
        {
          "replaceInFile [nodeType:tomcat7]": {
            "path": "${WEBAPPS}/ROOT/WEB-INF/classes/cyclos.properties",
            "replacements": [
              {
                "pattern": "{DB_HOST}",
                "replacement": "${nodes.postgres9.address}"
              },
              {
                "pattern": "{DB_USER}",
                "replacement": "cyclos"
              },
              {
                "pattern": "{DB_PASSWORD}",
                "replacement": "${user.appPassword}"
              },
              {
                "pattern": "{DB_NAME}",
                "replacement": "cyclos4"
              }
            ]
          }
        },
        {
          "restartNodes": {
            "nodeType": "tomcat7"
          }
        }
      ]
    }
  ]
}
```

##Paraya Clusters
Java-based app server clusters with autoscaling and session replication
<h3>Payara Micro Cluster</h3>

The JPS package initially deploys one container with Payara Micro application server.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic%2Fpayara%2Fraw%2Fmaster%2Fpayara-micro-cluster%2Fmanifest.jps&min-version=4.6&keys=app.mircloud.host;app.jelastic.dogado.eu;app.fi.cloudplatform.fi;app.appengine.flow.ch;app.jelasticlw.com.br;app.paas.datacenter.fi;app.whelastic.net)

[More details here](https://github.com/jelastic-jps/payara/tree/master/payara-micro-cluster)

``` json
{
  "type": "install",
  "name": "Simple Payara Micro Cluster",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/payara/master/images/70.png",
  "categories": "apps/clusters",
  "homepage": "http://www.payara.fish/",
  "description": {
    "text": "Autoscalable and Highly Available Payara Micro Cluster",
    "short": "Payara Micro Cluster with session replication based on Hazelcast"
  },
  "nodes": {
    "cloudlets": 16,
    "nodeGroup": "cp",
    "image": "jelastic/payara-micro-cluster",
    "env": {
      "HAZELCAST_GROUP": "CHANGE_ME",
      "HAZELCAST_PASSWORD": "CHANGE_ME",
      "VERT_SCALING": "true"
    },
    "volumes": [
      "/opt/payara/deployments",
      "/opt/payara/config",
      "/var/log"
    ]
  },
  "onBeforeServiceScaleOut[nodeGroup:cp]": "addClusterMembers",
  "onAfterScaleIn[nodeGroup:cp]": {
    "forEach(event.response.nodes)": {
      "execCmd [nodeGroup:cp]": "$PAYARA_PATH/bin/clusterManager.sh --removehost ${@i.intIP}"
    }
  },
  "onInstall": "addClusterMembers",
  "actions": {
    "addClusterMembers": {
      "forEach(nodes.cp)": {
        "execCmd [nodeGroup:cp]": "$PAYARA_PATH/bin/clusterManager.sh --addhost ${@i.intIP}"
      }
    }
  }
}
```

<h3>Payara Server Full</h3>

The JPS package initially deploys one container with Payara Server Full. The package is based on the official Payara Docker image.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic%2Fpayara%2Fraw%2Fmaster%2Fpayara-server-full%2Fmanifest.jps&min-version=4.6&keys=app.mircloud.host;app.jelastic.dogado.eu;app.fi.cloudplatform.fi;app.appengine.flow.ch;app.jelasticlw.com.br;app.paas.datacenter.fi;app.whelastic.net)

[More details here](https://github.com/jelastic-jps/payara/tree/master/payara-server-full)

``` json
{
  "type": "install",
  "name": "Payara Server Full",
  "homepage": "http://www.payara.fish/",
  "description": "Example of Payara Server in Docker",
  "nodes": {
    "cloudlets": 16,
    "nodeGroup": "cp",
    "image": "payara/server-full",
    "cmd": "/opt/payara41/bin/asadmin start-domain"
  },
  "onInstall": {
    "script": "https://raw.githubusercontent.com/jelastic/payara/master/payara-server-full/add-endpoint.js",
    "params": {
      "nodeGroup": "cp",
      "name": "AdminPort",
      "port": 4848
    }
  }
}
```

<h3>Payara Micro Cluster Multicast</h3>

The JPS package initially deploys one container with Payara Micro application server and one container with VTun bridge together with DCHP server for multicast networking setup across all containers in the environment.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic%2Fpayara%2Fraw%2Fmaster%2Fpayara-micro-cluster-multicast%2Fmanifest.jps&min-version=4.6&keys=app.mircloud.host;app.jelastic.dogado.eu;app.fi.cloudplatform.fi;app.appengine.flow.ch;app.jelasticlw.com.br;app.paas.datacenter.fi;app.whelastic.net)

[More details here]([More details here](https://github.com/jelastic-jps/payara/tree/master/payara-server-full)

``` json
{
  "type": "install",
  "name": "Multicast Payara Cluster",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/payara/master/images/70.png",
  "categories": "apps/clusters",
  "homepage": "https://github.com/jelastic-jps/payara/tree/master/payara-micro-cluster-multicast",
  "description": {
    "text": "Payara Micro cluster based on multicast networking",
    "short": "Payara Micro Cluster with session replication based on IP multicast"
  },
  "nodes": [
    {
      "cloudlets": 16,
      "count": 2,
      "nodeGroup": "cp",
      "image": "jelastic/payara-micro-cluster-multicast",
      "env": {
        "VTUN_PASSWORD": "CHANGE_ME"
      },
      "links": "mcast:vtun_server"
    },
    {
      "cloudlets": 16,
      "nodeGroup": "mcast",
      "displayName": "Bridge",
      "image": "jelastic/payara-micro-cluster-multicast-vtun-bridge:latest",
      "env": {
        "VTUN_PASSWORD": "CHANGE_ME"
      }
    }
  ]
}
```

<h3>Payara Micro Cluster Advanced</h3>

Autoscaling triggers + Load balancing and Auto-discovery + Storage container with pre-deployed war application.

[![Deploy](https://github.com/jelastic-jps/git-push-deploy/raw/master/images/deploy-to-jelastic.png)](https://jelastic.com/install-application/?manifest=https://raw.githubusercontent.com/jelastic-jps/payara/master/payara-micro-cluster-advanced/manifest.jps&min-version=4.6&keys=app.mircloud.host;app.jelastic.dogado.eu;app.fi.cloudplatform.fi;app.appengine.flow.ch;app.jelasticlw.com.br;app.paas.datacenter.fi;app.whelastic.net) 

[More details here]([More details here](https://github.com/jelastic-jps/payara/tree/master/payara-micro-cluster-advanced)

``` json
{
  "type": "install",
  "name": "Advanced Payara Micro Cluster",
  "categories": "apps/clusters",
  "homepage": "https://github.com/jelastic-jps/payara/tree/master/payara-micro-cluster-advanced",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/payara/master/images/70.png",
  "description": {
    "text": "The package automatically provisions Payara Micro cluster, installs autoscaling triggers, mounts storage container, deploys application war and adds load balancing layer.",
    "short": "Advanced Payara Cluster with preconfigured horizontal autoscaling, load balancing, auto-discovery and storage container with pre-deployed war application."
  },
  "nodes": {
    "cloudlets": 16,
    "nodeGroup": "cp",
    "image": "jelastic/payara-micro-cluster",
    "env": {
      "HAZELCAST_GROUP": "${fn.uuid}",
      "HAZELCAST_PASSWORD": "${fn.password}",
      "VERT_SCALING": "true"
    },
    "volumes": [
      "/opt/payara/deployments",
      "/opt/payara/config",
      "/var/log"
    ]
  },
  "onBeforeServiceScaleOut[nodeGroup:cp]": "addClusterMembers",
  "onAfterScaleIn[nodeGroup:cp]": {
    "forEach(event.response.nodes)": {
      "execCmd [nodeGroup:cp]": "$PAYARA_PATH/bin/clusterManager.sh --removehost ${@i.intIP}"
    }
  },
  "onInstall": [
    "addClusterMembers",
    {
      "action": "install-jps",
      "params": {
        "jps": [
          "https://github.com/jelastic-jps/payara/raw/master/addons/application-storage/manifest.jps",
          "https://github.com/jelastic-jps/payara/raw/master/addons/autoscaling-triggers/manifest.jps",
          "https://github.com/jelastic-jps/payara/raw/master/addons/haproxy-load-balancing/manifest.json"
        ]
      }
    }
  ],
  "actions": [
    {
      "addClusterMembers": {
        "forEach(nodes.cp)": {
          "execCmd [nodeGroup:cp]": "$PAYARA_PATH/bin/clusterManager.sh --addhost ${@i.intIP}"
        }
      }
    },
    {
      "install-jps": {
        "forEach(this.jps)": {
          "script": "https://github.com/jelastic-jps/payara/raw/master/payara-micro-cluster-advanced/proc-install-jps.js",
          "params": {
            "jps": "${@i}"
          }
        }
      }
    }
  ]
}
```
