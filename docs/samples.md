# Samples

Cloud Scripting provides almost unlimited possibilities for environment management, allowing you to automatically tune its settings, adjust topology, implement events handling and much more. Having a pool of scripts with such basic actions can speed up new project development and become a basis for more complex automation solutions.

Below are categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions. You can use them independently or examine and adjust scripts to create your own packages.

### Operation Examples

The following list contains examples of some basic environment management procedures, which can be subsequently combined to implement more complex solutions and application lifecycle pipelines.

<table id="bs-pr">
    <tr>
        <td id="first-col">
            <b>Name</b>
        </td>
        <td id="first-col">
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Automatic Vertical Scaling](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-vertical-scaling)
        </td>
        <td>
            Optimization of Nginx Balancer workers number based on allocated CPU amount
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Automatic Horizontal Scaling](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-horizontal-scaling)
        </td>
        <td>
            Setting triggers for server horizontal scaling based on load
        </td>
    </tr>
  <!--  <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/using-docker-containers">Using Docker Containers</a>
        </td>
        <td>
            Bundle of linked WordPress-Web and WordPress-DB Docker containers
        </td>
    </tr>
    <tr> -->
        <td id="first-col">
            [Application Clustering](https://github.com/jelastic-jps/wordpress-cluster)
        </td>
        <td>
            Building highly available and scalable clustered solution for WordPress
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Migration After Cloning](https://github.com/jelastic-jps/basic-examples/tree/master/automatic-environment-migration-after-cloning)
        </td>
        <td>
            Automatic environment migration to another region after cloning
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Create Environment from Script](https://github.com/jelastic-jps/basic-examples/tree/master/two-environments-from-one-jps-in-diff-regions)
        </td>
        <td>
            Simultaneous creation of two identical environments in different regions
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Install Add-on within Environment Manifest](https://github.com/jelastic-jps/basic-examples/tree/master/install-add-on-inside-manifest)
        </td>
        <td>
            Manifest template to create an environment and attach Public IP as an add-on
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Mount Data from Storage](https://github.com/jelastic-jps/basic-examples/tree/master/mount-data-storage)
        </td>
        <td>
            Mounting directory from Storage node to application server
        </td>
    </tr>
</table>

### Add-On Examples

Use pluggable add-ons to easily extend functionality of the already existing environments without the necessity to reconfigure each of them manually.

<table id="bs-pr">
    <tr>
        <td id="first-col">
            <b>Name</b>
        </td>
        <td id="first-col">
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Let's Encrypt](https://github.com/jelastic-jps/lets-encrypt)
        </td>
        <td>
            Add-on to secure application with custom SSL for free
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Fail2ban](https://github.com/jelastic-jps/fail2ban)
        </td>
        <td>
            Add-on for advanced application security with automated firewall rules tuning
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Managecat](https://github.com/jelastic-jps/managecat)
        </td>
        <td>
            Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers
        </td>
    </tr>
    </table>

### Complex Ready-to-Go Solutions

Virtuozzo Application Platform also provides you with a set of ready-to-go preconfigured CS packages for some of the most popular solutions' deployment and CI/CD integration. All of them can be used without any additional changes and provide all of the options for being properly tuned according to your needs.

<table id="bs-pr">
    <tr>
        <td id="first-col">
            <b>Name</b>
        </td>
        <td id="first-col">
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Minio Cluster](https://github.com/jelastic-jps/minio)
        </td>
        <td>
            Highly reliable S3-compatible storage
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Glassfish Cluster](https://github.com/jelastic-jps/glassfish)
        </td>
        <td>
            Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [CI from Git Repo](https://github.com/jelastic-jps/git-push-deploy)
        </td>
        <td>
            Automated CI from private GIT repository with authentication via private SSH key
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [WildFly Continuous Deployment](https://github.com/jelastic-jps/wildfly)
        </td>
        <td>
            Bundle of WildFly application server and Maven build node for CD from GIT
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [PostgreSQL Cluster](https://github.com/jelastic-jps/postgresql-replication)
        </td>
        <td>
            PostgreSQL Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [MariaDB Cluster](https://github.com/jelastic-jps/mariadb-replication)
        </td>
        <td>
            MariaDB Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [MySQL Cluster](https://github.com/jelastic-jps/mysql-cluster)
        </td>
        <td>
            MySQL Cluster with preconfigured different replication types
        </td>
    </tr>
    <tr>
        <td id="first-col">
            [Cyclos 4](https://github.com/jelastic-jps/cyclos/tree/master/cyclos-4)
        </td>
        <td>
            Auto-deployed Cyclos 4 online bancking solution
        </td>
    </tr>
</table>

Сheck out even more awesome open source solutions within our [JPS Collection](https://github.com/jelastic-jps) at GitHub (continuously updating). All the given packages are completely free to use and, simultaneously, represent a good basis to learn about the Cloud Scripting possibilities.

## What’s next?

- See [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions
- Read [Realese Notes](/releasenotes/) to find out about the recent CS improvements
- Find out the correspondence between [CS & Virtuozzo Application Platform Versions](/virtuozzo-cs-correspondence/)
