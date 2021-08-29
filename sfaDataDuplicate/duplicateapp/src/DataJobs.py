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


class MakeDataJobs:
    def __init__(self):
        """コネクター接続"""
        # Salesforce
        self.sfac = SfaC.SfaConnection()
        print(f'{sub.nowdate()}, Info, Success Salesforce Connection')
        # Box
        self.boxc = BoxC.Connector()
        print(f'{sub.nowdate()}, Info, Success Box Connection')
        # MongoDB
        self.mongoc = MongoC.Connector("sObjectData")
        print(f'{sub.nowdate()}, Info, Success MongoDB Connection')
    
    def UploadCsvFileCurrent(self, filenameBase: str, Datas: list):
        """CSV出力しアップロード"""
        csvFilename = "/uploadvolume/" + filenameBase + ".csv"
        sub.writerCsv(csvFilename,Datas)
        self.boxc.uploadCurrentFolderFile(csvFilename)
        
    def ListUpColumns(self, sObjectsList: list):
        """カラムのリスト生成"""
        # Salesforcdカラム取得
        columnsList = sum([self.sfac.sObjectColumns(sObject) for sObject in sObjectsList], [])
        # Boxアップロード
        self.UploadCsvFileCurrent("sObjectColumns", columnsList)
        # MongoDB登録
        self.mongoc.reCreateCollection("sObjectColumns", columnsList)
        
    def GetsObjectData(self, taskList: list):
        for task in taskList:
            print(f'{sub.nowdate()}, Info, Get {task["sObject"]} Data.')
            # Salesforcdデータ取得
            datas = self.sfac.SOQLgetQuery(task["SOQL"])
            # Boxアップロード
            self.UploadCsvFileCurrent(task["sObject"], datas)
            # MongoDB登録
            self.mongoc.reCreateCollection(task["sObject"], datas)
        
        
        
        
        