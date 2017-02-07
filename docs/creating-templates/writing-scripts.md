# Writing Scripts

Custom users scripts can be written in Java or JavaScript. Inside these scripts, the set of client libraries for <a href="https://docs.jelastic.com/api/" target="_blank">Jelastic API</a> methods calling is available. 
A script can be subscribed to the <b>*onAfterReturn*</b> event on its outlet for an execution of any [action](/reference/actions/).


## Intercontainer Scripts
In order to execute a shell script inside a container, the [ExecuteShellCommands](http://docs.cloudscripting.com/reference/actions/#cmd) action is used.           

**Example #1 Execute bash script from URL**
```example
{
  "cmd [cp]": "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```

**Example #2 Restore MySQL database**

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

`${nodes.sqldb.password}` - available only for *jpsType* `install`, when a SQL node is created               

## Top Level Scripts  
Using `script` action              
              
### Java   
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

### JavaScript    
```example
{
  "script ["Hello World!"]": "return getParam('greeting');"
}
```

## What's next?
Learn more about using <a href="http://docs.jelastic.com/api/" target="_blank">Jelastic Cloud API</a>.                                    
