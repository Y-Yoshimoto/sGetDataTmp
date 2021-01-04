#!/bin/bash
function dateFormat(){
    date "+%Y/%m/%d %H:%M:%S"
}

CnfFiles="ConfigurationFiles"
DataFiles="sObjectData"
function initEnvironment(){
    mkdir $CnfFiles
    mkdir $DataFiles
    sfdx force:schema:sobject:list -c all > allSobjectList.dat
}

function setSOQLRequest(){
    # Setting timer
    SECONDS=0
    # Setting Output file name 
    SchemaJq=$CnfFiles"/"$1"Schema.json"
    ColumnJq=$CnfFiles"/"$1"Column.json"
    SOQLFile=$CnfFiles"/Select"$1".soql"

    # Get sObject's Schema
    sfdx force:schema:sobject:describe -s $1 --json > $SchemaJq
    # Get sObject's Column
    #cat $SchemaJq  | jq '.result.fields[] | {name: .name, label: .label}' > $ColumnJq
    cat $SchemaJq  | jq '.result.fields[] | {name: .name, label: .label, sObject: "SOBJECTNAME"}' |sed -e "s/SOBJECTNAME/$1/" > $ColumnJq
    #sed -i -e "s/^SOBJECTNAME/$1/" $ColumnJq
    # make Sobject's SOQL (SELECT * FROM sObject)
    Column=$(cat $SchemaJq | jq -r '.result.fields[].name' | head -c -1| tr '\n' ',')
    echo "SELECT "$Column" FROM "$1 > $SOQLFile

    # Return 0
    echo $(dateFormat)", "$SECONDS", Set Request Schema and SOQL, "$1
    return 0
}

function setsObjectColumnsRegistration(){
    allColumnJq=$CnfFiles"/AllColumns.json"
    cat $CnfFiles/*Column.json | jq -s . > $allColumnJq
    curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://flask_sfadata_replicaapi:5000/registration/sObjectColumns/ -d @./$allColumnJq
}

function getSOQLData(){
    # Setting timer
    SECONDS=0
    # Setting Output file name
    SOQLFile=$CnfFiles"/""Select"$1".soql"
    ROWdataJq=$DataFiles"/Row"$1"Data.json"
    dataJq=$DataFiles"/"$1"Data.json"
    # Make SOQL
    SOQL=$(cat $SOQLFile)

    # Get sObject's Data
    sfdx force:data:soql:query -q "$SOQL" -r json > $ROWdataJq
    cat $ROWdataJq | jq '.result.records[]' | jq 'del(.attributes)' | jq -s . > $dataJq

    # Return 0
    echo $(dateFormat)", "$SECONDS", Get sObject's Data, "$1
    SECONDS=0
    postBulkRegistration $1
    echo $(dateFormat)", "$SECONDS", Push sObject's Data, "$1
    return 0
}

function postBulkRegistration(){
    #curl --noproxy "*" http://flask_sfadata_replicaapi:5000/healthCheck
    curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://flask_sfadata_replicaapi:5000/registration/$1/ -d @./$DataFiles/$1Data.json
}

#curl --noproxy "*" -L -X POST -H "Content-Type: application/json" http://flask_sfadata_replicaapi:5000/registration/Opportunity/ -d @./sObjectData/OpportunityData.json
