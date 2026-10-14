---
draft: false
title: "Samples"
aliases: "/samples/"
seoindex: "index, follow"
seotitle: "Samples"
seokeywords: "cloud scripting, samples"
seodesc: "Cloud Scripting provides almost unlimited possibilities for environment management, allowing to automatically tune its settings, adjust topology"
menu:
    docs:
        title: "Samples"
        url: "/samples/"
        weight: 3
        parent: ""
        identifier: "samples"
---

# Samples

Cloud Scripting provides almost unlimited possibilities for environment management, allowing to automatically tune its settings, adjust topology, implement events handling and a lot of more. Having a pool of scripts with such basic actions prescribed can speed up the new projects development and become a basis for more complex automation solutions.

Below we provide a bunch of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions. You can use them independently or examine and adjust scripts to create your own packages.

In this section:

{{%childrenList%}}

### Operation Examples

The following list contains examples of some basic environment management procedures, which can be subsequently combined to implement more complex solutions and application lifecycle pipelines.

| Name | Description |
|---|---|
| [Hello World](/hello-world/) | Minimal install package that deploys an application into a single Apache node |
| [Automatic Vertical Scaling](/automatic-vertical-scaling/) | Optimization of Nginx Balancer workers number based on allocated CPU amount |
| [Automatic Horizontal Scaling](/automatic-horizontal-scaling/) | Setting triggers for server horizontal scaling based on load |
| [Mount Data from Storage](/mount-data-storage/) | Mounting directory from Storage node to application server |
| [Application Clustering](https://github.com/jelastic-jps/wordpress-cluster) | Building highly available and scalable clustered solution for WordPress |
| [Install Add-on within Environment Manifest](/install-add-on-inside-manifest/) | Manifest template to create an environment and attach Public IP as an add-on |
| [Create Two Environments in Different Regions](/two-environments-in-different-regions/) | Simultaneous creation of two identical environments in different regions |
| [Deploy an Image from a Custom Registry](/custom-registry/) | Provisioning a node from a private container registry with credentials from the installation form |
| [Subscription Upgrade Flow](/subscriptions/) | Handling subscription settings changes and product moves in a marketplace package |

### Add-On Examples

Use pluggable add-ons to easily extend functionality of the already existing environments without the necessity to reconfigure each of them manually.

| Name | Description |
|---|---|
| [Let's Encrypt](https://github.com/jelastic-jps/lets-encrypt) | Add-on to secure application with custom SSL for free |
| [Fail2ban](https://github.com/jelastic-jps/fail2ban) | Add-on for advanced application security with automated firewall rules tuning |
| [Managecat](https://github.com/jelastic-jps/managecat) | Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers |
    
### Complex Ready-to-Go Solutions

Virtuozzo Application Management also provides you with a set of ready-to-go preconfigured CS packages for some of the most popular solutions’ deployment and CI/CD integration. All of them can be used without any additional changes and provide all of the options for being properly tuned according to your needs.

| Name | Description |
|---|---|
| [Minio Cluster](https://github.com/jelastic-jps/minio) | Highly reliable S3-compatible storage |
| [Glassfish Cluster](https://github.com/jelastic-jps/glassfish) | Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount |
| [CI from Git Repo](https://github.com/jelastic-jps/git-push-deploy) | Automated CI from private GIT repository with authentication via private SSH key |
| [WildFly Continuous Deployment](https://github.com/jelastic-jps/wildfly) | Bundle of WildFly application server and Maven build node for CD from GIT |
| [PostgreSQL Cluster](https://github.com/jelastic-jps/postgresql-replication) | PostgreSQL Cluster with preconfigured Master-Slave replication |
| [MariaDB Cluster](https://github.com/jelastic-jps/mariadb-replication) | MariaDB Cluster with preconfigured Master-Slave replication |
| [MySQL Cluster](https://github.com/jelastic-jps/mysql-cluster) | MySQL Cluster with preconfigured different replication types |
| [Cyclos 4](https://github.com/jelastic-jps/cyclos/tree/master/cyclos-4) | Auto-deployed Cyclos 4 online bancking solution |

Сheck out even more awesome open source solutions within our [JPS Collection](https://github.com/jelastic-jps) at GitHub (continuously updating). All the given packages are completely free to use and, simultaneously, represent a good basis to learn about the Cloud Scripting possibilities.

## What's next?

- See [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions                      
- Find out the correspondence between [CS & Virtuozzo Application Management Versions](/virtuozzo-cs-correspondence/)
