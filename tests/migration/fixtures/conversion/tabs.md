# Example

@@@
```` yaml
# preserved
x: ${value}
url: https://example.test/a?x=1&y=2
html: <div>literal</div>
@@@
@@!
```
````
~~~ json
{"nested": [1, 2], "space": "  "}
~~~
@@!

@@@
``` bash
printf '<h1>Example</h1>\n'
```
@@!
