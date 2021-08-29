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
    DataJob.ListUpColumns(sObjectsList)
    
    print(f'{sub.nowdate()}, Info, Get sObject Data.')
    taskList = [{"sObject": "Account", "SOQL": "SELECT Id, Name, OwnerId FROM Account"}, 
                {"sObject": "Contact", "SOQL": "SELECT Id, Name, OwnerId FROM Contact"},
                {"sObject": "Contact", "SOQL": "SELECT Id, Name, OwnerId FROM Contact"}]
    DataJob.GetsObjectData(taskList)

    print(f'{sub.nowdate()}, Info, End.') 


if __name__ == '__main__':
    main()
