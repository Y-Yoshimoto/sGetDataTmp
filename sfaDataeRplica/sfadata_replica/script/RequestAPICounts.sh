#!/bin/bash
#echo $CLIENTID
#echo $USERNAME
#echo $JWTKEYFILE
#echo $APPNAME
## Docs
# https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_force_data.htm#cli_reference_force_data

source subFunctions.sh

# JWT認証
sfdx force:auth:jwt:grant --clientid $CLIENTID \
--jwtkeyfile $JWTKEYFILE --username $USERNAME \
--setdefaultdevhubusername --setalias $APPNAME --setdefaultusername

# 環境イニシャライズ SOQL生成
SECONDS=0
echo $(dateFormat)", "$SECONDS",Init Environment"
initEnvironment
while read sObject
do
    setSOQLRequest $sObject &
done < getSobjectList.dat
    wait
## カラム情報データベース登録
ColumnsRegistration


while true
do
    # データ取得/データベース登録/Boxアップロード
    SECONDS=0
    echo $(dateFormat)", "$SECONDS",Get Data"
    while read sObject
    do
        getSOQLData $sObject &
    done < getSobjectList.dat
    wait
    echo $(dateFormat)", "$SECONDS",End Get Data"

    # パイプラインデータ取得/Boxアップロード
    while read pipeline
    do
        getPipeline $pipeline &
    done < getPipelineList.dat
    wait
    echo $(dateFormat)", "$SECONDS",End Update Pipeline Data"
    echo $(dateFormat)", "$SECONDS",Complete Update Data"

    # AM1時から8時間(28800秒)毎に実行
    tomorrow=$(date '+%Y-%m-%d' -d 'tomorrow')
    # 翌日1時までの秒数を算出
    intervalDay=$(expr $(date +%s -d $tomorrow) - $(date +%s -d '1 hour ago'))
    # 8時間の間隔の区切り時間までの残り時間を算出
    sleeptime=$(($intervalDay % 28800))
    # プロセススリープ
    echo $(dateFormat)", "$SECONDS", "$sleeptime" Seconds wait"
    sleep $sleeptime
done
