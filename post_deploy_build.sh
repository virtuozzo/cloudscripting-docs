#!/usr/bin/env bash
GIT_CS_PATH="/var/www/webroot/git-cs-docs"
USER="cloudscripting"
HTTPS="https://"
API_REPO_URL="${HTTPS}api.github.com/repos/${USER}/docs/"
REPO_URL="${HTTPS}github.com/${USER}/docs/"
SLACK_API_SEND_MSG="slack.com/api/chat.postMessage"
BRANCH="master"
WEBROOT="/var/www/webroot/ROOT"
LOG_FILE="/var/www/webroot/post_deploy.log"
EMAILS=""
CHANNEL_ID="CKYECANDP"
#"DBS19HYHK"- test
SLACK_CS_TOKEN=""

function getLatestVersion() {
    str=$(cat ${GIT_CS_PATH}/mkdocs.yml  | tail -1 | grep -Eo '(.*):');
    latest_version=${str::-1}
}

function sendErrorMailResponse() {
    mail -s "[CS docs] ERROR POST DEPLOY&BUILD" ${EMAILS} < ${LOG_FILE}
}

function sendSuccessMailResponse() {
    mail -s "[CS docs] POST DEPLOY&BUILD" ${EMAILS} <<< "CS docs successfully updated. Commit: ${REPO_URL}commit/${SHA}"
}

function defineAttachments() {
    environment=$(hostname)

    if [ -n "${SHA}" ]; then
        commitURL="${REPO_URL}commit/${SHA}"
    fi

    field=$(
        jq --arg key0 'title' \
           --arg value0 'SHA Commit' \
           --arg key1 'value' \
           --arg value1 "${commitURL}" \
           '. | .[$key0]=$value0 | .[$key1]=$value1' \
        <<< '{}'
    )

    triggeredBy=$(
        jq --arg key0 'title' \
           --arg value0 'Triggered By' \
           --arg key1 'value' \
           --arg value1 "Post Deploy Hook" \
           '. | .[$key0]=$value0 | .[$key1]=$value1' \
        <<< '{}'
    )

    envField=$(
        jq --arg key0 'title' \
           --arg value0 'Environment' \
           --arg key1 'value' \
           --arg value1 "${environment}" \
           '. | .[$key0]=$value0 | .[$key1]=$value1' \
        <<< '{}'
    )

    echo ${result}
    if [ "${result}" -ne 0 ]; then
        errorField=$(
            jq --arg key0 'title' \
               --arg value0 'Error' \
               --arg key1 'value' \
               --arg value1 "${errorCode}" \
               '. | .[$key0]=$value0 | .[$key1]=$value1' \
            <<< '{}'
        )
        argJson="[${field},${triggeredBy},${envField},${errorField}]"
    else
        argJson="[${field},${triggeredBy},${envField}]"
    fi

    attach=$(
        jq --arg key0 'pretext' \
         --arg value0 "${Status}" \
         --arg key1 'color' \
         --arg value1 "${color}" \
         --arg key2 'text' \
         --arg value2 "" \
         --arg key3 'fields' \
         --argjson value3 "${argJson}" \
         '. | .[$key0]=$value0 | .[$key1]=$value1 | .[$key2]=$value2 | .[$key3]=$value3' \
        <<< '{}'
    )
}

function notifyInSlackChannel() {
    title=' - Build CS Docs ['${BRANCH}'] from - '${REPO_URL}

    if [ -n "$1" ]; then
        Status="Running"
        color="#b7b7b7" #grey
    fi

    if [ -n "$result" ]; then

        text="$text. Result code is - $result";

        if [ "$result" -ne 0 ]; then
            Status="Failed"
            color="#fe4141"
            errorCode=$(cat ${LOG_FILE})

        else
            Status="Succeeded"
            color="#07a41d" #green
        fi

    fi

    Status+=$title
    defineAttachments
    text="$text build CS docs from the repository - ${REPO_URL}"

    formated=$(echo $attach | sed "s/'/\\\\\'/g")
    formated='['${formated}']'
    resp=$(curl -fsSL --data-urlencode "attachments=${formated}" "${HTTPS}${SLACK_API_SEND_MSG}?token=${SLACK_CS_TOKEN}&channel=${CHANNEL_ID}&pretty=1")
    echo $resp
}

getLatestVersion

[ ! -f ${LOG_FILE} ] && touch ${LOG_FILE}

cd ${GIT_CS_PATH}
SHA=$(git rev-parse HEAD)

notifyInSlackChannel 'start'
./build.sh $latest_version > ${LOG_FILE}
result=$?
if [ "$result" != 0 ]
then
    echo "not GOOD";
    sendErrorMailResponse
else
    echo "OK";
    [ ! -d "${WEBROOT}/backup" ] && mkdir ${WEBROOT}/backup;
    cp -r ${WEBROOT}/site/* ${WEBROOT}/backup/
    ln -sfn ${GIT_CS_PATH}/site/ ${WEBROOT}/site
    sendSuccessMailResponse
fi

notifyInSlackChannel
