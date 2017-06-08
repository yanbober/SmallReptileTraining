import re
from urllib import request
from QiuBaiSpider.tools import Tools


class PageItems(object):
    def __init__(self, page=None):
        self.page = page

    def get_page_dict_items(self):
        if self.page is None:
            return None
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(self.page)
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
            }
            req = request.Request(url, headers=headers)
            content = request.urlopen(req).read().decode("utf-8")

            pattern = re.compile(r'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>', re.S)
            items = re.findall(pattern, content)
            dict_list = list()
            for item in items:
                temp = {"name": Tools.wash_off_html_tag(item[0]), "content": Tools.wash_off_html_tag(item[1])}
                dict_list.append(temp)
                Tools.log("get qiubai " + str(self.page) + " page item is:" + str(temp))
            return dict_list
        except BaseException as e:
            Tools.log("#ERROR# get qiubai " + str(self.page) + " page item failed. " + str(e))
            return None


