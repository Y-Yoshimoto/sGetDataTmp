import json
import datetime
import schedule
import time

# SalesforceAPIコネクター
import SfaRestClient
# 制限値整形
import SfaLimitProcessing
# Job取得
import Job

def main():
    # Salesforce接続クライアント インスタンス生成/認証
    print("--- Authorization ---")
    connection = SfaRestClient.SfaConnection()

    # 組織制限値取得
    print("--- Data Limits ---")
    limitData=connection.GetLimitsInfo()

    ## ローカルファイルモック
    #limitData=json.load(open('./limit.json', 'r'))
    #print(str(limitData))

    # 取得値の整形
    limitInfo = SfaLimitProcessing.SfaLimitProcessing(limitData)
    #print(limitInfo)
    #print(datetime.datetime.now().timestamp())

    # 最新値のRedisデータベース登録_NodeJS経由
    #SfaLimitProcessing.RegistrationLatestValue(limitInfo)
    # 最新値のRedisデータベース登録
    SfaLimitProcessing.RegistrationLatestValue_REDIS(limitInfo)

    # 最新値のInfluxdbデータベース登録
    SfaLimitProcessing.RegistrationLatestValue_Influxdb(limitInfo)

    ## ログイン履歴
    Job.GetLoginHistoryData(connection)


    """
    #ページ別メトリクス取得
    #print("--- Lightning Usage By Page Metrics ---")
    pageMetrics=connection.GetLightningUsageByPageMetrics()
    print(json.dumps(pageMetrics["recentItems"], indent=4))
    file_path = "./PageMetrics.json"
    with open(file_path, 'w') as outfile:
        json.dump(pageMetrics, outfile)

    # アプリケーション別メトリクス取得
    #print("--- Lightning Usage By AppType Metrics ---")
    appTypeMetrics=connection.GetLightningUsageByAppTypeMetrics()
    print(json.dumps(appTypeMetrics["recentItems"], indent=4))
    file_path = "./AppTypeMetrics.json"
    with open(file_path, 'w') as outfile:
        json.dump(appTypeMetrics, outfile)
    """

if __name__ == '__main__':
    main()
