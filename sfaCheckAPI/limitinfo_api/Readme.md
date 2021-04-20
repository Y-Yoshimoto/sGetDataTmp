# Express

Expressアプリケーションサンプルセット

## 動作確認コマンド
コンテナのログを確認しながら以下のコマンドを実行する
```bash
curl -X GET 'http://127.0.0.1:8040/api?id=3'
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8040/api -d '{"id":123}'
curl -X PUT -H "Content-Type: application/json" http://127.0.0.1:8040/api -d '{"id":123}'
curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:8040/api -d '{"id":123}'
 ```