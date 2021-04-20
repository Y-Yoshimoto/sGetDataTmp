# SalesforceDX

## DokcerHub
    - [salesforcedx](https://hub.docker.com/r/salesforce/salesforcedx)

## 実行時動作
    コンテナ起動後、認証を行う。
    15分間隔で、API使用状況を取得

## 認証設定
JWTで認証を行う[参考](https://developer.salesforce.com/docs/atlas.ja-jp.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth_jwt_flow.htm)
Salesforceのアプリケーション設定で接続アプリケーションを作成

　JWT電子署名用の秘密鍵及び証明書を作成する。
```bash
openssl genrsa 2048 > sfadxinfo.pem
openssl req -new -key sfadxinfo.pem -out sfadxinfo.csr
openssl x509 -req -days 1826 -in sfadxinfo.csr -signkey sfadxinfo.pem -out sfadxinfo.crt 
```
証明書(sfadxinfo.crt)ファイルをSalesforceのAPI(OAtuth設定有効化)からデジタル証明書をアップロードする。