from selenium import webdriver
import copy
import time
import csv

def normChara(x):
    x = x.replace('/','_')
    x = x.replace('\\','_')
    x = x.replace('：','_')
    x = x.replace(':','_')
    return x
def anchorClick(page):
    page.click()
    time.sleep(1)
def scriptClick(page):
    br.execute_script('arguments[0].click();', page)
    time.sleep(1)
def saveCSV(data,name):
    f = open(name,'w+',newline='',encoding='utf-8')
    filewriter = csv.writer(f)
    filewriter.writerow(list(data[0].keys()))
    for d in data:
        filewriter.writerow(list(d.values()))
    f.close()
def commentsParser(comments):
    comment_list = []
    template_dict = {
        'nick':'',
        'comment':'',
        'refer_nick':'',
        'refer':'',
        'time':'',
        'star':0
    }
    for comment in comments:
        comment_dict = copy.deepcopy(template_dict)
        cmt = comment.find_element_by_css_selector('.cnt.f-brk')
        nick = cmt.find_element_by_tag_name('a').text
        cmt_con = cmt.text[cmt.text.find(nick)+len(nick)+1:]
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
                print('评论已删除')
                pass
        comment_dict['time']=comment.find_element_by_css_selector('.time.s-fc4').text
        star = comment.find_element_by_css_selector('.rp').find_elements_by_tag_name('a')[0].text
        comment_dict['star']=0
        if(len(star)!=0):
            comment_dict['star']=int(star[1:-1])
        comment_list.append(comment_dict)
    return comment_list

if __name__ == '__main__':
    fo = webdriver.FirefoxOptions()
    # fo.add_argument('--headless')
    # fo.add_argument('--disable-gpu')

    br = webdriver.Firefox(firefox_options=fo)
    print('浏览器打开成功')
    url = 'https://music.163.com/'
    br.get(url)
    print(url+'页面到达')

    mix_button = br.find_element_by_class_name("nav").find_element_by_link_text('歌单')
    anchorClick(mix_button)
    br.switch_to.frame('contentFrame')
    time.sleep(1)
    mixs = br.find_element_by_id('m-pl-container').find_elements_by_tag_name('li')

    anchorClick(mixs[0])
    playlists = br.find_element_by_id('song-list-pre-cache').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
    song_col = []
    for playlist in playlists:
        song_url = playlist.find_elements_by_tag_name('td')[1].find_element_by_class_name('txt').find_element_by_tag_name('a').get_attribute('href')
        song_name = playlist.find_elements_by_tag_name('td')[1].find_element_by_class_name('txt').find_element_by_tag_name('b').get_attribute('title')
        song_name = normChara(song_name)
        song_author = playlist.find_elements_by_tag_name('td')[-2].find_element_by_tag_name('span').get_attribute('title')
        song_author = normChara(song_author)
        song_col.append([song_url,song_name,song_author])
    for index,s_col in enumerate(song_col):
        br.get(s_col[0])
        print('<%d/%d>%s_%s-->评论开始抓取...' % ((index + 1),len(song_col),s_col[1],s_col[2]) )
        br.switch_to.frame('contentFrame')
        time.sleep(1)
        totalPages = int(br.find_elements_by_class_name('zpgi')[-1].text)
        # anchorClick(song_url)
        tmp = []
        for i in range(2):
            print('第<%d/%d>页评论开始抓取...' % (i+1,totalPages))
            cmts = br.find_elements_by_class_name('itm')
            comment_list = commentsParser(cmts[-20:])
            tmp.extend(comment_list)
            scriptClick(br.find_element_by_link_text('下一页'))
        print(tmp)
        print('data/'+s_col[1]+'_'+s_col[2]+'.csv')
        saveCSV(tmp,'data/'+s_col[1]+'_'+s_col[2]+'.csv')
        print('-------------')




