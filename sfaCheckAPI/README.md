# Pythonコンテナ

## 参考URL
 -[Gocker Hub](https://hub.docker.com/_/python)
 
## デプロイ


## APIテスト
### 最新値
curl http://127.0.0.1:8280/limitinfo/latestvalue/DailyApiRequests

### 履歴値
curl 'http://127.0.0.1:8280/limitinfo/historyvalue/DailyApiRequests?field=UsageRate'
curl 'http://127.0.0.1:8280/limitinfo/historyvalue/DailyApiRequests?field=Using'


## グラフ用
curl 'http://127.0.0.1:8280/limitinfo/latestvalue/PieChartdata/DailyApiRequests'
curl 'http://127.0.0.1:8280/limitinfo/historyvalue/AreaChartdata/DailyApiRequests?field=UsageRate'


curl -X POST http://127.0.0.1:8040/DailyApiRequests

## ダッシュボード
    http://127.0.0.1:3000/


## グラフライブラリー
    - Nino: https://nivo.rocks/
    - recharts: 
