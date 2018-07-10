#-*-coding:utf-8-*-

import urllib.request as urllib2
from urllib import request
import time, random
from bs4 import BeautifulSoup
time.clock()


url="https://etherscan.io/txs?a=0xbd9d6e7489a7b450937fa7ecbabd71be819bee3d&p=1"
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
for i in soup.find_all('tbody'):
	
	# .get_text() 用于获取文本内容，括号内可以加关键词
	tx=i.get_text("/")
	print(tx)
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
#print(time.clock())
