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
    
    ## ファイル出力/アップロード #########################
    def UploadCsvFileCurrent(self, filenameBase: str, Datas: list):
        """CSV出力しカレントフォルダーにアップロード"""
        csvFilename = "/uploadvolume/" + filenameBase + ".csv"
        sub.writerCsv(csvFilename,Datas)
        self.boxc.uploadCurrentFolderFile(csvFilename)
        
    def UploadCsvFile(self, filenameBase: str, folderId: int, Datas: list):
        """CSV出力しカレントフォルダーにアップロード"""
        csvFilename = "/uploadvolume/" + filenameBase + ".csv"
        sub.writerCsv(csvFilename,Datas)
        self.boxc.uploadFile(folderId,csvFilename)
        
    ## JSONファイル出力/アップロード #########################
    def UploadJsonFile(self, filenameBase: str, folderId: int, Datas: list):
        """JSON出力し指定フォルダーにアップロード"""
        jsonFilename = "/uploadvolume/" + filenameBase + ".json"
        sub.writerJson(jsonFilename,Datas)
        self.boxc.uploadFile(folderId,jsonFilename)
        
    ## 初期データ作成 #########################
    def ListUpColumns(self, sObjectsList: list):
        """カラムのリスト生成"""
        # Salesforcdカラム取得
        columnsList = sum([self.sfac.sObjectColumns(sObject) for sObject in sObjectsList], [])
        # Boxアップロード
        self.UploadCsvFileCurrent("sObjectColumns", columnsList)
        # MongoDB登録
        self.mongoc.reCreateCollection("sObjectColumns", columnsList)
        
    def sObjectList(self) -> list:
        """オブジェクトリスト生成"""
        sObjectList = self.sfac.sObjectList()
        # Boxアップロード
        self.UploadCsvFileCurrent("sObjectList", sObjectList)
        # MongoDB登録
        self.mongoc.reCreateCollection("sObjectList", sObjectList)
        
    ## Salesforceデータ取得 #########################
    def GetsObjectData(self, taskList: list):
        """データ取得ジョブ"""
        for task in taskList:
            print(f'{sub.nowdate()}, Info, Get {task["sObject"]} Data.')
            # Salesforcdデータ取得
            datas = self.sfac.SOQLgetQuery(task["SOQL"])
            # CSV出力/Boxアップロード
            self.UploadCsvFileCurrent(task["sObject"], datas)
            # MongoDB登録
            self.mongoc.reCreateCollection(task["sObject"], datas)
            ## MongoDBインデックス追加
            [ self.mongoc.addIndex(task["sObject"],Index) for Index in task["MongoDBIndex"] ]
        
    def GetDataTask(self, taskList: list):
        """データ取得タスク"""
        print(f'{sub.nowdate()}, Info, Start GetData Task.')
        for sObject in taskList:
            sObjectJson="./GetData/" + str(sObject) + ".json"
            self.GetsObjectData(taskList=sub.readJson(sObjectJson))
            
        
    ## Boxデータ設置 #########################
    def QueryMongoDBData(self, queryList: list):
        """MongoDBデータ出力"""
        print(f'{sub.nowdate()}, Info, Start {queryList["name"]} Querys.')
        boxFolderID = queryList["boxFolderID"]
        for task in queryList["tasks"]:
            # クエリー読み込み
            query = sub.readJson(task["query"])
            # MongoDBクエリーデータ取得取得
            datas = self.mongoc.pipelineQuery(query)
            # CSV出力/Boxアップロード
            self.UploadCsvFile(task["label"], boxFolderID ,datas)
   
    def DataSourceTask(self, taskList: list):
        """Boxデータソース作成タスク"""
        print(f'{sub.nowdate()}, Info, Start DataSource Task.')
        for queryList in taskList:
            queryTaskJson="./Tasks/" + str(queryList) + "/queryDataTask.json"
            self.QueryMongoDBData(queryList=sub.readJson(queryTaskJson))
        
    ## 特殊タスク #########################
    def ChatterBlend(self):
        """"Cahher投稿とChatterコメントの複合データソースを作成"""
        print(f'{sub.nowdate()}, Info, Start ChatterBlend Task.')
        queryTaskJson=sub.readJson("./Tasks/ChatterBlend/queryDataTask.json")
        print(str(queryTaskJson))
        boxFolderID = queryTaskJson["boxFolderID"]
        ChatterData=[]
        for task in queryTaskJson["tasks"]:
            # クエリー読み込み
            query = sub.readJson(task["query"])
            # MongoDBクエリーデータ取得取得
            datas = self.mongoc.pipelineQuery(query)
            self.UploadCsvFile(task["label"], boxFolderID ,datas)
            ChatterData += datas
        print(len(ChatterData))
        # CSV出力/Boxアップロード
        self.UploadCsvFile("Cahtter", boxFolderID ,ChatterData)
        
        
    def upsertLoginHistory(self):
        """ログイン履歴データの更新"""
        print(f'{sub.nowdate()}, Info, Update LoginHistory Data.')
        ## ログイン履歴(指定日以降のデータを取得)
        MaxLoginTime = self._CheckMaxMongodb("LoginHistory", "LoginTime")
        SOQL='''SELECT+Id,UserId,LoginTime,LoginType,SourceIp,LoginUrl,Status,ApiType,Browser,Platform,CountryIso+FROM+LoginHistory+WHERE+LoginTime+>+'''
        if MaxLoginTime is None:
            MaxLoginTime = '2019-04-01T10:00:00Z'
            SOQL += MaxLoginTime
            LoginHistory = self.sfac.SOQLgetQuery(SOQL)
            print(len(LoginHistory))
            # MongoDB登録
            self.mongoc.reCreateCollection("LoginHistory", LoginHistory)
            ## MongoDBインデックス追加
            [ self.mongoc.addIndex("LoginHistory",Index) for Index in ["Id", "UserId", "LoginTime"] ]
        else: 
            SOQL += MaxLoginTime
            LoginHistory = self.sfac.SOQLgetQuery(SOQL)
            print(len(LoginHistory))
            print(len(LoginHistory))
            self.mongoc.insertManydata("LoginHistory", LoginHistory)
        
        
    def _CheckMaxMongodb(self, collection, column):
        MaxValue = self.mongoc.searchMaxValue(collection, column)
        print(MaxValue)
        if MaxValue  is None:
            return "2020-04-01T00:00:00Z"
        return MaxValue[0:19] + "Z"