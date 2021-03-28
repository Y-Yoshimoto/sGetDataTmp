#!/usr/bin/env python
# coding:utf-8
from flask import Flask, request, jsonify
app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False

@app.route('/healthCheck')
def hello_world():
    return '200 OK'

## データアップロード ################################
import upload as upload
app.register_blueprint(upload.app)

