#-*-coding:utf-8-*-

import urllib.request as urllib2
from urllib import request
import time, random
from bs4 import BeautifulSoup
time.clock()

# user_agent是爬虫与反爬虫斗争的第一步
ua_headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}

# 通过Request()方法构造一个请求对象
url="https://etherscan.io/"
request1=urllib2.Request(url,headers=ua_headers)
print(request1.headers,request1.type,request1.data)

# 向指定的url地址发送请求，并返回服务器响应的类文件对象
response=urllib2.urlopen(request1)
# 服务器返回的类文件对象支持python文件对象的操作方法
html=response.read()
print(html.decode('utf-8')) 

'''

for i in range(3):
    url = 'https://etherscan.io/txs?a=0xbd168cbf9d3a375b38dc51a202b5e8a4e52069ed&p='+str(i+1)
    print(url)
    page = request.urlopen("https://www.baidu.com/")
    '''
'''for i in range(3):
    url = 'https://etherscan.io/txs?a=0xbd168cbf9d3a375b38dc51a202b5e8a4e52069ed&p='+str(i+1)+'/'
    page = request.urlopen(url)
    soup = BeautifulSoup(page)
    for link in soup.find_all('div','wrapper'):
        context = link.get_text()
        print(context)
'''
print(time.clock())
