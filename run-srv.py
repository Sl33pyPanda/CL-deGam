from config import * #import setting
from ngrok import open_ngrok,close_ngrok
from utils.logger import *
import hashlib, random, secrets
import json

try:
    open_ngrok()
except Exception as ex :
    printlg(ex, 'main-head')

import socket
import os
from _thread import *

ServerSocket = socket.socket()
ThreadCount = 0
srv_command = -1
srv_stop = 1 
users = {}
tokens = {}

try:
    ServerSocket.bind((srv_host, srv_port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


#   Utils
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def random_tokens():
    return md5(secrets.token_bytes(random.randint(20,50)).decode(errors='ignore'))


def client_login(user):
    global users, tokens
    hashes = users.keys()
    if user in hashes:
        if users[user]['logged'] == 0:
            users[user]['logged'] = 1
            id = random_tokens()
            users[user]['token'] = id
            tokens[id] = user
            return id
        else: 
            return 2
    else:
        return 0


def client_logout(id):
    global users, tokens
    if id in tokens:
        try:
            user = tokens[id]
            if users[user]['logged'] == 1:
                users[user]['logged'] = 0
                users[user]['token'] = ''
                tokens.pop(id)
                return 1000
            else: 
                return 999
        except Exception as ex:
            printlg(ex, 'client_logout')
    else:
        return 400


def client_message(id, message): # testing
    ret = {'from': 'Teo', 'To': 'Ti', 'text' : message}
    status_code = 1000
    return {"response_code": status_code, "response": response_status[status_code], 'data' : ret}


#session thing :>
def client_auth(id):
    if id in tokens.keys():
        return 1 
    else:
        return 0


# handle data transfer
def threaded_client_handler(id, rdata):  # type raw data <string> rdata
    status_code = -1
    try:
        # some JSON: rdata =  '{ "name":"John", "age":30, "city":"New York"}'
        if not rdata:
            client_logout(id)
            status_code =3
        else:
            data = json.loads(rdata)            
            if data['auth_token'] == id: # some auth things =))
                #printlg something
                if data['action'] == 'message':                
                    return client_message(id, data['data'])            
                else:
                    status_code = 404
            else:
                status_code = 401    
    except Exception as ex:
        printlg(ex, 'threaded_client_handler')
        status_code = 400

    return {"response_code": status_code, "response": response_status[status_code]}


# handle connection
def threaded_client(connection): 
    global ThreadCount
    try:        
        connection.send(BANNER.encode()) 
        print('sent BANNER - logging in')
        data = connection.recv(1024).decode()
        print(data)
        id = -1
        id = client_login(data)
        print(id)
        if id in stop_code:
            connection.send(json.dumps({"response_code": id, "response": response_status[id]})) 
            ThreadCount-=1
            print('Connection closed on:', connection)
            connection.close()
            return 0        
        connection.send(json.dumps({"response_code": 1,
                                    "response": response_status[1], 
                                    "data": {"token" : id,
                                             "name"  : 'on develop :3 '}}).encode())
        print('start communicate')
        while True:
            data = connection.recv(2048).decode()
            response = threaded_client_handler(id, data)
            if response["response_code"] in stop_code:
                break
            connection.send(json.dumps(response).encode())
        ThreadCount-=1
        print('Connection closed on:', connection)
        connection.close()

    except Exception as ex:
        printlg(ex,'Threaded_Client' + str(connection) )
        print('Connection closed on:', connection)
        ThreadCount-=1


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
            printlg(ex, 'Server listener')
            ServerSocket.close()
            print('Server Crashed')
            break


def read_creds(): # only small user allowed
    global users
    try :
        f = open("users.dat", "r")
        lines = f.read().splitlines()
        for line in lines: # line just a logintokens #insecure T.T
            users[md5(md5(line))] = {'username':'', 'logged': 0, 'token' : ''}
        f.close()
    except Exception as ex:
        printlg(ex,'read creds')


if __name__ == '__main__':  
    read_creds()
    start_new_thread(srv_listener, ())
    for i in range(10):
        srv_command = int(input('>>> '))