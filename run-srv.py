from config import * #import setting
from ngrok import open_ngrok,close_ngrok
from utils.logger import *
import hashlib

try:
    open_ngrok()
except Exception as ex :
    log(ex, 'main-head')

import socket
import os
from _thread import *

ServerSocket = socket.socket()
ThreadCount = 0
srv_command = -1
srv_stop = 1 
users = {}

try:
    ServerSocket.bind((srv_host, srv_port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    try:
        global ThreadCount, users
        connection.send(str.encode('Welcome to the Tsu de server <3'))
        user = connection.recv(1024).decode('utf-8')
        hashes = users.keys()
        print(users[user][1])
        if user in hashes:
            if users[user][1] == 0:
                users[user][1] = 1                
                connection.send(str.encode('001 Login success as ' + users[user][0]))
                print('001 Login success as ' + users[user][0])
                while True:
                    data = connection.recv(2048)
                    reply = 'Server re: ' + data.decode('utf-8')
                    if not data:
                        users[user][1] = 0
                        print(users[user][0] + ' Logged out')
                        break
                    connection.sendall(str.encode(reply))
            else: 
                connection.send(str.encode('002 Someone already login as ' + users[user][0]))
                print('002 Someone already login as ' + users[user][0])
        
        ThreadCount-=1
        print('Connection closed on:', connection)
        connection.close()

    except Exception as ex:
        log(ex,'Threaded_Client' + str(connection) )


def srv_listener(): # for threading 
    global srv_command
    global ThreadCount
    while 1:
        if srv_command == srv_stop:
            break
        try:
            Client, address = ServerSocket.accept()
            print('Connected to: ', address)#[0] + ':' + str(address[1]))
            start_new_thread(threaded_client, (Client, ))
            ThreadCount += 1
            print('Thread Count: ' + str(ThreadCount))
        except Exception as ex:
            log(ex, 'Server listener')
            ServerSocket.close()
            print('Server Crashed')
            break


def read_creds(): # only small user allowed
    global users
    try :
        f = open("users.dat", "r")
        lines = f.read().splitlines()
        for line in lines:
            users[hashlib.md5(line.encode()).hexdigest()] = [line, 0, '']
        f.close()
    except Exception as ex:
        log(ex,'read creds')


if __name__ == '__main__':  
    read_creds()
    start_new_thread(srv_listener, ())
    for i in range(10):
        srv_command = int(input('>>> '))