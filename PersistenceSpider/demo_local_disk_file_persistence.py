import dbm
import pickle
import shelve
'''
Python3 常用本地磁盘文件型持久化演示
'''

class NormalFilePersistence(object):
    '''
    普通文件持久化或者缓存持久化
    '''
    def save(self, data):
        with open('NormalFilePersistence.txt', 'w') as open_file:
            open_file.write(data)

    def load(self):
        with open('NormalFilePersistence.txt', 'r') as open_file:
            return open_file.read()


class DBMPersistence(object):
    '''
    DBM字符串键值对持久化或者缓存持久化
    '''
    def save(self, key, value):
        try:
            dbm_file = dbm.open('DBMPersistence', 'c')
            dbm_file[key] = str(value)
        finally:
            dbm_file.close()

    def load(self, key):
        try:
            dbm_file = dbm.open('DBMPersistence', 'r')
            if key in dbm_file:
                result = dbm_file[key]
            else:
                result = None
        finally:
            dbm_file.close()
        return result


class PicklePersistence(object):
    '''
     Pickle把复杂对象序列化到文件持久化或者缓存持久化
    '''
    def save(self, obj):
        with open('PicklePersistence', 'wb') as pickle_file:
            pickle.dump(obj, pickle_file)

    def load(self):
        with open('PicklePersistence', 'rb') as pickle_file:
            return pickle.load(pickle_file)


class ShelvePersistence(object):
    '''
    Shelve为DBM和Pickle的结合，以键值对的方式把复杂对象序列化到文件持久化或者缓存持久化
    '''
    def save(self, key, obj):
        try:
            shelve_file = shelve.open('ShelvePersistence')
            shelve_file[key] = obj
        finally:
            shelve_file.close()

    def load(self, key):
        try:
            shelve_file = shelve.open('ShelvePersistence')
            if key in shelve_file:
                result = shelve_file[key]
            else:
                result = None
        finally:
            shelve_file.close()
        return result


if __name__ == '__main__':
    t_normal = NormalFilePersistence()
    t_normal.save('Test NormalFilePersistence')
    print('NormalFilePersistence load: ' + t_normal.load())

    t_dbm = DBMPersistence()
    t_dbm.save('user', 'GJRS')
    t_dbm.save('age', 27)
    print('DBMPersistence load: ' + str(t_dbm.load('user')))
    print('DBMPersistence load: ' + str(t_dbm.load('address')))

    t_pickle = PicklePersistence()
    obj = {'name': 'GJRS', 'age': 27, 'skills':['Android', 'C', 'Python', 'Web']}
    t_pickle.save(obj)
    print('PicklePersistence load: ' + str(t_pickle.load()))

    t_shelve = ShelvePersistence()
    obj1 = {'name': 'WL', 'age': 27, 'skills': ['Test', 'AutoTest']}
    obj2 = {'name': 'GJRS', 'age': 27, 'skills': ['Android', 'C', 'Python', 'Web']}
    t_shelve.save('obj1', obj1)
    t_shelve.save('obj2', obj2)
    print('ShelvePersistence load: ' + str(t_shelve.load('obj1')))
    print('ShelvePersistence load: ' + str(t_shelve.load('objn')))