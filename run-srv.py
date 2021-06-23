from config import * #import setting
from ngrok import open_ngrok,close_ngrok
from utils.logger import *

try:
    open_ngrok()
except Exception as ex :
    log(ex, 'main-head')

import socket
import os
from _thread import *

ServerSocket = socket.socket()


host = srv_host
port = srv_port
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Tsu de server <3'))
    while True:
        data = connection.recv(2048)
        reply = 'Server re: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

