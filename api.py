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
host='172.30.121.56'
port='80'
username='admin'
password='admin'

log_file = os.path.join(os.getcwd(),'log/liveappapi.log')
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=log_format,filename=log_file,filemode='w',level=logging.INFO)
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
# 	sessionid,csrf=login(host, port, username, password)
# 	HEADERS = {"cookie": "csrftoken="+csrf+"; sessionid="+sessionid}

# 	url="http://172.30.121.56/network/"
# 	response = requests.get(url, headers=HEADERS)
# 	text = response.text
# 	print text
def apiTest(num,api_name,host,request_url,request_data,check_point,request_method,request_data_type):
	# headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	#            'X-Requested-With':'XMLHttpRequest',
	#            'Connection':'keep-alive',
	#            'Referer':'http://'+host+':'+port+'/',
	#            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
	#sessionid,csrf=login(host, username, password)
	#HEADERS = {"cookie": "csrftoken="+csrf+"; sessionid="+sessionid}
	HEADERS={"X-Auth-Token":"16b23c15c7ba4cd1b2e06e8d5a881c23"}
	#request_data=request_data+'&csrfmiddlewaretoken='+csrf
	#request_data=json.dumps(request_data)
	if request_method == 'POST':
		response = requests.post(host+request_url, data=request_data,headers=HEADERS)
	if request_method=='GET':
		response=requests.get(host+request_url, data=request_data,headers=HEADERS)
	status = response.status_code
	resp = response.text
	if status == 200:
		#resp = resp.decode('utf-8')
		#print check_point
		try:
			assert check_point in resp
			logging.info("编号为："+num + '的 ' + api_name + ' 测试成功, ' + str(status) + ', ' + str(resp))
			return "Pass"
		except Exception, e:
			logging.error("编号为："+num + '的 ' + api_name + ' 失败！！！, [ ' + str(status) + ' ], ' + str(resp))
			return "200Fail"
	else:
		logging.error("编号为："+num + '的 ' + api_name + ' 失败！！！, [ ' + str(status) + ' ], ' + str(resp))
		return "2001Fail"
def runTest(testCaseFile):
	testCase = xlrd.open_workbook(testCaseFile)
	table = testCase.sheet_by_index(0)
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
		status=apiTest(num, api_name, host, request_url, request_data, check_point, request_method, request_data_type)
		html=html+'<tr><td>' + num + '</td><td>' + api_name + '</td><td>' + host+request_url + '</td><td>' + status + '</td></tr>'
	return table.nrows,html
def sendMail(text):
	sender = '1034977055@qq.com'  
	receiver = ['408496353@qq.com']
	mailToCc = ['1034977055@qq.com']
	subject = '[AutomantionTest]接口自动化测试报告通知'  
	smtpserver = 'smtp.qq.com'  
	username = '1034977055@qq.com'  
	password = ''  

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
	num,reporthtml=runTest('TestCase.xlsx')
	#print type(num)
	html = '<html><meta charset=\"utf-8\"><body>接口测试，共有 ' + str(num-1) + '个 ，列表如下：' + '</p><table><tr><td style="width:100px;">接口序号</td><td style="width:200px;">接口名称</td><td style="width:300px;">接口地址</td><td style="width:200px;">测试结果</td></tr>'
	html = html + reporthtml+'</table></body></html>'
	print html
	f = open("report.html",'w')
	f.write(html)
	f.close()
	sendMail(html)