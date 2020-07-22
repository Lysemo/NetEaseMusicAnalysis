'''
json parser
'''
import sys
def jsonParser(path):
    with open(path,'r+',encoding='utf-8') as f:  #打开json文件
        datas = f.readlines()   #将json文件所有行读出，存储为list，每一个元素为字符串后的dict
    datas = [eval(data) for data in datas] #将字符串（字典）转为dict
    print('data length:',len(datas))    #打印评论长度
    return datas
def jsonSaver(data_list,path):
    f = open(path,'w+',encoding='utf-8')
    for d in data_list:
        f.write(str(d)+'\n')
    f.close()
if __name__ == '__main__':
    pass
