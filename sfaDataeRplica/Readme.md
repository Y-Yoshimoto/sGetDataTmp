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
