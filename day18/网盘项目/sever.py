

from socket import *
import struct
import os
class Sever:
    def __init__(self,ip,port):
        self.s_listen:socket = None # 用来listen的socket对象
        self.ip = ip
        self.port = port

    def tcp_init(self):
        self.s_listen = socket(AF_INET,SOCK_STREAM)
        self.s_listen.bind((self.ip,self.port))
        self.s_listen.listen(128)

    def task(self):
        """
        处理用户发来的命令
        :return:
        """
        new_client,_ =self.s_listen.accept()
        user = User(new_client)
        user.deal_command()




class User:
    def __init__(self,new_client):
        self.new_client:socket = new_client
        self.user_name = None
        self.path = os.getcwd() #存储连上的用户路径
    def deal_command(self):
        while True:
            data = self.recv_train().decode("utf8")
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
        train_head_len = struct.unpack("I",self.new_client.recv(4))[0]
        return self.new_client.recv(train_head_len)
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

    def do_gets(self, command):
        pass

    def do_puts(self, command):
        pass
if __name__ == '__main__':
    s = Sever("",3000)
    s.tcp_init()
    s.task()
