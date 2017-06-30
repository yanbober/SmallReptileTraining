# coding=utf-8
import json
import os
import re
import urllib
from urllib import request
'''
Python3.X 动态页面爬取（逆向解析）实例
爬取今日头条关键词搜索结果的所有详细页面大图片并按照关键词及文章标题分类存储图片
'''

class CrawlOptAnalysis(object):
    def __init__(self, search_word="美女"):
        self.search_word = search_word
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': 'www.toutiao.com',
            'Referer': 'http://www.toutiao.com/search/?keyword={0}'.format(urllib.parse.quote(self.search_word)),
            'Accept': 'application/json, text/javascript',
        }

    def _crawl_data(self, offset):
        '''
        模拟依据传入 offset 进行分段式上拉加载更多 item 数据爬取
        '''
        url = 'http://www.toutiao.com/search_content/?offset={0}&format=json&keyword={1}&autoload=true&count=20&cur_tab=1'.format(offset, urllib.parse.quote(self.search_word))
        print(url)
        try:
            with request.urlopen(url, timeout=10) as response:
                content = response.read()
        except Exception as e:
            content = None
            print('crawl data exception.'+str(e))
        return content

    def _parse_data(self, content):
        '''
        解析每次上拉加载更多爬取的 item 数据及每个 item 点进去详情页所有大图下载链接
        [
            {'article_title':XXX, 'article_image_detail':['url1', 'url2', 'url3']},
            {'article_title':XXX, 'article_image_detail':['url1', 'url2', 'url3']}
        ]
        '''
        if content is None:
            return None
        try:
            data_list = json.loads(content)['data']
            print(data_list)
            result_list = list()
            for item in data_list:
                result_dict = {'article_title': item['title']}
                url_list = list()
                for url in item['image_detail']:
                    url_list.append(url['url'])
                result_dict['article_image_detail'] = url_list
                result_list.append(result_dict)
        except Exception as e:
            print('parse data exception.'+str(e))
        return result_list

    def _save_picture(self, page_title, url):
        '''
        把爬取的所有大图下载下来
        下载目录为./output/search_word/page_title/image_file
        '''
        if url is None or page_title is None:
            print('save picture params is None!')
            return
        reg_str = r"[\/\\\:\*\?\"\<\>\|]"  #For Windows File filter: '/\:*?"<>|'
        page_title = re.sub(reg_str, "", page_title)
        save_dir = './output/{0}/{1}/'.format(self.search_word, page_title)
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        save_file = save_dir + url.split("/")[-1] + '.png'
        if os.path.exists(save_file):
            return
        try:
            with request.urlopen(url, timeout=30) as response, open(save_file, 'wb') as f_save:
                f_save.write(response.read())
            print('Image is saved! search_word={0}, page_title={1}, save_file={2}'.format(self.search_word, page_title, save_file))
        except Exception as e:
            print('save picture exception.'+str(e))

    def go(self):
        offset = 0
        while True:
            page_list = self._parse_data(self._crawl_data(offset))
            if page_list is None or len(page_list) <= 0:
                break
            try:
                for page in page_list:
                    article_title = page['article_title']
                    for img in page['article_image_detail']:
                        self._save_picture(article_title, img)
            except Exception as e:
                print('go exception.'+str(e))
            finally:
                offset += 20


if __name__ == '__main__':
    CrawlOptAnalysis("美女").go()
    CrawlOptAnalysis("旅游").go()
    CrawlOptAnalysis("风景").go()
