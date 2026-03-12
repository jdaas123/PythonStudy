import threading
import time
# def saySorry():
#     print("sorry")
#     time.sleep(1)

#
# if __name__ == '__main__':
#     for i in range(5):
#         # saySorry()
#         t = threading.Thread(target=saySorry)
#         t.start()


# mutex = threading.Lock()
# num = 0
# def child1():
#     global num
#     for i in range(100000000):
#         mutex.acquire()
#         num += 1
#         mutex.release()
#     print(num)
#
#
# def child2():
#     global num
#     for i in range(100000000):
#         mutex.acquire()
#         num += 1
#         mutex.release()
#     print(num)
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target=child1)
#     t2 = threading.Thread(target=child2)
#
#     t1.start()
#     t2.start()
#     print("进程数量%d" % len(threading.enumerate()))


from collections.abc import Iterable

# print(isinstance([1,2],Iterable))

class MyList():
    def __init__(self):
        self.content = []

    def add(self,num):
        self.content.append(num)

    def __iter__(self):
        my = MyIterator(self)
        return my


class MyIterator():
    def __init__(self,mylist:MyList):
        self.mylist = mylist
        self.count = 0

    def __iter__(self):
        return self
    def __next__(self):
        if self.count < len(self.mylist.content):
            temp = self.count
            self.count += 1
            return self.mylist.content[temp]
        else:
            raise StopIteration



if __name__ == '__main__':
    ss = MyList()
    ss.add(1)
    ss.add(2)
    ss.add(3)
    ss.add(4)
    for i in ss:
        print(i)



