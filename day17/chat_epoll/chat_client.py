import socket
import select
import sys

def chat_client():
    if len(sys.argv) == 1:
        return
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    addr = (sys.argv[1],3000)

    client.connect(addr)

    epoll = select.epoll()

    epoll.register(client.fileno(),select.EPOLLIN)
    epoll.register(sys.stdin.fileno(),select.EPOLLIN)

    while True:
        events = epoll.poll(-1)
        for fd,event in events:
            if fd == client.fileno():
                rdata = client.recv(1000)
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



if __name__ == "__main__":


    chat_client()