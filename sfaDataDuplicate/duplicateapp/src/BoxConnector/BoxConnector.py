#!/usr/bin/env python
# coding:utf-8
from boxsdk import Client, JWTAuth
from boxsdk.exception import BoxAPIException
import os

# 409警告抑止
import warnings

# Boxコネクター
class Connector: 
    def __init__(self, authfile:str = os.environ['BOX_AUTH'],
                    user_id:str = os.environ['BOX_USER_ID'], 
                    currentFolder_id:str = os.environ['BOX_UPLOADFOLDER_ID']):
        auth = JWTAuth.from_settings_file(authfile)

        # 認証
        root_client = Client(auth)
        # ユーザ指定
        user_to_impersonate = root_client.user(user_id=user_id)
        self.user_client = root_client.as_user(user_to_impersonate)
        # カレントディレクトリー指定
        self.currentFolder_id = currentFolder_id
        folderUpload = self.user_client.folder(folder_id=self.currentFolder_id).get()
        #print("FolderName: {0}".format(folderUpload.name), flush=True)
        #print("Items: {0}".format(folderUpload.item_collection['total_count']), flush=True)
        
    # Type: dictionary
    # 指定フォルダーの情報を表示
    def getFolder(self, folder_id):
        folder = self.user_client.folder(folder_id=folder_id).get()
        folderInfo = {'folderName':folder.name,'items':folder.item_collection['total_count']}
        #print(str(folderInfo), flush=True)
        return folderInfo

    # カレントフォルダーの情報を表示
    def getCurrentFolder(self, folder_id):
        return self.getFolder(self.currentFolder_id)

    # Type: list
    # 指定フォルダー内のファイルをリストを取得
    def getFolderItems(self, folder_id):
        items = self.user_client.folder(folder_id=folder_id).get_items()
        itemlist = [{'id':item.id ,'type':item.type,'name':item.name} for item in items]
        return itemlist
    
    # カレントフォルダー内のファイルをリストを取得
    def getCurrentFolderItems(self):
        return self.getFolderItems(self.currentFolder_id)

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
        #print(f'Start Update {filepath}.') 
        try:
            new_file = self.user_client.folder(folder_id).upload(filepath)
            return {'Type':'upload', 'id':new_file.id,'id':new_file.name, 'status': 200, 'API': 'Box Upload'}
    # ファイルを新バージョンとしてアップロード
        except BoxAPIException as ex:
            if ex.status == 409:
                updated_file = self.user_client.file(ex.context_info['conflicts']['id']).update_contents(filepath, etag=ex.context_info['conflicts']['etag'])
                #print(f'Success Update {filepath}.') 
                return {'Type':'update', 'id': ex.context_info['conflicts']['id'], 'name': ex.context_info['conflicts']['name'], 'status': 200, 'API': 'Box Upload'}
            else:
                return {'status':ex.status}

    # ファイルをカレントフォルダー内にアップロード 同一名の場合は新バージョンとしてアップデート
    def uploadCurrentFolderFile(self, filepath):
        return self.uploadFile(self.currentFolder_id,filepath)
