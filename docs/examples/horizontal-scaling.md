# Automatic Horizontal Scaling

Create two Nginx PHP nodes with Nginx balancer and automatic horizontal scaling with the following rules:

- add 1 node if CPU > 70% up to 10 nodes
- remove 1 node if CPU < 5% down to 1 nodes
   
``` json
{
  "type": "install",
  "name": "Nginx PHP Auto Scaling",
  "engine": "php5.4",
  "nodes": [
    {
      "extip": true,
      "count": 2,
      "cloudlets": 16,
      "nodeType": "nginx"
    },
    {
      "count": 2,
      "cloudlets": 64,
      "nodeType": "nginxphp"
    }
  ],
  "onInstall": {
    "description": "Enable Auto Scaling Triggers",
    "script": "https://download.jelastic.com/public.php?service=files&t=f7dcaa75b7b3680af46ec6d107807c12&download"
  }
}
```

**Enable Auto Scaling Triggers script:**
      
``` json
import com.hivext.api.environment.Trigger;

var APPID = hivext.local.getParam("TARGET_APPID");
var SESSION = hivext.local.getParam("session");
triger = hivext.local.exp.wrapRequest(new Trigger(APPID, SESSION));

oRespTurnOn = triger.addTrigger({
    data : {
        "isEnabled": true,
        "name": "hs-add-nginx",
        "nodeType": "nginxphp",
        "period": 1,
        "condition": {
            "type": "GREATER",
            "value": 70,
            "resourceType": "CPU"
        },
        "actions": [
            {
                "type": "ADD_NODE",
                "customData": {
                    "limit": 10,
                    "count": 1,
                    "notify": true
                }
            }
        ]
    }
});

if (oRespTurnOn.result != 0) {
    return oRespTurnOn;
}

oRespTurnOff = triger.addTrigger({
    data : {
        "isEnabled": true,
        "name": "hs-remove-nginx",
        "nodeType": "nginxphp",
        "period": 15,
        "condition": {
            "type": "LESS",
            "value": 5,
            "resourceType": "CPU"
        },
        "actions": [
            {
                "type": "REMOVE_NODE",
                "customData": {
                    "limit": 2,
                    "count": 1,
                    "notify": true
                }
            }
        ]
    }
});


if (oRespTurnOff.result != 0) {
    return oRespTurnOff;
}

return {
    result : 0
};
```