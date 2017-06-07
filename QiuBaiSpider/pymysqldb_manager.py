import pymysql

from QiuBaiSpider.tools import Tools


class DbManager(object):
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        try:
            self.db = pymysql.connect("localhost", "testuser", "test123", "TESTDB")
            self.db.set_charset('utf8')
            self.cursor = self.db.cursor()
        except:
            pass

    def close(self):
        try:
            if self.db is not None:
                self.db.close()
        except BaseException as e:
            Tools.log("#ERROR# DbManager close failed."+str(e))

    def insertDict(self, dict_data=None):
        if dict_data is None:
            return False
        pass
        return True