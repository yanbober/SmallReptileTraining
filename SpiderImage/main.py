# -*-coding:utf-8-*-

# 天堂图片网爬取高质量图片


import urllib.request as urllib2
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

#要爬取的关键词
Img_Name='girl'



# 构造图片页数

page_number_s=0
# 图片总页数
page_count=1


for p in range(page_count):
	page_number_s=page_number_s+1
	page_number=str(page_number_s)

	# 构建URL
	url="http://www.ivsky.com/search.php?q="+Img_Name+"&PageNo="+page_number

	# 通过Request()方法构造一个请求对象

	request1=urllib2.Request(url=url)
	# 把头添加进去
	request1.add_header('User-Agent',user_agent)
	# 向指定的url地址发送请求，并返回服务器响应的类文件对象
	response=urllib2.urlopen(request1)
	# 服务器返回的类文件对象支持python文件对象的操作方法
	#html=response.read()
	#print(html.decode('utf-8')) 


	response.encoding=('utf-8', 'ignore')

	#.decode('utf-8', 'ignore').replace(u'\xa9', u'')
	soup=BeautifulSoup(response,"html.parser")
	#for i in soup.find_all('div',{'class':'il_img'}):
	for i in soup.find_all('div',{'class':{'il_img',}}):
		for ii in i.find_all('a'):
			# 可以直接取属性获得href内容 https://bbs.csdn.net/topics/392161042?list=lz
			url2='http://www.ivsky.com'+ii['href']
			request2=urllib2.Request(url=url2)
			request2.add_header('User-Agent',user_agent)

			response2=urllib2.urlopen(request2)
			response2.encoding=('utf-8', 'ignore')
			soup2=BeautifulSoup(response2,"html.parser")
			soup22=soup2.find_all('div',{'class':{'left',}})
			for url3 in soup22.find_all("a"):

			#url3=soup2.find_all('div',{'class':'bt-green'})
				print(url3)


'''
	k=0
	for i in soup.find_all('td',limit=400):
		k=k+1
		m=k%8

		if m==0:
			br='\n'
		else:
			br=''
		tbody=i.get_text() 
		data=str(tbody.encode('gbk','ignore'))+","+br
		with open('test11.csv', 'a') as f:
			f.write(data)


	print("已完成:",str(page_number)+"/"+str(page_count))
'''