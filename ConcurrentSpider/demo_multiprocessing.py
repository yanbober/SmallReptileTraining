import multiprocessing
import time
from multiprocessing import Process
'''
Python 3.X multiprocess 模块演示 Demo

其实完全类似 threading 用法，只不过含义和实质不同而已
multiprocess 的 Process 类基本使用方式（继承重写 run 方法及直接传递方法）
'''


class NormalProcess(Process):
    def __init__(self, name=None):
        Process.__init__(self, name=name)
        self.counter = 0

    def run(self):
        print(self.name + ' process is start!')
        self.do_customer_things()
        print(self.name + ' process is end!')

    def do_customer_things(self):
        while self.counter < 10:
            time.sleep(1)
            print('do customer things counter is:'+str(self.counter))
            self.counter += 1


def loop_runner(max_counter=5):
    print(multiprocessing.current_process().name + " process is start!")
    cur_counter = 0
    while cur_counter < max_counter:
        time.sleep(1)
        print('loop runner current counter is:' + str(cur_counter))
        cur_counter += 1
    print(multiprocessing.current_process().name + " process is end!")


if __name__ == '__main__':
    print(multiprocessing.current_process().name + " process is start!")
    print("cpu count:"+str(multiprocessing.cpu_count())+", active chiled count:"+str(len(multiprocessing.active_children())))
    normal_process = NormalProcess("NORMAL PROCESS")
    normal_process.start()

    loop_process = Process(target=loop_runner, args=(10,), name='LOOP PROCESS')
    loop_process.start()

    print("cpu count:" + str(multiprocessing.cpu_count()) + ", active chiled count:" + str(len(multiprocessing.active_children())))
    normal_process.join()
    loop_process.join()
    print(multiprocessing.current_process().name + " process is end!")