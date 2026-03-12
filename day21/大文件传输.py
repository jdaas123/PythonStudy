from socket import *
import struct
import os

def read_file_name(s:socket):
    file_name_len =struct.unpack("I",s.recv(4))[0]
    file_name = s.recv(file_name_len).decode("utf8")
    return file_name

def send_file_size_all(s,file_name):
    file_size = os.stat(file_name).st_size
    file_size_bytes_len = struct.pack("I",file_size)
    s.send(file_size_bytes_len)

def circle_send_file(s,file_name):
    f = open(file_name,"rb")
    while True:
        data = f.read(1000)
        if data:
            s.send(data)
        else:
            break
    f.close()

if __name__ == '__main__':
    s = socket(AF_INET,SOCK_STREAM)
    #定义ip 和 端口
    addr = ("",3440)
    #绑定
    s.bind(addr)

    s.listen(128)
    new_client,client_addr = s.accept()
    print("连接成功，用户ip,port:",client_addr)

    #####传输文件
    #接收要传输的文件名
    file_name = read_file_name(new_client)

    #计算文件大小并发送
    send_file_size_all(new_client,file_name)

    #循环发送文件
    circle_send_file(new_client,file_name)

    new_client.close()
    s.close()




