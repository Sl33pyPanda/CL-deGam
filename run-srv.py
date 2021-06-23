from config import * #import setting

from ngrok import open_ngrok,close_ngrok

from utils.logger import *

p = open_ngrok()
close_ngrok(p)