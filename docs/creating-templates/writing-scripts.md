# Writing Scripts

Custom users’ scripts can be written in Java or JavaScript. Inside these scripts, the set of client libraries for platform’s API methods calling is available. 
A script can be subscribed to the onAfterReturn event on its outlet for, for example, execution of the [Call](/reference/actions/#call) action.


## Intercontainer Scripts
In order to execute a shell script inside the container, action [ExecuteShellCommands](/reference/actions/#executeshellcommands) is used.

**Example #1 Execute bash script from URL**
```example
{
  "executeShellCommands": [
    {
      "nodeGroup": "cp",
      "commands": [
        "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
      ]
    }
  ]
}
```

**Example #2 Restore MySQL database**

```
{
  "executeShellCommands": [
    {
      "nodeType": "mysql5",
      "commands": [
        "curl -fsS http://example.com/script.sh | /bin/bash -s '${nodes.sqldb.password}' 'http://example.com/dump.sql' '${user.appPassword}'"
      ]
    }
  ]
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

## Top level scripts
Using `executeScript` action.

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
  "executeScript": [
    {
        "type" : "js",        
        "params" : {
            "greeting" : "Hello World!"
        },
        "script" : "return getParam('greeting');"
    }
  ]
}
```

## What's next?
Learn more about using [Jelastic Cloud API](http://docs.jelastic.com/api/)
