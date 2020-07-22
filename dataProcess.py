from utils.jsonParser import jsonParser
from utils.jsonParser import jsonSaver
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import jieba
import re
import time
import jieba.analyse
from collections import OrderedDict

def filter_str(desstr,restr=''):
    #过滤除中英文、数字及常用标点以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9,.!?，。！？《》……]")
    return res.sub(restr, desstr)

def getWordCloud(data_list):
    #生成词云图
    def getStopWds(path):
        return [line.strip() for line in open(path).readlines()]
    word = ''
    for com in data_list:
        word = word + filter_str(com)
    txt = ' '.join(jieba.cut(word))
    print('word length:',len(txt))
    stopwd = getStopWds('./data/materials/ChineseStopWords.txt')
    wc = WordCloud(font_path='./data/simfang.ttf',min_font_size=1, stopwords=stopwd, background_color='white', width=1000, height=860,
                          margin=2).generate(txt)
    wc.to_file('01.jpg')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def getWordFreq(data_list):
    #获取评论前10关键字词频
    word = ''
    for com in data_list:
        word = word + filter_str(com)
    count = 0
    for i in jieba.cut(word):
        count = count + 1
    print('word length:', count)
    tags = jieba.analyse.extract_tags(word,topK=10,withWeight=True)
    for tag in tags:
        print('%s:%.4f' % (tag[0],tag[1]))

def filter(data_list):
    #爬取数据预处理
    for d in data_list:
        d['comment'] = filter_str(d['comment'])
        d['comment'] = d['comment'].replace(' ','')
        star = d['star']
        if (star.find('万') != -1):
            d['star'] = str(int(float(star.replace('万', '')) * 10000))
    return data_list




if __name__ == '__main__':
    start = time.time()
    '''
    数据过滤，去除特殊字符和将star中的万转换为数字
    '''
    # data_list = jsonParser('./data/comment/comments-lastdance.json')
    # data_list = filter(data_list)
    # jsonSaver(data_list,'./data/comment/comments-lastdance-filter.json')
    # ---------------------------------------
    '''
    词云
    '''
    # data_list = jsonParser('./data/comment/comments-fengjixuchui-filter.json')
    # data = []
    # for d in data_list:
    #     data.append([d['comment'],int(d['star'])])
    # data.sort(key=lambda s:s[1],reverse=True)
    # data = data[:]
    # print(data)
    # data = [i[0] for i in data]
    # getWordCloud(data)
    # --------------------------------------------
    '''
    评论点赞数前10
    '''
    # data_list = jsonParser('./data/comment/comments-lastdance-filter.json')
    # data = []
    # for d in data_list:
    #     data.append([d['comment'],int(d['star']),d['refer']])
    # data.sort(key=lambda s:s[1],reverse=True)
    # data = data[:10]
    # for d in data:
    #     if(len(d[2])!=0):
    #         print('star:', d[1], '|comment:', d[0],'refer comment:',d[2])
    #     else:
    #         print('star:',d[1],'|comment:',d[0])
    # --------------------------------------------------------------
    '''
    词频前10统计
    '''
    # data_list = jsonParser('./data/comment/comments-lastdance-filter.json')
    # data = []
    # for d in data_list:
    #     data.append(d['comment'])
    # getWordFreq(data)
    # --------------------------------------------------------------
    data_list = jsonParser('./data/comment/comments-lastdance-filter.json')
    for d in data_list:
        d['time']
    print('spend time:',int(time.time()-start))