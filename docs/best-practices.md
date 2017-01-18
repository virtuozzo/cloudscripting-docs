#Best Practices

There is a list of Jelastic manifests which published on Jelastic hosting providers.

**Operation Examples**

<table class="bs-pr">
    <tr>
        <td>
            <b>Name</b>
        </td>
        <td>
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#automatic-vertical-scaling">Automatic Vertical Scaling</a>
        </td>
        <td>
            Optimization of Nginx Balancer workers number based on allocated CPU amount
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#automatic-horizontal-scaling">Automatic Horizontal Scaling</a>
        </td>
        <td>
            Setting triggers for server horizontal scaling based on load
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#using-dockers">Docker Containers Using</a>
        </td>
        <td>
            Bundle of linked WordPress-Web and WordPress-DB Docker containers
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#wordpress-cluster">Application Clustering</a>
        </td>
        <td>
            Building highly available and scalable clustered solution for WordPress
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#automated-environment-migration-after-cloning">Migration After Cloning</a>
        </td>
        <td>
            Automatic environment migration to another region after cloning
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#create-two-environments-from-one-jps-in-different-regions">Create Environment from Script</a>
        </td>
        <td>
            Simultaneous creation of two identical environments in different regions
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#install-add-on-inside-manifest">Install Add-on within Environment Manifest</a>
        </td>
        <td>
            Manifest template to create an environment and attach Public IP as an add-on
        </td>
    </tr>
    <tr>
        <td>
            <a href="http://docs.cloudscripting.com/examples/operation-examples/#mount-data-storage">Mount Data from Storage</a>
        </td>
        <td>
            Mounting directory from Storage node to application server
        </td>
    </tr>
</table>

**Add-ons**

<table>
    <tr>
        <td>
            <b>Name</b>
        </td>
        <td>
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/lets-encrypt">Let's Encrypt</a>
        </td>
        <td>
            Add-on to secure application with custom SSL for free
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/fail2ban">Fail2ban</a>
        </td>
        <td>
            Add-on for advanced application security with automated firewall rules tuning
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/payara/tree/master/addons/haproxy-load-balancing">Managed Haproxy Load Balancer</a>
        </td>
        <td>
            Add-on to complement environment with auto-configured Docker Haproxy LB container
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/managecat">Managecat</a>
        </td>
        <td>
            Add-on to install Managecat administration console to manage and monitor Tomcat-based app servers
        </td>
    </tr>
    </table>
    
**Complex Ready-to-Go Solutions**

<table>
    <tr>
        <td>
            <b>Name</b>
        </td>
        <td>
            <b>Description</b>
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/minio">Minio Cluster</a>
        </td>
        <td>
            Highly reliable S3-compatible storage
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/glassfish">Glassfish Cluster</a>
        </td>
        <td>
            Highly available GlassFish cluster on Docker containers with scalable Worker Nodes amount
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/payara">Payara Micro Cluster</a>
        </td>
        <td>
            Java-based app server cluster with autoscaling and session replication
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/minecraft-server">Minecraft Server</a>
        </td>
        <td>
            Personal Docker-based Minecraft server with auto-deploy
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/git-push-deploy">CI from Git Repo</a>
        </td>
        <td>
            Automated CI from private GIT repository with authentication via private SSH key
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/wildfly">WildFly Continuous Deployment</a>
        </td>
        <td>
            Bundle of WildFly application server and Maven build node for CD from GIT
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/wildfly">PostgreSQL Cluster</a>
        </td>
        <td>
            PostgreSQL Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/mariadb-replication">MariaDB Cluster</a>
        </td>
        <td>
            MariaDB Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/mysql-replication">MySQL Cluster</a>
        </td>
        <td>
            MySQL Cluster with preconfigured Master-Slave replication
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://github.com/jelastic-jps/mysql-replication">Cyclos 4</a>
        </td>
        <td>
            Auto-deployed Cyclos 4 online bancking solution
        </td>
    </tr>
</table>
