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
Response_code ={    '000':'Login failed',
'001':'Login succes',
'002':'Account already login',
'003':'',
'004':''}#share with srv