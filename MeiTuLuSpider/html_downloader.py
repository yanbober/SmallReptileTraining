import requests
from requests import Timeout
'''
http://docs.python-requests.org/en/master/
'''


class Downloader(object):
    def __init__(self):
        self.request_session = requests.session()
        self.request_session.proxies

    def download(self, url, retry_count=3, headers=None, proxies=None, data=None):
        '''
        :param url: 准备下载的 URL 链接
        :param retry_count: 如果 url 下载失败重试次数
        :param headers: http header={'X':'x', 'X':'x'}
        :param proxies: 代理设置 proxies={"https": "http://12.112.122.12:3212"}
        :param data: 需要 urlencode(post_data) 的 POST 数据
        :return: 网页内容或者 None
        '''
        if headers:
            self.request_session.headers.update(headers)
        try:
            if data:
                content = self.request_session.post(url, data, proxies=proxies).content
            else:
                content = self.request_session.get(url, proxies=proxies).content
        except (ConnectionError, Timeout) as e:
            print('Downloader download ConnectionError or Timeout:' + str(e))
            content = None
            if retry_count > 0:
                self.download(url, retry_count - 1, headers, proxies, data)
        except Exception as e:
            print('Downloader download Exception:' + str(e))
            content = None
        return content

if __name__ == '__main__':
    content = Downloader().download('http://www.baidu.com')
    print(str(content))