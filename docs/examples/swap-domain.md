# Swap domain between two environments

``` json
{
	"type": "install",
	"application": {
		"name": "swapDomain",
		"env": {
			"topology": {
				"engine": "php5.3",
				"nodes": [{
						"cloudlets": 6,
						"nodeType": "nginxphp"
					}
				]
			}
		},
		"onInstall": {
			"call": ["secondEnvInstallation"]
		},
		"procedures": [{
				"id": "secondEnvInstallation",
				"onCall": [{
						"executeScript": {
							"type": "javascript",
							"script": "https://download.jelastic.com/public.php?service=files&t=6922fed7efb17261e038bfc6d8947924&download"
						}
					}
				]
			}
		]
	}
}
```


```
import com.hivext.api.environment.Environment;
import com.hivext.api.environment.Binder;

var APPID = hivext.local.getParam("TARGET_APPID"),
    SESSION = hivext.local.getParam("session"),
    oEnvService,
    oBinderService,
    oResp,
    oAppNodes,
    sDefaultRegion,
    oCreateEnv;

function generateEnvName(sPrefix) {
    sPrefix = sPrefix || "env-";

    return sPrefix + parseInt(Math.random() * 100000, 10);
}

oEnvService = hivext.local.exp.wrapRequest(new Environment(APPID, SESSION));
oBinderService = hivext.local.exp.wrapRequest(new Binder(APPID, SESSION));

oCreateEnv =oEnvService.createEnvironment({
    nodes: [{
        "nodeType": "nginxphp",
        "engine": "php5.4",
        "flexibleCloudlets": 10,
    }],
    env: {
        "engine": "php5.4",
        "shortdomain": generateEnvName()
    },
    actionkey : "createenv;env;expert;1;region;jelastic.com"
});

java.lang.System.out.println("---------dzotic-oCreateEnv-------->" + toJSON(oCreateEnv));


if (!oCreateEnv.isOK()) {
    return oCreateEnv;
}
oCreateEnv = toNative(oCreateEnv);

oResp = oBinderService.bindExtDomain({
    "extdomain" : "testDomain.com"
});

java.lang.System.out.println("---------dzotic-oResp-BindDomain------->" + toJSON(oResp));
if (!oResp.isOK()) {
    return oResp;
}

oResp = oBinderService.swapExtDomains({
    "targetappid" : oCreateEnv.response.appid
});

java.lang.System.out.println("---------dzotic-oResp-swapDomain------->" + toJSON(oResp));

return oResp;
```
