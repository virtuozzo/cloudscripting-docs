#!/usr/bin/env bash
GIT_CS_PATH="/var/www/webroot/git-cs-docs"
USER="dzotic9"
API_REPO_URL="https://api.github.com/repos/${USER}/docs/"
REPO_URL="https://github.com/${USER}/docs/"
BRANCH="master"
WEBROOT="/var/www/webroot/ROOT"
LOG_FILE="/var/www/webroot/post_deploy.log"
EMAILS="alexey.lazarenko@jelastic.com"

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
getLatestVersion

[ ! -f ${LOG_FILE} ] && touch ${LOG_FILE}

cd ${GIT_CS_PATH}
./build.sh $latest_version > ${LOG_FILE}
result=$?
if [ "$result" != 0 ]
then
    echo "not GOOD";
    sendErrorMailResponse
else
    echo "OK";
    ln -sfn ${GIT_CS_PATH}/site/ ${WEBROOT}/site
    curl -lsSL $API_REPO_URL"commits/"$BRANCH > test
    SHA=$(grep -Poi 'sha.{4}\K[0-9a-z]*' -m 1 test)
    sendSuccessMailResponse
fi