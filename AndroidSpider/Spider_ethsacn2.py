#-*-coding:utf-8 -*-
# 将ETHSCAN记录保存的脚本
import urllib.request as urllib2
from urllib import request
import random
from bs4 import BeautifulSoup

'''
# user_agent是爬虫与反爬虫斗争的第一步
ua_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}'''
# 用于模拟http头的User-agent
ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]

user_agent=random.choice(ua_list)

#要查询的以太地址
address="0x7751278c8b6b224946d065776fc67c81a5202958"
page_number_start=0
page_count=1
for ii in range(page_count):
	page_number_start=page_number_start+1
	page_number=str(page_number_start)

	#url="https://etherscan.io/txs?a="+address+"&p="+page_number
	url='https://etherscan.io/txsInternal?a='+address+'&&valid=true&p='+page_number

	# 通过Request()方法构造一个请求对象

	request1=urllib2.Request(url=url)
	# 把头添加进去
	request1.add_header('User-Agent',user_agent)
	# 向指定的url地址发送请求，并返回服务器响应的类文件对象
	response=urllib2.urlopen(request1)
	# 服务器返回的类文件对象支持python文件对象的操作方法
	#html=response.read()
	#print(html.decode('utf-8')) 
	soup=BeautifulSoup(response,"html.parser")

	k=0
	for i in soup.find_all('form',{'id':'ctl00'}):
		print(i.get_text())
		'''k=k+1
		m=k%7

		if m==0:
			br='\n'
		else:
			br=''
		tbody=i.get_text() 
		data=str(tbody.encode('gbk','ignore'))+","+br
		with open('test12.csv', 'a') as f:
			f.write(data)
'''

	print("已完成:",str(page_number)+"/"+str(page_count))