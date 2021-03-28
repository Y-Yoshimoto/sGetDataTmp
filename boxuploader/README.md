# Boxアップローダ
 BoxにファイルをアップロードするWebアプリケーション
 アップロードするフォルダーは固定
 - Bodyで受け取ったファイルをアップロードするAPI
 - 共有ボリュームの指定ファイルをアップロードするAPI

# 共有ボリュームアップロードAPI
curl -X POST http://boxuploader:5000/upload/sharedvolume/testfile

##  ヘルスチェック
curl http://boxuploader:5000/healthCheck

## アップロード先フォルダチェック
curl http://boxuploader:5000/folder

## 参考URL
 -[Gocker Hub](https://github.com/box/box-python-sdk)
