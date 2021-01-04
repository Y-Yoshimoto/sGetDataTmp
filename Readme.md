# SalesforceGetData

## API
### カラム情報取得
curl -L http://127.0.0.1:5000/Columns/Account
### 全データ取得
curl -L http://127.0.0.1:5000/data/all/Opportunity

curl -L http://127.0.0.1:5000/data/all/LoginHistory

### 期間指定検索
curl -L 'http://127.0.0.1:5000/data/period/Opportunity?dateColumn=CreatedDate&startDate=2020-05-27&endDate=2020-05-29'


### 結合データ取得
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/data/join  -d @./flask_sfadata_replicaapi/code/datajoinTest.json