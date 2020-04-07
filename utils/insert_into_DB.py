#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""在python脚本中，将文件导入到数据库中
"""
import csv

from pymongo import MongoClient



## 定义插入数据的函数
def saveComments_to_mongo(data):
    MONGO_URL = "mongodb://localhost:27017"  # how to hnow
    MONGO_DB = "web_crawler"
    MONGO_TABLE = "comments"

    client = MongoClient(MONGO_URL)  # 生成mongodb对象
    db = client[MONGO_DB]
    if db[MONGO_TABLE].insert(data):
        print("成功储存到MongoDB.comments", data)
        return True
    return False
class Song_info:
    def __init__(self,id, name, singer):
        self.id = id
        self.name = name
        self.singer = singer
def saveSongInfo_to_mongo(song):
    MONGO_URL = "mongodb://localhost:27017"  # how to hnow
    MONGO_DB = "web_crawler"
    MONGO_TABLE = "songs"
    client = MongoClient(MONGO_URL)  # 生成mongodb对象
    db = client[MONGO_DB]
    info={'id':song.id,'name':song.name,'singer':song.singer}
    if db[MONGO_TABLE].insert(info):
        print("成功储存到MongoDB.songs", info)
        return True
    return False


def getCSV(path):

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


if __name__=='__main__':
    # path = '后会无期-OT_ The End of the World_G.E.M.邓紫棋.csv'
#     # getCSV(path)
    song = Song_info('123', 'song', 'singer')
    saveSongInfo_to_mongo(song)

