import os
import datetime
import requests
import time

import redis
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

#class SfaLimitProcessing:
#    def __init__(self, limit):

# 登録データの整形
def SfaLimitProcessing(limitData):
    LimiteDataList = []
    for key in limitData:
        Item=key                                    # 項目名
        Max=int(limitData[key]['Max'])              # 最大値
        Remaining=int(limitData[key]['Remaining'])  # 残量 
        UsageRate=percentage(Max,Remaining)         # 使用率(%)
        LimiteDataList.append({"Item": Item, "Max": Max, "Using": Max-Remaining, "Remaining": Remaining,"UsageRate": UsageRate})
    return LimiteDataList

# パーセント計算
def percentage(Max, Remaining):
    if int(Max)==0:
        return 0
    else:
        percent = 100.0 * ( Max - Remaining)/Max
        return percent

# API経由での最新値Redis登録
def RegistrationLatestValue(Data):
    for Item in Data:
        key=Item['Item']
        result = requests.post(
        'http://latestvalue_api:8040/' + key,
        data=Item,
        headers={'Access_key': os.environ['ACCESS_KEY']}
        )
        body = result.json()
        if result.status_code != 200:
            raise print(body['error'], body['error_description'])

# Redisへ直接登録
def RegistrationLatestValue_REDIS(Data):
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ", Registration Limits to Redis")

    # クライアント接続
    redisC = redis.Redis(host='redis_c', port=6379, db=0)
    # 値の登録
    for Item in Data:
        key=Item['Item']
        redisC.set(key + "_Max", Item['Max'])
        redisC.set(key + "_Using", Item['Using'])
        redisC.set(key + "_UsageRate", Item['UsageRate'])
        redisC.set(key + "_Remaining", Item['Remaining'])


# influxdbへ登録
def RegistrationLatestValue_Influxdb(Data):
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ", Registration Limits to Influxdb")
    # クライアント接続
    client = influxdb_client.InfluxDBClient(url="http://influxdb_c:8086", token="wJmvpkBMrn0OTtcWtxQJylBPqIo7H931GJ5xl917aJ9mBJxW4PmWC6LUk-twLorSbfjLZomMukXiIuBFtEdCgw==", org="SfaTimebaseMetrics")
    #print(vars(client))
    #write_api = client.write_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    ## Bucket, Org, item
    nanoTime = time.time_ns()
    
    for Item in Data:
        key=Item['Item']
        Lineprotocol = key + " Using=" + str(Item['Using']) #+ " " + nanoTime
        # 使用量/使用率登録
        p = influxdb_client.Point("LimitProcessing")
        # タグ指定
        p = p.tag("key", key)
        # フィールド指定
        p = p.field("UsageRate", float(Item['UsageRate'])).field("Using", int(Item['Using']))
        p = p.time(nanoTime)
        # print(vars(p))
        write_api.write(bucket="SfaTimebaseMetrics", org="SfaTimebaseMetrics", record=p)