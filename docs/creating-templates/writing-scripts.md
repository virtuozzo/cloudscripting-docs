<h1>Writing Scripts</h1>

<p dir="ltr" style="text-align: justify;">Custom users scripts can be written in Java or JavaScript. Inside these scripts, a set of client libraries for <a href="https://docs.jelastic.com/api/" target="_blank">Jelastic API</a> methods calling is available. 
A script can also be subscribed to the <b>*onAfterReturn*</b> event to execute any <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">action</a> on its outlet.                    


<h2>Intercontainer Scripts</h2>
<p dir="ltr" style="text-align: justify;">In order to execute a shell script in confines of a container, the <a href="http://docs.cloudscripting.com/reference/actions/#cmd" target="_blank">ExecuteShellCommands</a> action is used.</p>                

**Example of executing bash script from URL**
```example
{
  "cmd [cp]": "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```

**Example of restoring MySQL database**         

```
{
  "cmd [mysql5]": "curl -fsS http://example.com/script.sh | /bin/bash -s '${nodes.sqldb.password}' 'http://example.com/dump.sql' '${user.appPassword}'"
}
```

`script.sh`:

```bash
#!/bin/bash
USER="root"
PASSWORD="$1"

DUMP_URL="$2"
DUMP_PATH="/var/lib/mysql/dump.sql"

NEW_USER_NAME="test"
NEW_USER_PASS="$3"
NEW_DB_NAME="test"


curl -fs ${DUMP_URL} -o ${DUMP_PATH} 2>&1

mysql -u${USER} -p${PASSWORD} << END 
    CREATE DATABASE ${NEW_DB_NAME};
    GRANT USAGE ON *.* TO ${NEW_USER_NAME}@localhost  IDENTIFIED BY '${NEW_USER_PASS}';
    GRANT ALL PRIVILEGES ON ${NEW_USER_NAME}.* to ${NEW_DB_NAME}@localhost;
    USE ${NEW_DB_NAME};

\. ${DUMP_PATH}
END
```

`${nodes.sqldb.password}` - available only for <b>*'install'*</b> type, when a SQL node is created               


<h2>Top Level Scripts</h2>

**Examples of using a <em>script</em> action**              
              
<h3>Java</h3>   
```example
{
  "executeScript": [
    {
        "type" : "java",        
        "params" : {
            "greeting" : "Hello World!"
        },
        "script" : "return hivext.local.GetParam(\"greeting\");"
    }
  ]
}
```

<!--
**Example #1 Generate random password**
-->

<h3>JavaScript</h3>     
```example
{
  "script ["Hello World!"]": "return getParam('greeting');"
}
```
<br>
<h2>What's next?</h2>
<ul><li>Learn more about using <a href="http://docs.jelastic.com/api/" target="_blank">Jelastic Cloud API</a></li></ul>

