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
        """CSV出力し指定フォルダーにアップロード"""
        csvFilename = "/uploadvolume/" + filenameBase + ".csv"
        sub.writerCsv(csvFilename,Datas)
        self.boxc.uploadFile(folderId,csvFilename)
        
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
        """
        print(f'{sub.nowdate()}, Info, Get Chatter Data.')
        ChatterData=[]
        
        taskList=sub.readJson("./GetData/FeedData.json")
        FeedItemJob = next(x for x in taskList if x["sObject"] == "FeedItem")
        FeedCommentJob = next(x for x in taskList if x["sObject"] == "FeedComment")
        
        
        FeedCommentData = self.sfac.SOQLgetQuery(FeedCommentJob["SOQL"])
        
  
        FeedItemData += self.sfac.SOQLgetQuery(FeedItemJob["SOQL"])

        ChatterData = FeedCommentData + FeedItemData;        
        #print(str(FeedItemSOQL))
        #print(str(FeedCommentSOQL))
        
        # CSV出力/Boxアップロード
        #self.UploadCsvFileCurrent("Chatter", ChatterData)
        # MongoDB登録
        self.mongoc.reCreateCollection("Chatter", ChatterData)
        ## MongoDBインデックス追加
        #[ self.mongoc.addIndex("Chatter",Index) for Index in FeedCommentJob["MongoDBIndex"] ]
        #[ self.mongoc.addIndex("Chatter",Index) for Index in FeedItemJob["FeedComment"] ]
        #for task in taskList:
        #    datas = self.sfac.SOQLgetQuery(task["SOQL"])
        """
        
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
        self.UploadCsvFile("Cahtter", boxFolderID, ChatterData)
        
        
    #def upsertLoginHistory(self)