from bs4 import BeautifulSoup
from urllib import request

url='http://www.baidu.com'
resp=request.urlopen(url)
html=resp.read()

bs=BeautifulSoup(html)

print(bs.title, type(bs.title))
