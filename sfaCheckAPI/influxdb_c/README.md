# Influxdb 

# CLI
https://docs.influxdata.com/influxdb/v2.0/reference/cli/

## ユーザ一覧
    influx user list
## バケット一覧
    influx bucket list

## トークン表示
    influx auth list | awk '{print $4}'

## サンプルデータ登録(秒単位で保存)
    date +%s
    time=$(date +%s)
    ## influx write -p s --bucket SfaTimebaseMetrics "DailyApiRequests Max=100,Using=20,Remaining=80,UsageRate=20.0 $time"

## サンプルデータの表示(24時間以内のデータ表示)
    influx query 'from(bucket: "SfaTimebaseMetrics") |> range(start: -24h)'

## サンプルデータの表示(フィールドUsingの24時間以内のデータ表示)
    influx query 'from(bucket: "SfaTimebaseMetrics") 
            |> range(start: -24h)
            |> filter(fn:(r) =>
                r._measurement == "LimitProcessing" and
                r.key == "DailyApiRequests" and
                r._field == "Using")'

    influx query 'from(bucket: "SfaTimebaseMetrics") 
            |> range(start: -24h)
            |> filter(fn:(r) =>
                r._measurement == "LimitProcessing" and
                r.key == "DailyApiRequests")'


## Pythonライブラリー
https://docs.influxdata.com/influxdb/cloud/tools/client-libraries/python/
https://www.influxdata.com/blog/getting-started-with-python-and-influxdb-v2-0/