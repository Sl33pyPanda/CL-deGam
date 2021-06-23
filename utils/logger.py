#by ThanhNC
import os

from datetime import *


def write(result, mode = 'a'):
    today = date.today() 
    logfile = 'logs\\' + today.strftime("%d-%b") + '.log'
    try:
        f = open(logfile, mode)
        f.close()
    except Exception as e :
        if "No such file or directory" in str(e):
            os.mkdir('logs')
       
    f = open(logfile, mode)
    for line in result:
        f.write(line + "\n")
    f.close()
def log(event, func ,site = "", subFunc = ""):
    now = str(datetime.now()) + ' ' + site + ' at ' + str(func)  + str(subFunc) + ' '
    lines = list(map(lambda x : now + x,list(str(event).split('\n'))))
    write(lines)
