
from multiprocessing.pool import Pool
from socket import *
import struct
import os
import sys
import select
class Sever:
    def __init__(self,ip,port):
        self.s_listen:socket = None # 用来listen的socket对象
        self.ip = ip
        self.port = port
        self.sever_manage = {}

    def tcp_init(self):
        self.s_listen = socket(AF_INET,SOCK_STREAM)
        self.s_listen.bind((self.ip,self.port))
        self.s_listen.listen(128)

    #建立tcp连接，一个客户端，
    def tcp_connect(self,epoll:select.epoll,pool:Pool):
        """
        建立tcp连接，并且判断是用户名还是token
        用户名：accept + 返回token，并且监视
        token：调用其他函数
        :return:
        """
        #建立accept并且接收data : 可能为用户名或token
        new_client,new_client_address = self.s_listen.accept()
        data_len = struct.unpack("I",new_client.recv(4))[0]
        data = new_client.recv(data_len).decode("utf8")
        #判断是用户名还是token
        if len(data) < 20: #得到用户名
            """
            用户名要求小于20个字节。
            """
            #接收密码
            passport_len = struct.unpack("I", new_client.recv(4))[0]
            passport = new_client.recv(data_len).decode("utf8")
            #生成token
            token = data  + "aaaabbbbccccddddffffeeee"
            token_bytes = token.encode("utf8")
            #发送token
            train_head_bytes = struct.pack("I", len(token_bytes))
            new_client.send(train_head_bytes + token_bytes)
            #监控new_client
            epoll.register(new_client.fileno(),select.EPOLLIN)
            #创建user对象
            user = User(new_client)
            user.user_name = data
            user.user_passport = passport
            self.sever_manage[new_client.fileno()] = user
            print(f"连接user_name：{user.user_name},密码：{user.user_passport}")
        else:
            """
            如果发来的是token
            """
            pool.apply_async(self.task_transform,(new_client,))


    def task(self,fd,epoll):
        """
        处理用户发来的命令
        :return:
        """
        self.sever_manage[fd].deal_command(epoll)

    def task_transform(self,new_client):
        """
        处理传输文件等任务
        :param new_client:
        :return:
        """
        user = User(new_client)
        command = user.recv_train().decode("utf8")
        #得到文件名
        file_name = command[5:]
        command = command[:4]
        if command == "puts":
            print("puts")
        else:
            print("gets")



class User:
    def __init__(self,new_client):
        self.new_client:socket = new_client
        self.user_name = ""
        self.user_passport = ""
        self.path = os.getcwd() #存储连上的用户路径
    def deal_command(self,epoll:select.epoll):
        # while True:
        data = self.recv_train()
        if not data:
            epoll.unregister(self.new_client.fileno())
            print(f"{self.user_name} 已退出连接")
        else:
            data = data.decode("utf8")
            if data[:2] == "ls":
                self.do_ls()
            elif data[:2] == "cd":
                self.do_cd(data)
            elif data[:3] == "pwd":
                self.do_pwd()
            elif data[:2] == "rm":
                self.do_rm()
            elif data[:4] == "gets":
                self.do_gets()
            elif data[:4] == "puts":
                self.do_puts()
            else:
                self.send_train("Error comments".encode("utf8"))
    def send_train(self,send_bytes):#send_bytes 是字节流
        """
        send火车，就是把某个字节流内容以火车形式发过去
        :param send_bytes:
        :return:
        """
        train_head_bytes = struct.pack("I",len(send_bytes))
        self.new_client.send(train_head_bytes + send_bytes)
    def recv_train(self):
        """
        recv 火车，就是把火车recv的内容返回回去
        :return:字节流
        """
        data = self.new_client.recv(4)
        if data:
            train_head_len = struct.unpack("I",data)[0]
            return self.new_client.recv(train_head_len)
        else:
            return None
    def do_ls(self):
        list_dir = os.listdir(self.path)
        data = ""
        for i in list_dir:
            data += i + " " * 5 + str(os.stat(i).st_size) + "\n"
        self.send_train(data.encode("utf8"))
    def do_cd(self,comment):
        dir_name = comment.split()[1]
        os.chdir(dir_name)
        self.path = os.getcwd()
        self.send_train(self.path.encode("utf8")) #给客户显示更新后的路径
    def do_pwd(self):
        self.send_train(self.path.encode("utf8"))

    def do_rm(self, command):
        pass

    def do_gets(self):
        pass

    def do_puts(self):
        pass
if __name__ == '__main__':
    s = Sever("",3000)
    epoll = select.epoll()
    pool = Pool(3)

    s.tcp_init()
    # s.tcp_connect(epoll)
    epoll.register(s.s_listen.fileno(),select.EPOLLIN)

    while True:
        events = epoll.poll(-1)
        for fd,_ in events:
            if fd == s.s_listen.fileno():
                """
                如果是s的缓冲区有数据，则代表有连接请求，进入连接请求。
                """
                s.tcp_connect(epoll,pool)
            else:
                """
                其他客户发来命令
                """
                s.task(fd,epoll)

    # s.task()
    # pool.close()
    # pool.join()
    # epoll.close()
