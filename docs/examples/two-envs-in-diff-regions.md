#Create two environments from one JPS in different regions

```example
{
	"jpsType": "install",
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
			"call": "secondEnvInstallation"
		},
		"procedures": [{
				"id": "secondEnvInstallation",
				"onCall": [{
						"executeScript": {
							"type": "javascript",
							"script": "http://owncloud.demo.jelastic.com/public.php?service=files&t=ff20c945d8076e43c499a620e29c3692&download"
						}
					}
				]
			}
		]
	}
}
```

```example
import com.hivext.api.environment.Environment;

var APPID = hivext.local.getParam("TARGET_APPID"),
    SESSION = hivext.local.getParam("session"),
    oEnvService,
    oRespCreateEnv;

function generateEnvName(sPrefix) {
    sPrefix = sPrefix || "env-";

    return sPrefix + parseInt(Math.random() * 100000, 10);
}

oEnvService = hivext.local.exp.wrapRequest(new Environment(APPID, SESSION));

oEnvInfoResponse = oEnvService.getEnvInfo();
if (!oEnvInfoResponse.isOK()) {
    return oEnvInfoResponse;
}

oRespCreateEnv = oEnvService.createEnvironment({
    nodes: [{
        "nodeType": "nginxphp",
        "flexibleCloudlets": 10,
        "engine": "php5.4"
    }],
    env: {
        "region": "windows1",
        "engine": "php5.4",
        "shortdomain": generateEnvName()
    },
    actionkey : "createenv;env;expert;1;region;jelastic.com"
});

return oRespCreateEnv;
```