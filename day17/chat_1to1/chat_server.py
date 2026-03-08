import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

addr = ("192.168.57.72",4000)

#绑定

s.bind(addr)
s.listen(128)
client,client_addr = s.accept()
print(client_addr)
while True:
    # 服务器先输入
    sdata = input()
    client.send(sdata.encode("utf8"))
    rdata = client.recv(1000)
    print(rdata.decode("utf8"))

client.close()
s.close()