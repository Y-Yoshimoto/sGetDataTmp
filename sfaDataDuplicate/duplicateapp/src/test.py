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
    
    # データ操作インスタンス起動
    DataJob = DataJobs.MakeDataJobs()
    
    # データ取得タスク設定 ##########################################
    print(f'{sub.nowdate()}, Info, Get sObject Datas.')
    # 基本データ取得
    #getTaskList=["BasicData"]
    #DataJob.GetDataTask(taskList=getTaskList)
    #DataJob.GetsObjectData(sub.readJson("./GetData/FeedData.json"))
    
    DataJob.ChatterBlend()
    
    # データソース作成 #############################################
    print(f'{sub.nowdate()}, Info, Query MongoDB and make DataSources.')
    


    print(f'{sub.nowdate()}, Info, End.') 

if __name__ == '__main__':
    main()
