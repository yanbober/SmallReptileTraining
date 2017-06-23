'''
Python 3.X ProcessPoolExecutor 模块演示 Demo
'''
import concurrent
from concurrent.futures import ProcessPoolExecutor
from urllib import request


class TestProcessPoolExecutor(object):
    def __init__(self):
        self.urls = [
            'https://www.baidu.com/',
            'http://blog.jobbole.com/',
            'http://www.csdn.net/',
            'https://juejin.im/',
            'https://www.zhihu.com/'
        ]

    def get_web_content(self, url=None):
        print('start get web content from: '+url)
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            req = request.Request(url, headers=headers)
            return request.urlopen(req).read().decode("utf-8")
        except BaseException as e:
            print(str(e))
            return None
        print('get web content end from: ' + str(url))

    def runner(self):
        process_pool = ProcessPoolExecutor(max_workers=4)
        futures = dict()
        for url in self.urls:
            future = process_pool.submit(self.get_web_content, url)
            futures[future] = url

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                data = future.result()
            except Exception as e:
                print('Run process url ('+url+') error. '+str(e))
            else:
                print(url+'Request data ok. size='+str(len(data)))
        print('Finished!')

if __name__ == '__main__':
    TestProcessPoolExecutor().runner()