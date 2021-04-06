#!/usr/bin/env python
# coding:utf-8
import pymongo
from pymongo import ASCENDING, DESCENDING

# MongoDB コネクタ
class Connector:
    def __init__(self, dbName):
        # DB認証情報
        user = 'sObjectDataAdmin'
        pwd = 'Password01'
        self.client = pymongo.MongoClient('mongodb://mongo:27017/')
        # DB接続
        self.db = self.client[dbName]
        self.db.authenticate(user, pwd)
        assert self.client is not None

        #self.db.collection_names()
        #print(str(self.db.name), flush=True)

    def __del__(self):
        print("__del__", flush=True)
        #self.client.close()

    # コレクションの確認, インデックス追加
    def checkCollection(self, collectionName, indexColumn):
        self.collection = self.db[collectionName]
        assert self.collection is not None
        ## インデックス追加
        self.collection.create_index([(indexColumn, ASCENDING)])
        print("Check Collection: " + collectionName, flush=True)
        print(str(self.collection.name) + ' recodes : ' + str(self.collection.find().count()), flush=True)

    # コレクション削除
    def dropCollection(self, collectionName):
        self.collection = self.db[collectionName]
        assert self.collection is not None
        print("Drop Collection: " + collectionName, flush=True)
        self.collection.drop()

    # バルクデータ登録
    def insertBulkdata(self, collectionName, data):
        if len(data) == 0:
            print("Noinsart Collection: " + collectionName, flush=True)
            return 
        self.collection = self.db[collectionName]
        assert self.collection is not None
        print("Insart Collection: " + collectionName, flush=True)
        print(str(len(data)), flush=True)
        ## データ追加
        self.collection.insert_many(data)
        #assert self.collection.count_documents({}) == len(data)

        print(str(self.collection.name) + ' recodes : ' + str(self.collection.find().count()), flush=True)
        return len(data)

    ### 検索表示
    # 全データ表示
    def getAlldata(self, collectionName):
        self.collection = self.db[collectionName]
        assert self.collection is not None
        print("Get Collection: " + collectionName, flush=True)
        datas = [data for data in self.collection.find({}, {'_id': False})]
        return datas

    # 1条件検索
    def searchSingleFilter(self, collectionName, Columns, value):
        self.collection = self.db[collectionName]
        assert self.collection is not None
        print("Search Collection: " + Columns + "= " + value, flush=True)
        datas = [data for data in self.collection.find({Columns: value}, {'_id': False})]
        return datas

    # 期間指定検索
    def searchDatePeriodFilter(self, collectionName, dateColumn, startDate, endDate):
        self.collection = self.db[collectionName]
        assert self.collection is not None
        print("Search Collection: " + startDate + " - " + endDate, flush=True)
        dateFilter= {dateColumn :{"$gte": str(startDate), "$lte": str(endDate)}}
        datas = [data for data in self.collection.find(dateFilter, {'_id': False}, sort = [(dateColumn, ASCENDING)])]
        return datas

    ####  複合検索-カラム作成 ############ 
    def makeColumnsProject(self, mainColumns, subColumns, subCollectionName):
        columns = {}
        # メインコレクションカラム
        for column in mainColumns:
            #print(str(column), flush=True)
            columns[column] = "$" + column
        # サブコレクションカラム
        for column in subColumns:
            #print(str(column), flush=True)
            columns[column] = "$" + subCollectionName + "." + column
        # オブジェクトId無効
        columns["_id"] = False
        project={"$project": columns}
        return project

    ####  複合検索-結合ルール作成 ############ 
    def makeJoinLookup(self, mainCollection, subCollection):
        lookup={"$lookup":
        {
            "from":subCollection["collection"],
            "localField": mainCollection["joinField"],
            "foreignField":subCollection["joinField"],
            "as":subCollection["collection"]
        }}
        return lookup

    ####  複合検索 
    def joinsearchData(self, mainCollection, subCollection):
        self.collection = self.db[mainCollection["collection"]]
        assert self.collection is not None
        ## 結合ルール
        lookup = self.makeJoinLookup(mainCollection, subCollection)
        ## subコレクションデータの配列解除
        unwind={"$unwind": "$"+subCollection["collection"]}
        ## 必要なカラムの取り出し
        project=self.makeColumnsProject(mainCollection["columns"], subCollection["columns"], subCollection["collection"])

        print("lookup Info: " + str(lookup), flush=True)
        print("project Info: " + str(project), flush=True)
        datas = [data for data in self.collection.aggregate([lookup, unwind, project])]
        return datas

    ####  複合検索-期間指定
    def joinsearchDataPeriod(self, mainCollection, subCollection,datePeriod):
        self.collection = self.db[mainCollection["collection"]]
        assert self.collection is not None
        ## 結合ルール
        lookup = self.makeJoinLookup(mainCollection, subCollection)
        ## subコレクションデータの配列解除
        unwind={"$unwind": "$"+subCollection["collection"]}
        ## 必要なカラムの取り出し
        project=self.makeColumnsProject(mainCollection["columns"], subCollection["columns"], subCollection["collection"])

        print("lookup Info: " + str(lookup), flush=True)
        print("project Info: " + str(project), flush=True)

        #dateFilter= {dateColumn :{"$gte": str(startDate), "$lte": str(EndDate)}}
        dateFilter= {"$match": {datePeriod["dateColumn"] :{"$gte": datePeriod["startDate"], "$lte": datePeriod["endDate"]}}}
        print("dateFilter Info: " + str(dateFilter), flush=True)

        datas = [data for data in self.collection.aggregate([lookup, dateFilter, unwind, project])]
        print("dateFilter Info: " + str([lookup, dateFilter, unwind, project]), flush=True)
        return datas

    def pipelineQuery(self, CollectionName, pipeline):
        self.collection = self.db[CollectionName]
        assert self.collection is not None
        datas = [data for data in self.collection.aggregate(pipeline)]
        return datas