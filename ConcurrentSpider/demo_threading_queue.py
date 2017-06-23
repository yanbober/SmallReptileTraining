from queue import Queue
from random import randint
from threading import Thread
from time import sleep
'''
Python 3.X threading 与 Queue 结合演示 Demo
经典的并发生产消费者模型
'''


class TestQueue(object):
    def __init__(self):
        self.queue = Queue(2)

    def writer(self):
        print('Producter start write to queue.')
        self.queue.put('key', block=1)
        print('Producter write to queue end. size is:'+str(self.queue.qsize()))

    def reader(self):
        value = self.queue.get(block=1)
        print('Consumer read from queue end. size is:'+str(self.queue.qsize()))

    def producter(self):
        for i in range(5):
            self.writer()
            sleep(randint(0, 3))

    def consumer(self):
        for i in range(5):
            self.reader()
            sleep(randint(2, 4))

    def go(self):
        print('TestQueue Start!')
        threads = []
        functions = [self.consumer, self.producter]
        for func in functions:
            thread = Thread(target=func, name=func.__name__)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print('TestQueue Done!')

if __name__ == '__main__':
    TestQueue().go()