from config import * #import setting
from git import Repo
from utils.logger import *

def git_push_server_address():
    try:
        repo = Repo(GIT_REPO)
        # commit change
        repo.git.add(GIT_FILE)
        repo.index.commit(GIT_COMMIT)
        # push
        origin = repo.remote(name="origin")
        pushinfo = origin.push()[0]
        if pushinfo:
            log('Git auto update log: ' + str(pushinfo.summary),func ='git-Push')
            return True
    except Exception as e:
        log('Unknown error: ' + str(e),func ='git-Push')
        return False   
'''
if __name__ == '__main__': 
    git_push_server_address()
'''