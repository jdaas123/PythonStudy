from socket import *
import struct
class Client:
    def __init__(self,ip,port):
        self.client:socket  = None
        self.ip =  ip
        self.port = port
        self.token = None
        self.name = ""
        self.passport = ""
    #初始化client对象，name and passport
    def init_client(self):
        client_name = input("please input client_name:")
        client_passport = input("please input client_passport:")
        self.name = client_name
        self.passport = client_passport

    def tcp_connect(self):
        self.client = socket(AF_INET,SOCK_STREAM)
        # self.client.connect((self.ip,self.port))
        #用户连接之后发送用户名得到token
        self.client.connect((self.ip,self.port))
        #发用户名和密码
        self.send_train(self.name.encode("utf8"))
        self.send_train(self.passport.encode("utf8"))
        #得到token
        self.token = self.recv_train().decode("utf8")
        print(self.token)

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
            try:
                comment = input()
            except EOFError:
                exit()
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

    def do_rm(self):
        pass

    def do_gets(self):
        pass

    def do_puts(self):
        pass


if __name__ == '__main__':
    client = Client("192.168.2.128",3000)
    client.init_client()



    client.tcp_connect()
    client.send_comment()
    client.close()