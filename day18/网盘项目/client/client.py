from socket import *
import struct
class Client:
    def __init__(self,ip,port):
        self.client:socket  = None
        self.ip =  ip
        self.port = port
    def tcp_connect(self):
        self.client = socket(AF_INET,SOCK_STREAM)
        self.client.connect((self.ip,self.port))
    def send_train(self,send_bytes):#send_bytes 是字节流
        """
        send火车，就是把某个字节流内容以火车形式发过去
        :param send_bytes:
        :return:
        """
        train_head_bytes = struct.pack("I",len(send_bytes))
        self.client.send(train_head_bytes + send_bytes)
    def recv_train(self):
        """
        recv 火车，就是把火车recv的内容返回回去
        :return:字节流
        """
        train_head_len = struct.unpack("I",self.client.recv(4))[0]
        return self.client.recv(train_head_len)

    def send_comment(self):
        """
        发送各种命令给服务器
        :return:
        """
        while True:
            comment = input()
            self.send_train(comment.encode("utf8"))
            if comment[:2] == "ls":
                self.do_ls()
            elif comment[:2] == "cd":
                self.do_cd()
            elif comment[:3] == "pwd":
                self.do_pwd()
            elif comment[:2] == "rm":
                self.do_rm()
            elif comment[:4] == "gets":
                self.do_gets()
            elif comment[:4] == "puts":
                self.do_puts()
            else:
                print(self.recv_train().decode("utf8"))
    def do_ls(self):
        print(self.recv_train().decode("utf8"))
    def do_cd(self):
        print(self.recv_train().decode("utf8"))
    def do_pwd(self):
        print(self.recv_train().decode("utf8"))

    def do_rm(self, command):
        pass

    def do_gets(self, command):
        pass

    def do_puts(self, command):
        pass


if __name__ == '__main__':
    client = Client("192.168.57.72",3000)
    client.tcp_connect()
    client.send_comment()