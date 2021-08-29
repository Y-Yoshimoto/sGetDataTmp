#!/usr/bin/env python
# coding:utf-8
## 標準モジュールのインポート

# SalesforceAPIコネクター
import SalesforceConnector.RestClient as SfaC
# MongoDBコネクター接続
import MongoConnector.MongoConnector as MongoC
# Boxコネクター接続
import BoxConnector.BoxConnector as BoxC

#  補助関数読み込み
import subFunctions as sub

def main():
    print(f'{sub.nowdate()}, Info, Start.')
    
    # Salesforce
    print(f'{sub.nowdate()}, Info, Start Salesforce Connection')
    sfac = SfaC.SfaConnection()
    print(f'{sub.nowdate()}, Info, Success Salesforce Connection')
    
    ## カラム一覧表生成
    sObjectsList = ["Account","Opportunity","Contact"]
    columnsList = sum([sfac.sObjectColumns(sObject) for sObject in sObjectsList], [])
    #print(columnsList)

    # Box
    print(f'{sub.nowdate()}, Info, Start Box Connection.')
    boxc = BoxC.Connector()
    
    print(f'{sub.nowdate()}, Info, Success Box Connection')
    
    # ファイルアップロード

    boxc.uploadCurrentFolderFile("/uploadvolume/columnsList.csv")
    boxc.uploadCurrentFolderFile("/uploadvolume/columnsList.json")
    
    # MongoDB
    print(f'{sub.nowdate()}, Info, Start MongoDB Connection')
    mongoc = MongoC.Connector("sObjectData")
    print(f'{sub.nowdate()}, Info, Success MongoDB Connection')
    
    ## カラム一覧表登録
    mongoc.reCreateCollection("columnsList", columnsList)

    print(f'{sub.nowdate()}, Info, End.') 


if __name__ == '__main__':
    main()
