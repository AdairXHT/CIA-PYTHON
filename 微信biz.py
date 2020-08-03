#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import selenium
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#读取"d:/微信test.txt"该地址下的txt文档，同时不读取文档的抬头
wechatlist=pd.read_csv("d:/微信test.txt",header=None)
#把位置为在最左的字串更换为list数据格式
wechatlist=wechatlist[0].tolist()


chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')

chrome_options.add_argument('--window-size=400,600')

#创建两个变量
name=[]
biz=[]

for i in wechatlist:
    browser = webdriver.Chrome(options=chrome_options)


    url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query='+i+'&ie=utf8&_sug_=n&_sug_type_='
    browser.get(url)#打开浏览器预设网址
    urls = browser.find_elements_by_xpath("//a")
    window_before = browser.window_handles[0]

    time.sleep(1)

    if (urls[17]!=None) and (urls[17].get_attribute("href")!="javascript:void(0);") :
        urls[17].click()
        window_after = browser.window_handles[1]
        browser.switch_to_window(window_after)

        time.sleep(4)

        res3=requests.get(browser.current_url)
        a=re.findall('var biz = "(\w+==)',res3.text)
        b=re.findall('var title ="([a-zA-Z0-9_\u4e00-\u9fa5]+)',res3.text)
        biz.append(a)
        name.append(b)

    else:
        a=[]
        b=[]
        biz.append(a)
        name.append(b)
        
    browser.quit()   
    print(a,b)
    
final=pd.DataFrame((pd.Series([x[0] if len(x[:])!=0 else x[:] for x in name]),pd.Series([y[0] if len(y[:])!=0 else y[:] for y in biz]))).T
final.to_excel("d:/微信biz.xlsx",header=["name","biz"],index=False)

