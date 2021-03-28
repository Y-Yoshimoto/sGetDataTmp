#!/usr/bin/env python
# coding:utf-8
# Flaskのインポート，Blueprintのインポート
from flask import Blueprint, request, jsonify
from boxsdk import Client, JWTAuth
import json
import os
import Class_BoxConnector

#Blueprintでモジュールの登録
app = Blueprint('upload', __name__)

# Init Client ########################################################################
AUTH = JWTAuth.from_settings_file('./.config.json')
USER_ID=os.environ['BOX_USER_ID']
CURRENTFOLDER_ID = os.environ['BOX_UPLOADFOLDER_ID']
BoxC = Class_BoxConnector.Connector(AUTH, USER_ID, CURRENTFOLDER_ID)

## Salesforce Update Environ
PIPELINEDATA_ID = os.environ['BOX_PIPELINEDATA_ID']
QUERYALLDATA_ID = os.environ['BOX_QUERYALLDATA_ID']

## GET upload folder ########################################################################
@app.route('/folder/', methods=['GET'])
def folder():
    folderInfo = BoxC.getFolder(CURRENTFOLDER_ID)
    return jsonify(folderInfo)

## GET upload folder Items ########################################################################
@app.route('/folder/Items', methods=['GET'])
def items():
    itemlist = BoxC.getFolderItems(CURRENTFOLDER_ID)
    return jsonify(itemlist)

## GET Items Download use Id ########################################################################
@app.route('/download/id/<file_id>', methods=['GET'])
def download_fileID(file_id):
    fileInfo = BoxC.getFile(file_id)
    if fileInfo['status'] == 200:
       return fileInfo['file'], 200
    return jsonify(fileInfo), fileInfo['status']

## POST upload shardvol data ########################################################################
@app.route('/upload/sharedvolume/<filename>', methods=['POST'])
def sharedvolume(filename):
    folder_id=CURRENTFOLDER_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

## POST upload PIPELINEDATA ########################################################################
@app.route('/upload/pipelinedata/<filename>', methods=['POST'])
def pipelinedata(filename):
    folder_id=PIPELINEDATA_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']

## POST upload QUERYALLDATA ########################################################################
@app.route('/upload/queryalldata/<filename>', methods=['POST'])
def queryalldata(filename):
    folder_id=QUERYALLDATA_ID
    filepath='../uploadvolume/' + filename
    status = BoxC.uploadFile(folder_id, filepath)
    return jsonify(status), status['status']