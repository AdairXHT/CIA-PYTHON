#!/usr/bin/env python
# coding: utf-8



import requests
import time
import pandas as pd

#用pandas包读取指定xlsx文档
df1=pd.read_excel("抖音 url list.xlsx")
#转换为list数据格式
urllist=df1.抖音URL.tolist()

#创建名为“geturl”的功能，输入参数为url
def geturl(url):
    res = requests.head(url)
    #获取具体的长链接
    url = res.headers.get('location')
    #返回变量
    return url

#创建名为list1的变量
list1=[]
#长度为urllist变量行数的循环
for i in urllist:
    a=geturl(i)
    #把返回得到的变量储存在变量名为list1的数组里
    list1.append(a)
    print(a)
    time.sleep(2)

#写出list1里的所有内容到"iris.csv"文档里，不带有列名
pd.DataFrame(list1).to_csv("iris.csv",header=None,index=False)

