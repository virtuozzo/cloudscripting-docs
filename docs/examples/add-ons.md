#Add-ons

##Free SSL Let’s Encrypt Add-On

Add-on to secure application with custom SSL for free.  
Let’s Encrypt Add-on for Automatic SSL Configuration of Your Jelastic Environment.  
This add-on allows to configure SSL for:

 - Internal environment address
 - Custom domains
 
 See [more details about add-on installation and configuration here.](https://github.com/jelastic-jps/lets-encrypt)

``` json
{
  "type": "update",
  "id": "letsencrypt-ssl-addon",
  "name": "Let's Encrypt Free SSL",
  "categories": [
    "apps/dev-and-admin-tools"
  ],
  "targetNodes": {
    "nodeType": [
      "tomcat6",
      "tomcat7",
      "tomcat8",
      "tomcat9",
      "tomee",
      "glassfish3",
      "glassfish4",
      "jetty6",
      "apache2",
      "nginxphp",
      "apache2-ruby",
      "nginx-ruby",
      "nginx",
      "haproxy",
      "apache-lb"
    ]
  },
  "Appversion": "1.1",
  "homepage": "https://github.com/jelastic-jps/lets-encrypt",
  "logo": "https://raw.githubusercontent.com/jelastic-jps/lets-encrypt/master/images/lets-encrypt.png",
  "description": {
    "text": "<div class='description'><b>Let's Encrypt</b> is a free and open Certificate Authority (CA), aimed to simplify and automate processes of browser-trusted SSL certificates issuing and appliance.</div><div class='description'><u>Supported stacks:</u> All Jelastic certified container templates except of Jetty 8/9, JBoss/WildFly, Node.js, Apache-Python, Varnish and Docker containers (coming soon)</div><div class='warning-lower'><b>Note</b> that Public IP address(es) will be automatically attached to all nodes within the entry point environment layer (i.e. either application server or load balancer).<br></div>",
    "short": "Free tool to configure support of secured SSL connection for an environment, by either internal or custom domain name."
  },
  "onInstall": [
    {
      "execScript": {
        "type": "js",
        "script": "https://raw.githubusercontent.com/jelastic-jps/lets-encrypt/master/scripts/create-installation-script.js",
        "params": {
          "baseDir": "https://raw.githubusercontent.com/jelastic-jps/lets-encrypt/master/scripts",
          "cronTime": "0 3 * * * *"
        }
      }
    }
  ],
  "actions": [
    {
      "log": {
        "log": "${this.message}"
      }
    },
    {
      "callScript": {
        "script": "var p = eval('(' + jelastic.dev.apps.GetApp('${env.appid}').description + ')'); p['${this.action}']=1; return jelastic.dev.scripting.Eval(p.script, p)"
      }
    }
  ],
  "buttons": [
    {
      "confirmText": "Do you want to update attached SSL certificate(s)?",
      "loadingText": "Updating...",
      "action": "callScript",
      "caption": "Update",
      "successText": "SSL certificate files have been successfully updated!"
    }
  ],
  "onUninstall": {
    "call": [
      {
        "procedure": "callScript",
        "params": {
          "action": "uninstall"
        }
      }
    ]
  },
  "settings": {
    "fields": [
      {
        "type": "radio-fieldset",
        "name": "extDomain",
        "default": "currentDomain",
        "values": {
          "currentDomain": "Environment Domain Name - get test (invalid) SSL certificate for your environment internal URL to be used in testing",
          "customDomain": "Custom Domain - get valid SSL certificate for previously attached external domain(s) to be used in production"
        },
        "showIf": {
          "customDomain": [
            {
              "type": "string",
              "name": "customDomain",
              "regex": "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9])$",
              "caption": {
                "en": "Domain"
              },
              "required": true
            }
          ]
        }
      }
    ]
  },
  "success": "<div class='description'>Your Let’s Encrypt SSL certificate(s) will remain valid for 90 days. To avoid their expiration, use the Update option at add-on’s panel (you'll get the appropriate email notification beforehand).</div><div class='description'>Starting with 4.9.5 Jelastic version, this operation is handled by the system automatically.</div><br><div>Useful links:</div><div><a href='https://github.com/jelastic-jps/lets-encrypt#how-to-renew-ssl-certificate' target='_blank'>How to renew SSL certificate</div><div><a href='https://docs.jelastic.com/custom-domain-via-cname'target='_blank'>How to bind custom domain via CNAME</a></div><div><a href='https://docs.jelastic.com/custom-domain-via-arecord' target='_blank'>How to bind custom domain via A Record</a></div>"
}
```

##Jelastic Fail2Ban Add-on

Add-on for advanced application security with automated firewall rules tuning.  
Fail2Ban is an intrusion prevention software framework that protects computer servers from brute-force attacks.

Type of nodes this add-on can be applied to:

- Application server (cp)
- Load Balancing (bl)
- Database server (db)

In order to get this solution instantly deployed, click the "Get It Hosted Now" button, specify your email address within the widget, choose one of the [Jelastic Public Cloud providers](https://jelastic.cloud) and press Install.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Ffail2ban%2Fraw%2Fmaster%2Fmanifest.jps)

``` json
{
  "type": "update",
  "Appversion": "0.9.6",
  "categories": [
    "apps/others",
    "apps/management-and-monitoring"
  ],
  "description": "Fail2Ban scans log files like and bans IP addresses that make too many password failures. It updates firewall rules to reject the IP address. These rules can be defined by the user. Fail2Ban can read multiple log files such as sshd or Apache Web server ones.",
  "homepage": "http://www.fail2ban.org/",
  "logo": "https://github.com/jelastic-jps/fail2ban/raw/master/images/Fail2Ban.png",
  "targetNodes": {
    "nodeGroup": "*"
  },
  "globals": {
    "installScript": "https://github.com/jelastic-jps/fail2ban/raw/master/scripts/install.sh",
    "setupScript": "https://github.com/jelastic-jps/fail2ban/raw/master/scripts/setup.sh",
    "removeScript": "https://github.com/jelastic-jps/fail2ban/raw/master/scripts/remove.sh",
    "documentationLink": "http://www.fail2ban.org/wiki/index.php/Manual"
  },
  "menu": {
    "caption": "Remove the IP from the Ban list",
    "confirmText": "You are going to remove the IP from the Ban list. Continue?",
    "loadingText": "Performing the IP removing..",
    "action": "removeIP",
    "settings": "removeSettings",
    "successText": "The IP was removed."
  },
  "name": "Fail2Ban",
  "onInstall": [
    "installFail2ban",
    "setupFail2ban"
  ],
  "onUninstall": "removeFail2Ban",
  "actions": [
    {
      "removeIP": {
        "execCmd [nodeGroup:${targetNodes.nodeGroup}]": [
          "for jail in $(fail2ban-client status | awk -F 'Jail list:' '{ print $2}' | grep -oE '[a-z0-9\\-]*'); do fail2ban-client set $jail unbanip ${this.bannedip} 2>&1 | echo '${this.bannedip} was unbanned at '$jail; done"
        ]
      }
    },
    {
      "installFail2ban": {
        "execCmd [nodeGroup:${targetNodes.nodeGroup}]": [
          "curl -sSfL \"${globals.installScript}\" -o ${SERVER_SCRIPTS}/install.sh 2>&1",
          "/bin/bash ${SERVER_SCRIPTS}/install.sh"
        ]
      }
    },
    {
      "setupFail2ban": {
        "execCmd [nodeGroup:${targetNodes.nodeGroup}]": [
          "curl -sSfL \"${globals.setupScript}\" -o ${SERVER_SCRIPTS}/setup.sh 2>&1",
          "/bin/bash ${SERVER_SCRIPTS}/setup.sh \"${user.email}\""
        ]
      }
    },
    {
      "removeFail2Ban": {
        "execCmd [nodeGroup:${targetNodes.nodeGroup}]": [
          "curl -sSfL \"${globals.removeScript}\" -o ${SERVER_SCRIPTS}/remove.sh 2>&1",
          "/bin/bash ${SERVER_SCRIPTS}/remove.sh"
        ]
      }
    }
  ],
  "settings": {
    "removeSettings": {
      "fields": {
        "caption": "Banned IP",
        "name": "bannedip",
        "required": true,
        "type": "string",
        "regex": "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
        "regexText": "Not valid IP address."
      }
    }
  },
  "success": "Addon was successufully installed with default Jelastic configuration. If you desire to set custom behaviour for your environment - please please refer to <a href='${globals.documentationLink}' target='_blank'>ducumentation</a>"
}
```

##Managecat

Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers.  
Managecat is an administration console platform to manage, monitor and troubleshoot Apache Tomcat, Apache TomEE and all other Apache Tomcat based application servers.

Type of nodes this add-on can be applied to:

- Tomcat 8
- Tomcat 7
- Tomcat 6
- TomEE

In order to get this solution instantly deployed, click the "Get It Hosted Now" button, specify your email address within the widget, choose one of the [Jelastic Public Cloud providers](https://jelastic.cloud) and press Install.

[![GET IT HOSTED](https://raw.githubusercontent.com/jelastic-jps/jpswiki/master/images/getithosted.png)](https://jelastic.com/install-application/?manifest=https%3A%2F%2Fgithub.com%2Fjelastic-jps%2Fmanagecat%2Fraw%2Fmaster%2Fmanifest.jps)

To deploy this package to Jelastic Private Cloud, import [this JPS manifest](../../raw/master/manifest.jps) within your dashboard ([detailed instruction](https://docs.jelastic.com/environment-export-import#import)).

``` json
{
  "version": "0.4",
  "type": "update",
  "logo": "https://github.com/jelastic-jps/managecat/raw/master/images/manageCat.png",
  "onUninstall": "removeManageCat",
  "settings": {
    "fields": [
      {
        "default": "${user.email}",
        "name": "email",
        "caption": "Email",
        "vtype": "email",
        "type": "string",
        "required": true
      },
      {
        "name": "password",
        "inputType": "password",
        "caption": "Password",
        "type": "string",
        "required": true
      },
      {
        "name": "fName",
        "caption": "First Name",
        "type": "string",
        "required": false,
        "regex": "^[a-zA-Z\\s]{0,60}$",
        "regexText": "Only latin characters, whitespaces and length no more than 60 symbols."
      },
      {
        "name": "lName",
        "caption": "Last Name",
        "type": "string",
        "required": false,
        "regex": "^[a-zA-Z\\s]{0,60}$",
        "regexText": "Only latin characters, whitespaces and length no more than 60 symbols."
      }
    ]
  },
  "actions": [
    {
      "update_catalina_properties": [
        {
          "script": "https://github.com/jelastic-jps/managecat/raw/master/scripts/ArchiveDetector.js",
          "description": "Detect archive and deploy"
        },
        {
          "execCmd [nodeMission:cp]": [
            "wget -q \"https://github.com/jelastic-jps/managecat/raw/master/scripts/mcat_installer.sh\"  -O \"/tmp/mcat_installer\"",
            "bash /tmp/mcat_installer ${license.key}"
          ]
        },
        {
          "script": "https://github.com/jelastic-jps/managecat/raw/master/scripts/ReplaceServerName.js"
        }
      ]
    },
    {
      "restartApp": {
        "restartNodes": {
          "nodeMission": "cp"
        }
      }
    },
    {
      "removeManageCat": {
        "execCmd [nodeMission:cp]": [
          "[ -f /opt/tomcat/conf/catalina.properties ] && sed -i \"/com.managecat/d\"  /opt/tomcat/conf/catalina.properties 2>>/dev/null 1>>/dev/null",
          "if [ -d /opt/tomcat8 ]; then [ -f /opt/tomcat8/conf/catalina.properties ] && sed -i \"/com.managecat/d\" /opt/tomcat8/conf/catalina.properties; fi"
        ]
      }
    },
    {
      "replace": {
        "replaceInFile [nodeId:${this.nodeid}]": [
          {
            "replacements": [
              {
                "replacement": "${this.replacement}",
                "pattern": "${this.pattern}"
              }
            ],
            "path": "${this.path}"
          }
        ]
      }
    }
  ],
  "homepage": "http://www.managecat.com/",
  "Appversion": "1.0.0",
  "targetNodes": {
    "nodeType": [
      "tomcat8",
      "tomcat7",
      "tomcat6",
      "tomee"
    ]
  },
  "description": "Managecat has all the tools you need to manage, monitor and troubleshoot your Apache Tomcat instances in one view.",
  "name": "ManageCat",
  "categories": [
    "apps/others",
    "apps/management-and-monitoring"
  ],
  "license": {
    "terms": "I agree with <a href='https://saas.managecat.com/freetrial/privacy' target='_blank'><u>terms of service</u></a>",
    "url": "http://7f0a21d8a92c209144be640de301ba79.app.jelastic.com/ManageCat"
  },
  "success": "Hello ${settings.fName} </br></br>Below you will find your ManageCat SaaS platform link, username.</br></br> <table style='font-size:13px; border: none;'><tr><td> ManageCat URL:</td><td style='padding-left: 10px;'><a href='https://saas.managecat.com' target='_blank'>https://saas.managecat.com</a></td></tr>  <tr><td>User name:</td><td style='padding-left: 10px;'>${settings.email}</td></tr></table></br>",
  "onInstall": [
    "update_catalina_properties",
    "restartApp"
  ]
}
```

##Managed Haproxy Load Balancer

Add-on to complement environment with auto-configured Docker Haproxy LB container.  
``` json
{
  "type": "update",
  "name": "Managed Load Balancer for Payara micro cluster",
  "homepage": "http://www.payara.fish/",
  "description": "Autoscalable Load Balancer",
  "nodes": [
    {
      "cloudlets": 16,
      "nodeGroup": "bl",
      "image": "jelastic/haproxy-managed-lb",
      "volumes": [
        "/usr/local/etc/haproxy"
      ]
    }
  ],
  "onInstall": [
    "add-lb-layer",
    {
      "installAddon": {
        "id": "add-cluster-members-addon",
        "nodeGroup": "cp"
      }
    }
  ],
  "addons": {
    "id": "add-cluster-members-addon",
    "env": {
      "onAfterScaleOut[nodeGroup:cp]": "add-cluster-members",
      "onAfterScaleIn[nodeGroup:cp]": {
        "forEach(event.response.nodes)": {
          "execCmd [nodeGroup:bl]": "/root/lb_manager.sh --removehost ${@i.intIP}"
        }
      }
    },
    "onInstall": "add-cluster-members"
  },
  "actions": [
    {
      "add-cluster-members": {
        "forEach(nodes.cp)": {
          "execCmd [nodeGroup:bl]": "/root/lb_manager.sh --addhosts ${@i.intIP}"
        }
      }
    },
    {
      "add-lb-layer": {
        "addNodes": {
          "nodeType": "docker",
          "cloudlets": 16,
          "dockerName": "jelastic/haproxy-managed-lb",
          "dockerTag": "latest",
          "displayName": "LoadBalancer",
          "nodeGroup": "bl",
          "metadata": {
            "layer": "bl"
          }
        }
      }
    }
  ]
}
```