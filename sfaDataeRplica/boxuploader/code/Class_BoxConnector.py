#!/usr/bin/env python
# coding:utf-8
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException
import os

# Boxコネクター
class Connector: 
    def __init__(self, auth, user_id, currentFolder_id):
        #auth = JWTAuth.from_settings_file('./.config.json')
        # 認証
        root_client = Client(auth)
        # ユーザ指定
        user_to_impersonate = root_client.user(user_id=user_id)
        self.user_client = root_client.as_user(user_to_impersonate)
        # カレントディレクトリー指定
        self.currentFolder_id = currentFolder_id
        folderUpload = self.user_client.folder(folder_id=currentFolder_id).get()
        print("FolderName: {0}".format(folderUpload.name), flush=True)
        print("Items: {0}".format(folderUpload.item_collection['total_count']), flush=True)
        
    # Type: dictionary
    # 指定フォルダーの情報を表示
    def getFolder(self, folder_id):
        folder = self.user_client.folder(folder_id=folder_id).get()
        folderInfo = {'folderName':folder.name,'items':folder.item_collection['total_count']}
        #print(str(folderInfo), flush=True)
        return folderInfo

    # Type: list
    # 指定フォルダー内のファイルをリストを取得
    def getFolderItems(self, folder_id):
        items = self.user_client.folder(folder_id=folder_id).get_items()
        itemlist = [{'id':item.id ,'type':item.type,'name':item.name} for item in items]
        return itemlist

    # Type: list
    # 指定IDのファイルをダウンロード
    def getFile(self, file_id):
        try:   
            file_content = self.user_client.file(file_id).content()
            return {'status':200, 'file': file_content} 
        except BoxAPIException as ex:
            return {'status':ex.status}


    # Type: dictionary
    # ファイルを指定のフォルダー内にアップロード 同一名の場合は新バージョンとしてアップデート
    def uploadFile(self, folder_id, filepath):
        try:
            new_file = self.user_client.folder(folder_id).upload(filepath)
            #print(vars(new_file), flush=True)
            return {'Type':'upload', 'id':new_file.id,'id':new_file.name, 'status': 200, 'API': 'Box Upload'}
     # ファイルを新バージョンとしてアップロード
        except BoxAPIException as ex:
            if ex.status == 409:
                print(ex.context_info['conflicts']['id'], flush=True)
                updated_file = self.user_client.file(ex.context_info['conflicts']['id']).update_contents(filepath, etag=ex.context_info['conflicts']['etag'])
                return {'Type':'update', 'id': ex.context_info['conflicts']['id'], 'name': ex.context_info['conflicts']['name'], 'status': 200, 'API': 'Box Upload'}
            else:
                return {'status':ex.status}
