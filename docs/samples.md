# Samples

Cloud Scripting provides almost unlimited possibilities for environment management, allowing you to automatically tune its settings, adjust topology, implement events handling and much more. Having a pool of scripts with such basic actions can speed up new project development and become a basis for more complex automation solutions.

Below are categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions. You can use them independently or examine and adjust scripts to create your own packages.


## Operation Examples

The following list contains examples of some basic environment management procedures, which can be subsequently combined to implement more complex solutions and application lifecycle pipelines.

| Name | Description |
|------|-------------|
| [Automatic Vertical Scaling](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-vertical-scaling) | Optimization of Nginx Balancer workers number based on allocated CPU amount |
| [Automatic Horizontal Scaling](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-horizontal-scaling) | Setting triggers for server horizontal scaling based on load |
| [Application Clustering](https://github.com/jelastic-jps/wordpress-cluster) | Building highly available and scalable clustered solution for WordPress |
| [Migration After Cloning](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-environment-migration-after-cloning) | Automatic environment migration to another region after cloning |
| [Create Environment from Script](https://github.com/jelastic-jps/basic-examples/tree/master/two-environments-from-one-jps-in-diff-regions) | Simultaneous creation of two identical environments in different regions |
| [Install Add-on within Environment Manifest](https://github.com/jelastic-jps/basic-examples/tree/master/install-add-on-inside-manifest) | Manifest template to create an environment and attach Public IP as an add-on |
| [Mount Data from Storage](https://github.com/jelastic-jps/basic-examples/tree/master/mount-data-storage) | Mounting directory from Storage node to application server |


## Add-On Examples

Use pluggable add-ons to easily extend functionality of the already existing environments without the necessity to reconfigure each of them manually.

| Name | Description |
|------|-------------|
| [Let's Encrypt](https://github.com/jelastic-jps/lets-encrypt) | Add-on to secure application with custom SSL for free |
| [Fail2ban](https://github.com/jelastic-jps/fail2ban) | Add-on for advanced application security with automated firewall rules tuning |
| [Managecat](https://github.com/jelastic-jps/managecat) | Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers |


## Complex Ready-to-Go Solutions

Virtuozzo Application Platform also provides you with a set of ready-to-go preconfigured CS packages for some of the most popular solutions' deployment and CI/CD integration. All of them can be used without any additional changes and provide all of the options for being properly tuned according to your needs.

| Name | Description |
|------|-------------|
| [Glassfish Cluster](https://github.com/jelastic-jps/glassfish) | Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount |
| [CI from Git Repo](https://github.com/jelastic-jps/git-push-deploy) | Automated CI from private GIT repository with authentication via private SSH key |
| [WildFly Continuous Deployment](https://github.com/jelastic-jps/wildfly) | Bundle of WildFly application server and Maven build node for CD from GIT |
| [PostgreSQL Cluster](https://github.com/jelastic-jps/postgresql-replication) | PostgreSQL Cluster with pre-configured Primary-Secondary replication |
| [MariaDB Cluster](https://github.com/jelastic-jps/mariadb-replication) | MariaDB Cluster with pre-configured Primary-Secondary replication |
| [MySQL Cluster](https://github.com/jelastic-jps/mysql-cluster) | MySQL Cluster with pre-configured different replication types |
| [Cyclos 4](https://github.com/jelastic-jps/cyclos/tree/master/cyclos-4) | Auto-deployed Cyclos 4 online banking solution |

Сheck out even more awesome open source solutions within our [JPS Collection](https://github.com/jelastic-jps) at GitHub (continuously updating). All the given packages are completely free to use and, simultaneously, represent a good basis to learn about the Cloud Scripting possibilities.


## What’s next?

- See [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions
- Find out the correspondence between [CS & Virtuozzo Application Platform Versions](/virtuozzo-cs-correspondence/)
