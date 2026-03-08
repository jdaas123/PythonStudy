import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

addr =("192.168.57.72",4000)
client.connect(addr)

while True:
    #先收
    rdata = client.recv(1000)
    print(rdata.decode("utf8"))
    sdata = input()
    client.send(sdata.encode("utf8"))
client.close()