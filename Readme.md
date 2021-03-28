# SalesforceGetData
##  初期設定
### Salesforce
    アプリケーションを作成し、JWT認証の設定,権限設定などを行う
    ./sfadata_replica/config/
        - hoge.crt
        - hoge.csr
        - hoge.pem
        公開鍵/秘密鍵関連のファイルを設置

### Box
    アプリケーションを作成し、JWT認証の設定,権限設定などを行う
    ./boxuploader/code/.config.json
    秘密鍵関連のファイルを設置

    ファイルアップデート先以下を作成し、環境変数ファイルでID指定
        - カレントフォルダ
        - 全データのアップロードフォルダ
        - パイプライン処理データのアップロードフォルダ

### 環境変数
    cp .env.prot .env
    環境変数ファイルをコピーし、それぞれの指定

## API
### カラム情報取得
curl --noproxy "*" -L http://127.0.0.1:35000/Columns/Account
### 全データ取得
curl --noproxy "*" -L http://127.0.0.1:35000/data/all/Opportunity

curl --noproxy "*" -L http://127.0.0.1:35000/data/all/LoginHistory

### 期間指定検索
curl --noproxy "*" -L 'http://127.0.0.1:35000/data/period/Opportunity?dateColumn=CreatedDate&startDate=2020-05-27&endDate=2020-05-29'


### パイプライン指定検索
curl --noproxy "*" -L http://127.0.0.1:35000/data/pipeline/sample

### 結合データ取得
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:35000/data/join  -d @./flask_sfadata_replicaapi/code/datajoinTest.json

### 期間指定
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:35000/data/period/join  -d @./flask_sfadata_replicaapi/code/datajoinTest.json

### パイプライン指定検索
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:35000/data/pipeline/post/LoginHistory  -d @./flask_sfadata_replicaapi/code/pipelineQuery.json

### パイプライン指定検索-単一オブジェクト
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:35000/data/pipeline/post/User  -d @./flask_sfadata_replicaapi/code/pipelineQuerySingle.json
### パイプライン指定検索-グループ
curl --noproxy "*" -sS -L -X POST -H "Content-Type: application/json" http://127.0.0.1:35000/data/pipeline/post/LoginHistory  -d @./flask_sfadata_replicaapi/code/pipelineQueryGroup.json