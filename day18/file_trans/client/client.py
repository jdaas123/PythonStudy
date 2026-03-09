from socket import *

import struct

client = socket(AF_INET,SOCK_STREAM)

client.connect(("172.20.10.5",3000))

file_name_len = struct.unpack("I",client.recv(4))[0]
file_name = client.recv(file_name_len)

file_content_len = struct.unpack('I',client.recv(4))[0]
file_content = client.recv(file_content_len)

f = open(file_name.decode("utf8"),"wb")
f.write(file_content)

f.close()
client.close()