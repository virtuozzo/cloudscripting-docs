---
draft: false
title: "Create two environments from one JPS in different regions"
aliases: "/two-envs-in-diff-regions/"
seoindex: "index, follow"
seotitle: "Create two environments from one JPS in different regions"
seokeywords: "cloud scripting, create two environments from one jps in different regions"
seodesc: "json { \"type\": \"install\", \"application\": { \"name\": \"2Envs\", \"env\": { \"topology\": { \"engine\": \"php5.3\", \"region\": \"defaulthngroup\", \"nodes\": [{"
menu:
    docs:
        title: "Create two environments from one JPS in different regions"
        url: "/two-envs-in-diff-regions/"
        identifier: "two-envs-in-diff-regions"
---

# Create two environments from one JPS in different regions

```json
{
	"type": "install",
	"application": {
		"name": "2Envs",
		"env": {
			"topology": {
				"engine": "php5.3",
				"region": "default_hn_group",
				"nodes": [{
						"cloudlets": 16,
						"nodeType": "nginxphp"
					}
				]
			}
		},
		"onInstall": {
			"executeScript": {
				"type": "javascript",
				"script": "https://download.jelastic.com/public.php?service=files&t=169362776e246cbf756eb7aad325f676&download"
			}
		}
	}
}
```

```json
var sAppid = hivext.local.getParam("TARGET_APPID"),
    sSession = hivext.local.getParam("session"),
    sRegion = "windows1",
    sEnvGeneratedName = generateEnvName(),
    oNodes = [{
        "nodeType": "nginxphp",
        "flexibleCloudlets": 10,
        "engine": "php5.4"
    }],
    oEnv = {
        "region": sRegion,
        "engine": "php5.4",
        "shortdomain": sEnvGeneratedName
    },
    sActionkey = "createenv;" + sEnvGeneratedName;

function generateEnvName(sPrefix) {
    sPrefix = sPrefix || "env-";

    return sPrefix + parseInt(Math.random() * 100000, 10);
}

return api.env.control.CreateEnvironment(sAppid, sSession, sActionkey, oEnv, oNodes);
```
