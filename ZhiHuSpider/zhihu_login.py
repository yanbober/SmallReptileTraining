from urllib.parse import urlencode

import requests
import time
from bs4 import BeautifulSoup


class ZhiHuLogIn(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Host': 'www.zhihu.com',
            'Origin': 'https://www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh - CN,zh;q=0.8',
            'Connection': 'keep-alive'
        }
        self.request_session = requests.session()
        self.request_session.headers.update(self.headers)

    def get_login_xsrf_and_captcha(self):
        try:
            url_login = "https://www.zhihu.com/#signin"
            url_captcha = 'http://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn' % (time.time() * 1000)
            login_content = self.request_session.get(url_login).content
            soup = BeautifulSoup(login_content, 'lxml')
            xsrf = soup.find('input', attrs={'name': '_xsrf'})['value']
            captcha_content = self.request_session.get(url_captcha).content
            return {'xsrf': xsrf, 'captcha_content': captcha_content}
        except Exception as e:
            print('get login xsrf and captcha failed!'+str(e))
            return dict()

    def parse_captcha_manual(self, captcha=None):
        '''
        zhihu登录验证码是选择图片中反方向的文字
        这里姑且将验证码存盘后等待用户手动打开输入
        :param captcha: 获取的实时验证码
        :return: 用户打开login_captcha.gif文件获取的反向文字
        '''
        if captcha is None:
            return None
        with open('login_captcha.gif', 'wb') as open_file:
            open_file.write(captcha)
        return input('请输入login_captcha.gif图片中所有倒立的文字(Enter Finsh)：')

    def login(self, account=None, pwd=None):
        valid_dict = self.get_login_xsrf_and_captcha()
        post_data = {
            '_xsrf': str(valid_dict['xsrf']),
            'captcha_type': 'cn',
            'captcha': self.parse_captcha_manual(valid_dict['captcha_content']),
            'phone_num': account,
            'password': pwd
        }
        print(str(post_data))
        e_post_data = urlencode(post_data).encode("utf8")
        url_real_login = 'http://www.zhihu.com/login/phone_num'
        response = self.request_session.post(url_real_login, e_post_data)
        print(str(response.content.decode('utf8')))