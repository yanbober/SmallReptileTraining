import pymysql
from QiuBaiSpider.tools import Tools


class DbManager(object):
    sql_create_table = """CREATE TABLE IF NOT EXISTS `QiuShiBaiKe` (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `name` varchar(512) COLLATE utf8_bin NOT NULL,
                                `content` TEXT COLLATE utf8_bin NOT NULL,
                                PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                            AUTO_INCREMENT=1"""

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        try:
            self.db = pymysql.connect("localhost", "yanbober", "XXXXXX", "database_yan_php")
            self.db.set_charset('utf8')
            self.cursor = self.db.cursor()
            self.cursor.execute(DbManager.sql_create_table)
        except Exception as e:
            Tools.log("#ERROR# DbManager connect failed." + str(e))

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
        try:
            cols = ', '.join(dict_data.keys())
            values = '"," '.join(dict_data.values())
            sql_insert = "INSERT INTO `QiuShiBaiKe`(%s) VALUES (%s)" % (cols, '"'+values+'"')
            self.cursor.execute(sql_insert)
            self.db.commit()
        except BaseException as e:
            self.db.rollback()
            Tools.log("#ERROR# DbManager insert error." + str(e))
        return True