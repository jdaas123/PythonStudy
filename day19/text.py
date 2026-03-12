from multiprocessing import Process
import time
import os
from multiprocessing import Queue
from multiprocessing import Pool,Manager

def write(q):

    for i in ["a","b","c"]:
        print(f"我是进程{os.getpid()},我写入queue->{i}")
        q.put(i)
        time.sleep(1)

def read(q:Queue):
    while True:
        if not q.empty():
            data = q.get()
            print(f"我是进程{os.getpid()},我拿出queue->{data}")
            time.sleep(2)

def run():
    while True:
        print(f"我是进程{os.getpid()}")
        time.sleep(2)

if __name__ == '__main__':
    po = Pool(3)
    for i in range(10):
        po.apply_async(run)
    po.close()
    po.join()
