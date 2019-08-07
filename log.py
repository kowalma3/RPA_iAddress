#LOG

import time
from datetime import datetime

wasProcessed = './log_wasProcessed.txt' #date:ticket_nr:sys_id:action
today = datetime.today().strftime('%Y-%m-%d')
#LOGS=''

def add_log(log):
    with open(wasProcessed,'a') as file:
        file.write(today+':'+log+'\n')


def exists(sys_id):
    #if LOGS=='':
    with open(wasProcessed,'r') as file:
        logs = file.read()
        #LOGS=f1

    if sys_id in logs:
        return True
    else:
        return False
