from MeiTuLuSpider.html_downloader import Downloader
from MeiTuLuSpider.html_parser import HtmlParser
from MeiTuLuSpider.spider_output import OutPutUse
from MeiTuLuSpider.url_manager import UrlManager
'''
爬取美图录网站妹子图，然后按照目录命名下载下来
Extra module:
requests
LXml
'''


class Scheduler(object):
    def __init__(self):
        self.url = UrlManager()
        self.downloader = Downloader()
        self.parser = HtmlParser()
        self.output = OutPutUse()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        }

    def run(self):
        url_seed_main = self.url.get_main_seed_url()
        content = self.downloader.download(url_seed_main, retry_count=2, headers=self.headers).decode('utf8')
        subject_urls = self.parser.parse_main_subjects(content)
        for subject_url in subject_urls:
            self._run_subject(subject_url)

    def _run_subject(self, subject_url):
        print('#subject_url#:'+subject_url)
        content = self.downloader.download(subject_url, retry_count=2, headers=self.headers).decode('utf8')
        mj_info = self.parser.parse_subject_mj_info(content)
        if mj_info is None:
            return
        mj_max_count = int(mj_info['count'])
        mj_name = str(mj_info['mj_name'])
        cur_count = 1
        index = 1
        while cur_count <= mj_max_count:
            real_url = subject_url
            if index > 1:
                real_url = subject_url[0:len(subject_url)-5] + ('_'+str(index)+'.html')
            index = index + 1
            # 正常每页的大图个数为4
            cur_count = cur_count + 4
            print('正在获取大图的页面是:'+real_url)
            content = self.downloader.download(real_url, retry_count=2, headers=self.headers).decode('utf8')
            pic_urls = self.parser.parse_page_pics(content)
            for pic_url in pic_urls:
                self.output.download_and_save(pic_url, mj_name)

if __name__ == '__main__':
    Scheduler().run()