'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import os
import re

class FatalError(Exception):
    ''' Exception class for errors that force the application to terminate.
    '''
    def __init__(self, message):
        Exception.__init__(self, message)
        


class LogChecker():
    def __init__(self, app_name, version):
        location = os.path.join("Logs", os.path.join(os.path.join(app_name, "v%s"%version), "log"))
        self.log_f = open(location, "r").readlines()
    
    def check_successful_completion(self):
        i=1
        if self.log_f:
            while True:
                actcomp_re = re.compile('^\[ACTION_COMPLETE\]')
                actstrt_re = re.compile('^\[ACTION_BEGIN\]')
                if actcomp_re.search(self.log_f[-i]):
                    return True
                if actstrt_re.search(self.log_f[-i]):
                    return False
                i+=1
        else:
            return True
        
    def get_last_checkpoint(self):
        i=1
        chkpt_re = re.compile('^\[CHECKPOINT::(\d+)\]')
        actstrt_re = re.compile('^\[ACTION_BEGIN\]')
        while True:        
            line = self.log_f[-i]
            latest_checkpoint = chkpt_re.findall(line)
            no_checkpoint = actstrt_re.search(line)
            if latest_checkpoint:
                return latest_checkpoint[0]
            elif no_checkpoint:
                return 0
            i+=1
            
def yes_or_no(question, default):
    while True:
        print "%s (y/n) : (default answer is '%s')" %(question, default)
        response = raw_input()
        if not response and default in {'y', 'Y'}:
            return True
        elif not response and default in {'n', 'N'}:
            return False
        elif response in {"y", "n", "Y", "N"}:
            if response.lower() == "y":
                return True
            else:
                return False
        else:
            print "Invalid response, please try again."
            
               
        
              

    
    
    
    
    
    
    
    
    
