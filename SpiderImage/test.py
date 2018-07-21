# -*- coding:utf-8 -*-

from urllib import request
from urllib import parse
import json

if __name__ == '__main__':
	Request_URL='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
	Form_Date={}
	Form_Date['from']='AUTO'
	Form_Date['to']='AUTO'
	Form_Date['smartresult']='dict'
	Form_Date['salt']='1532162790927'
	Form_Date['sign']='0de828ac92067f5078cb84f32b613623'
	Form_Date['i']='jack'
	Form_Date['doctype']='json'
	Form_Date['type']='en2zh-CHS'
	Form_Date['version']='2.1'
	Form_Date['keyfrom']='fanyi.web'
	Form_Date['action']='FY_BY_REALTIME'
	Form_Date['typoResult']='false'
	data=parse.urlencode(Form_Date).encode('utf-8')
	response=request.urlopen(Request_URL,data)
	html=response.read().decode('utf-8')
	translate_results=json.loads(html)
	#translate_results=translate_results['translateResult']#[0][0]['tgt']
	print('翻译的结果是：%s' % html)
'''
	i: jack
from: AUTO
to: AUTO
smartresult: dict
client: fanyideskweb
salt: 1532162790927
sign: 0de828ac92067f5078cb84f32b613623
doctype: json
version: 2.1
keyfrom: fanyi.web
action: FY_BY_CLICKBUTTION
typoResult: false'''