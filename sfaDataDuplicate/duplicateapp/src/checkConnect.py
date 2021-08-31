import json
import datetime
import schedule
import time

# SalesforceAPIコネクター
import SalesforceConnector.RestClient as SfaC
# MongoDBコネクター接続
import MongoConnector.MongoConnector as MongoC
# Boxコネクター接続
import BoxConnector.BoxConnector as BoxC

#  補助関数読み込み
import subFunctions as sub

def main():
    print(f'{sub.nowdate()}, Info, Start.')
    
    # Salesforce
    print(f'{sub.nowdate()}, Info, Start Salesforce Connection')
    sfac = SfaC.SfaConnection()
    print(f'{sub.nowdate()}, Info, Success Salesforce Connection')
    
    # Box
    print(f'{sub.nowdate()}, Info, Start Box Connection.')
    boxc = BoxC.Connector()
    print(f'{sub.nowdate()}, Info, Success Box Connection')
    
    # MongoDB
    print(f'{sub.nowdate()}, Info, Start MongoDB Connection')
    mongoc = MongoC.Connector("sObjectData")
    print(f'{sub.nowdate()}, Info, Success MongoDB Connection')

    print(f'{sub.nowdate()}, Info, End.')

if __name__ == '__main__':
    main()
