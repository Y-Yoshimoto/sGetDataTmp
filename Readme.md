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

### 期間指定
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/data/period/join  -d @./flask_sfadata_replicaapi/code/datajoinTest.json

### パイプライン指定検索
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/data/pipeline/LoginHistory  -d @./flask_sfadata_replicaapi/code/pipelineQuery.json

### パイプライン指定検索-単一オブジェクト
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/data/pipeline/User  -d @./flask_sfadata_replicaapi/code/pipelineQuerySingle.json
### パイプライン指定検索-グループ
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/data/pipeline/LoginHistory  -d @./flask_sfadata_replicaapi/code/pipelineQueryGroup.json