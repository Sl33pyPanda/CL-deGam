from requests_html import HTMLSession
import socket
import hashlib,time
import json

session = HTMLSession()
r = session.get('https://github.com/Sl33pyPanda/CL-deGam/blob/main/info.txt') # server info

info = r.html.find('table')[0].text.replace('tcp://','')

host = info.split(':')[0]
port = int(info.split(':')[1])

#--------------------------------------------
#return code to client
response_status ={-1:'Unknown',
0:'Login failed',
1:'Login succes',
2:'Account already login',
3:'Logged out',
400:'Bad request',
401:'Unauthorized',
404: 'Nothing found',
500:'Internal server error',
999:'Failed',
1000:'Success'}#share with srv
stop_code = (-1, 0, 2, 3, 401)


def message(id, n=10):
    request = {'action' : 'message',
               'auth_token' : id,
               'data' : ''}
    

    for i in range(n):
        request['data'] = input('Say Something: ')
        ClientSocket.send(json.dumps(request).encode())
        Response = ClientSocket.recv(2048).decode()
        print(Response)
    ClientSocket.close()


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()
#--------------------------------------------

# handle data transfer
def client_handler(rdata, id):  # type raw data <string> rdata
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
                if data['action'] == 'mess':                
                    return client_message(data['data'])            
                else:
                    status_code = 404
            else:
                status_code = 401
    except Exception as ex:
        print(ex)
        status_code = 400

    return {"response_code": status_code, "response": response_status[status_code]}


ClientSocket = socket.socket()
cred = ''

try :
    f = open("login.dat", "r")
    cred = f.read()
    f.close()
except Exception as ex:
    if "No such file or directory: 'login.dat'" in str(ex):
        cred = md5(md5(input('Enter your cred: ')))
        f = open("login.dat", "w")
        f.write(cred)
        f.close()
    else:
        print('Error while authenticate')


print('Connecting to server at:', host, port)
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
Response = ClientSocket.recv(2048).decode()
print(Response) # banner


ClientSocket.send(str.encode(cred))
data = json.loads(ClientSocket.recv(2048).decode())
if data['response_code'] in stop_code:
    print(data['response'])
else:
    print(data)
    id = data['data']['token']  
    message(id)
