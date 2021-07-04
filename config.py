from pathlib import Path

#change value to enable/disable debug
isDebug = 1

#public srv info path
cur_dir = str(Path('.').absolute())
info_path = cur_dir + '\\info.txt'

#local srv info
srv_host = '127.0.0.1'
srv_port = 4444

#ngrok var
path_to_ngrok = "C:\\Users\\nct28\\Desktop\\Shared\\tools\\ngrok.exe" # need to be change when clone
open_shell_cmd = 'start cmd.exe /K'

ngrok_type = 'tcp'
ngrok_port = srv_port
ngrok_local = 'http://127.0.0.1:4040'

#for .git auto commit 
GIT_REPO = cur_dir + '\\.git'  # make sure .git folder is properly configured
GIT_FILE = 'info.txt'
GIT_COMMIT = 'Auto update srv address'


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

BANNER =''' 
 .d8888b.  888                                               
d88P  Y88b 888                                               
888    888 888                                               
888        888                                               
888        888                                               
888    888 888                                               
Y88b  d88P 888                                               
 "Y8888P"  88888888                                          
                                                             
                                                             
                                                             
     888                .d8888b.         d8888 888b     d888 
     888               d88P  Y88b       d88888 8888b   d8888 
     888               888    888      d88P888 88888b.d88888 
 .d88888  .d88b.       888            d88P 888 888Y88888P888 
d88" 888 d8P  Y8b      888  88888    d88P  888 888 Y888P 888 
888  888 88888888      888    888   d88P   888 888  Y8P  888 
Y88b 888 Y8b.          Y88b  d88P  d8888888888 888   "   888 
 "Y88888  "Y8888        "Y8888P88 d88P     888 888       888                                                              
                                                             
                                            --by Tsu--
'''