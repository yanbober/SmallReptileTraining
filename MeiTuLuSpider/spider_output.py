import os
import requests


class OutPutUse(object):
    def __init__(self):
        self.real_download = True
        self.save_root_dir = 'output'

    def download_and_save(self, url, mj_name):
        print('正在下载图片:', mj_name, url)
        if self.real_download is False:
            return
        save_dir = self.save_root_dir + os.path.sep + mj_name
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        save_file = save_dir + os.path.sep + url.split("/")[-1]

        if os.path.exists(save_file):
            print('本地已经存在该图片:', mj_name, url)
            return
        try:
            content = requests.get(url, timeout=60).content
            with open(save_file, "wb") as file_input:
                file_input.write(content)
        except requests.exceptions.ConnectionError:
            print('#ERROR# 下载[%s]的图片:%s出错！', mj_name, url)