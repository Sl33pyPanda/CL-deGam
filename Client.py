from requests_html import HTMLSession
import socket
import hashlib,time

session = HTMLSession()
r = session.get('https://github.com/Sl33pyPanda/CL-deGam/blob/main/info.txt') # server info

info = r.html.find('table')[0].text.replace('tcp://','')

host = info.split(':')[0]
port = int(info.split(':')[1])

#--------------------------------------------
Response_code ={    '000':'Login failed',
'001':'Login succes',
'002':'Account already login',
'003':'',
'004':''}#share with srv

def com(n=10):
    for i in range(n):
        Input = input('Say Something: ')
        ClientSocket.send(str.encode(Input))
        Response = ClientSocket.recv(2048)
        print(Response.decode('utf-8'))
    ClientSocket.close()
#--------------------------------------------
ClientSocket = socket.socket()
cred = ''

try :
    f = open("login.dat", "r")
    cred = f.read()
    f.close()
except Exception as ex:
    if "No such file or directory: 'login.dat'" in str(ex):
        cred = hashlib.md5(input('Enter your cred: ').encode()).hexdigest()
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
Response = ClientSocket.recv(1024).decode()
print(Response)

try:
    ClientSocket.send(str.encode(cred))
    Response = ClientSocket.recv(2048).decode()
    print(Response)
    if "001" in Response:
        com()
    elif "002" in Response:
        print('Already logged in')
    else :
        print('exiting')
except Exception as ex:
    print(ex)