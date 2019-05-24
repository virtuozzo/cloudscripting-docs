# Samples

<p dir="ltr" style="text-align: justify;">Cloud Scripting provides almost unlimited possibilities for environment management, allowing to automatically tune its settings, adjust topology, implement events handling and a lot of more. Having a pool of scripts with such basic actions prescribed can speed up the new projects development and become a basis for more complex automation solutions.</p>

<p dir="ltr" style="text-align: justify;">Below we provide a bunch of categorized CS examples, divided by sections with simple standalone operations, add-ons for existing environments and complete ready-to-go solutions. You can use them independently or examine and adjust scripts to create your own packages.</p>

### Operation Examples

<p dir="ltr" style="text-align: justify;">The following list contains examples of some basic environment management procedures, which can be subsequently combined to implement more complex solutions and application lifecycle pipelines.</p>

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
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/automatic-vertical-scaling">Automatic Vertical Scaling</a>
        </td>
        <td>
            Optimization of Nginx Balancer workers number based on allocated CPU amount
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/automatic-horizontal-scaling">Automatic Horizontal Scaling</a>
        </td>
        <td>
            Setting triggers for server horizontal scaling based on load
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/using-docker-containers">Using Docker Containers</a>
        </td>
        <td>
            Bundle of linked WordPress-Web and WordPress-DB Docker containers
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/wordpress-cluster">Application Clustering</a>
        </td>
        <td>
            Building highly available and scalable clustered solution for WordPress
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/automatic-environment-migration-after-cloning">Migration After Cloning</a>
        </td>
        <td>
            Automatic environment migration to another region after cloning
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/two-environments-from-one-jps-in-diff-regions">Create Environment from Script</a>
        </td>
        <td>
            Simultaneous creation of two identical environments in different regions
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/install-add-on-inside-manifest">Install Add-on within Environment Manifest</a>
        </td>
        <td>
            Manifest template to create an environment and attach Public IP as an add-on
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/basic-examples/tree/master/mount-data-storage">Mount Data from Storage</a>
        </td>
        <td>
            Mounting directory from Storage node to application server
        </td>
    </tr>
</table>

### Add-ons Examples

<p dir="ltr" style="text-align: justify;">Use pluggable add-ons to easily extend functionality of the already existing environments without the necessity to reconfigure each of them manually.</p>

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
            <a target="_blank" href="https://github.com/jelastic-jps/lets-encrypt">Let's Encrypt</a>
        </td>
        <td>
            Add-on to secure application with custom SSL for free
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/fail2ban">Fail2ban</a>
        </td>
        <td>
            Add-on for advanced application security with automated firewall rules tuning
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/payara/tree/master/addons/haproxy-load-balancing">Managed Haproxy Load Balancer</a>
        </td>
        <td>
            Add-on to complement environment with auto-configured Docker Haproxy LB container
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/managecat">Managecat</a>
        </td>
        <td>
            Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers
        </td>
    </tr>
    </table>
    
### Complex Ready-to-Go Solutions

<p dir="ltr" style="text-align: justify;">Jelastic also provides you with a set of ready-to-go preconfigured CS packages for some of the most popular solutions’ deployment and CI/CD integration. All of them can be used without any additional changes and provide all of the options for being properly tuned according to your needs.</p>

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
            <a target="_blank" href="https://github.com/jelastic-jps/minio">Minio Cluster</a>
        </td>
        <td>
            Highly reliable S3-compatible storage
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/glassfish">Glassfish Cluster</a>
        </td>
        <td>
            Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/payara">Payara Micro Cluster</a>
        </td>
        <td>
            Java-based app server cluster with autoscaling and session replication
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/minecraft-server">Minecraft Server</a>
        </td>
        <td>
            Personal Docker-based Minecraft server with auto-deploy
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/git-push-deploy">CI from Git Repo</a>
        </td>
        <td>
            Automated CI from private GIT repository with authentication via private SSH key
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/wildfly">WildFly Continuous Deployment</a>
        </td>
        <td>
            Bundle of WildFly application server and Maven build node for CD from GIT
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/postgresql-replication">PostgreSQL Cluster</a>
        </td>
        <td>
            PostgreSQL Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/mariadb-replication">MariaDB Cluster</a>
        </td>
        <td>
            MariaDB Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/mysql-cluster">MySQL Cluster</a>
        </td>
        <td>
            MySQL Cluster with preconfigured different replication types
        </td>
    </tr>
    <tr>
        <td id="first-col">
            <a target="_blank" href="https://github.com/jelastic-jps/cyclos/tree/master/cyclos-4">Cyclos 4</a>
        </td>
        <td>
            Auto-deployed Cyclos 4 online bancking solution
        </td>
    </tr>
</table>

<p dir="ltr" style="text-align: justify;">Сheck out even more awesome open source solutions within our <a href="https://github.com/jelastic-jps" target="_blank">JPS Collection</a> at GitHub (continuously updating). All the given packages are completely free to use and, simultaneously, represent a good basis to learn about the Cloud Scripting possibilities.</p>
<br>
<h2> What's next?</h2>

- See <a href="/troubleshooting/" target="_blank">Troubleshooting</a> for helpful tips and specific suggestions                      

- Read <a href="/releasenotes/" target="_blank">Realese Notes</a> to find out about the recent CS improvements                                      

- Find out the correspondence between <a href="/jelastic-cs-correspondence/" target="_blank">CS & Jelastic Versions</a>                                              
