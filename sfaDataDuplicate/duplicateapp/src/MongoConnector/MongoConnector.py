#!/usr/bin/env python
# coding:utf-8
import pymongo
from pymongo import ASCENDING, DESCENDING
from pymongo import UpdateOne,InsertOne

import os
#ドキュメント
## https://pymongo.readthedocs.io/en/stable/api/pymongo/index.html
## https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html

from logging import getLogger
logger = getLogger(__name__)

# MongoDB コネクタ
class Connector:
    """MongoDBコネクター"""
    def __init__ (self, 
                    databaseName:str = os.environ['MONGO_DATABASE'],
                    endpoint:str = os.environ['MONGO_ROOTURL'],
                    user:str = os.environ['MONGO_EDITORTHEME'], 
                    password:str = os.environ['MONGO_EDITORPASS']):
        ## DBへの接続と認証
        ### 接続先MongoDBの指定
        self._client = pymongo.MongoClient(endpoint)
        ### 接続先データベースの指定
        self._db = self._client[databaseName]
        ### 認証
        self._db.authenticate(user, password)
        assert self._client is not None
        #logger.info(str(self._db.name))
        #print("Success Connect MongoDB: " + str(self._db.name), flush=True)

    #def __del__(self):
    #    print("__del__", flush=True)
    #    self._client.close()

    ### コレクション操作 ###########################################
    def listupCollection(self) -> list:
        """コレクション一覧"""
        return [x for x in self._db.collection_names()]

    def checkCollection(self, collection＿name: str) -> bool:
        """コレクションの存在チェック"""
        return collection＿name in self._db.collection_names()
        
    def dropCollection(self, collectionName: str):
        """コレクションの削除"""
        self._db[collectionName].drop()



    ### 登録 #####################################################
    def insertData(self, collectionName: str, data: dict) -> int:
        """1件登録 登録したデータ数を返す"""
        ## 型チェック
        if not type(data) is dict:
            #print("Not dict data.", flush=True)
            raise TypeError("Not dict data.")
            return 0
        #print("Insart Collection[" + collectionName + "]: 1", flush=True)
        self._db[collectionName].insert_one(data)
        return 1
        
    def insertManydata(self, collectionName: str, datas: list) -> int:
        """大量登録 登録したデータ数を返す"""
        ## データチェック
        if len(datas) == 0:
            print("Noinsart Collection: " + collectionName, flush=True)
            return 0
        elif not type(datas) is list:
            #print("Not list data.", flush=True)
            raise TypeError("Not list data.")
            return 0
        #print("Insart Collection[" + collectionName + "]: " + str(len(datas)), flush=True)
        self._db[collectionName].insert_many(datas)
        return len(datas)
        
    def addIndex(self, collectionName: str, indexColumn: str):
        """ インデックス追加 """
        self._db[collectionName].create_index([(indexColumn, ASCENDING)])
        return 0
    
    def reCreateCollection(self, collectionName: str, datas: list) -> int:
        """新規データでコレクションを再作成"""
        self.dropCollection(collectionName)
        self.insertManydata(collectionName, datas)
        #print("Recreate Collection[" + collectionName + "]: " + str(len(datas)), flush=True)



    ### 参照: 全件 #################################################
    def getAllData(self, collectionName: str) -> list:
        """コレクション内の全てのドキュメントを取得"""
        datas = [data for data in self._db[collectionName].find({}, {'_id': False})]
        return datas

    def getAllData_AndID(self, collectionName: str) -> list:
        """コレクション内の全てのドキュメントを取得 MongoDBID付き"""
        datas = [data for data in self._db[collectionName].find({})]
        return datas

    def getCount(self, collectionName) -> int:
        """コレクション内の全てのドキュメント数取得"""
        return self._db[collectionName].find({}).count()

    def getKeys(self, collectionName) -> list:
        """コレクション内で使用しているキーを取得"""
        ## 全データからキーリスト項目の取り出し
        datas = [list(data.keys()) for data in self._db[collectionName].find({}, {'_id': False})]
        ## キーリストのリスト構造から、2重リストの解消とユニークな値の取り出し
        keys = list(set([key for keys_list in datas for key in keys_list]))
        return keys



    ### 参照: 条件指定 ################################################# 
    ## filter={"column": "value"}
    def searchSingleFilter(self, collectionName: str, filter: dict) -> list:
        """1カラムを指定し値が一致するドキュメントを取得"""
        datas = [data for data in self._db[collectionName].find(filter, {'_id': False})]
        return datas

    def searchDatePeriodFilter(self, collectionName: str, dateColumn: str, startDate: str, endDate: str) -> list:
        """日時系のカラムを指定し、期間内のドキュメントを表示"""
        ## 正規表現で検索対象期間のフィルターを作成
        dateFilter= {dateColumn :{"$gte": str(startDate), "$lte": str(endDate)}}
        datas = [data for data in self._db[collectionName].find(dateFilter, {'_id': False}, sort = [(dateColumn, ASCENDING)])]
        return datas

    def searchMinimumValue(self, collectionName: str, column: str):
        """指定したカラム内の最小値を取得"""
        return self._searchLimitValue(collectionName, column, 1)

    def searchMaxValue(self, collectionName: str, column: str):
        """指定したカラム内の最大値を取得"""
        return self._searchLimitValue(collectionName, column, -1)

    def _searchLimitValue(self, collectionName: str, column: str, sort: int):
        """指定したカラム内の最大値/最小値を取得"""
        match = {"$match": {column:{"$exists": "true"}}}
        sort = {"$sort": {column: sort}} # 並び順の指定(1,昇順, -1:降順)
        limit = {"$limit": 1}         # 取得数の指定
        project = {"$project": { "_id": 0, column: 1 }} # 取得するカラムを指定
        #要所の一番目だけを取得
        #print([data for data in self._db[collectionName].aggregate([match, sort, limit, project])], flush=True)
        try:
            MaxMinimum = [data for data in self._db[collectionName].aggregate([match, sort, limit, project])][0]
        except IndexError:
            return None
        return MaxMinimum[column]


    ### 更新 ##############################################
    ## filter={"column": "value"}, update={"column": "value"}
    def updateValueMany(self, collectionName: str, filter: dict, update: dict) -> int:
        """指定した値を持つドキュメントの値を更新"""
        updateSet = {"$set":update}
        updateinfo = self._db[collectionName].update_many(filter,updateSet)
        return updateinfo.matched_count

    def replaceData(self, collectionName: str, filter: dict, data: dict) -> int:
        """指定した値を持つドキュメントを置き換え"""
        ## 型チェック
        if not type(data) is dict:
            #print("Not dict data.", flush=True)
            raise TypeError("Not dict data.")
            return 0
        replaceinfo = self._db[collectionName].replace_one(filter,data)
        return replaceinfo.matched_count
    
    def upsertData(self, collectionName: str, filter: dict, update: dict) -> int:
        """指定した値を持つドキュメントを更新or挿入"""
                ## 型チェック
        if not type(update) is dict:
            #print("Not dict data.", flush=True)
            raise TypeError("Not dict data.")
            return 0
        updateSet = {"$set":update}
        upsertinfo = self._db[collectionName].update_many(filter,updateSet, upsert=True)
        return upsertinfo.matched_count if upsertinfo.matched_count > 0 else 1

    ### 削除 ##############################################
    def deleteDataMany(self, collectionName: str, filter: dict) -> int:
        """指定した値を持つドキュメントをすべて削除"""
        deleteinfo = self._db[collectionName].delete_many(filter)
        return deleteinfo.deleted_count

    def deleteDataAndGet(self, collectionName: str, filter: dict):
        """指定した値を持つドキュメントを1つ削除し取得"""
        deleteinfo = self._db[collectionName].find_one_and_delete(filter, {'_id': False})
        return deleteinfo

    def deleteData(self, collectionName: str, filter: dict):
        """指定した値を持つドキュメントを1つ削除"""
        deleteinfo= self.deleteDataAndGet(self, collectionName, filter)
        return 

    ### バルク処理 ##########################################
    def insertBulkdata(self, collectionName: str, datas: list) -> int:
        """バルク登録 登録したデータ数を返す"""
        ## データチェック
        if len(datas) == 0:
            print("Noinsart Collection: " + collectionName, flush=True)
            return 0
        elif not type(datas) is list:
            #print("Not list data.", flush=True)
            raise TypeError("Not list data.")
            return 0
        InsertList = [ InsertOne(i) for i in datas]
        try:    
            result = self._db[collectionName].bulk_write(InsertList)
            #print(result.bulk_api_result)
        except pymongo.errors.BulkWriteError as bwe:
            print(bwe.details)
        return len(datas)
    
    ### パイプラインクエリー実行 ##########################################
    ### 参考: https://docs.mongodb.com/master/aggregation/#aggregation-pipeline
    ### 参考: https://docs.mongodb.com/manual/core/aggregation-pipeline/ 
    def pipelineQuery(self, pipelineInfo: dict):
        """受け取ったパイプラインクエリーの実行"""
        assert self._db[pipelineInfo["mainCollection"]] is not None
        datas = [data for data in self._db[pipelineInfo["mainCollection"]].aggregate(pipelineInfo["pipeline"])]
        return datas
    