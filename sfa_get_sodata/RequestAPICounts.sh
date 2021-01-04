#!/bin/bash
#echo $CLIENTID
#echo $USERNAME
#echo $JWTKEYFILE
## Docs
# https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_force_data.htm#cli_reference_force_data

source subFunctions.sh

# Auth
sfdx force:auth:jwt:grant --clientid $CLIENTID \
--jwtkeyfile $JWTKEYFILE --username $USERNAME \
--setdefaultdevhubusername --setalias sfa_get_sodata --setdefaultusername

# Init Environment
SECONDS=0
echo $(dateFormat)", "$SECONDS",Init Environment"
initEnvironment
while read sObject
do
    setSOQLRequest $sObject &
done < getSobjectList.dat
    wait
setsObjectColumnsRegistration


while true
do
    SECONDS=0
    echo $(dateFormat)", "$SECONDS",Get Data"
    while read sObject
    do
        getSOQLData $sObject &
    done < getSobjectList.dat
    wait
    echo $(dateFormat)", "$SECONDS",End Get Data"

    sleep 3600
done