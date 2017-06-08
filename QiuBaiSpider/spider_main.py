from QiuBaiSpider.pymysqldb_manager import DbManager
from QiuBaiSpider.page_items import PageItems
from QiuBaiSpider.tools import Tools

'''
爬取糗事百科笑话剔除正文DOM标签然后将爬取数据存入MySQL数据库

Extra module:
PyMySQL
'''
class Main(object):
    def __init__(self, max_page=1):
        self.max_page = max_page
        self.db_manager = DbManager()

    def run(self):
        self.db_manager.connect()

        for index in range(self.max_page):
            self._page_run(index)

        self.db_manager.close()

    def _page_run(self, page):
        page_dict_items = PageItems(page).get_page_dict_items()
        if page_dict_items is None:
            return
        for dict_item in page_dict_items:
            self.db_manager.insertDict(dict_item)
        pass

if __name__ == "__main__":
    Tools.setup_log_mode(False)
    Main(10).run()