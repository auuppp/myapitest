#!/usr/bin/env python
#coding=utf-8

import requests
import re
import json
payload = {
           "auth": {
           "tenantName": "admin",
           "passwordCredentials": {
                "username": "admin",
                "password": "123456"
            }
           }
         }
payload = json.dumps(payload)
r = requests.post("http://172.30.121.32:5000/v2.0/tokens",data=payload)
print r.text
decodejson = json.loads(r.text)
print decodejson
tokenId=decodejson['access']['token']['id']
#print tokenId
#tenantid=decodejson['access']['token']['tenant']['id']
print tokenId
url=decodejson['access']['serviceCatalog'][0]['endpoints'][0]['publicURL']
print url
header={"X-Auth-Token":tokenId}
#header = json.dumps(header)
payload={
    "flavor": {
        "name": "test_flavor",
        "ram": 1024,
        "vcpus": 2,
        "disk": 10,
        "id": "10"
    }
}
payload = json.dumps(payload)
r = requests.post(url+"/flavors",headers=header,data=payload)
print r.text