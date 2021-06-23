# FOR WINDOWS
#   Sample use: open_ngrok('tcp', 4444)
from config import * #import setting

import subprocess
import threading
import os
from requests_html import HTMLSession
from gitpush import git_push_server_address

def update_info(info):
    try:
        f = open(info_path, 'a')
        f.write(info + "\n")
        f.close()
        git_push_server_address()
    except Exception as e :
        log(e, 'update_info')   

def open_ngrok(type=ngrok_type, port=ngrok_port):
    session = HTMLSession()
    try:
        r = session.get(ngrok_local)
        r.html.render()
        srv = r.html.find('a')[-1].text
        if srv:
            print('''WARNING: ngrok already running
            This might cause the program Errors!
            Make sure no ngrok tunnel is running on your pc.''')
    except Exception as ex:
        pass

    p = subprocess.Popen('{} "{} {} {}"'.format(open_shell_cmd,path_to_ngrok,type,port), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #getting public srv address
    r = session.get(ngrok_local)
    r.html.render()
    srv = r.html.find('a')[-1].text

    update_info(srv)

    if isDebug:
        print('Ngrok open {} port {}'.format(type, port))
        print('server is at:', srv)        
    return p

def close_ngrok(Popen_proc: subprocess.Popen):
    Popen_proc.kill()
    return True
'''
if __name__ == '__main__':    
    p= open_ngrok(port=8888)
    close_ngrok(p)
'''