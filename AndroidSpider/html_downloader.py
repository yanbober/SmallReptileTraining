from urllib import request, error
from urllib.parse import urlparse


class HtmlDownLoader(object):
    def download(self, url, retry_count=3, headers=None, proxy=None):
        if url is None:
            return None
        try:
            req = request.Request(url, headers=headers)
            opener = request.build_opener()
            if proxy:
                proxies = {urlparse(url).scheme: proxy}
                opener.add_handler(request.ProxyHandler(proxies))
            content = request.urlopen(req).read()
        except error.URLError as e:
            print('HtmlDownLoader download error:', e.reason)
            content = None
            if retry_count > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    #说明是 HTTPError 错误且 HTTP CODE 为 5XX 范围说明是服务器错误，可以尝试再次下载
                    return self.download(url, retry_count-1)
        return content