import pymysql

from QiuBaiSpider.tools import Tools


class DbManager(object):
    sql_create_table = """CREATE TABLE IF NOT EXISTS QiuShiBaiKe (
             name  CHAR(512) NOT NULL,
             content  CHAR(4096))"""

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        try:
            self.db = pymysql.connect("localhost", "yanbober", "19900322", "database_yan_php")
            #self.db.set_charset('utf8')
            self.cursor = self.db.cursor()
            self.cursor.execute(DbManager.sql_create_table)
        except Exception as e:
            print(str(e))

    def close(self):
        try:
            if self.db is not None:
                self.db.close()
            if self.db is not None:
                self.cursor.close()
        except BaseException as e:
            Tools.log("#ERROR# DbManager close failed."+str(e))

    def insertDict(self, dict_data=None):
        if dict_data is None:
            return False
        sql = "INSERT INTO QiuShiBaiKe(name, content) VALUES ("+dict_data["name"]+","+dict_data["content"]+")"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        return True