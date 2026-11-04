---
title: Article
aliases: ['/old-article/']
menu:
  docs:
    identifier: article
    parent: getting-started
    weight: 20
---
# Article

[Root article](/article/?q=1#details)
[Already prefixed]({{< relref "/article" >}})
[Relative](../article/#details)
[Fragment](#details)
[Query](?q=1)
[External](https://example.org/article/)
[Protocol relative](//example.org/article/)
<a href="../article/#details" id="normalized-raw">Normalized raw HTML</a>

## Details

{{% cs-admonition type="note" title="Careful & exact" %}}

A **bold** note.

- Outer item
    - Inner item

{{% tabs %}}
{{% tabs-item title="YAML" %}}

```yaml

key: ${value}
text: "<script>& literal"
```

{{% /tabs-item %}}
{{% tabs-item title="JSON" %}}

```json {cs_trailing_newlines=2}
{"text": "x"}

```

{{% /tabs-item %}}
{{% /tabs %}}

{{% /cs-admonition %}}

```bash
#!/bin/bash
  echo "preserve spaces"
```

```text
{{</* literal */>}}
```

```yaml
onInstall:
  script [12345, 123456]: |
    return { result: 0, nodeId: nodeId };
```

```text {cs_trailing_newlines=0}
```

```text

```

```text {cs_trailing_newlines=2}


```
