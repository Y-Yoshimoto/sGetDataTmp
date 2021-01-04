#!/usr/bin/env python
# coding:utf-8
import sys

## MongoConnector 
import MongoConnector

MongoC = MongoConnector.Connector("sObjectData")

MongoC.joinsearchDataTest("LoginHistory","UserId" , "User", "Id")

sys.exit()