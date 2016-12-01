#!/usr/bin/env python
#coding=utf-8

import requests
import re
import xlrd
import os
import logging
import json
import smtplib  
from email.mime.text import MIMEText
import xlwt
from xlutils.copy import copy
log_file = os.path.join(os.getcwd(),'log/liveappapi.log')
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format,filename=log_file,filemode='w',level=logging.INFO)
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
	decodejson = json.loads(r.text)
	tokenId=decodejson['access']['token']['id']
	novaurl=decodejson['access']['serviceCatalog'][0]['endpoints'][0]['publicURL']
	return tokenId,novaurl
def apiTest(num,api_name,host,request_url,request_data,check_point,request_method,request_data_type):
	tokenId,novaurl=gettoken_url()
	host=novaurl
	HEADERS={"X-Auth-Token":tokenId}
	if request_method == 'POST':
		response = requests.post(host+request_url, data=request_data,headers=HEADERS)
	if request_method=='GET':
		response=requests.get(host+request_url, data=request_data,headers=HEADERS)
	status = response.status_code
	resp = response.text
	if status == 200:
		try:
			assert check_point in resp
			logging.info("编号为："+num + '的 ' + api_name + ' 测试成功, ' + str(status) + ', ' + str(resp))
			return "Pass",resp,host
		except Exception, e:
			logging.error("编号为："+num + '的 ' + api_name + ' 失败！！！, [ ' + str(status) + ' ], ' + str(resp))
			return "200Fail",resp,host
	else:
		logging.error("编号为："+num + '的 ' + api_name + ' 失败！！！, [ ' + str(status) + ' ], ' + str(resp))
		return "测试失败，错误代码为："+str(status),resp,host
def runTest(testCaseFile):
	testCase = xlrd.open_workbook(testCaseFile)
	table = testCase.sheet_by_index(0)
	wb = copy(testCase)  
	html=''
	for i in range(1,table.nrows):
		num = str(int(table.cell(i,0).value)).replace('\n','').replace('\r','')
		api_name = table.cell(i,1).value.replace('\n','').replace('\r','')
		host = table.cell(i,2).value.replace('\n','').replace('\r','')
		request_url = table.cell(i,3).value.replace('\n','').replace('\r','')
		request_method = table.cell(i,4).value.replace('\n','').replace('\r','')
		request_data_type = table.cell(i,5).value.replace('\n','').replace('\r','')
		request_data = table.cell(i,6).value.replace('\n','').replace('\r','')
		encryption = table.cell(i,7).value.replace('\n','').replace('\r','')
		check_point = table.cell(i,8).value
		correlation = table.cell(i,9).value.replace('\n','').replace('\r','').split(';')
		active=table.cell(i,10).value.replace('\n','').replace('\r','')
		status,resp,host=apiTest(num, api_name, host, request_url, request_data, check_point, request_method, request_data_type)
		print status,resp,host  
		#通过get_sheet()获取的sheet有write()方法
		ws = wb.get_sheet(0)
		ws.write(i, 2, host)
		ws.write(i, 10, resp)
		ws.write(i, 11, unicode(status))
		wb.save(testCaseFile)
		html=html+'<tr><td>' + num + '</td><td>' + api_name + '</td><td>' + host+request_url + '</td><td>' + status + '</td></tr>'
	return table.nrows,html
def sendMail(text):
	sender = '1034977055@qq.com'  
	receiver = ['408496353@qq.com']
	mailToCc = ['1034977055@qq.com']
	subject = '[AutomantionTest]接口自动化测试报告通知'  
	smtpserver = 'smtp.qq.com'  
	username = '1034977055@qq.com'  
	password = '1qr'  

	msg = MIMEText(text,'html','utf-8')      
	msg['Subject'] = subject  
	msg['From'] = sender
	msg['To'] = ';'.join(receiver)
	msg['Cc'] = ';'.join(mailToCc)
	smtp = smtplib.SMTP()  
	smtp.connect(smtpserver)  
	smtp.login(username, password)  
	smtp.sendmail(sender, receiver + mailToCc, msg.as_string())  
	smtp.quit()
if __name__ == '__main__':
	num,reporthtml=runTest('TestCase.xls')
	#print type(num)
	html = '<html><meta charset=\"utf-8\"><body>接口测试，共有 ' + str(num-1) + '个 ，列表如下：' + '</p><table><tr><td style="width:100px;">接口序号</td><td style="width:200px;">接口名称</td><td style="width:300px;">接口地址</td><td style="width:200px;">测试结果</td></tr>'
	html = html + reporthtml+'</table></body></html>'
	#print html
	f = open("report.html",'w')
	f.write(html)
	f.close()
	sendMail(html)