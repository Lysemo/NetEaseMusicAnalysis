'''
crawel comments by songid
'''
from selenium import webdriver
import copy
import time
import csv
import re
from utils.CrawImg import CrawImg
from utils.MongoDBForData import MongoDBForData

song_id_coll = []

def normChara(x):
    x = x.replace('/','_')
    x = x.replace('\\','_')
    x = x.replace('：','_')
    x = x.replace(':','_')
    x = x.replace('\n','-')
    return x
def anchorClick(page):
    page.click()
    time.sleep(1)
def findSongURLs(page_source):
    p = re.compile(r'/song\?id=\d+')
    return p.findall(page_source)
def scriptClick(bro,page):
    bro.execute_script('arguments[0].click();', page)
    time.sleep(1)
def saveCSV(data,name):
    f = open(name,'a+',newline='',encoding='utf-8')
    filewriter = csv.writer(f)
    for d in data:
        filewriter.writerow(list(d.values()))
    f.close()
def saveAvatar(url,user_id):
    crawImg = CrawImg()
    crawImg.getImg(url)
    imgName = 'data/avatar-leslie/' + user_id + crawImg.getArray()[0].getSuffixName()
    with open(imgName,'wb+') as f:
        f.write(crawImg.getArray()[0].getImg())
def commentsParser(comments,song_id):
    comment_list = []
    template_dict = {
        'id':'',
        'userid':'',
        'nick':'',
        'comment':'',
        'refer_nick':'',
        'refer':'',
        'crawler_time':'',
        'time':'',
        'star':'0'
    }
    for comment in comments:
        comment_dict = copy.deepcopy(template_dict)
        cmt = comment.find_element_by_css_selector('.cnt.f-brk')
        nick = cmt.find_element_by_tag_name('a').text
        cmt_con = cmt.text[cmt.text.find(nick)+len(nick)+1:]
        comment_dict['id']=song_id
        comment_dict['nick']=nick
        comment_dict['comment']=cmt_con
        ref = comment.find_elements_by_css_selector('.que.f-brk.f-pr.s-fc3')
        comment_dict['refer_nick']=''
        comment_dict['refer']=''
        if(len(ref)!=0):
            if(len(ref[0].find_elements_by_tag_name('a'))!=0):
                refer_nick = ref[0].find_element_by_tag_name('a').text
                comment_dict['refer_nick']=refer_nick
                comment_dict['refer']=ref[0].text[ref[0].text.find(refer_nick)+len(refer_nick)+1:]
            else:
                # print('评论已删除')
                comment_dict['refer_nick']='0xffff'
        comment_dict['crawler_time'] = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        comment_dict['time']=comment.find_element_by_css_selector('.time.s-fc4').text
        star = comment.find_element_by_css_selector('.rp').find_elements_by_tag_name('a')[0].text
        # comment_dict['star']=0
        if(len(star)!=0):
            comment_dict['star']=str(star[1:-1])
        useridurl = comment.find_element_by_css_selector('.cnt.f-brk').find_element_by_tag_name('a').get_attribute('href')
        user_id = useridurl.split('=')[-1]
        comment_dict['userid'] = user_id
        avatarURL = comment.find_element_by_css_selector('.head').find_element_by_tag_name('img').get_attribute('src')
        try:
            saveAvatar(avatarURL,user_id)
        except:
            print(nick + 'avatar save happen error')
        comment_list.append(comment_dict)
    return comment_list

def songParser(url):
    p = re.compile(r'\d+')
    song_id = p.findall(url)[0]
    fo_t = webdriver.FirefoxOptions()
    # fo_t.add_argument('--headless')
    br_t = webdriver.Firefox(firefox_options=fo_t)
    print(url+'-浏览器打开成功')
    url = 'https://music.163.com'+url
    br_t.get(url)
    print(url+'页面到达')
    br_t.switch_to.frame('contentFrame')
    time.sleep(1)
    s_n = br_t.find_element_by_css_selector('.tit').text
    s_a = br_t.find_elements_by_css_selector('.des.s-fc4')[0].find_element_by_tag_name('span').get_attribute('title')
    print('%s-%s-->评论开始抓取...' % (s_n, s_a))
    try:
        totalPages = int(br_t.find_elements_by_class_name('zpgi')[-1].text)
    except:
        print(s_n + ' || ' + s_a + 'ignore')
        return -2
    for i in range(totalPages):
        print('(%s-%s)第<%d/%d>页评论开始抓取...' % (s_n, s_a,i + 1, totalPages))
        cmts = br_t.find_elements_by_class_name('itm')
        comment_list = commentsParser(cmts,song_id)
        print(i,':',comment_list)
        com_mongo.sync(comment_list)
        scriptClick(br_t, br_t.find_element_by_link_text('下一页'))
        time.sleep(1)
    print('-----%s_%s抓取完毕-----' % (s_n,s_a))
    br_t.quit()

if __name__ == '__main__':
    com_mongo = MongoDBForData(MONGO_DB='web_crawler_leslie',MONGO_COLLECTION='comments')
    song_urls = ['/song?id=188489']
    songParser(song_urls[0])
    # threads = []
    # for song_url in song_urls:
    #     threads.append(threading.Thread(target=songParser, args=(song_url,)))
    # threads[0].start()
    # for t in threads:
    #     t.start()
    #     while (True):
    #         time.sleep(2)
    #         if (len(threading.enumerate()) < 3):
    #             break
