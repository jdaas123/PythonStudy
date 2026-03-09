import socket
import select
import sys


def chat_server():

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    addr = ("",3000)

    s.bind(addr)

    s.listen(128)

    epoll = select.epoll()

    client,client_addr = s.accpet()
    epoll.register(client.fileno(),select.EPOLLIN)
    epoll.register(sys.stdin.fileno(),select.EPOLLIN)

    while True:
        events = epoll.poll(-1)#注意，返回值是一个元组，即(sys.stdin.fileno(),select.EPOLLIN)
        for fd,event in events:
            if fd == client.fileno():
                rdata = client.recv(1000)#如果断开连接了，recv不会卡住，而是返回空
                if rdata:
                    print(rdata.decode("utf8"))
                else:
                    print("对方已断开连接")
                    return
            if fd == sys.stdin.fileno():
                try:
                    wdata = input()
                except EOFError:
                    exit()
                client.send(wdata.encode("utf8"))

    client.close()
    s.close()


if __name__ == "__main__":
    chat_server()