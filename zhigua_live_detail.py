# coding=utf-8
# zhigua视频页url到topic的转换 

import csv
import json
import os
import re
import urllib
import urllib.request


def get(url, cookie):
    if "treasure/monitor/detail" in url:
        req = urllib.request.Request(
            url="http://api.zhigua.cn/v1/Monitor/Report/Get?liveVideoId=%s&monitorLiveId=%s" % (re.findall("detail/\d+/\w+/(\d+)/(\d+)", url)[0]),
            method='GET', headers={"Cookie": "User=" + cookie})
        data=json.loads(urllib.request.urlopen(req).read())
        resp = data['Data']
        return {'url': url, 'broadcast_begin':resp['StartTime'],'topic': resp['TaoBaoUrl'].split("=")[-1]}
    elif "live/detail/" in url:
        req = urllib.request.Request(
            url="http://api.zhigua.cn/v1/Live/GetLive?liveVideoId=%s&sign=%s" % (re.findall("detail/(\d+)/(\w+)", url)[0]),
            method='GET', headers={"Cookie": "User=" + cookie})
        data=json.loads(urllib.request.urlopen(req).read())
        resp = data['Data']
        return {'url': url, 'broadcast_begin':resp['StartTime'],'topic': resp['Topic'].split("=")[-1]}


def login(username, password):
    req = urllib.request.Request(url="http://api.zhigua.cn/v1/login/Login",
                                 data=json.dumps({"tel": username, "pwd": password}).encode('utf-8'),
                                 headers={'Content-Type': 'application/json;charset=UTF-8'}, method='POST')
    return urllib.request.urlopen(req).getheader("Set-Cookie").split(";")[0].replace("User=", "")


def generator2Csv(generator, fields, outputFile):
    with open(outputFile, "w", encoding="gb18030", newline='') as f:
        writer = csv.DictWriter(f, fields, dialect="excel")
        writer.writerow(dict(zip(fields, fields)))
        for item in generator:
            writer.writerow(item)


if __name__ == '__main__':
    if not os.path.exists("auth.txt"):
        username = input("请输入账号：")
        password = input("请输入密码：")
        with open("auth.txt", "w") as f:
            f.write("%s\n%s" % (username, password))
    with open("auth.txt", "r") as f:
        username, password = f.read().split("\n")
    urls = input("请输入视频页url（多个连接请用半角符英文逗号分隔）：")
    print("正在下载数据，请稍候....")


    def gen(urls):
        cookie = login(username, password)
        for url in urls.split(","):
            try:
                yield get(url, cookie)
            except:
                print(url,"转换失败")


    path = "直播链接转换.csv"
    generator2Csv(gen(urls), ["url", "broadcast_begin", "topic"], path)
    print("下载完成，csv路径：%s" % os.path.abspath(path))
    input("按下回车键退出")
