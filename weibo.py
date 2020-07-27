#!/usr/bin/env python
# coding: utf-8

import re
import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


option=webdriver.ChromeOptions()
# option.add_argument('headless') # 设置option
driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器    
driver.get('https://weibo.com/')
print('正在加载界面....')
time.sleep(1)

WebDriverWait(driver,20,0.5).until(EC.visibility_of_element_located((By.ID,'loginname'))).send_keys('把这段话改成你的账号')
        
driver.find_element_by_name('password').send_keys('把这段话改成你的密码')
driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span').click()
time.sleep(1)
        

       
        
WebDriverWait(driver,100,0.5).until(EC.visibility_of_element_located((By.CLASS_NAME,'B_index')))
        
cookies = driver.get_cookies()
cookie_list=[]
for dict in cookies:
    cookie = dict['name'] + '=' + dict['value']
    cookie_list.append(cookie)
    cookie2 = ';'.join(cookie_list)

cookies = {i.split("=")[0]:i.split("=")[1] for i in cookie2.split(";")}

driver.close()


weibolist=pd.read_excel("转uid和biz.xlsx",sheet_name=0)
weibolist=weibolist.KOL.tolist()

weibo_uid=[]
weibo_name=[]
print("当前查询微博为")
print("    ")

for i in weibolist[30:45]:
    res=requests.get("https://s.weibo.com/user?q="+i+"&Refer=index")
    website=re.search("//weibo.com/([/a-zA-Z0-9_\u4e00-\u9fa5]+)",res.text).group(0)
    res2=requests.get("https:"+website,cookies=cookies)
    a=re.findall("fuid=(\d+)&",res2.text)
    b=re.findall("&fname=([-a-zA-Z0-9_\u4e00-\u9fa5]+)&",res2.text)
    weibo_uid.append(a)
    weibo_name.append(b)
    print(i+"                ",end="\r")
    time.sleep(2)
    

conseq=pd.DataFrame((pd.Series([x[0] if len(x[:])!=0 else x[:] for x in weibo_name]),pd.Series([y[0] if len(y[:])!=0 else y[:] for y in weibo_uid]))).T
conseq.to_excel("d:/weibo.xlsx",index=False,header=["name","uid"])
print("    ")
print("已完成所有搜索")
