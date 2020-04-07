import re
from utils.ImgObj import ImgObj

import requests
class CrawImg:
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36 Edg/80.0.361.109"}
        self.timeout=10
        self.array=[]
    def setHeaders(self,headers):
        self.headers=headers
    def setTimeout(self,timeout):
        self.timeout=timeout
    def getArray(self):
        return self.array
    #图片的后缀名
    def __getSuffixName(self,url):
        findall = re.findall("\\.[a-zA-Z]{3}", url,re.I)
        for i in range(0, len(findall)):
            if re.findall("jpg|png|gif", findall[i], re.I):
                return findall[i]

    #获取图片并以对象的形式保存到array列表中
    def getImg(self,url):
        flag=1
        content=""
        suffixName=""
        try:
            r = requests.get(url, timeout=self.timeout, headers=self.headers)
            if(r.status_code!=200):
                raise Exception()
            content=r.content
            suffixName=self.__getSuffixName(url)
        except :
            flag=0
        img=ImgObj(flag,content,url,suffixName)
        self.array.append(img)

