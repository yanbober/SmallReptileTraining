import re
from lxml import etree


class HtmlParser(object):
    def parse_main_subjects(self, content):
        '''
        解析美图录网站主页模特分类页面链接
        :param content: 美图录主页内容
        :return: ['一个模特的大图页面', '一个模特的大图页面']
        '''
        try:
            html = etree.HTML(content.lower())
            subject = html.xpath('//ul[@class="img"]/li')
            subject_urls = list()
            for sub in subject:
                a_href = sub[0].get('href')
                subject_urls.append(a_href)
            return subject_urls
        except Exception as e:
            print(str(e))
            return list()

    def parse_subject_mj_info(self, content):
        '''
        获取具体模特大图页面开头的模特信息
        :param content: 一个类别的模特页面内容
        :return: {'count': 该模特具备图总数, 'mj_name': 模特名字}
        '''
        try:
            html = etree.HTML(content.lower())
            div_cl = html.xpath('//div[@class="c_l"]')
            pic_count = re.search(re.compile(r'.*?(\d+).*?'), div_cl[0][2].text).group(1)
            return {'count': pic_count, 'mj_name': div_cl[0][4].text}
        except Exception as e:
            print(str(e))
            return None

    def parse_page_pics(self, content):
        '''
        获取一个模特页面的模特大图下载链接
        :param content: 一个类别的模特页面内容
        :return: ['大图链接', '大图链接']
        '''
        try:
            html = etree.HTML(content.lower())
            return html.xpath('//div[@class="content"]/center/img/@src')
        except Exception as e:
            print(str(e))
            return list()