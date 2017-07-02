import os
import time
from urllib import request
from PIL import Image
from selenium import webdriver
'''
爬取自己 QQ 空间所有照片
不怎么用 QQ 空间， 但是舍不得空间的照片，一张一张下载太慢，所以按照相册趴下来硬盘留念
'''
class SpiderSelenium(object):
    def __init__(self, qq='', pwd=None):
        self.driver = webdriver.PhantomJS()  #Run in Ubuntu, Windows need set executable_path.
        self.driver.maximize_window()
        self.qq = qq
        self.pwd = pwd
        print('webdriver start init success!')

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
            print('webdriver close and quit success!')
        except:
            pass

    def _need_login(self):
        '''
        通过判断页面是否存在 id 为 login_div 的元素来决定是否需要登录
        :return: 未登录返回 True，反之
        '''
        try:
            self.driver.find_element_by_id('login_div')
            return True
        except:
            return False

    def _login(self):
        '''
        登录 QQ 空间，先点击切换到 QQ 帐号密码登录方式，然后模拟输入 QQ 帐号密码登录，
        接着通过判断页面是否存在 id 为 QM_OwnerInfo_ModifyIcon 的元素来验证是否登录成功
        :return: 登录成功返回 True，反之
        '''
        self.driver.switch_to.frame('login_frame')
        self.driver.find_element_by_id('switcher_plogin').click()
        self.driver.find_element_by_id('u').clear()
        self.driver.find_element_by_id('u').send_keys(self.qq)
        self.driver.find_element_by_id('p').clear()
        self.driver.find_element_by_id('p').send_keys(self.pwd)
        self.driver.find_element_by_id('login_button').click()
        try:
            self.driver.find_element_by_id('QM_OwnerInfo_ModifyIcon')
            return True
        except:
            return False

    def _auto_scroll_to_bottom(self):
        '''
        将当前页面滑动到最底端
        '''
        js = "var q=document.body.scrollTop=10000"
        self.driver.execute_script(js)
        time.sleep(6)

    def _get_gallery_list(self, picture_callback):
        '''
        从相册列表点击一个相册进入以后依次点击该相册里每幅图片然后回调，依此重复各个相册
        所有注释掉的 self.driver.get_screenshot_as_file 与 self.driver.page_source 仅仅为了方便调试观察
        :param picture_callback: 回调函数，当点击一个相册的一幅大图时回调
        '''
        time.sleep(5)
        self._auto_scroll_to_bottom()
        #self.driver.get_screenshot_as_file('my_qzone_gallery_screen.png')
        self.driver.switch_to.frame('app_canvas_frame')

        elements = self.driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
        gallery_count = len(elements)
        index = 0
        while index < gallery_count:
            print('WHILE index='+str(index)+', gallery_count='+str(gallery_count))
            self._auto_scroll_to_bottom()
            elements = self.driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
            if index >= len(elements):
                print('WHILE index='+str(index)+', elements='+str(len(elements)))
                break
            print('size='+str(len(elements)))
            #self.driver.get_screenshot_as_file('pppp' + str(hash(elements[index])) + '.png')
            gallery_title = elements[index].text
            elements[index].click()
            time.sleep(5)
            self._auto_scroll_to_bottom()
            #self.driver.get_screenshot_as_file('a_gallery_details_list' + str(hash(elements[index])) + '.png')
            pic_elements = self.driver.find_elements_by_xpath("//*[@class='item-cover j-pl-photoitem-imgctn']")
            for pic in pic_elements:
                pic.click()
                time.sleep(5)
                #self.driver.get_screenshot_as_file('details_' + str(hash(elements[index])) + '_' + str(hash(pic)) + '.png')
                self.driver.switch_to.default_content()
                pic_url = self.driver.find_element_by_id('js-img-border').find_element_by_tag_name('img').get_attribute('src')
                print(gallery_title + ' ---> ' + pic_url)
                if not picture_callback is None:
                    picture_callback(gallery_title, pic_url)
                self.driver.find_element_by_class_name('photo_layer_close').click()
                self.driver.switch_to.frame('app_canvas_frame')
            self.driver.back()
            time.sleep(10)
            index += 1

    def crawl_pictures(self):
        '''
        开始爬取 QQ 空间相册里图片
        '''
        self.driver.get('http://user.qzone.qq.com/{0}/photo'.format(self.qq))
        self.driver.implicitly_wait(20)
        if self._need_login():
            if self._login():
                self._get_gallery_list(self._download_save_pic)
                print("========== QQ " + str(self.qq) + " 的相册爬取下载结束 ===========")
            else:
                print('login with '+str(self.qq)+' failed, please check your account and password!')
        else:
            print('already login with '+str(self.qq))

    def _download_save_pic(self, gallery_title, pic_url):
        '''
        下载指定 url 链接的图片到指定的目录下，图片文件后缀自动识别
        :param gallery_title: QQ 空间相册名
        :param pic_url: 该相册下一张详情图片的 url
        '''
        if gallery_title is None or pic_url is None:
            print('save picture params is None!')
            return
        save_dir = './output/{0}/'.format(gallery_title)
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        save_file = save_dir + str(hash(gallery_title)) + '_' + str(hash(pic_url))
        if os.path.exists(save_file):
            return
        try:
            with request.urlopen(pic_url, timeout=30) as response, open(save_file, 'wb') as f_save:
                f_save.write(response.read())
            new_stuffer_file = save_file + '.' + Image.open(save_file).format.lower()
            os.rename(save_file, new_stuffer_file)

            print('Image is saved! gallery_title={0}, save_file={1}'.format(gallery_title, new_stuffer_file))
        except Exception as e:
            print('save picture exception.'+str(e))


if __name__ == '__main__':
    SpiderSelenium('请用你的QQ号替换', '请用你的QQ密码替换').crawl_pictures()