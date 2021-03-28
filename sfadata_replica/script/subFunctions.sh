#!/bin/bash
function dateFormat(){
    date "+%Y/%m/%d %H:%M:%S"
}

CnfFiles="ConfigurationFiles"
DataFiles="sObjectData"
RowDataFiles="sObjectRowData"
UPLOADFOLDER="/uploadvolume"
function initEnvironment(){
    mkdir $CnfFiles
    mkdir $DataFiles
    mkdir $RowDataFiles
    sfdx force:schema:sobject:list -c all > allSobjectList.dat
}

# スキーマ情報の取得と、全データ取得SOQLの生成
function setSOQLRequest(){
    # 処理時間タイマーセット
    SECONDS=0
    # エクスポート先ファイル指定 $1: sObuject名
    SchemaJq=$CnfFiles"/"$1"Schema.json"
    ColumnJq=$CnfFiles"/"$1"Column.json"
    SOQLFile=$CnfFiles"/Select"$1".soql"

    # sObuject スキーマ情報取得
    sfdx force:schema:sobject:describe -s $1 --json > $SchemaJq
    # sObuject カラム情報データ作成取得
    cat $SchemaJq  | jq '.result.fields[] | {name: .name, label: .label, type: .type, soapType: .soapType, sObject: "SOBJECTNAME"}' |sed -e "s/SOBJECTNAME/$1/" > $ColumnJq
    # sObuject カラム名抽出とSOQL生成
    Column=$(cat $SchemaJq | jq -r '.result.fields[].name' | head -c -1| tr '\n' ',')
    echo "SELECT "$Column" FROM "$1 > $SOQLFile

    echo $(dateFormat)", "$SECONDS", Set Request Schema and SOQL, "$1
    return 0
}
# カラム情報のデータベース登録
function ColumnsRegistration(){
    allColumnJq=$CnfFiles"/AllColumns.json"
    cat $CnfFiles/*Column.json | jq -s . > $allColumnJq
    curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" -o /dev/null http://flask_sfadata_replicaapi:5000/registration/sObjectColumns -d @./$allColumnJq
}

function getSOQLData(){
    # 処理時間タイマーセット
    SECONDS=0
    # エクスポート先ファイル指定 $1: sObuject名
    SOQLFile=$CnfFiles"/""Select"$1".soql"      #SOQL
    ROWdataJq=$RowDataFiles"/Row"$1"Data.json"  #RowData
    dataJq=$DataFiles"/"$1"Data.json"           #Data
                    
    # SOQL発行/データ取得/結果取り出し
    SOQL=$(cat $SOQLFile)   
    sfdx force:data:soql:query -q "$SOQL" -r json > $ROWdataJq
    cat $ROWdataJq | jq '.result.records[]' | jq 'del(.attributes)' | jq -s . > $dataJq
    echo $(dateFormat)", "$SECONDS", Get sObject's Data, "$1
    
    # データベースデータ登録
    SECONDS=0
    dataRegistration $1
    echo $(dateFormat)", "$SECONDS", Push sObject's Data to MongoDB, "$1

    # Boxデータアップロード
    SECONDS=0
    dataUploadBox $1
    echo $(dateFormat)", "$SECONDS", Update sObject's Data to Box, "$1
    return 0
}

function dataRegistration(){
    #curl --noproxy "*" http://flask_sfadata_replicaapi:5000/healthCheck
    curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" -o /dev/null http://flask_sfadata_replicaapi:5000/registration/$1 -d @./$DataFiles/$1Data.json
    return 0
}

function dataUploadBox(){
    dataJq=$DataFiles"/"$1"Data.json"
    upDataJq=$1"Data.json"
    \cp -f $dataJq $UPLOADFOLDER"/"$upDataJq
    curl --noproxy "*" -sS -L -X POST -o /dev/null http://boxuploader:5000/upload/queryalldata/$upDataJq 
    return 0
}

function getPipeline(){
    SECONDS=0
    upDataJq=$1"Data.json"
    upDataPath=$UPLOADFOLDER"/"$upDataJq
    # データベースからパイプラインクエリー結果を取得し保存
    curl --noproxy "*" -sS -L -X GET -o upDataPath http://flask_sfadata_replicaapi:5000/data/pipeline/sample
    # Boxに取得結果を保存
    curl --noproxy "*" -sS -L -X POST -o /dev/null http://boxuploader:5000/upload/pipelinedata/$upDataJq 
    echo $(dateFormat)", "$SECONDS", Update pipeline Data to Box, "$1
    return 0
}