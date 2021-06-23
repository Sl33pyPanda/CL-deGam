from requests_html import HTMLSession
import socket

session = HTMLSession()
r = session.get('https://github.com/Sl33pyPanda/CL-deGam/blob/main/info.txt') # server info

info = r.html.find('table')[0].text.replace('tcp://','')

host = info.split(':')[0]
port = int(info.split(':')[1])

print(host,port)

#--------------------------------------------
ClientSocket = socket.socket()
print('Connecting to server at:', host, port)
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()