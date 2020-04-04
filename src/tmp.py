# from selenium import webdriver
# # br = webdriver.Firefox()
# # br.get('http://localhost:63342/NetEaseMusicAnalysis/src/test.html')
# # s = br.find_element_by_class_name('c 1')
# # print(s)
# # br.quit()
# for i in range(5):
#     if(i==3):
#         print('33')
#     else:
#         pass
#     print(i,'ni')
#     print('---------')
# import pandas as pd
# # # import csv
# # # def saveCSV(data,name):
# # #     f = open(name,'w+',newline='')
# # #     filewriter = csv.writer(f)
# # #     filewriter.writerow(list(data[0].keys()))
# # #     for d in data:
# # #         filewriter.writerow(list(d.values()))
# # #     f.close()
# # # x = {'user':'lele','age':18}
# # # y = []
# # # y.append(x)
# # # y.append(x)
# # # saveCSV(y,'data.csv')
# # pd.set_option('display.max_rows',500)
# # pd.set_option('display.max_columns',500)
# # pd.set_option('display.width',1000)
# # d = pd.read_csv('data.csv')
# # print(d)
# from selenium import webdriver
# br = webdriver.Firefox()
# br.get('https://music.163.com/')
# br.get('https://www.baidu.com/')
# from selenium import webdriver
#
# driver = webdriver.Firefox()
#
# driver.get("https://www.baidu.com")
#
# Guanyubaidu = driver.find_element_by_link_text("关于百度")
# LianJie = Guanyubaidu.get_attribute("href")
#
# js = f"window.open('{LianJie}')"  # 打开新窗口的JS代码
# driver.execute_script(js)  # 执行打开新窗口的JS代码
#
# js2 = "window.open('http://ir.baidu.com/')"  # 打开新窗口的JS代码
# driver.execute_script(js2)
#
# handles = driver.window_handles
# for handle in handles:  # 历遍所有标签的句柄
#     driver.switch_to.window(handle)  # 通过句柄切换到该浏览器的标签
#     if '关于百度' in driver.title:  # driver.title当前标签名
#         print(driver.title)
#         break  # 退出循环
# print(driver.title, driver.current_window_handle)
import threading
import time
def f1(ll):
    for i in range(100):
        ll.append(i)
        time.sleep(2)
