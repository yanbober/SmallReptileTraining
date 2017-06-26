'''
Python3 MySQL数据库持久化演示
'''
import pymysql


class MySQLPersistence(object):
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        try:
            self.db = pymysql.connect("localhost", "yanbober", "TQJJtaJWNbGAMU44", "database_yan_php")
            self.db.set_charset('utf8')
            self.cursor = self.db.cursor()

            sql_create_table = """CREATE TABLE IF NOT EXISTS `StudentTable` (
                                    `id` int(11) NOT NULL AUTO_INCREMENT,
                                    `name` varchar(512) COLLATE utf8_bin NOT NULL,
                                    `content` TEXT COLLATE utf8_bin NOT NULL,
                                    PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                                    AUTO_INCREMENT=1"""
            self.cursor.execute(sql_create_table)
        except Exception as e:
            print("mysql connect failed." + str(e))

    def close(self):
        try:
            if self.db is not None:
                self.db.close()
            if self.cursor is not None:
                self.cursor.close()
        except BaseException as e:
            print("mysql close failed."+str(e))

    def insert_table_dict(self, dict_data=None):
        if self.db is None or self.cursor is None:
            print('Please ensure you have connected to mysql server!')
            return False
        if dict_data is None:
            return False
        try:
            cols = ', '.join(dict_data.keys())
            values = '"," '.join(dict_data.values())
            sql_insert = "INSERT INTO `StudentTable`(%s) VALUES (%s)" % (cols, '"'+values+'"')
            self.cursor.execute(sql_insert)
            self.db.commit()
        except BaseException as e:
            self.db.rollback()
            print("mysql insert error." + str(e))
        return True

    def get_dict_by_name(self, name=None):
        if self.db is None or self.cursor is None:
            print('Please ensure you have connected to mysql server!')
            return None
        if name is None:
            sql_select_table = "SELECT * FROM `StudentTable`"
        else:
            sql_select_table = "SELECT * FROM `StudentTable` WHERE name=%s" % ('"'+name+'"')
        self.cursor.execute(sql_select_table)
        ret_list = list()
        for item in self.cursor.fetchall():
            ret_list.append({'id': item[0], 'name': item[1], 'content': item[2]})
        return ret_list

if __name__ == '__main__':
    t_mysql = MySQLPersistence()
    t_mysql.connect()
    t_mysql.insert_table_dict({'name': 'Test1', 'content': 'XXXXXXXXXXXXX'})
    t_mysql.insert_table_dict({'name': 'Test2', 'content': 'vvvvvvvvvvvv'})
    t_mysql.insert_table_dict({'name': 'Test3', 'content': 'qqqqqqqqqqqq'})
    t_mysql.insert_table_dict({'name': 'Test4', 'content': 'wwwwwwwwwwwww'})
    print('MySQLPersistence get Test2: ' + str(t_mysql.get_dict_by_name('Test2')))
    print('MySQLPersistence get All: ' + str(t_mysql.get_dict_by_name()))
    t_mysql.close()