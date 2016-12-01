#!/usr/bin/env python
#coding=utf-8

import requests
import re
import json
import xlutils
from xlrd import open_workbook
from xlutils.copy import copy
host='172.30.121.54'
port='80'
username='admin'
password='admin'

def gettoken_url():
    payload = {
             "auth": {
             "tenantName": "admin",
             "passwordCredentials": {
                  "username": "admin",
                  "password": "teamsun"
              }
             }
           }
    payload = json.dumps(payload)
    r = requests.post("http://172.30.121.32:5000/v2.0/tokens",data=payload)
    #print r.text
    decodejson = json.loads(r.text)
    #print decodejson
    tokenId=decodejson['access']['token']['id']
    #print tokenId
    novaurl=decodejson['access']['serviceCatalog'][0]['endpoints'][0]['publicURL']
    #print novaurl
    return tokenId,novaurl
def writeexcel(testCaseFile,**kwargs):
    rb = open_workbook(testCaseFile)
    rs = rb.sheet_by_index(0)     
    wb = copy(rb)     
    #通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(0)
    #dict1={(0,1):"test1",(0,2):"test2"}
    #print kwargs["12"]
    for a,value in kwargs.items():
        ws.write(int(a[0]), int(a[2]), value)
    wb.save(testCaseFile)
def getcsrf(host):
  request = requests.Session()
  r = request.get(host+'/')
  #print r.text
  pattern="<input type='hidden' name='csrfmiddlewaretoken' value='(.*)' />"
  csrfmiddlewaretoken=re.findall(pattern,r.text)
  print '**********'
  print csrfmiddlewaretoken
  csrfmiddlewaretoken=csrfmiddlewaretoken[0]
  return csrfmiddlewaretoken,request
def login(host,username,password):
  csrfmiddlewaretoken,request=getcsrf(host)
  #print csrfmiddlewaretoken
  request_data={'username': username, 'password': password,'submit':u'登 录','csrfmiddlewaretoken':csrfmiddlewaretoken}
  headers={'Cookie':'csrftoken='+csrfmiddlewaretoken,'Host':host,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
       'Referer':host+'/',
       'Content-Type':'application/x-www-form-urlencoded'}
  r = request.post(host+'/',data=request_data)
  #print r.cookies
  #print r.text
  try:
    assert "网络" in r.text
    print '登录成功'
    return r.cookies['sessionid'],csrfmiddlewaretoken
  except Exception, e:
    print '登录失败'
  finally:
    print '###'

# def testapi():
#   sessionid,csrf=login(host, port, username, password)
#   HEADERS = {"cookie": "csrftoken="+csrf+"; sessionid="+sessionid}

#   url="http://172.30.121.56/network/"
#   response = requests.get(url, headers=HEADERS)
#   text = response.text
#   print text
if __name__ == '__main__':
    tokenid,novaurl=gettoken_url()
    print tokenid
    print novaurl
    dict1={"8 8":"test1","9 9":"test2"}
    print dict1
    writeexcel('test1.xls',**dict1)