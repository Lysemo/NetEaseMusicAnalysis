'''
current newest vision
'''
from selenium import webdriver
import copy
import time
import csv
import re
import threading
from utils.CrawImg import CrawImg
from utils.insert_into_DB import saveComments_to_mongo,saveSongAndSinger_to_mongo
from utils.read_frmo_DB import read_from_mongo

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
def saveAvatar(url,nick):
    crawImg = CrawImg()
    crawImg.getImg(url)
    imgName = 'data/avatar/' + normChara(nick) + crawImg.getArray()[0].getSuffixName()
    with open(imgName,'wb+') as f:
        f.write(crawImg.getArray()[0].getImg())
def commentsParser(comments,song_id):
    comment_list = []
    template_dict = {
        'id':'',
        'nick':'',
        'comment':'',
        'refer_nick':'',
        'refer':'',
        'crawler_time':'',
        'time':'',
        'star':0
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
        comment_dict['star']=0
        if(len(star)!=0):
            comment_dict['star']=int(star[1:-1])
        avatarURL = comment.find_element_by_css_selector('.head').find_element_by_tag_name('img').get_attribute('src')
        try:
            saveAvatar(avatarURL,nick)
        except:
            print(nick + 'avatar save happen error')
        comment_list.append(comment_dict)
    return comment_list

def songParser(url):
    p = re.compile(r'\d+')
    song_id = p.findall(url)[0]
    fo_t = webdriver.FirefoxOptions()
    fo_t.add_argument('--headless')
    br_t = webdriver.Firefox(firefox_options=fo_t)
    print(url+'-浏览器打开成功')
    url = 'https://music.163.com'+url
    br_t.get(url)
    print(url+'页面到达')
    br_t.switch_to.frame('contentFrame')
    time.sleep(1)
    s_n = br_t.find_element_by_css_selector('.tit').text
    s_a = br_t.find_elements_by_css_selector('.des.s-fc4')[0].find_element_by_tag_name('span').get_attribute('title')
    song_name = normChara(br_t.find_element_by_css_selector('.tit').text)
    song_author = normChara(br_t.find_elements_by_css_selector('.des.s-fc4')[0].find_element_by_tag_name('span').get_attribute('title'))
    saveSongAndSinger_to_mongo({'id':song_id,'song_name':s_n,'song_author':s_a})
    print('%s-%s-->评论开始抓取...' % (s_n, s_a))
    try:
        totalPages = int(br_t.find_elements_by_class_name('zpgi')[-1].text)
    except:
        print(s_n + ' || ' + s_a + 'ignore')
        return -2

    f = open('data/comment/' + song_name + '_' + song_author + '.csv', 'w+', newline='', encoding='utf-8')
    keys = ['id','nick','comment','refer_nick','refer','time','star']
    filewriter = csv.writer(f)
    filewriter.writerow(list(keys))
    f.close()

    for i in range(totalPages):
        print('(%s-%s)第<%d/%d>页评论开始抓取...' % (s_n, s_a,i + 1, totalPages))
        cmts = br_t.find_elements_by_class_name('itm')
        comment_list = commentsParser(cmts[-20:],song_id)
        saveComments_to_mongo(comment_list)
        saveCSV(comment_list, 'data/comment/' + song_name + '_' + song_author + '.csv')
        scriptClick(br_t, br_t.find_element_by_link_text('下一页'))
        # print(comment_list)
    print('-----%s_%s抓取完毕-----' % (song_name,song_author))
    br_t.quit()

if __name__ == '__main__':
    fo = webdriver.FirefoxOptions()
    fo.add_argument('--headless')
    # fo.add_argument('--disable-gpu')

    br = webdriver.Firefox(firefox_options=fo)
    url = 'https://music.163.com/'
    br.get(url)
    print('主程序启动')

    mix_button = br.find_element_by_class_name("nav").find_element_by_link_text('歌单')
    anchorClick(mix_button)
    br.switch_to.frame('contentFrame')
    time.sleep(1)
    totalPages = int(br.find_elements_by_class_name('zpgi')[-1].text)
    for perpage in range(totalPages):
        mixs_len = len(br.find_element_by_id('m-pl-container').find_elements_by_tag_name('li'))
        for permix in range(mixs_len):
            mix = br.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')[permix]
            anchorClick(mix)
            song_urls = findSongURLs(br.page_source)
            threads = []
            for song_url in song_urls:
                threads.append(threading.Thread(target=songParser, args=(song_url,)))
            for t in threads:
                t.start()
                while(True):
                    time.sleep(2)
                    if(len(threading.enumerate())<3):
                        break
            br.back()
            time.sleep(1)
        scriptClick(br, br.find_element_by_link_text('下一页'))
    br.quit()




