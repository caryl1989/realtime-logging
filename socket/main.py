import socket
import threading
import sys
import os
import time


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/test_uds")
    msg = 'how are you'
    sock.sendall(msg.encode(encoding='utf_8'))

    while True:
        data = sock.recv(100)
        print("receive ", data.decode(encoding='utf_8'))
        time.sleep(2)
        sock.sendall(msg.encode(encoding='utf_8'))

