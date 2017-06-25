import os
from concurrent.futures import ProcessPoolExecutor
from urllib import request
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
'''
使用进程池爬取解析及存储解析结果示例
爬取百度百科Android词条简介及该词条链接词条的简介信息，将结果输出到当前目录下output目录
'''


class CrawlProcess(object):
    '''
    配合进程池进行URL链接爬取及结果解析；
    最终通过crawl方法的complete_callback参数进行爬取解析结果回调
    '''
    def _request_parse_runnable(self, url):
        print('start get web content from: ' + url)
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            req = request.Request(url, headers=headers)
            content = request.urlopen(req).read().decode("utf-8")
            soup = BeautifulSoup(content, "html.parser", from_encoding='utf-8')
            new_urls = set()
            links = soup.find_all("a", href=re.compile(r"/item/\w+"))
            for link in links:
                new_urls.add(urljoin(url, link["href"]))
            data = {"url": url, "new_urls": new_urls}
            data["title"] = soup.find("dd", class_="lemmaWgt-lemmaTitle-title").find("h1").get_text()
            data["summary"] = soup.find("div", class_="lemma-summary").get_text()
        except BaseException as e:
            print(str(e))
            data = None
        return data

    def crawl(self, url, complete_callback, process_pool):
        future = process_pool.submit(self._request_parse_runnable, url)
        future.add_done_callback(complete_callback)


class OutPutProcess(object):
    '''
    配合进程池对上面爬取解析进程结果进行进程池处理存储；
    '''
    def _output_runnable(self, crawl_result):
        try:
            url = crawl_result['url']
            title = crawl_result['title']
            summary = crawl_result['summary']
            save_dir = 'output'
            print('start save %s as %s.txt.' % (url, title))
            if os.path.exists(save_dir) is False:
                os.makedirs(save_dir)
            save_file = save_dir + os.path.sep + title + '.txt'
            if os.path.exists(save_file):
                print('file %s is already exist!' % title)
                return None
            with open(save_file, "w") as file_input:
                file_input.write(summary)
        except Exception as e:
            print('save file error.'+str(e))
        return crawl_result

    def save(self, crawl_result, process_pool):
        process_pool.submit(self._output_runnable, crawl_result)


class CrawlManager(object):
    '''
    爬虫管理类，进程池负责统一管理调度爬取解析及存储进程
    '''
    def __init__(self):
        self.crawl = CrawlProcess()
        self.output = OutPutProcess()
        self.crawl_pool = ProcessPoolExecutor(max_workers=8)
        self.crawl_deep = 100   #爬取深度
        self.crawl_cur_count = 0

    def _crawl_future_callback(self, crawl_url_future):
        try:
            data = crawl_url_future.result()
            self.output.save(data, self.crawl_pool)
            for new_url in data['new_urls']:
                self.start_runner(new_url)
        except Exception as e:
            print('Run crawl url future process error. '+str(e))

    def start_runner(self, url):
        if self.crawl_cur_count > self.crawl_deep:
            return
        self.crawl_cur_count += 1
        self.crawl.crawl(url, self._crawl_future_callback, self.crawl_pool)


if __name__ == '__main__':
    root_url = 'http://baike.baidu.com/item/Android'
    CrawlManager().start_runner(root_url)