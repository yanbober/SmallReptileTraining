from lxml import etree


class HtmlParser(object):
    pass

    def parse_main_subjects(self, content):
        print(str(content))
        html = etree.HTML(content.lower())
        subject = html.xpath('//ul[@class="img"]/li/a')
        print(str(len(subject)))
        for href in subject:
            print(href.attrib)
        return list()