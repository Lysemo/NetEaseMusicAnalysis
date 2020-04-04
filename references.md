## 1.Python+Selenium基础+环境配置：
* URL：https://www.jianshu.com/p/1531e12f8852

## 2.WebDriver配置：
* URL：https://www.cnblogs.com/alex-13/p/11152435.html
## find_elements_by_xpath("./*")  找到所有子元素
## find_elements_by_xpath("./..")  找到父元素
## # print(cmt.get_attribute("innerHTML"))  获取元素下源码
## current_window = br.current_window_handle
## page.click()
## all_windows = br.window_handles
## for window in all_windows:
##     if window != current_window:
##         br.switch_to.window(window)
## br.switch_to.default_content()
## br.switch_to.frame('contentFrame')
## time.sleep(1)