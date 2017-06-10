'''
知乎登录(使用手机号登录)
Extra module:
requests
BeautifulSoup
'''
from ZhiHuSpider.zhihu_login import ZhiHuLogIn


class ZhiHuMain(object):
    def __init__(self):
        self.login = ZhiHuLogIn()

    def run(self):
        self.login.login('phone number', 'password')

if __name__ == '__main__':
    ZhiHuMain().run()