# Custom Scripts

Custom users scripts can be written in Java or JavaScript. Inside these scripts, the set of client libraries for <a href="https://docs.jelastic.com/api/" target="_blank">Jelastic API</a> methods calling is available. 
A script can be subscribed to the <b>*onAfterReturn*</b> event on its outlet for an execution of any <a href="http://docs.cloudscripting.com/reference/actions/" target="_blank">action</a>.          


## Intercontainer Scripts
In order to execute a shell script inside a container, the <a href="http://docs.cloudscripting.com/reference/actions/#cmd" target="_blank">ExecuteShellCommands</a> action is used.                

Executing bash script from URL
``` json
{
  "cmd [cp]": "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```

Restoring MySQL database

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

`${nodes.sqldb.password}` - available only for *type* `install`, when a SQL node is created               

## Top Level Scripts  

Using *script* action

### Java

``` json
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

### JavaScript

``` json
{
  "script ["Hello World!"]": "return getParam('greeting');"
}
```

## What's next?

Learn more about using <a href="http://docs.jelastic.com/api/" target="_blank">Jelastic Cloud API</a>.                                      
