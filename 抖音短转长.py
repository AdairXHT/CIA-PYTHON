#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import time
import pandas as pd

df1=pd.read_excel("抖音 url list.xlsx")
urllist=df1.抖音URL.tolist()

def geturl(url):
    res = requests.head(url)
    url = res.headers.get('location')
    return url

list1=[]
for i in urllist:
    a=geturl(i)
    list1.append(a)
    print(a)
    time.sleep(2)

pd.DataFrame(list1).to_csv("iris.csv",header=None,index=False)

