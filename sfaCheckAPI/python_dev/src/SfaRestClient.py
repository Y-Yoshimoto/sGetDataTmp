import os
import jwt         # Pyjwt
import requests
import datetime

# Salesforceコネクター
class SfaConnection:
    def __init__(self):
        print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " Initialize Salesforce Connecter")
        ## 秘密鍵読み込み
        f = open('./sfadxinfo.pem', 'r')
        self.private_key = f.read()
        f.close()
        ## API接続情報指定
        self.apiVer=os.environ['SalesforceAPIVersion']
        self.instance_url, self.access_token = self.jwt_login(os.environ['CONSUMER_ID'], os.environ['USERNAME'], self.private_key, False)
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
        self.instance_url, self.access_token = self.jwt_login(os.environ['CONSUMER_ID'], os.environ['USERNAME'], self.private_key, False)
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
    def SOQLquery(self, SOQL):
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/queryAll/?q=' + SOQL,
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
            recodes += self.SOQLqueryNext(response["nextRecordsUrl"])            
        return recodes

    ## nextRecordsUrlデータの取得
    def SOQLqueryNext(self, nextRecordsUrl):
        result = requests.get(
            self.instance_url + nextRecordsUrl,
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
            recodes += self.SOQLqueryNext(response["nextRecordsUrl"])
        return recodes


    ## SOQLクエリー(Limit 2000)
    def SOQLqueryLimit(self, SOQL):
        result = requests.get(
            self.instance_url + '/services/data/' + self.apiVer +'/query/?q=' + SOQL,
            headers=self.baseHeaders
        )
        if result.status_code != 200:
            print(vars(result))
        response = result.json()

        print((response.keys()))
        print('nextRecordsUrl' in response)
        # nextRecordsUrl
        return response['records']

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