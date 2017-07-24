# For cmd running not add to os path, pycharm not need.
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
import codecs
from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager


'''
[分布式调度控制端]

简单主从模式的分布式爬虫，支持多节点管理

简单模拟分布式爬虫调度系统，在一台服务器上启动 NodeManager，然后在多台设备启动 SpiderWork，
这样就是主从模式的分布式爬虫系统，本实例演示了多台机器爬取解析链接然后将爬取解析的深度链接
和数据通过分布式网络回传给调度器，调度器再将爬取的链接进行下发到分布式服务器上同时将爬取的
数据存储在文件。

Ubuntu OSError: [Errno 98] Address already in use
$ sudo netstat -tlnp|grep 8001
tcp 0   0 0.0.0.0:8001  0.0.0.0:*   LISTEN  24314/python3.5 
$ kill -9 24314
'''


class NodeManager(object):
    def __init__(self):
        self.addr_port = ('127.0.0.1', 8001)
        self.url_q = Queue()
        self.result_q = Queue()
        self.store_q = Queue()
        self.conn_q = Queue()

        BaseManager.register('get_task_queue', callable=lambda: self.url_q)
        BaseManager.register('get_result_queue', callable=lambda: self.result_q)
        self.base_manager = BaseManager(address=self.addr_port, authkey=b'baidu-baike-android')

    def _url_manager_proc(self, url_q, conn_q, root_url):
        cur_crawl_count = 1
        url_list = list()
        url_list.append(root_url)
        while True:
            while len(url_list) > 0:
                new_url = url_list.pop()
                url_q.put(new_url)
                print('调度器URL处理进程派发新URL到分布式集群：'+new_url)
                if cur_crawl_count > 1000:  # 模拟爬取1000个链接结束
                    # 调度器多发几个结束指令是因为假设分布式集群个数为4个且均各自独占
                    for try_count in range(4):
                        url_q.put('CMD_END')
                    print('调度器向集群派发爬取结束指令！')
                    return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    for url in urls:
                        url_list.append(url)
                    cur_crawl_count += len(urls)
                    print('调度器URL处理进程接收分布式集群传回的解析页面深度链接个数：'+len(urls))
            except BaseException as e:
                print('url_manager_proc:'+str(e))
                time.sleep(0.1)

    def _result_solve_proc(self, result_q, conn_q, store_q):
        while True:
            try:
                if not result_q.empty():
                    connect = result_q.get(True)
                    if connect['new_urls'] == 'CMD_END':
                        print('调度器结果分析进程接收到结束指令！')
                        store_q.put('CMD_END')
                        return
                    conn_q.put(connect['new_urls'])     # url - set
                    store_q.put(connect['data'])    # data - dict
                else:
                    time.sleep(0.1)
            except BaseException as e:
                print('result_solve_proc:'+str(e))
                time.sleep(0.1)

    def _store_proc(self, store_q):
        filepath = 'output_result.html'
        fout = codecs.open(filepath, 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == 'CMD_END':
                    print('调度器爬虫结果存储进程接收到停止指令！')
                    fout = codecs.open(filepath, 'a', encoding='utf-8')
                    fout.write('</table>')
                    fout.write('</body>')
                    fout.write('</html>')
                    fout.close()
                    return
                print('调度器爬取结果存储进程接收分布式爬取集群传回的解析价值数据！')
                fout = codecs.open(filepath, 'a', encoding='utf-8')
                fout.write('<tr>')
                fout.write('<td>%s</td>' % data['url'])
                fout.write('<td>%s</td>' % data['title'])
                fout.write('<td>%s</td>' % data['summary'])
                fout.write('</tr>')
            else:
                time.sleep(0.1)

    def go(self, seed_url):
        url_manager_proc = Process(target=self._url_manager_proc, args=(self.url_q, self.conn_q, seed_url,))
        result_solve_proc = Process(target=self._result_solve_proc, args=(self.result_q, self.conn_q, self.store_q,))
        store_proc = Process(target=self._store_proc, args=(self.store_q,))
        url_manager_proc.start()
        result_solve_proc.start()
        store_proc.start()
        self.base_manager.get_server().serve_forever()


if __name__ == '__main__':
    root_seed_url = 'http://baike.baidu.com/item/Android'
    NodeManager().go(root_seed_url)
