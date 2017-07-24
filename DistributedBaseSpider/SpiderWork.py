import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from multiprocessing.managers import BaseManager


'''
[分布式爬取解析工作端，可台机器分别运行]

简单主从模式的分布式爬虫，支持多节点管理

Ubuntu OSError: [Errno 98] Address already in use
$ sudo netstat -tlnp|grep 8001
tcp 0   0 0.0.0.0:8001  0.0.0.0:*   LISTEN  24314/python3.5 
$ kill -9 24314
'''


class SpiderWork(object):
    def __init__(self):
        self.addr_port = ('127.0.0.1', 8001)

        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')

        print('工作集群节点正在连接集群控制中心 {0}......'.format(str(self.addr_port)))
        self.m = BaseManager(address=self.addr_port, authkey=b'baidu-baike-android')
        self.m.connect()

        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        print('工作集群节点连接集群控制中心完成！')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'CMD_END':
                        print('工作集群节点回应集群控制中心结束指令！')
                        self.result.put({'new_urls': 'CMD_END', 'data': 'CMD_END'})
                        return
                    print('工作集群节点正在解析URL：{0}'.format(url.encode('utf-8')))
                    content = self._download(url)
                    new_urls, data = self._parser(url, content)
                    self.result.put({'new_urls': new_urls, 'data': data})
            except EOFError as e:
                print('工作集群节点连接工作节点失败！'+str(e))
                return
            except Exception as e:
                print('SpiderWork crawl fail!'+str(e))

    def _parser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all("a", href=re.compile(r"/item/\w+"))
        for link in links:
            url_path = link["href"]
            new_url = urljoin(page_url, url_path)
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        data = {}
        data['url'] = page_url
        title_node = soup.find("dd", class_="lemmaWgt-lemmaTitle-title").find("h1")
        data["title"] = title_node.get_text()
        summary_node = soup.find("div", class_="lemma-summary")
        data["summary"] = summary_node.get_text()
        return data

    def _download(self, url):
        if url is None:
            return None
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None


if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()
