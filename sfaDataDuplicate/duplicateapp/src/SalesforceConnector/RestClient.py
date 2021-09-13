import os
import jwt         # Pyjwt
import requests
import datetime
import json

# Salesforceコネクター
class SfaConnection:
    def __init__(self):
        print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " Initialize Salesforce Connecter")
        ## 秘密鍵読み込み
        #f = open('./sfadxinfo.pem', 'r')
        f = open(os.environ['SAF_ACCESS_PEM'], 'r')
        self.private_key = f.read()
        f.close()
        self.consumer_id = os.environ['SAF_CONSUMER_ID']
        self.username = os.environ['SAF_USERNAME']
        ## API接続情報指定
        self.apiVer=os.environ['SAF_SalesforceAPIVersion']
        self.instance_url, self.access_token = self.jwt_login(self.consumer_id, self.username , self.private_key, False)
        self.baseHeaders={
            'content-type': 'application/json',
            'Authorization': "Bearer " + self.access_token
        }

    ## 認証
    def jwt_login(self, consumer_id, username, private_key, sandbox=False):
        endpoint = 'https://test.salesforce.com' if sandbox is True else 'https://login.salesforce.com'
        jwt_payload = jwt.encode(
            { 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                'iss': consumer_id,
                'aud': endpoint,
                'sub': username
            },
            private_key,
            algorithm='RS256'
        )
        # トークン取得
        result = requests.post(
        endpoint + '/services/oauth2/token',
        data={
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': jwt_payload
        }
        )
        body = result.json()
        if result.status_code != 200:
            raise print(body['error'], body['error_description'])

        return (body['instance_url'], body['access_token'])
        
    ## トークン更新
    def update_token(self):
        print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " Update Salesforce token")
        self.instance_url, self.access_token = self.jwt_login(self.consumer_id, self.username, self.private_key, False)
        self.baseHeaders={
            'content-type': 'application/json',
            'Authorization': "Bearer " + self.access_token
        }

    ## 制限値の取得
    def GetLimitsInfo(self):
        # https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_limits.htm
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/limits',
            headers=self.baseHeaders
        )
        if result.status_code != 200:
            raise print(body['error'], body['error_description'])
        return result.json()

    ## SOQLクエリー
    def SOQLgetQuery(self, SOQL: str) -> list:
        """SOQLでデータ取得
        
        """
        baseUrl = '/services/data/' + self.apiVer +'/queryAll/?q=' + SOQL
        return self.SOQLRecursiveCall(baseUrl)

    def SOQLRecursiveCall(self, callUrl: str) -> list:
        result = requests.get(
            self.instance_url + callUrl,
            headers=self.baseHeaders
        )
        if result.status_code != 200:
            print(vars(result))
        ## リクエストデータ取り出し
        response = result.json()
        recodes = response['records']
        ## nextRecordsUrl チェック/取得
        if 'nextRecordsUrl' in response:
            #print("Next")
            recodes += self.SOQLRecursiveCall(response["nextRecordsUrl"])
        return [self._＿DellAttributes(recode) for recode in recodes]
        
    def _＿DellAttributes(self, data: dict):
        """Attributes データを除外"""
        data.pop('attributes', None)
        return data
        

    ## SOQLクエリー(Limit 2000)
    def SOQLqueryLimit(self, SOQL, limit):
        SOQLl = SOQL + " LIMIT " + str(limit)
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/query/?q=' + SOQLl,
            headers=self.baseHeaders
        )
        if result.status_code != 200:
            print(vars(result))
        response = result.json()

        print((response.keys()))
        print('nextRecordsUrl' in response)
        # nextRecordsUrl
        return response['records']

    ## sObjectsカラム取得
    def sObjectColumns(self, sObjects):
        #print(self.instance_url + '/services/data/' + self.apiVer +'/sobjects/' + sObjects + '/describe/')
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/sobjects/' + sObjects + '/describe/',
            headers=self.baseHeaders
        )
        response = result.json()
        #print(sObjects)
        sObjectsName = response['name']
        sObjectsLabel = response['label']
        columns = [{'sObjectsName':sObjectsName,
                    'sObjectsLabel':sObjectsLabel,
                    'name':column["name"],
                    'label':column["label"],
                    'soapType':column["soapType"],
                    'type':column["type"]} for column in response['fields'] ]
                
        return columns
        #yield columns

    ## データ追加 ######################################################
    ### 1レコード追加
    def insertRecode(self, sObjects, data):
        result = requests.post(
            self.instance_url + '/services/data/' + self.apiVer + "/sobjects/" + sObjects + "/",
            headers=self.baseHeaders,
            data=json.dumps(data)
        )
        #print(vars(result))
        return (result.status_code, json.loads(result.text))
    
    ## データバルク追加 
    def bulkInsertRecode(self, sObjects, refcolumn, datas):
        if len(datas) > 200:
            return (500, {'success': False, 'errors': ["Over 200 recode"]})
        # リクエストデータ生成
        for data in datas:
            data["attributes"] = {"type" : sObjects, "referenceId" : data[refcolumn]}
            #print(data)
        #print({"records": datas})
        # APIコール
        result = requests.post(
            self.instance_url + '/services/data/' + self.apiVer + "/composite/tree/" + sObjects + "/",
            headers=self.baseHeaders,
            data=json.dumps({"records": datas})
        )
        #print(vars(result))
        return (result.status_code, json.loads(result.text))
    
    
    ## データ更新 ######################################################
    ### 1レコード更新
    def updateRecode(self, sObjects, id, data):
        result = requests.patch(
            self.instance_url + '/services/data/' + self.apiVer + "/sobjects/" + sObjects + "/" + id,
            headers=self.baseHeaders,
            data=json.dumps(data)
        )
        #print(vars(result))
        if result.text == "":
            return (204, {'id': id, 'success': True, 'errors': []})
        return (result.status_code, json.loads(result.text))
    
    ### 複数レコード更新
    def bulkUpdateRecode(self, sObjects, datas):
        if len(datas) > 200:
            return (500, {'success': False, 'errors': ["Over 200 recode"]})
        # リクエストデータ生成
        for data in datas:
            data["attributes"] = {"type" : sObjects}
        #print({"records": datas})
        # APIコール
        result = requests.patch(
            self.instance_url + '/services/data/' + self.apiVer + "/composite/sObjects/",
            headers=self.baseHeaders,
            data=json.dumps({"allOrNone" : True,"records": datas})
        )
        #print(vars(result))
        return (result.status_code, json.loads(result.text))


    ## 外部IDデータ更新/追加 ######################################################
    ### 1レコード更新
    def upsertRecodeExid(self, sObjects, ExidColumn, data):
        Exid = str(data.pop(ExidColumn))
        result = requests.patch(
            self.instance_url + '/services/data/' + self.apiVer + "/sobjects/" + sObjects + "/" + ExidColumn + "/" + Exid,
            headers=self.baseHeaders,
            data=json.dumps(data)
        )
        #print(vars(result))
        if result.text == "":
            return (204, {'id': id, 'success': True, 'errors': []})
        return (result.status_code, json.loads(result.text))
    ### 複数レコード更新
    def bulkUpsertRecodeExid(self, sObjects, ExidColumn, datas):
        if len(datas) > 200:
            return (500, {'success': False, 'errors': ["Over 200 recode"]})
        # リクエストデータ生成
        for data in datas:
            data["attributes"] = {"type" : sObjects}
        #print({"records": datas})
        # APIコール
        result = requests.patch(
            self.instance_url + '/services/data/' + self.apiVer + "/composite/sObjects/" + sObjects + "/" + ExidColumn,
            headers=self.baseHeaders,
            data=json.dumps({"allOrNone" : True,"records": datas})
        )
        #print(vars(result))
        return (result.status_code, json.loads(result.text))


    ## 利用状況
    ### ページ別メトリクス
    def GetLightningUsageByPageMetrics(self):
        # https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_limits.htm
        SOQL='''SELECT PageName, EptBinUnder3, EptBin3To5, EptBin5To8, EptBin8To10, EptBinOver10, TotalCount 
                FROM LightningUsageByPageMetrics 
                ORDER BY PageName'
                LIMIT 20 '''
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/sobjects/LightningUsageByPageMetrics',
            headers=self.baseHeaders,
            data=SOQL
        )
        if result.status_code != 200:
            print(vars(result))
        return result.json()

    ### アプリケーション別メトリクス
    def GetLightningUsageByAppTypeMetrics(self):
        # https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_lightning_usagebyapptypemetrics.htm
        #SOQL='''SELECT MetricsDate,user.profile.name,COUNT_DISTINCT(user.id) Total 
        #        FROM LightningUsageByAppTypeMetrics 
        #        WHERE MetricsDate = LAST_N_DAYS:30 AND AppExperience = 'Salesforce Mobile' 
        #        GROUP BY MetricsDate,user.profile.name'''
        SOQL='''SELECT MetricsDate,user.profile.name,COUNT_DISTINCT(user.id) Total 
            FROM LightningUsageByAppTypeMetrics LIMIT 20 '''
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/sobjects/LightningUsageByAppTypeMetrics',
            headers=self.baseHeaders,
            data=SOQL
        )
        if result.status_code != 200:
            print(vars(result))
        return result.json()


    ## DataDell
    #def DataDell(self, datas):
    #    for data in datas:
    #        print(data["Id"])
    #        result = requests.delete(
    #            self.instance_url + '/services/data/' + self.apiVer +'/sobjects/Contact/' + data["Id"],
    #            headers=self.baseHeaders
    #        )