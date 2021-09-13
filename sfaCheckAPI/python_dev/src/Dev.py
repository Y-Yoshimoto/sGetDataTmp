import json
import datetime

# 取引先/更新追加
def AddAccount(connection):
    print("AddAccount")
    # 1データ追加
    Idata = {
        "Name": "Banking6 APITEST",
        "Industry": "Banking",
        "AccountCode__c": "AH000004"
    }
    Account=connection.insertRecode("Account", Idata)
    print(str(Account))

    # 1データ更新
    Udata = {
        "BillingCountry": "Japan", 
        "BillingCity": "Tokyo",
        "BillingState": "Chuouku",
        "BillingStreet": "Ginza"
    }
    #print(str(Udata))
    Account=connection.updateRecode("Account",Account[1]["id"], Udata)
    print(str(Account))
    
    # 1データ外部キー更新
    Sdata = {
        "AccountCode__c": "AH000004",
        "Ownership": "Public",
        "AnnualRevenue": 100
    }
    Account=connection.upsertRecodeExid("Account","AccountCode__c", Sdata)
    print(str(Account))
    
    return 0

def BulkAddsAccount(connection):
    print("BulkAddsAccount")
    # 3データ追加
    Idatas = [{
        "Name": "Banking APITEST",
        "Industry": "Banking",
        "AccountCode__c": "AH000001"
    },
    {
        "Name": "Electronics APITEST",
        "Industry": "Electronics",
        "AccountCode__c": "AH000002"
    },
    {
        "Name": "Utilities APITEST",
        "Industry": "Utilities",
        "AccountCode__c": "AH000003"
    }]
    Accounts=connection.bulkInsertRecode("Account", "Name", Idatas)
    print(Accounts)
    
    # 3データ更新
    Udatas = [{
        "id": Accounts[1]["results"][0]["id"],
        "BillingCountry": "Japan", 
        "BillingCity": "Tokyo",
    },
    {
        "id": Accounts[1]["results"][1]["id"],
        "BillingCountry": "Japan", 
        "BillingCity": "Kawasaki",
    },
    {
        "id": Accounts[1]["results"][2]["id"],
        "BillingCountry": "Japan", 
        "BillingCity": "Yokohama",
    }]
    Accounts=connection.bulkUpdateRecode("Account", Udatas)
    print(str(Accounts))
    
    # 3データ外部キー更新
    Sdata = [{
        "AccountCode__c": "AH000001",
        "Ownership": "Public",
        "AnnualRevenue": 100
    },{
        "AccountCode__c": "AH000002",
        "Ownership": "Private",
        "AnnualRevenue": 350
    },{
        "AccountCode__c": "AH000003",
        "Ownership": "Subsidiary",
        "AnnualRevenue": 400
    }]
    Accounts=connection.bulkUpsertRecodeExid("Account", "AccountCode__c", Sdata)
    print(str(Accounts))
    
    
    return 0