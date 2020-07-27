#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import requests
import re

df1=pd.read_excel("weibo.xlsx")
urllist=df1.链接.tolist()

list=[]

for i in urllist:
    res = requests.get(i)
    uid=re.search(r'"uid": (\d+)',res.text).group(1)
    bid=re.search(r'"bid": "([A-Za-z0-9]+)',res.text).group(1)
    url="https://weibo.com/"+uid+"/"+bid
    list.append(url)
    
pd.DataFrame(list).to_csv("hehe.csv",header=None,index=False)

