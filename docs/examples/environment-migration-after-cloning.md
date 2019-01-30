# Automated Environment Migration after Cloning
``` json
{
	"type": "install",
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
						"script": "https://download.jelastic.com/public.php?service=files&t=a6a659b4fcb85f4289559747b5568e4e&download"
					}
				}
			]
		},
		"onInstall": {
			"call": [
					"deployApp",
					"uploadFiles",
					"createDb",
					"replaceInFiles",
					"bindDomain"
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
								"nodeGroup": "cp",
								"sourcePath": "http://app.jelastic.com/xssu/cross/download/RTYYHA81VwNaVlRAYAw4TUMVCRBUShURWBZsHH8iIlYQQktYDwIBQmNTTEBI",
								"destPath": "${WEBAPPS}/alfresco/WEB-INF/classes/alfresco-global.properties"
							}, {
								"nodeGroup": "cp",
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
							"nodeGroup": "sqldb",
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
								"nodeGroup": "cp",
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
								"nodeGroup": "cp",
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
			}, {
				"id": "bindDomain",
				"onCall": [{
						"executeScript": {
							"type": "javascript",
							"script": "https://download.jelastic.com/public.php?service=files&t=6f5ccac2b011cbc1d6239464ea0a4c97&download"
						}
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

/**
 * JS script for executing actions with the newly cloned environment.
 * The script is subscribed on the onAfterClone event and will be executed after old environment cloning.
 */
var APPID = hivext.local.getParam("TARGET_APPID"),
    CLONED_ENV_APPID = "${event.response.env.appid}", // placeholder for the cloned environment AppID

    APP_CONFIG_FILE_PATH = "/opt/tomcat/webapps/alfresco/WEB-INF/classes/alfresco-global.properties", // path to Alfresco config, where the database connection string should be replaced
    APP_INDEX_FILE_PATH = "/opt/tomcat/webapps/alfresco/index.jsp", // path to the Alfresco index.jsp file for the new environment URL substitution
    SOURCE_ENV_URL = "${env.url}", // placeholder for the old environment URL; will be substituted during the script execution

    NODE_TYPE_CP = "tomcat7", // keyword of the compute node's software stack.
    NODE_TYPE_DB = "mysql5", // keyword of the DB node's software stack

    HN_GROUP_PROFIT_BRICKS = "pbricks-de"; // second hardware node group's identifier

/**
 * Adjust application settings according to a new database connection string
 * @param {Object} oClonedEnvInfo - meta information of the cloned environment
 * @returns {Response}
 */
function configureAppSettings(oClonedEnvInfo) {
    var oFileService,
        oResp,
        sDbAddress;

    // fetch internal IP address of a new database node
    oClonedEnvInfo.nodes.some(function (oNode) {

        if (oNode.nodeType == NODE_TYPE_DB) {
            sDbAddress =  oNode.address;
        }
    });

    // adjust old database connection string with parameters of the cloned one
    oResp = jelastic.env.file.ReplaceInBody(CLONED_ENV_APPID, session, APP_CONFIG_FILE_PATH, "db.url=jdbc:mysql://.*", "db.url=jdbc:mysql://" + sDbAddress + "/alfresco?useUnicode=yes\\&characterEncoding=UTF-8", "", NODE_TYPE_CP);

    // replace environment URL with the cloned one
return jelastic.env.file.ReplaceInBody(CLONED_ENV_APPID, session, APP_INDEX_FILE_PATH, SOURCE_ENV_URL, oClonedEnvInfo.url, "", NODE_TYPE_CP);
}

/**
 * Method for migrating new environment to another hardware node group
 * @param {object} oEnvService - new environment service
 * @param {object} oClonedEnvInfo - meta information about the cloned environment
 * @returns {Response}
 */
function migrateEnv(oClonedEnvInfo) {
    // migrate environment API to another hardware node group
    return jelastic.env.control.Migrate(CLONED_ENV_APPID, session, HN_GROUP_PROFIT_BRICKS, true);
}

/**
 * Main method for executing actions with cloned environment
 * @returns {Response}
 */
function processEnvironment() {
    var oClonedEnvInfo,
        oEnvService,
        oResp;

    // Get meta information of the new environment.
    // Meta information includes all the data about environment, comprised nodes and their properties
     oClonedEnvInfo = jelastic.env.control.GetEnvInfo(CLONED_ENV_APPID, session);

    if (oClonedEnvInfo.result !== 0) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the cloned environment properties
    oResp = configureAppSettings(oClonedEnvInfo);

    if (oResp.result !== 0) {
        return oResp;
    }

    // migrate cloned environment to a new hardware node group, located in another region
/*    oResp = migrateEnv(oClonedEnvInfo);

    if (oResp.result !== 0) {
        return oResp;
    }
*/
    // Get meta information of the new environment after migrating into new region.
    oClonedEnvInfo = jelastic.env.control.GetEnvInfo(CLONED_ENV_APPID, session);

    if (oClonedEnvInfo.result !== 0) {
        return oClonedEnvInfo;
    }

    // apply new configurations according to the migrated environment properties
    oResp =  configureAppSettings(oClonedEnvInfo);

    return jelastic.env.binder.SwapExtDomains(APPID, session, CLONED_ENV_APPID);
}

return processEnvironment();
```

