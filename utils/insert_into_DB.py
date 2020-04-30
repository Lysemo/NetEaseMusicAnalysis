#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""在python脚本中，将文件导入到数据库中
"""
from pymongo import MongoClient

def saveComments_to_mongo(data):
    MONGO_URL = "mongodb://localhost:27017"
    MONGO_DB = "web_crawler"
    MONGO_TABLE = "comments"

    client = MongoClient(MONGO_URL)  # 生成mongodb对象
    collection = client[MONGO_DB][MONGO_TABLE]
    for d in data:
        try:
            collection.update_many(d,{'$set':d},upsert=True)
        except:
            print(d,' save happen error!!!')
def saveSongAndSinger_to_mongo(data):
    MONGO_URL = "mongodb://localhost:27017"
    MONGO_DB = "web_crawler"
    MONGO_TABLE = "song_info"

    client = MongoClient(MONGO_URL)
    collection = client[MONGO_DB][MONGO_TABLE]
    try:
        collection.update_many(data,{'$set':data},upsert=True)
    except:
        print(data,' save happen error!!!')
def getCSV(path):
    import csv
    with open('%s' %path, 'r', encoding='utf-8')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader = csv.DictReader(csvfile)
        # 创建一个counts计数一下 看自己一共添加了了多少条数据
        counts = 0
        for each in reader:
            # 将数据中需要转换类型的数据转换类型。原本全是字符串（string）。
            # each['index']=int(each['index'])
            saveComments_to_mongo(each)
            counts += 1
            print('成功添加了' + str(counts) + '条数据 ')

