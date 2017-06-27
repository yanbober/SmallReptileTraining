import pymongo
'''
Python3 MongoDB数据库持久化演示
'''


class MongoDBPersistence(object):
    def __init__(self):
        self.conn = None
        self.database = None

    def connect(self, database):
        try:
            self.conn = pymongo.MongoClient('mongodb://localhost:27017/')
            self.database = self.conn[database]
        except Exception as e:
            print("MongoDB connect failed." + str(e))

    def close(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except BaseException as e:
            print("MongoDB close failed."+str(e))

    def insert_table_dict(self, dict_data=None):
        if self.conn is None or self.database is None:
            print('Please ensure you have connected to MongoDB server!')
            return False
        if dict_data is None:
            return False
        try:
            collection = self.database['DemoTable']
            collection.save(dict_data)
        except BaseException as e:
            print("MongoDB insert error." + str(e))
        return True

    def get_dict_by_name(self, name=None):
        if self.conn is None or self.database is None:
            print('Please ensure you have connected to MongoDB server!')
            return None
        collection = self.database['DemoTable']
        if name is None:
            documents = collection.find()
        else:
            documents = collection.find({"name": name})
        document_list = list()
        for document in documents:
            document_list.append(document)
        return document_list


if __name__ == '__main__':
    t_mysql = MongoDBPersistence()
    t_mysql.connect("DemoDatabase")
    t_mysql.insert_table_dict({'name': 'Test1', 'content': 'XXXXXXXXXXXXX'})
    t_mysql.insert_table_dict({'name': 'Test2', 'content': 'vvvvvvvvvvvv'})
    t_mysql.insert_table_dict({'name': 'Test3', 'content': 'qqqqqqqqqqqq'})
    t_mysql.insert_table_dict({'name': 'Test4', 'content': 'wwwwwwwwwwwww'})
    print('MongoDBPersistence get Test2: ' + str(t_mysql.get_dict_by_name('Test2')))
    print('MongoDBPersistence get All: ' + str(t_mysql.get_dict_by_name()))
    t_mysql.close()