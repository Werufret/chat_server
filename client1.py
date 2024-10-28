import socket
import threading

socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socks.connect(("localhost", 12345))

def server_prinatie():
    global socks
    while True:
        data = socks.recv(1024).decode('utf-8')
        if not data:
            break
        print(data)

d=input("Name:",)
thread=threading.Thread(target=server_prinatie,daemon=True)
thread.start()
socks.sendall(f"Name:{d}".encode('utf-8'))
while True:
    d=input()
    socks.sendall(f"message:{d}".encode('utf-8'))


