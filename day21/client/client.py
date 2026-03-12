from socket import *
import os
import sys
import struct
def send_file_name(client,file_name):
    file_name = file_name.encode("utf8")
    file_name_len = struct.pack("I",len(file_name))
    client.send(file_name_len + file_name)
def recv_file_size_all(client:socket):
    size = struct.unpack("I",client.recv(4))[0]

    return size
def circle_recv_file_and_write(client:socket,file_name,file_size):
    total = 0
    f = open(file_name,"wb")
    while total < file_size:
        data = client.recv(1000)
        total += len(data)
        f.write(data)
    f.close()

if __name__ == '__main__':
    # 创建用户并连接服务器
    client = socket(AF_INET,SOCK_STREAM)
    addr =("172.20.10.5",3440)
    client.connect(addr)

    #文件名
    # file_name = sys.argv[1]
    file_name = "aatext.mp4"
    send_file_name(client,file_name)

    #接收文件总大小 单位：字节
    file_size = recv_file_size_all(client)
    #循环接收并写入
    circle_recv_file_and_write(client,file_name,file_size)

    client.close()


