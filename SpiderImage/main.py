# -*-coding:utf-8-*-

# 天堂图片网爬取高质量图片


import urllib.request as urllib2
import random, re
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

#要爬取的关键词，中文编码出错，待解决
Img_Name='new'
url_pre="http://www.ivsky.com/search.php?q="+Img_Name+"&PageNo="
# 构造图片页数
# 利用抛出错误的代码，判断结果小于2也的情况
page_count1=0
page_count2=1
while page_count2>page_count1:
	request_pre=urllib2.Request(url=url_pre+str(page_count2))

	request_pre.add_header('User-Agent',user_agent)

	response_pre=urllib2.urlopen(request_pre)

	soup_pre=BeautifulSoup(response_pre,"html.parser")
	aaa=soup_pre.find_all('div',{'class':'pagelist'})
	for a_a in aaa:
		a_a_a=a_a.get_text(',')
		a_a_a=a_a_a.split(',')
		page_count1=int(a_a_a[-2])

	if a_a_a[-1]!='下一页':

		break

	print('正在计算总页数，已搜索到第%s页' %page_count1)
	request_pre1=urllib2.Request(url=url_pre+str(page_count1))
	request_pre1.add_header('User-Agent',user_agent)

	response_pre1=urllib2.urlopen(request_pre1)

	soup_pre1=BeautifulSoup(response_pre1,"html.parser")
	aaa1=soup_pre1.find_all('div',{'class':'pagelist'})
	for a_a1 in aaa1:
		a_a_a1=a_a1.get_text(',')
		a_a_a1=a_a_a1.split(',')
		page_count2=int(a_a_a1[-2])

	if a_a_a[-1]!='下一页':
		break
if page_count1>page_count2:
	page_count=page_count1
else:
	page_count=page_count2
# 得用类解决上边代码重复问题


page_number_s=0
# 图片总页数，待更新自动获取总页数。
#page_count=1
print('计算完成，关键词为%s的图片总计有%s页' %(Img_Name,page_count))

print('现在开始下载...')
for p in range(page_count):
	page_number_s=page_number_s+1
	page_number=str(page_number_s)

	# 构建URL
	url=url_pre+page_number


	# 通过Request()方法构造一个请求对象

	request1=urllib2.Request(url=url)
	# 把头添加进去
	request1.add_header('User-Agent',user_agent)
	# 向指定的url地址发送请求，并返回服务器响应的类文件对象
	response=urllib2.urlopen(request1)
	# 服务器返回的类文件对象支持python文件对象的操作方法
	#html=response.read()
	#print(html.decode('utf-8')) 

	#如出现编码错误，试试这个 response.encoding=('utf-8', 'ignore')

	#.decode('utf-8', 'ignore').replace(u'\xa9', u'')
	soup=BeautifulSoup(response,"html.parser")
	#for i in soup.find_all('div',{'class':'il_img'}):
	img_name=0
	for i in soup.find_all('div',{'class':{'il_img',}}):
		img_name=img_name+1
		for ii in i.find_all('a'):

			# 可以直接取属性获得href内容 https://bbs.csdn.net/topics/392161042?list=lz
			url2='http://www.ivsky.com'+ii['href']
			request2=urllib2.Request(url=url2)
			request2.add_header('User-Agent',user_agent)

			response2=urllib2.urlopen(request2)
			#response2.encoding=('utf-8', 'ignore')
			soup2=BeautifulSoup(response2,"html.parser")
			soup22=soup2.find_all('img',{'id':'imgis'})

			#url3=soup2.find_all('div',{'class':'bt-green'})
			img_url=re.findall('src="+(.*)"', str(soup22))[0]

			# 这是MAC下的目录
			#urllib2.urlretrieve(img_url,'/Users/lhuibin/py/img/%s%s.jpg' % (page_number_s,img_name))

			# 这是WIN10HOME下的目录
			urllib2.urlretrieve(img_url,'C:/py/img/%s%s.jpg' % (page_number_s,img_name))
			print('正在下载第%s页第%s张图片，总计%s页' %(page_number_s,img_name,page_count))
			print('存储为C:/py/img/%s%s.jpg' % (page_number_s,img_name))


print("已经全部下载完毕！")
