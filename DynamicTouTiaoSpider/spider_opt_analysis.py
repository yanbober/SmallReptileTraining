# coding=utf-8
import json
import urllib
from pathlib import Path
from urllib import request
'''
Python3.X 动态页面爬取（逆向解析）实例
爬取今日头条关键词搜索结果的所有详细页面大图片并按照关键词及文章标题分类存储图片
'''

class CrawlOptAnalysis(object):
    def __init__(self, search_word="美女"):
        self.search_word = urllib.parse.quote(search_word)

    def _crawl_data(self, offset):
        url = 'http://www.toutiao.com/search_content/?offset={0}&format=json&keyword={1}&autoload=true&count=20&cur_tab=1'.format(self.search_word, offset)
        try:
            with request.urlopen(url, timeout=10) as response:
                content = response.read()
        except Exception as e:
            content = None
            print('crawl data exception.'+str(e))
        return content

    def _parse_data(self, content):
        if content is None:
            return None
        try:
            data_list = json.loads(content)['data']
            result_dict = data_list
        except Exception as e:
            result_dict = None
            print('parse data exception.'+str(e))
        return result_dict

    def _save_picture(self, page_title, url):
        if url is None or page_title is None:
            print('save picture params is None!')
            return
        save_dir = Path('./output/{0}/{1}/'.format(self.search_word, page_title))
        if not save_dir.exists():
            save_dir.mkdir()
        save_file = save_dir + url.split("/")[-1]
        try:
            with request.urlopen(url, timeout=30) as response, save_file.open('wb') as f_save:
                f_save.write(response.read())
            print('Image is saved! search_word={0}, page_title={1}, save_file={2}'.format(self.search_word, page_title, save_file))
        except Exception as e:
            print('save picture exception.'+str(e))

    def go(self):
        result = self._parse_data(self._crawl_data(0))
        # offset = 0
        # while len(result) >= 20:
        #     offset += len(result)
        #     result = self._parse_data(self._crawl_data(offset))


if __name__ == '__main__':
    CrawlOptAnalysis("美女").go()
    CrawlOptAnalysis("旅游").go()
    CrawlOptAnalysis("风景").go()
