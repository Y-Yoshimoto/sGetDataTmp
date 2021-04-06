#!/usr/bin/env python
# coding:utf-8
# Flaskのインポート，Blueprintのインポート
from flask import Blueprint, request, jsonify
from boxsdk import Client, JWTAuth
import json
import os
import Class_BoxConnector
## CSV変換用
import pandas as pd


#Blueprintでモジュールの登録
app = Blueprint('upload', __name__)

# Box接続クライアント設定
## Init Client ########################################################################
AUTH = JWTAuth.from_settings_file('./.config.json')
USER_ID=os.environ['BOX_USER_ID']
CURRENTFOLDER_ID = os.environ['BOX_UPLOADFOLDER_ID']
BoxC = Class_BoxConnector.Connector(AUTH, USER_ID, CURRENTFOLDER_ID)

# アップロードフォルダー設定
## Salesforce Update Environ
PIPELINEDATA_ID = os.environ['BOX_PIPELINEDATA_ID']
QUERYALLDATA_ID = os.environ['BOX_QUERYALLDATA_ID']

# フォルダー情報取得
## GET upload folder ########################################################################
@app.route('/folder/', methods=['GET'])
def folder():
    folderInfo = BoxC.getFolder(CURRENTFOLDER_ID)
    return jsonify(folderInfo)

# フォルダ配下のItem情報取得
## GET upload folder Items ########################################################################
@app.route('/folder/Items', methods=['GET'])
def items():
    itemlist = BoxC.getFolderItems(CURRENTFOLDER_ID)
    return jsonify(itemlist)

# ID指定ファイルダウンロード
## GET Items Download use Id ########################################################################
@app.route('/download/id/<file_id>', methods=['GET'])
def download_fileID(file_id):
    fileInfo = BoxC.getFile(file_id)
    if fileInfo['status'] == 200:
       return fileInfo['file'], 200
    return jsonify(fileInfo), fileInfo['status']

# 共有フォルダー配下のデータをアップロード
## POST upload shardvol data ########################################################################
@app.route('/upload/sharedvolume/<filename>', methods=['POST'])
def sharedvolume(filename):
    folder_id=CURRENTFOLDER_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

# パイプラインデータフォルダーにファイル設置
## POST upload PIPELINEDATA ########################################################################
@app.route('/upload/pipelinedata/<filename>', methods=['POST'])
def pipelinedata(filename):
    folder_id=PIPELINEDATA_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

# ROWデータフォルダーにファイル設置
## POST upload QUERYALLDATA ########################################################################
@app.route('/upload/queryalldata/<filename>', methods=['POST'])
def queryalldata(filename):
    folder_id=QUERYALLDATA_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']


## JSONデータをCSVに変換しアップロード
## POST upload ConvertCSV PIPELINEDATA ########################################################################
@app.route('/upload/pipelinedata/csv/<filename>', methods=['POST'])
def pipelinedataCSV(filename):
    folder_id=PIPELINEDATA_ID
    filepath = ConvertJsonToCsv(filename)
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

## POST upload ConvertCSV QUERYALLDATA ########################################################################
@app.route('/upload/queryalldata/csv/<filename>', methods=['POST'])
def queryalldataCSV(filename):
    folder_id=QUERYALLDATA_ID
    filepath = ConvertJsonToCsv(filename)
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

## JSONデータをCSVに変換
def ConvertJsonToCsv(jsonFileName):
    # フルパスファイル名の生成と、エクスポートファイル名の生成
    FileName = os.path.splitext(os.path.basename(jsonFileName))[0]
    jsonFilepath='../uploadvolume/' + jsonFileName
    csvFilepath='../uploadvolume/' + FileName + ".csv"
    ## Jsonファイルの読み込みとCSV変換
    pd.json_normalize(json.load(open(jsonFilepath, 'r'))).to_csv(csvFilepath, encoding='utf-8')
    return csvFilepath