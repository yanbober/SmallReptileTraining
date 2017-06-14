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
        subject_list = self.parser.parse_main_subjects(content)
        for subject in subject_list:
            self._run_subject(subject)

    def _run_subject(self, subject):
        #content = self.downloader.download(subject['url'], retry_count=2, headers=self.headers).decode('utf8')
        pass

if __name__ == '__main__':
    Scheduler().run()