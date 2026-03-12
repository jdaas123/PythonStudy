import socket
import select
import sys


def chat_server():

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    addr = ("",3000)

    s.bind(addr)

    s.listen(128)

    epoll = select.epoll()

    # client,client_addr = s.accpet()
    # epoll.register(client.fileno(),select.EPOLLIN)
    # epoll.register(sys.stdin.fileno(),select.EPOLLIN)
    epoll.register(s.fileno(),select.EPOLLIN)
    epoll.register(sys.stdin.fileno(), select.EPOLLIN)
    client_arr = []
    while True:
        events = epoll.poll(-1)#注意，返回值是一个元组，即(sys.stdin.fileno(),select.EPOLLIN)
        for fd,event in events:
            if fd == s.fileno():
                client,client_addr = s.accept()
                epoll.register(client.fileno(),select.EPOLLIN)
                client_arr.append(client)
            else:
                remove_client = None
                for i in client_arr:

                    if fd == i.fileno():
                        rdata = i.recv(1000)
                        if rdata:
                            for j in client_arr:
                                if j is i:
                                    continue
                                j.send(rdata)
                        else:
                            remove_client = i
                if remove_client:
                    client_arr.remove(remove_client)
                    epoll.unregister(remove_client)
                    remove_client.close()

    client.close()
    s.close()


if __name__ == "__main__":
    chat_server()