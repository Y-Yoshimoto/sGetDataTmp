#!/usr/bin/env python
# coding:utf-8
# Flaskのインポート，Blueprintのインポート
from flask import Blueprint, request, jsonify
import json

#Blueprintでモジュールの登録
app = Blueprint('registration', __name__)

## MongoConnector 
import MongoConnector

## 
class SObjectBulkRegistration:
    """sObject bulk registration"""
    def __init__(self):
        self.MongoC = MongoConnector.Connector("sObjectData")
        print("Init SObjectBulkRegistration", flush=True)

### POST Method ###################################################################################
    def post(self, jqbody, sObject):
    #def post(self, sObject):
        print(sObject, flush=True)
        #print(jqbody[0], flush=True)
        self.MongoC.dropCollection(sObject)
        self.MongoC.checkCollection(sObject, "Id")
        NumberOfRecords = self.MongoC.insertBulkdata(sObject, jqbody)

        #print(jqbody[0], flush=True)
        return (jsonify({'status':200, 'sObject': sObject, 'Records': NumberOfRecords, 'API': 'MongoDB Registration'}), 200)


#　Blueprint　#######################################################################################
sObjectBR = SObjectBulkRegistration()
@app.route('/registration/<sObject>', methods=['POST'])
def registration_post(sObject):
    body = request.get_data().decode().strip()
    #print(body, flush=True)
    #json.loads(body)
    return sObjectBR.post(json.loads(body),sObject)
    #return sObjectBR.post(sObject)

