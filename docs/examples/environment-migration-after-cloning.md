# Automated Environment Migration after Cloning
```example
{
	"jpsType": "install",
	"application": {
		"name": "cloneEnv",
		"env": {
			"topology": {
				"engine": "java7",
				"nodes": [{
						"cloudlets": 16,
						"nodeType": "tomcat7"
					}, {
						"cloudlets": 16,
						"nodeType": "mysql5"
					}
				]
			},
			"onAfterClone": [{
					"executeScript": {
						"type": "javascript",
						"script": "https://download.jelastic.com/public.php?service=files&t=7e49da37a7c6345cb3a1450b45b6771e&download"
					}
				}
			]
		},
		"onInstall": {
			"call": [
					"deployApp",
					"uploadFiles",
					"createDb",
					"replaceInFiles"
			]
		},
		"procedures": [{
				"id": "deployApp",
				"onCall": [{
						"deploy": [{
								"archive": "https://download.jelastic.com/public.php?service=files&t=c3afe9748a679a132d47c0148978e3b2&download",
								"name": "share-5.0.war",
								"context": "share"
							}, {
								"archive": "https://download.jelastic.com/public.php?service=files&t=91924607b72d9211c38cfe111d424263&download",
								"name": "alfresco-5.0.war",
								"context": "alfresco"
							}
						]
					}
				]
			}, {
				"id": "uploadFiles",
				"onCall": [{
						"upload": [{
								"nodeMission": "cp",
								"sourcePath": "http://app.jelastic.com/xssu/cross/download/RTYYHA81VwNaVlRAYAw4TUMVCRBUShURWBZsHH8iIlYQQktYDwIBQmNTTEBI",
								"destPath": "${WEBAPPS}/alfresco/WEB-INF/classes/alfresco-global.properties"
							}, {
								"nodeMission": "cp",
								"sourcePath": "http://app.jelastic.com/xssu/cross/download/QjYYHA81VwNaVlRAYAw4TUMVCRBUShURWBZsHH8iIlYQQktYDwIBQmNTTEBI",
								"destPath": "${JAVA_LIB}/mysql-connector-java-5.0.8-bin.jar"
							}
						]
					}
				]
			}, {
				"id": "createDb",
				"onCall": [{
						"executeShellCommands": {
							"nodeMission": "sqldb",
							"commands": [
									"curl \"https://download.jelastic.com/public.php?service=files&t=0f65b115eb5b9cdb889d135579414321&download\" -o /tmp/script.sh 2>&1",
									"bash /tmp/script.sh \"${nodes.sqldb.password}\" 2>&1"
							]
						}
					}
				]
			}, {
				"id": "replaceInFiles",
				"onCall": [{
						"replaceInFile": [{
								"nodeMission": "cp",
								"path": "${WEBAPPS}/alfresco/WEB-INF/classes/alfresco-global.properties",
								"replacements": [{
										"pattern": "{DB_HOST}",
										"replacement": "${nodes.mysql5.address}"
									}, {
										"pattern": "{DB_USER}",
										"replacement": "root"
									}, {
										"pattern": "{DB_PASSWORD}",
										"replacement": "${nodes.mysql5.password}"
									}, {
										"pattern": "{DB_NAME}",
										"replacement": "alfresco"
									}
								]
							}, {
								"nodeMission": "cp",
								"restart": true,
								"path": "/opt/tomcat/webapps/alfresco/index.jsp",
								"replacements": [{
										"pattern": "{HOSTNAME}",
										"replacement": "${env.url}"
									}
								]
							}
						]
					}
				]
			}
		],
		"success": {
			"text": "Below you will find your admin panel link, username and password.</br></br> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/share/' target='_blank'>${env.protocol}://${env.domain}/share/</a></td></tr>  <tr><td>Admin name:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>admin</td></tr></table></br>To bind a custom domain name with your Alfresco please refer to the steps described in Jelastic <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>",
			"email": "Below you will find your admin panel link, username and password.</br></br> <table style='font-size:13px; border: none;'><tr><td>Admin panel URL:</td><td style='padding-left: 10px;'><a href='${env.protocol}://${env.domain}/share/' target='_blank'>${env.protocol}://${env.domain}/share/</a></td></tr>  <tr><td>Admin name:</td><td style='padding-left: 10px;'>admin</td></tr><tr><td>Password:</td><td style='padding-left: 10px;'>admin</td></tr></table></br>To bind a custom domain name with your Alfresco please refer to the steps described in Jelastic <a href='http://docs.jelastic.com/custom-domains' target='_blank'>documentation</a>"
		}
	}
}

```


JS script for executing actions with the newly cloned environment
```example
/**
 * The script is subscribed on the onAfterClone event and will be executed after old environment cloning.
 */

import com.hivext.api.environment.Environment;
import com.hivext.api.environment.File;
import com.hivext.api.Response;

var CLONED_ENV_APPID = "${event.response.env.appid}", // placeholder for the cloned environment AppID

    APP_CONFIG_FILE_PATH = "/opt/tomcat/webapps/alfresco/WEB-INF/classes/alfresco-global.properties", // path to Alfresco config, where the database connection string should be replaced
    APP_INDEX_FILE_PATH = "/opt/tomcat/webapps/alfresco/index.jsp", // path to the Alfresco index.jsp file for the new environment URL substitution
    SOURCE_ENV_URL = "${env.url}", // placeholder for the old environment URL; will be substituted during the script execution

    NODE_TYPE_CP = "tomcat7", // keyword of the compute node's software stack.
    NODE_TYPE_DB = "mysql5", // keyword of the DB node's software stack

    HN_GROUP_PROFIT_BRICKS = "pbricks-de", // identifier of the hardware node group a new environment should be migrated to
    HN_GROUP_DEFAULT = "default_hn_group"; // second hardware node group's identifier

/**
 * Adjust application settings according to a new database connection string
 * @param {Object} oClonedEnvInfo - meta information of the cloned environment
 * @returns {Response}
 */
function configureAppSettings(oClonedEnvInfo) {
    var oFileService,
        oResp,
        sDbAddress;

    // convert environment info into JSON format
    oClonedEnvInfo = toNative(oClonedEnvInfo);

    oFileService = hivext.local.exp.WrapRequest(new File(CLONED_ENV_APPID, session));

    // fetch internal IP address of a new database node 
    oClonedEnvInfo.nodes.every(function (oNode) {

        if (oNode.nodeType == NODE_TYPE_DB) {
            sDbAddress =  oNode.address;

            return false;
        }
    });

    // adjust old database connection string with parameters of the cloned one
    oResp = oFileService.replaceInBody({
        path : APP_CONFIG_FILE_PATH,
        nodeType : NODE_TYPE_CP,
        pattern : "db.url=jdbc:mysql://.*",
        replacement : "db.url=jdbc:mysql://" + sDbAddress + "/alfresco?useUnicode=yes\\&characterEncoding=UTF-8"
    });

    if (!oResp.isOK()) {
        return oResp;
    }

    // replace environment URL with the cloned one
    return oFileService.replaceInBody({
        path    : APP_INDEX_FILE_PATH,
        nodeType: NODE_TYPE_CP,
        pattern : SOURCE_ENV_URL,
        replacement: oClonedEnvInfo.url
    });
}

/**
 * Method for migrating new environment to another hardware node group
 * @param {object} oEnvService - new environment service
 * @param {object} oClonedEnvInfo - meta information about the cloned environment
 * @returns {Response}
 */
function migrateEnv(oEnvService, oClonedEnvInfo) {
    var sHardwareNodeGroup;

    // convert environment info into JSON format
    oClonedEnvInfo = toNative(oClonedEnvInfo);

    // get current environment hardware node group from environment meta information
    sHardwareNodeGroup = oClonedEnvInfo.env.hardwareNodeGroup;

    // migrate environment API to another hardware node group
    return oEnvService.migrate({
        hardwareNodeGroup   : (sHardwareNodeGroup == HN_GROUP_PROFIT_BRICKS) ? HN_GROUP_DEFAULT : HN_GROUP_PROFIT_BRICKS,
        isOnline            : true
    });
}

/**
 * Main method for executing actions with cloned environment
 * @returns {Response}
 */
function processEnvironment() {
    var oClonedEnvInfo,
        oEnvService,
        oResp;

    oEnvService = hivext.local.exp.WrapRequest(new Environment(CLONED_ENV_APPID, session));

    // Get meta information of the new environment.
    // Meta information includes all the data about environment, comprised nodes and their properties
    oClonedEnvInfo = oEnvService.getEnvInfo();

    if (!oClonedEnvInfo.isOK()) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the cloned environment properties
    oResp = configureAppSettings(oClonedEnvInfo);

    if (!oResp.isOK()) {
        return oResp;
    }

    // migrate cloned environment to a new hardware node group, located in another region
    oResp = migrateEnv(oEnvService, oClonedEnvInfo);

    if (!oResp.isOK()) {
        return oResp;
    }

    // Get meta information of the new environment after migrating into new region.
    oClonedEnvInfo = oEnvService.getEnvInfo();

    if (!oClonedEnvInfo.isOK()) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the migrated environment properties
    return configureAppSettings(oClonedEnvInfo);
}

return processEnvironment();
```

