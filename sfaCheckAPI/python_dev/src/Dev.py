import json
import datetime

# 取引先/更新追加
def AddAccount(connection):
    print("AddAccount")
    
    Idata = {
        "Name": "Banking6 APITEST",
        "Industry": "Banking"
    }
    
    Account=connection.insertRecode("Account", Idata)
    print(str(Account))


    Udata = {
        "BillingCountry": "Japan", 
        "BillingCity": "Tokyo",
        "BillingState": "Chuouku",
        "BillingStreet": "Ginza"
    }
    #print(str(Udata))
    Account=connection.updateRecode("Account",Account[1]["id"], Udata)
    print(str(Account))
    
    return 0

def BulkAddsAccount(connection):
    print("BulkAddsAccount")
    Idatas = [{
        "Name": "Banking APITEST",
        "Industry": "Banking"
    },
    {
        "Name": "Electronics APITEST",
        "Industry": "Electronics"
    },
    {
        "Name": "Utilities APITEST",
        "Industry": "Utilities"
    }]
    Accounts=connection.bulkInsertRecode("Account", "Name", Idatas)
    #print(Accounts)
    
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
    
    return 0