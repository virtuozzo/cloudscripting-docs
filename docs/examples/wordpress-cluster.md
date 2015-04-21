# Wordpress Cluster
```
{
  "jpsType": "install",
  "jpsVersion": "0.3",
  "application": {
    "categories": [
      "apps/blogs"
    ],
    "name": "WordPress Cluster",
    "version": "4.0",
    "type": "php",
    "homepage": "http://www.wordpress.org/",
    "logo": "https://download.jelastic.com/public.php?service=files&t=3da2215839f82aa50d3d961271cd1cb9&download",
    "description": {
      "text": "Get your highly available and scalable clustered solution for WordPress, the extremely popular open source CMS and blogging tool. This package is designed to ensure the load tracking and distribution, as well as automatic adjusting the amount of allocated resources according to it."
    },
    "env": {
      "topology": {
        "ha": false,
        "engine": "php5.3",
        "ssl": false,
        "nodes": [
          {
            "extip": true,
            "count": 2,
            "cloudlets": 16,
            "nodeType": "nginx"
          },
          {
            "extip": false,
            "count": 2,
            "cloudlets": 64,
            "nodeType": "nginxphp"
          },
          {
            "nodeType": "mysql5",
            "extip": false,
            "count": 2,
            "cloudlets": 16
          }
        ]
      },
      "onInit": {
        "call": [
          "deployWordpress",
          "enableAutoScaling",
          "configureBalancers",
          "installRsyncDaemon",
          "configureReplication",
          "startLsyncDaemon"
        ]
      },
      "onAfterCloneNodes": {
        "call": [
          "installRsyncDaemon",
          "startLsyncDaemon",
          "applyNewCPNode"
        ]
      },
      "onBeforeLinkNode": [
        {
          "call": "stopEvent"
        }
      ],
      "onAfterRemoveNode": [
        {
          "call": [
            "ConfigCPAddress",
            "installRsyncDaemon",
            "startLsyncDaemon"
          ]
        }
      ]
    },
    "procedures": [
      {
        "id": "deployWordpress",
        "onCall": [
          {
            "deploy": [
              {
                "archive": "https://download.jelastic.com/public.php?service=files&t=c34ba789a018267bc931a7865e1e8de2&download",
                "name": "WordPress-4.1.zip",
                "context": "ROOT"
              }
            ]
          },
          {
            "upload": [
              {
                "destPath": "${SERVER_WEBROOT}/ROOT/db-config.php",
                "sourcePath": "https://download.jelastic.com/public.php?service=files&t=d90fd50c63fe018273db1ee9923caeb4&download",
                "nodeMission": "cp"
              },
              {
                "destPath": "${SERVER_WEBROOT}/ROOT/wp-content/db.php",
                "sourcePath": "https://download.jelastic.com/public.php?service=files&t=c6a3c4018c8465bfb75c99f7ac4c2192&download",
                "nodeMission": "cp"
              }
            ]
          },
          {
            "executeScript": {
              "description": "Configuring Db connections at cp nodes by pairs",
              "type": "javascript",
              "script": "https://download.jelastic.com/public.php?service=files&t=849165f775c84ab40b15c385e905a360&download"
            }
          },
          {
            "replaceInFile": [
              {
                "nodeMission": "cp",
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
              }
            ]
          },
          {
            "upload": [
              {
                "destPath": "/var/lib/jelastic/keys/DbCreation.sh",
                "sourcePath": "https://download.jelastic.com/public.php?service=files&t=78ae5e3ad1aefe25b13685fee7520e22&download",
                "nodeMission": "sqldb"
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeMission": "sqldb",
                "commands": [
                  "/bin/bash /var/lib/jelastic/keys/DbCreation.sh '${nodes.sqldb.password}' 'https://download.jelastic.com/public.php?service=files&t=7271e1a44982fe78025d4a98be84111e&download' '${env.url}' '${env.protocol}' '${env.domain}' '${user.email}'  '${user.appPassword}' 2>&1",
                  "rm -rf /var/lib/jelastic/keys/DbCreation.sh"
                ]
              }
            ]
          },
          {
            "replaceInFile": [
              {
                "nodeMission": "cp",
                "path": "${SERVER_WEBROOT}/ROOT/wp-config.php",
                "replacements": [
                  {
                    "pattern": "<?php",
                    "replacement": "<?php\nif (!session_id())\n    session_start();"
                  }
                ]
              },
              {
                "nodeMission": "cp",
                "path": "/etc/nginx/nginx.conf",
                "replacements": [
                  {
                    "pattern": "index  index.html index.htm index.php;",
                    "replacement": "index  index.html index.htm index.php; \n \n if (!-e $request_filename ) {\nrewrite ^(.*)$ /index.php?q=$1;\n}"
                  }
                ]
              },
              {
                "nodeMission": "cp",
                "path": "/etc/nginx/nginx.conf",
                "replacements": [
                  {
                    "pattern": "worker_processes  1;",
                    "replacement": "worker_processes  8;"
                  },
                  {
                    "pattern": "#tcp_nopush     on;",
                    "replacement": "tcp_nopush on;\n    tcp_nodelay on;\n    types_hash_max_size 2048;\n    gzip                on;\n    gzip_disable        \"msie6\";\n    gzip_vary           on;\n    gzip_proxied        any;\n    gzip_comp_level     5;\n    gzip_buffers        16 8k;\n    keepalive_timeout  2;\n    gzip_http_version   1.0;\n    gzip_types          image/svg+xml text/plain text/js text/svg text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript image/png image/gif image/jpeg;\n\n    open_file_cache          max=5000  inactive=20s;\n    open_file_cache_valid    30s;\n    open_file_cache_min_uses 2;\n    open_file_cache_errors   on;"
                  },
                  {
                    "pattern": "keepalive_timeout  2;",
                    "replacement": "#keepalive_timeout  2;"
                  },
                  {
                    "pattern": "location ~ \\.php$ {",
                    "replacement": "location ~*  \\.(jpg|jpeg|png|gif|ico|css|js)$ {\\    nexpires 365d;\n    }\nlocation ~*  \\.(pdf)$ {\n        expires 30d;\n    }\n\nlocation ~ \\.php$ {"
                  }
                ]
              },
              {
                "nodeMission": "cp",
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
              },
              {
                "nodeMission": "cp",
                "path": "/etc/php-fpm.conf",
                "replacements": [
                  {
                    "pattern": "; Jelastic autoconfiguration mark",
                    "replacement": ";"
                  },
                  {
                    "pattern": "pm.max_children = 50",
                    "replacement": "pm.max_children = 10"
                  },
                  {
                    "pattern": "pm.start_servers = 40",
                    "replacement": "pm.start_servers = 10"
                  },
                  {
                    "pattern": "pm.max_spare_servers = 40",
                    "replacement": "pm.max_spare_servers = 10"
                  },
                  {
                    "pattern": "pm.min_spare_servers = 1",
                    "replacement": "pm.min_spare_servers = 2"
                  }
                ]
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeMission": "cp",
                "commands": [
                  "rm -rf ${SERVER_WEBROOT}/ROOT/sessions",
                  "mkdir ${SERVER_WEBROOT}/ROOT/sessions"
                ]
              }
            ]
          },
          {
            "restartNodes": [
              {
                "nodeMission": "cp"
              }
            ]
          }
        ]
      },
      {
        "id": "enableAutoScaling",
        "onCall": [
          {
            "executeScript": [
              {
                "description": "Enable AutoScaling trigger",
                "type": "javascript",
                "script": "https://download.jelastic.com/public.php?service=files&t=f7dcaa75b7b3680af46ec6d107807c12&download"
              }
            ]
          }
        ]
      },
      {
        "id": "configureBalancers",
        "onCall": [
          {
            "replaceInFile": [
              {
                "nodeMission": "bl",
                "path": "/etc/nginx/conf.d/cache.conf",
                "replacements": [
                  {
                    "pattern": "#proxy",
                    "replacement": "proxy"
                  }
                ]
              },
              {
                "nodeMission": "bl",
                "path": "/etc/nginx/nginx.conf",
                "replacements": [
                  {
                    "pattern": "worker_processes  1",
                    "replacement": "worker_processes  5"
                  }
                ]
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeMission": "cp",
                "commands": [
                  "sudo /etc/init.d/nginx reload 2>&1"
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "applyNewCPNode",
        "onCall": [
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.bl[0].id}",
                "commands": [
                  "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${event.response.array.address};|g\" ${HOME}/nginx-jelastic.conf",
                  "sudo /etc/init.d/nginx reload 2>&1"
                ],
                "user": "root"
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.bl[1].id}",
                "commands": [
                  "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${event.response.array.address};|g\" ${HOME}/nginx-jelastic.conf",
                  "sudo /etc/init.d/nginx reload 2>&1"
                ],
                "user": "root"
              }
            ]
          },
          {
            "executeScript": {
              "description": "Configuring db's address on new compute nodes",
              "type": "javascript",
              "script": "https://download.jelastic.com/public.php?service=files&t=1dbb2213905dfbe4696813e218af1362&download"
            }
          }
        ]
      },
      {
        "id": "configureReplication",
        "onCall": [
          {
            "replaceInFile": [
              {
                "nodeMission": "sqldb",
                "path": "${MYSQL_CONF}/my.cnf",
                "replacements": [
                  {
                    "pattern": "#log-bin=mysql-bin",
                    "replacement": "log-bin=mysql-bin"
                  }
                ]
              }
            ]
          },
          {
            "replaceInFile": [
              {
                "nodeId": "${nodes.sqldb[0].id}",
                "path": "${MYSQL_CONF}/my.cnf",
                "replacements": [
                  {
                    "pattern": "server-id\\s*= 1",
                    "replacement": "server-id = 2"
                  }
                ]
              }
            ]
          },
          {
            "restartNodes": [
              {
                "nodeMission": "sqldb"
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.sqldb[0].id}",
                "commands": [
                  "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[1].address} IDENTIFIED BY 'rpl';\" 2>&1",
                  "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port} 2>&1"
                ]
              },
              {
                "nodeId": "${nodes.sqldb[1].id}",
                "commands": [
                  "mysql -uroot -p${nodes.sqldb.password} -e \"GRANT REPLICATION SLAVE ON *.* TO rpl@${nodes.sqldb[0].address} IDENTIFIED BY 'rpl';\" 2>&1",
                  "mysqlreplicate --master=root:${nodes.sqldb.password}@${nodes.sqldb[1].address}:${nodes.sqldb.port} --slave=root:${nodes.sqldb.password}@${nodes.sqldb[0].address}:${nodes.sqldb.port} 2>&1"
                ]
              }
            ]
          },
          {
            "restartNodes": [
              {
                "nodeMission": "sqldb"
              }
            ]
          }
        ]
      },
      {
        "id": "installRsyncDaemon",
        "onCall": [
          {
            "executeScript": {
              "description": "Get compute nodes Ids and mirrors compute node's address for rsync",
              "type": "javascript",
              "script": "https://download.jelastic.com/public.php?service=files&t=b55b2cb809638c3643cbb448adb375c7&download"
            }
          }
        ]
      },
      {
        "id": "installLsync",
        "onCall": [
          {
            "executeShellCommands": [
              {
                "nodeId": "${this.nodeId}",
                "commands": [
                  "rm -rf ${SERVER_WEBROOT}/lsyncd"
                ]
              }
            ]
          },
          {
            "createDirectory": [
              {
                "nodeId": "${this.nodeId}",
                "path": "${SERVER_WEBROOT}/lsyncd"
              }
            ]
          },
          {
            "upload": [
              {
                "nodeId": "${this.nodeId}",
                "destPath": "${SERVER_WEBROOT}/lsyncd/sync.tar",
                "sourcePath": "https://download.jelastic.com/public.php?service=files&t=6d780367c8a6a290f3ecdcace7e4087e&download"
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeId": "${this.nodeId}",
                "commands": [
                  "tar -xf ${SERVER_WEBROOT}/lsyncd/sync.tar -C ${SERVER_WEBROOT}/lsyncd/"
                ]
              }
            ]
          },
          {
            "replaceInFile": [
              {
                "nodeId": "${this.nodeId}",
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
                "nodeId": "${this.nodeId}",
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
                "nodeId": "${this.nodeId}",
                "path": "${SERVER_WEBROOT}/lsyncd/etc/rsyncd.pass",
                "replacements": [
                  {
                    "pattern": "_PASSWORD",
                    "replacement": "${user.appPassword}"
                  }
                ]
              },
              {
                "nodeId": "${this.nodeId}",
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
                "nodeId": "${this.nodeId}",
                "path": "${SERVER_WEBROOT}/lsyncd/init.sh",
                "replacements": [
                  {
                    "pattern": "_INSTALL_DIRECTORY",
                    "replacement": "${SERVER_WEBROOT}/lsyncd/"
                  }
                ]
              }
            ]
          },
          {
            "executeShellCommands": [
              {
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
            ]
          }
        ]
      },
      {
        "id": "startLsyncDaemon",
        "onCall": [
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.bl[0].id}",
                "commands": [
                  "sudo /etc/init.d/nginx reload"
                ]
              },
              {
                "nodeMission": "cp",
                "commands": [
                  "${SERVER_WEBROOT}/lsyncd/usr/bin/lsyncd ${SERVER_WEBROOT}/lsyncd/etc/lsyncd.conf &>> ${SERVER_WEBROOT}/lsyncd/var/log/lsyncd_start.log"
                ]
              }
            ]
          },
          {
            "appendFile": [
              {
                "nodeMission": "cp",
                "path": "/var/spool/cron/nginx",
                "body": "*/5 * * * * /bin/bash ${SERVER_WEBROOT}/lsyncd/init.sh"
              }
            ]
          }
        ]
      },
      {
        "id": "ConfigCPAddress",
        "onCall": [
          {
            "executeScript": {
              "description": "Configure balancers after remove compute node",
              "type": "javascript",
              "script": "https://download.jelastic.com/public.php?service=files&t=26f66db839c9bd3d0c7e13131750c5bc&download"
            }
          }
        ]
      },
      {
        "id": "BLConfiguring",
        "onCall": [
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.bl[1].id}",
                "commands": [
                  "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${this.replacement};|g\" ${HOME}/nginx-jelastic.conf"
                ],
                "user": "root"
              },
              {
                "nodeId": "${nodes.bl[1].id}",
                "commands": [
                  "sudo /etc/init.d/nginx reload"
                ]
              }
            ]
          },
          {
            "executeShellCommands": [
              {
                "nodeId": "${nodes.bl[0].id}",
                "commands": [
                  "sed -ri \"s|${nodes.cp[0].address};|${nodes.cp[0].address}; server ${this.replacement};|g\" ${HOME}/nginx-jelastic.conf"
                ],
                "user": "root"
              },
              {
                "nodeId": "${nodes.bl[0].id}",
                "commands": [
                  "sudo /etc/init.d/nginx reload"
                ]
              }
            ]
          }
        ]
      },
      {
        "id": "replace",
        "onCall": [
          {
            "replaceInFile": [
              {
                "nodeId": "${this.nodeid}",
                "path": "${this.path}",
                "replacements": [
                  {
                    "pattern": "${this.pattern}",
                    "replacement": "${this.replacement}"
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    "success": {
      "text": {
        "en": "Below you will find your admin panel link, username and password.</br></br> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/wp-admin/' target='_blank'>${env.protocol}://${env.domain}/wp-admin/</a></td></tr>  <tr><td>Admin name:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>${user.appPassword}</td></tr></table></br>To add custom domain name for your Wordpress installation follow the steps described in our <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>",
        "ru": "Ниже Вы увидите адрес админ панели, логин и пароль.</br></br> <table style='font-size:13px; border: none;'><tr><td>Адрес админ панели:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/wp-admin/' target='_blank'>${env.protocol}://${env.domain}/wp-admin/</a></td></tr>  <tr><td>Логин:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Пароль:</td><td style='padding-left: 10px;'>${user.appPassword}</td></tr></table></br>Добавить внешний домен для вашего установленного WordPress следуйте шагам описаным в нашей <a href='http://docs.jelastic.com/custom-domains' target='_blank'>документации</a>"
      }
    }
  }
}
```