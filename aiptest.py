#!/usr/bin/env python
#coding=utf-8

import requests
import re
s = requests.Session()
r = s.get("http://172.30.121.56/")
#print r.text
pattern="<input type='hidden' name='csrfmiddlewaretoken' value='(.*)' />"
csrfmiddlewaretoken=re.findall(pattern,r.text)
print csrfmiddlewaretoken
csrfmiddlewaretoken=csrfmiddlewaretoken[0]
print csrfmiddlewaretoken
payload = {'username': 'admin', 'password': '123456','submit':u'登 录','csrfmiddlewaretoken':csrfmiddlewaretoken}
#a = requests.session()
headers={'Cookie':'csrftoken='+csrfmiddlewaretoken,'Host':'172.30.121.56','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer':'http://172.30.121.56/',
    'Content-Type':'application/x-www-form-urlencoded'}
r = s.post("http://172.30.121.56/",data=payload)
print r.text
#f = s.get('http://172.30.121.56/dashboard/')
#print f.text
#csrfmiddlewaretoken=lqsaq0eh1GK1MJ0Eb2rrsKQDOTGoyqkb&username=guoyp1&password=123456&submit=%E7%99%BB%C2%A0%E5%BD%95