'''
Python3 sqlite3数据库持久化演示
'''
import sqlite3


class Sqlite3Persistence(object):
    def __init__(self):
        self.db = None

    def connect(self):
        try:
            self.db = sqlite3.connect("Sqlite3Persistence.db")
            sql_create_table = """CREATE TABLE IF NOT EXISTS `DemoTable` (
                                    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                                    `name` CHAR(512) NOT NULL,
                                    `content` TEXT NOT NULL)"""
            self.db.execute(sql_create_table)
        except Exception as e:
            print("sqlite3 connect failed." + str(e))

    def close(self):
        try:
            if self.db is not None:
                self.db.close()
        except BaseException as e:
            print("sqlite3 close failed."+str(e))

    def insert_table_dict(self, dict_data=None):
        if dict_data is None:
            return False
        try:
            cols = ', '.join(dict_data.keys())
            values = '"," '.join(dict_data.values())
            sql_insert = "INSERT INTO `DemoTable`(%s) VALUES (%s)" % (cols, '"'+values+'"')
            self.db.execute(sql_insert)
            self.db.commit()
        except BaseException as e:
            self.db.rollback()
            print("sqlite3 insert error." + str(e))
        return True

    def get_dict_by_name(self, name=None):
        if name is None:
            sql_select_table = "SELECT * FROM `DemoTable`"
        else:
            sql_select_table = "SELECT * FROM `DemoTable` WHERE name==%s" % ('"'+name+'"')
        cursor = self.db.execute(sql_select_table)
        ret_list = list()
        for row in cursor:
            ret_list.append({'id': row[0], 'name': row[1], 'content': row[2]})
        return ret_list


if __name__ == '__main__':
    t_sqlite3 = Sqlite3Persistence()
    t_sqlite3.connect()
    t_sqlite3.insert_table_dict({'name': 'Test1', 'content': 'XXXXXXXXXXXXX'})
    t_sqlite3.insert_table_dict({'name': 'Test2', 'content': 'vvvvvvvvvvvv'})
    t_sqlite3.insert_table_dict({'name': 'Test3', 'content': 'qqqqqqqqqqqq'})
    t_sqlite3.insert_table_dict({'name': 'Test4', 'content': 'wwwwwwwwwwwww'})
    print('Sqlite3Persistence get Test2: ' + str(t_sqlite3.get_dict_by_name('Test2')))
    print('Sqlite3Persistence get All: ' + str(t_sqlite3.get_dict_by_name()))