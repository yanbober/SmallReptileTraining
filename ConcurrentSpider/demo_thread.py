import _thread
import time
'''
Python 3.X _thread 模块演示 Demo
当注释掉 self.lock.acquire() 和 self.lock.release() 后运行代码会发现最后的 count 为 467195 等，并发问题。
当保留 self.lock.acquire() 和 self.lock.release() 后运行代码会发现最后的 count 为 1000000，锁机制保证了并发。
time.sleep(5) 就是为了解决 _thread 模块的诟病，注释掉的话子线程没机会执行了
'''


class ThreadTest(object):
    def __init__(self):
        self.count = 0
        self.lock = None

    def runnable(self):
        self.lock.acquire()
        print('thread ident is '+str(_thread.get_ident())+', lock acquired!')
        for i in range(0, 100000):
            self.count += 1
        print('thread ident is ' + str(_thread.get_ident()) + ', pre lock release!')
        self.lock.release()

    def test(self):
        self.lock = _thread.allocate_lock()
        for i in range(0, 10):
            _thread.start_new_thread(self.runnable, ())


if __name__ == '__main__':
    test = ThreadTest()
    test.test()
    print('thread is running...')
    time.sleep(5)
    print('test finish, count is:' + str(test.count))