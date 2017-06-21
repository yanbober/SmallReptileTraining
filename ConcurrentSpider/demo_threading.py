import threading
from threading import Thread
import time
'''
Python 3.X threading 模块演示 Demo

threading 的 Thread 类基本使用方式（继承重写 run 方法及直接传递方法）
'''


class NormalThread(Thread):
    '''
    重写类比 Java 的 Runnable 中 run 方法方式
    '''
    def __init__(self, name=None):
        Thread.__init__(self, name=name)
        self.counter = 0

    def run(self):
        print(self.getName() + ' thread is start!')
        self.do_customer_things()
        print(self.getName() + ' thread is end!')

    def do_customer_things(self):
        while self.counter < 10:
            time.sleep(1)
            print('do customer things counter is:'+str(self.counter))
            self.counter += 1


def loop_runner(max_counter=5):
    '''
    直接被 Thread 调用方式
    '''
    print(threading.current_thread().getName() + " thread is start!")
    cur_counter = 0
    while cur_counter < max_counter:
        time.sleep(1)
        print('loop runner current counter is:' + str(cur_counter))
        cur_counter += 1
    print(threading.current_thread().getName() + " thread is end!")


if __name__ == '__main__':
    print(threading.current_thread().getName() + " thread is start!")

    normal_thread = NormalThread("Normal Thread")
    normal_thread.start()

    loop_thread = Thread(target=loop_runner, args=(10,), name='LOOP THREAD')
    loop_thread.start()

    loop_thread.join()
    normal_thread.join()

    print(threading.current_thread().getName() + " thread is end!")