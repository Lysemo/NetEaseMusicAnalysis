#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
func: about mongodb data read, write, update.
author: Lele Wu.
update: 2020/07/18 19:26
'''
from pymongo import MongoClient

class MongoDBForData():
    def __init__(self,MONGO_URL="mongodb://localhost:27017",MONGO_DB="dataName",MONGO_COLLECTION="collectionName"):
        self.client = MongoClient(MONGO_URL)
        self.collection = self.client[MONGO_DB][MONGO_COLLECTION]
    def insert(self,data):
        try:
            if(isinstance(data,list) or isinstance(data,dict)):
                self.collection.insert_many(data)
            else:
                raise Exception('data type error!')
        except:
            print('data insert error!')
    def sync(self,data):
        for d in data:
            try:
                ds = {'id': d['id'], 'comment': d['comment'], 'userid': d['userid'], 'time': d['time']}
                self.collection.update_many(ds, {'$set': d}, upsert=True)
            except:
                print(d, ' save happen error!!!')
    def update(self,data,condition=None):
        if condition is None:
            condition = data
        if not isinstance(condition,dict):
            raise Exception('condition format error, should be dict type!')
        try:
            if (isinstance(data, list) or isinstance(data,dict)):
                self.collection.update_many(condition,{'$set':data},upsert=True)
            else:
                raise Exception('data type error!')
        except:
            print('data update error!')
    def delete(self,condition):
        try:
            self.collection.delete_many(condition)
        except:
            print('data delete error!')
    def find(self,condition=None):
        if not isinstance(condition,dict):
            raise Exception('condition format error, should be dict type!')
        try:
            if condition is not None:
                return self.collection.find({},condition)
            else:
                return self.collection.find()
        except:
            print('data find error!')