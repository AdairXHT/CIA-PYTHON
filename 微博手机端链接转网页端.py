#!/usr/bin/env python
# coding: utf-8


import pandas as pd 
import requests
import re

#用pandas包里专门读取excel下的各类文档类型的功能读取文档，并把‘链接’转为list数据类型
df1=pd.read_excel("weibo.xlsx")
urllist=df1.链接.tolist()

#创建变量
list=[]

#循环次数为行数长度
for i in urllist:
    res = requests.get(i)
    uid=re.search(r'"uid": (\d+)',res.text).group(1) #获得uid
    bid=re.search(r'"bid": "([A-Za-z0-9]+)',res.text).group(1) #获得bid
    url="https://weibo.com/"+uid+"/"+bid #创建网页端格式的链接
    
    #储存到list的变量里
    list.append(url)

#输出保存为"hehe.csv"同时不带有列抬头
pd.DataFrame(list).to_csv("hehe.csv",header=None,index=False)

