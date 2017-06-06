import re
from urllib import request

url = "http://www.qiushibaike.com/hot/page/1"
headers = {
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
}
req = request.Request(url, headers=headers)
content = request.urlopen(req).read().decode("utf-8")

pattern = re.compile(r'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>', re.S)
items = re.findall(pattern, content)
for item in items:
    con = re.sub(re.compile(r'<\w+>|</\w+>|<\w+/>|&quot'), '', item[1])
    print(item[0]+"--------"+con)