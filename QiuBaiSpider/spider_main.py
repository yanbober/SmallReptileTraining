from QiuBaiSpider.pymysqldb_manager import DbManager
from QiuBaiSpider.page_items import PageItems
from QiuBaiSpider.tools import Tools

'''
Extra module:
PyMySQL
'''
class Main(object):
    def __init__(self):
        self.db_manager = DbManager()

    def run(self):
        for index in range(10):
            self._page_run(index)

    def _page_run(self, page):
        page_dict_items = PageItems(page).get_page_dict_items()
        pass

if __name__ == "__main__":
    Tools.setup_log_mode(False)
    Main().run()