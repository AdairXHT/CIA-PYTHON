# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:23:30 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

#62进制转10进制的函数
def changeBase(n,b):
    baseList = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    x,y = divmod(n,b)
    if x > 0:
        return changeBase(x,b) + baseList[y]
    else:
        return baseList[y]
    

def main(): 
    #文件路径
    root = tk.Tk()
    root.withdraw()#获得选择好的文件夹
    Filepath = filedialog.askopenfilename() #获得选择好的文件
    data = pd.read_excel(Filepath)#读取文件
    
    #历遍每一个网址
    for i in range(data.shape[0]):
        if "://m.weibo" in data.iloc[i,0]:#以“://m.weibo”判断是否为手机端

            mobile_url = data.iloc[i,0][-16 :]#将每个手机端网址的后16位取出来

            first = changeBase(int(mobile_url[-7:]),62)#后七位进行转换

            second = changeBase(int(mobile_url[-14:-7]),62)#后八 -- 十四位进行转换

            third = changeBase(int(mobile_url[:2]),62)#前两位进行转换

            if len(second) != 4:#微博机制：如果7位十进制数字转换后不满4个占位符，则需要在前面加一个0
                second = "0" + second

            if len(first) != 4:
                first = "0" + first            

            fix_url = third + second + first#转换后的62进制，位数必定是9位

            data.iloc[i,0] = data.iloc[i,0][:30] + fix_url#将原有的10进制数字替换成62进制

            data.iloc[i,0] = data.iloc[i,0].replace("m.","")#规整格式

            data.iloc[i,0] = data.iloc[i,0].replace("cn","com")#规整格式
        else:
            pass
    data.columns=['网页端url']#更换表头名
    
    return data.to_excel("网页端.xlsx",index=False)#输出excel

main()
  
    



































