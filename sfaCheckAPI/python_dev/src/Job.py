import SfaRestClient
import SfaLimitProcessing
import SfaHistoryAnalytics
import json
import datetime

## 制限値取得/更新
def UpdateLimitData(connection):
    #### Data Limits ####
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ", Get Limits from Salesforce")
    ### トークン更新
    connection.update_token()
    ## 制限値取得
    limitData=connection.GetLimitsInfo()
    # 取得値の整形
    limitInfo = SfaLimitProcessing.SfaLimitProcessing(limitData)
    #print(limitInfo)
    # 最新値のRedisデータベース登録
    SfaLimitProcessing.RegistrationLatestValue_REDIS(limitInfo)
    # 最新値のInfluxdbデータベース登録
    SfaLimitProcessing.RegistrationLatestValue_Influxdb(limitInfo)

## ログイン履歴の取得
def GetLoginHistoryData(connection):
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ", Update LoginHistory Data")
    ## ログイン履歴(指定日以降のデータを取得)
    SOQL='''SELECT+Id,UserId,LoginTime,LoginType,SourceIp,LoginUrl,AuthenticationServiceId,
            LoginGeoId,TlsProtocol,CipherSuite,OptionsIsGet,OptionsIsPost,
            Browser,Platform,Status,Application,ClientVersion,ApiType,ApiVersion,CountryIso,
            AuthMethodReference+FROM+LoginHistory+WHERE+LoginTime+>+'''
    SOQL += '2019-04-01T10:00:00-08:00'
    LoginHistory=connection.SOQLquery(SOQL)
    #print(LoginHistory)
    print(len(LoginHistory))
    ## ユーザ情報
    SOQL='''SELECT+Id,Username,LastName,FirstName,Name,CompanyName,Division,Department,
        Title,Address,Email,Alias,IsActive,UserRoleId,ProfileId,
        UserType,LastLoginDate,CreatedDate+FROM+User+WHERE+IsActive=TRUE+LIMIT+1'''
    # Users=connection.SOQLquery(SOQL)
    # print(Users)

## TESTJob
def GetAccount(connection):
    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ", Get Account")
    SOQL='''SELECT+Id,Name,CreatedDate+FROM+Contact+WHERE+CreatedDate+>+'''
    SOQL += '2021-04-01T10:00:00-08:00'
    #SOQL += '2019-04-01T10:00:00-08:00'
    Contact=connection.SOQLquery(SOQL)
    #print(Contact)
    #print(len(Contact))
    #connection.DataDell(Contact)



