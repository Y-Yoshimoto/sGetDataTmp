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

def do_task():
    # 画面に「タスク実行を表示」
    print('タスク実行')

def main():
    # Salesforce接続クライアント インスタンス生成/認証
    #### Authorization ####
    connection = SfaRestClient.SfaConnection()

    # 制限値取得
    Job.UpdateLimitData(connection)

    # Job登録
    ## アクセストークン更新
    # schedule.every(10).minutes.do(lambda: connection.update_token())
    ## 制限値取得
    schedule.every(12).minutes.do(lambda: Job.UpdateLimitData(connection))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
