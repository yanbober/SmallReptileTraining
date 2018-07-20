# -*- coding:UTF-8 -*-

from urllib import request
import chardet

if __name__ == '__main__':
	respose=request.urlopen('http://www.baidu.com')
	html=respose.read()
	charset=chardet.detect(html)
	print(charset)