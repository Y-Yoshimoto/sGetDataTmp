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

sObjectsList = ["Account",
                "Opportunity",
                "Contact",
                "User",
                "FeedItem",
                "FeedComment"]

def main():
    print(f'{sub.nowdate()}, Info, Start.')

    DataJob = DataJobs.MakeDataJobs()
    print(f'{sub.nowdate()}, Info, List Up sObjexts.')
    DataJob.sObjectList()
    

    print(f'{sub.nowdate()}, Info, List Up Columns.')
    DataJob.ListUpColumns(sObjectsList)
    
if __name__ == '__main__':
    main()

