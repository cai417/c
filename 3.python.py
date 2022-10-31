# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 23:49:24 2022

@author: cai
"""

import requests
import json
from bs4 import BeautifulSoup
import re
import urllib.request
import datetime as dt
import time as t
def get_access_token():
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'}
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx417d8541e3854304&secret=2b68245d97b5e6f22761912dcad078c9"
    response=requests.get(url,headers=headers).json()
    access_token=response.get('access_token')
    return access_token
def push(access_token,openid,templateid,data):
    url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %access_token
    body={"touser":openid,"template_id":templateid,"data":data}
    res=requests.post(url=url,data=json.dumps(body))
def set_data(curriculum,classroom,teacher):
    url="https://www.msn.cn/zh-cn/weather/forecast/in-%E9%99%95%E8%A5%BF%E7%9C%81,%20%E6%B1%89%E4%B8%AD%E5%B8%82?loc=dW5kZWZpbmVk"
    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"}
    request=urllib.request.Request(url,headers=head)
    response=urllib.request.urlopen(request)
    html=response.read().decode("utf-8")
    soup=BeautifulSoup(html,"html.parser")
    item=str(soup.find_all('div',class_="summaryLineGroupCompact-E1_1"))
    r=re.compile(r'title="(.*?)"')
    findr=r.findall(item)
    weather=findr[0]
    temperature=findr[1]
    item=str(soup.find_all("p",class_="summaryDescCompact-E1_1"))
    r=re.compile(r'>(.*?)<')
    tips=r.findall(item)[0]
    data={"weather":{"value":weather,"color":"#173177"},"temperature":{"value":temperature,"color":"#173177"},"tips":{"value":tips,"color":"#173177"},"curriculum":{"value":curriculum,"color":"#173177"},"classroom":{"value":classroom,"color":"#173177"},"teacher":{"value":teacher,"color":"#173177"}}
    return data
def get_data(week,openid,excel):
    sumc=0
    for i in range(4):
        if excel[week][i]!="None":
            sumc+=1
    time=int(str(dt.datetime.now())[11:13])
    count=0
    while count<sumc:
        time=str(dt.datetime.now())[11:16]
        if int(time[0:2])>18:
            break
        
        timetable={"07:00":0,"09:10":1,"13:00":2,"15:00":3}
        if time in timetable.keys():
            data_class=excel[week][timetable[time]]
            if data_class!="None":
                curriculum,classroom,teacher=data_class.split(",")
                data=set_data(curriculum,classroom,teacher)
                access_token=get_access_token()
                templateid="eWcyc1rxSQ3At597fkdGSn7SiU0V9UnUiKx4tHunI6s"
                for i in openid:
                    push(access_token,i,templateid,data)
                count+=1
        t.sleep(60)
def push_sleep(openid):
    access_token=get_access_token()
    url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" %access_token
    for i in openid:
        body={"touser":i,"template_id":"JeLNHqmDP3UqhcdhqnGcbz4ZNBMg05HUysXWnm431mw"}
        res=requests.post(url=url,data=json.dumps(body))
#课表
timetable={1:["大学物理,@9A405[南区],王瑞斌","数学分析,@9A421[南区],平永周","None","马克思主义基本原理,@6205[南区],党建德"],
           2:["大学英语,@9A421[南区],李小梅","概率论,@9A219[南区],张亚男","常微分方程,@9A217[南区],郭三刚","大学体育,操场,None"],
           3:["数学分析,@9A421[南区],平永周","大学物理,@9A405[南区],王瑞斌","大学物理实验,@电磁学实验室[南区],张崇龙","None"],
           4:["None","大学英语,@41003[南区],李小梅","概率论,@9A219[南区],张亚男","形势与政策,@9A120[南区],杨旸"],
           5:["常微分方程,@9A217[南区],郭三刚","None","劳动教育,@9A207[南区],付明杰","None"],
           6:["None","None","None","None"],
           7:["None","None","None","None"]}
while True:
    #获取token
    access_token=get_access_token()
    url="https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s" %access_token
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'}
    #获取openid
    response=requests.get(url,headers=headers).json()
    openid=response.get('data')["openid"]
    #获取今天周几
    week=(dt.datetime.now().weekday())+1
    #上课推送
    get_data(week,openid,timetable)
    #早睡推送
    if timetable[week%7+1][0]!="None":
        time=str(dt.datetime.now())[11:16]
        while time!="22:00":
            t.sleep(60)
            time=str(dt.datetime.now())[11:16]
        push_sleep(openid)
    next_week=(dt.datetime.now().weekday())+1
    while week==next_week:
        t.sleep(10000)
        next_week=(dt.datetime.now().weekday())+1