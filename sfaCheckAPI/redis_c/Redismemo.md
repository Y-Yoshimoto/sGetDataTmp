# Redis

## 設定ファイル
    "redisOverwrite.conf"に追加の設定を記載する

## Mac用クライアントのインストール
Homebrewをインストールし、以下のコマンドでインストールする。
    ``brew install redis``
### 起動停止
 - 起動
    brew services start redis
 - 停止
    brew services stop redis
 - 状態確認
    brew services list

## 接続
``redis-cli``コマンドで接続ローカルホストのサーバに接続する。ホスト名及びポート番号を指定する場合は、``redis-cli -h localhost -p 6379``とオプションを追加する。

### 基本操作
- "key: test, value: hoge"の値を登録する。``> set test hoge``
- keyがtestのvalueを取得する。``> get test``
- keyを全て表示する。``> keys *``
- keyがtestのレコードを削除する。``> del test``


### 管理
  - リアルタイムにクエリ情報を監視 ``> monitor``
  - DBを削除する ``> flushdb``
  - DBを保存する　``> bgsave`` (/data/dump.rdb)

## コンテナ関連
 - 設定ファイルコピー先 /usr/local/etc/redis.conf
 - バックアップデータ: /data/dump.rdb
