# Custom Scripts

You can write your custom scripts in Java or JavaScript. Inside these scripts, a set of client libraries for <a href="https://docs.jelastic.com/api/" target="_blank">Jelastic API</a> methods calling is available. 
You can bind your scripts to the <b>*onAfterReturn*</b> event to execute the required <a href="/creating-manifest/actions/" target="_blank">actions</a>.                


## Intercontainer Scripts
In order to execute a shell script inside of a container, the <a href="/creating-manifest/actions/#cmd" target="_blank">ExecuteShellCommands</a> action is used.                

<b>Examples</b>

Executing bash script from URL.        
``` json
{
  "cmd [cp]": "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```

Restoring MySQL database.         
``` json
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

`${nodes.sqldb.password}` - available only for *install* type when a SQL node is created               

## Top Level Scripts  

Using *script* action

<h3>Java</h3>

``` json
{
  "script": [
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

``` json
{
  "script": "return getParam('greeting');",
  "greeting": "Hello World!"
}
```
<br>
<h2> What's next?</h2>         

- See how to create your custom <a href="/creating-manifest/addons/" target="_blank">Add-Ons</a>                                

- Explore how to customize <a href="/creating-manifest/visual-settings/" target="_blank">Visual Settings</a>                

- Examine a bunch of <a href="/samples/" target="_blank">Samples</a> with operation and package examples                      

- See <a href="/troubleshooting/" target="_blank">Troubleshooting</a> for helpful tips and specific suggestions                             
