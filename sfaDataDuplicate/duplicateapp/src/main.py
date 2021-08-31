#!/usr/bin/env python
# coding:utf-8
## 標準モジュールのインポート

# SalesforceAPIコネクター
import SalesforceConnector.RestClient as SfaC
# MongoDBコネクター接続
import MongoConnector.MongoConnector as MongoC
# Boxコネクター接続
import BoxConnector.BoxConnector as BoxC

# Boxコネクター接続
import DataJobs as DataJobs

#  補助関数読み込み
import subFunctions as sub


def main():
    print(f'{sub.nowdate()}, Info, Start.')
    
    sObjectsList = ["Account","Opportunity","Contact"]
    
    DataJob = DataJobs.MakeDataJobs()
    print(f'{sub.nowdate()}, Info, List Up Columns.')
    #DataJob.ListUpColumns(sObjectsList)
    
    # データ取得タスク設定
    print(f'{sub.nowdate()}, Info, Get sObject Data.')
    getDataTask = sub.readJson("./task/getDataTask.json")
    #print(str(getDataTask))
    #DataJob.GetsObjectData(getDataTask)
    
    # MongoDBデータ取得タスク設定
    print(f'{sub.nowdate()}, Info, Query MongoDB.')
    queryDataTask = sub.readJson("./task/queryDataTask.json")
    #print(str(queryDataTask))
    DataJob.QueryMongoDBData(queryDataTask)   

    print(f'{sub.nowdate()}, Info, End.') 

if __name__ == '__main__':
    main()
