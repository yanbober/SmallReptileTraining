'''
知乎登录及列表获取
Extra module:
requests
BeautifulSoup
'''
from ZhiHuSpider.zhihu_login import ZhiHuLogIn


class ZhiHuMain(object):
    def __init__(self):
        self.login = ZhiHuLogIn()

    def run(self):
        self.login.login('XXXX', 'XXXX')

if __name__ == '__main__':
    ZhiHuMain().run()