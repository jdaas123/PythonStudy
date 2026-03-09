from socket import *
import struct
def trans_file(file_name):
    s = socket(AF_INET,SOCK_STREAM)
    addr = ("172.20.10.5",3000)
    s.bind(addr)
    s.listen(128)
    client,client_addr = s.accept()
    #先发文件名
    file_name_betys = file_name.encode("utf8")
    file_name_len_betys = struct.pack('I',len(file_name_betys))
    client.send(file_name_len_betys + file_name_betys)

    #在发送文件内容
    f = open(file_name,'rb')
    file_content = f.read()
    file_content_len = struct.pack('I',len(file_content))
    client.send(file_content_len + file_content)

    f.close()
    client.close()
    s.close()

if __name__ == "__main__":
    trans_file("woshiwenjian")