# Custom Scripts

You can write your custom scripts in Java or JavaScript. Inside these scripts, a set of client libraries for [Virtuozzo Application Platform API](https://www.virtuozzo.com/application-platform-api-docs/) methods calling is available.

You can bind your scripts to the ***onAfterReturn*** event to execute the required [actions](../actions/).


## Intercontainer Scripts
In order to execute a shell script inside of a container, use the [ExecuteShellCommands](../actions/#cmd) (*cmd*) action.

### Examples

- Executing bash script from URL.

@@@
```yaml
cmd [cp]: curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2
```
```json
{
  "cmd [cp]": "curl -fsS http://example.com/script.sh | /bin/bash -s arg1 arg2"
}
```
@@!

- Restoring MySQL database.

@@@
```yaml
cmd [mysql5]: curl -fsS http://example.com/script.sh | /bin/bash -s '${nodes.sqldb.password}' 'http://example.com/dump.sql' '${user.appPassword}'
```
```json
{
  "cmd [mysql5]": "curl -fsS http://example.com/script.sh | /bin/bash -s '${nodes.sqldb.password}' 'http://example.com/dump.sql' '${user.appPassword}'"
}
```
@@!

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

Here, `${nodes.sqldb.password}` is available only for the *install* installation type when a SQL node is created.

## Top Level Scripts

Using a [*script*](../actions/#script) action.

### Java

@@@
```yaml
script:
  - type: java
    params:
      greeting: Hello World!
    script: |
      return hivext.local.GetParam("greeting");
```
```json
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
@@!

<!--
**Example #1 Generate random password**
-->

### JavaScript

@@@
```yaml
script: |
  return getParam('greeting');
greeting: Hello World!
```
```json
{
  "script": "return getParam('greeting');",
  "greeting": "Hello World!"
}
```
@@!

## What’s next?

- See how to create your custom [Add-Ons](../addons/)
- Find out how to handle [Custom Responses](../handling-custom-responses/)
- Explore how to customize [Visual Settings](../visual-settings/)
- Examine a bunch of [Samples](/samples/) with operation and package examples
- See [Troubleshooting](/troubleshooting/) for helpful tips and specific suggestions
