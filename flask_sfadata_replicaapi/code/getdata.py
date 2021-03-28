#!/usr/bin/env python
# coding:utf-8
# Flaskのインポート，Blueprintのインポート
from flask import Blueprint, request, jsonify
import json

## MongoConnector 
import MongoConnector

#Blueprintでモジュールの登録
app = Blueprint('getdata', __name__)
# app.config["JSON_AS_ASCII"] = False

# MongoDB
class SObjectGetsObjects:
    """sObject bulk registration"""
    def __init__(self):
        self.MongoC = MongoConnector.Connector("sObjectData")
        print("Init SObjectGetsObjects", flush=True)
    
    def responseResult(self, data):
        response = jsonify(data)
        response.status_code = 200
        return response 


#　Blueprint　#######################################################################################
sObjectBR = SObjectGetsObjects()

## カラム取得
@app.route('/Columns/<sObject>', methods=['GET'])
def Columns_get(sObject):
    datas=sObjectBR.MongoC.searchSingleFilter("sObjectColumns", "sObject", sObject)
    return sObjectBR.responseResult(datas)

############### 単一データ取得 ###############
# 全データ検索
@app.route('/data/all/<sObject>', methods=['GET'])
def all_get(sObject):
    datas=sObjectBR.MongoC.getAlldata(sObject)
    return sObjectBR.responseResult(datas)

# 期間指定検索
@app.route('/data/period/<sObject>', methods=['GET'])
def period_get(sObject):
    ## パラメータ取得
    dateColumn = str(request.args.get('dateColumn'))
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    ## DB検索
    datas=sObjectBR.MongoC.searchDatePeriodFilter(sObject, dateColumn, startDate, endDate)
    ## レスポンス
    return sObjectBR.responseResult(datas)

############### 複合データ取得 ###############
@app.route('/data/join', methods=['POST'])
def join_get():
    body = json.loads(request.get_data().decode().strip())
    ## DB検索
    datas=sObjectBR.MongoC.joinsearchData(body["mainCollection"],body["subCollection"])
    ## レスポンス
    return sObjectBR.responseResult(datas)

@app.route('/data/period/join', methods=['POST'])
def joinPeriod_get():
    body = json.loads(request.get_data().decode().strip())

    ## DB検索
    datas=sObjectBR.MongoC.joinsearchDataPeriod(body["mainCollection"],body["subCollection"],body["datePeriod"])
    ## レスポンス
    return sObjectBR.responseResult(datas)

############### パイプライン指定 ###############
@app.route('/data/pipeline/<pipelineName>', methods=['GET'])
def pipelineLoad(pipelineName):
    ## パイプラインファイル読み込み
    pipelinePathName = './piplineQuery/' + pipelineName + '.json'
    pipelineInfo = json.load(open(pipelinePathName, 'r'))
    ## 主オブジェクトとクエリーの読み込み
    sObject=pipelineInfo['mainsObject']
    pipeline=pipelineInfo['pipeline']
    ## パイプライン表示
    print(str(pipeline), flush=True)
    ## データ取得
    datas=sObjectBR.MongoC.pipelineQuery(sObject, pipeline)
    ## レスポンス
    return sObjectBR.responseResult(datas)

############### パイプラインPOST ###############
@app.route('/data/pipeline/post/<sObject>', methods=['POST'])
def pipeline_post(sObject):
    pipeline = json.loads(request.get_data().decode().strip())
    # pipeline
    print(str(pipeline), flush=True)
    datas=sObjectBR.MongoC.pipelineQuery(sObject, pipeline)
    ## レスポンス
    return sObjectBR.responseResult(datas)