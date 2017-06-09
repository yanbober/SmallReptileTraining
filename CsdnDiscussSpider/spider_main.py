from http import cookiejar
from urllib import request
import re
from urllib.parse import urlencode

'''
登录CSDN帐号后爬取我的博客评论管理列表

Extra module:
Cookie
'''
class CsdnSpider(object):
    def __init__(self):
        self.url_login = "https://passport.csdn.net/?service=http://write.blog.csdn.net/feedback"
        self.url_feedback = "http://write.blog.csdn.net/feedback"
        self.opener = self.create_cookie_opener()
        self.opener.addheaders = [
            ("User-Agent",
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"),
            ("Host", "passport.csdn.net")
        ]

    def create_cookie_opener(self):
        '''
        设置启用Cookie
        :return: 返回一个自定义的opener
        '''
        cookie = cookiejar.CookieJar()
        cookie_process = request.HTTPCookieProcessor(cookie)
        opener = request.build_opener(cookie_process)
        return opener

    def get_random_webflow_form(self):
        '''
        获取随机流水号，CSDN网站登录时需要随表单提交一个随机登录流水key
        :return: 返回FORM表单流水字典
        '''
        try:
            content = self.opener.open(self.url_login).read().decode("utf8")
            lt = re.search(re.compile(r'<input type="hidden" name="lt" value="(.*?)"'), content)
            execution = re.search(re.compile(r'<input type="hidden" name="execution" value="(.*?)"'), content)
            return {'lt': lt[1], 'execution': execution[1], '_eventId': 'submit'}
        except Exception as e:
            print("get random webflow form Exception."+str(e))
            return dict()

    def login(self, user_name=None, password=None):
        '''
        登录CSDN账号
        :param user_name: 用户名
        :param password: 密码
        :return: 返回登陆后的鬼JS自动跳转redirect
        '''
        if user_name is None or password is None:
            print('You need use a valied user name and password to login!')
            return None
        post_form = self.get_random_webflow_form()
        post_form['username'] = user_name
        post_form['password'] = password
        post_data = urlencode(post_form).encode("utf8")

        try:
            content = self.opener.open(self.url_login, data=post_data).read().decode("utf8")
            redirect = re.search(re.compile(r'var redirect = "(.*?)"'), content)
            return redirect[1]
        except Exception as e:
            print("login Exception."+str(e))
            return None

    def run_redirect_back(self, redirect=None):
        if redirect is None:
            return False
        self.opener.open(redirect)
        return True

    def get_feedback_items(self):
        response = self.opener.open(self.url_feedback)
        print(str(response.read().decode("utf-8")))

    def run(self):
        redirect = self.login("yanbober", "XXXXXXXX")
        self.run_redirect_back(redirect)
        self.get_feedback_items()

if __name__ == "__main__":
    CsdnSpider().run()