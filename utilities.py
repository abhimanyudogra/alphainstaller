'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import os


class FatalError(Exception):
    ''' Exception class for errors that force the application to terminate.
    '''
    def __init__(self, message):
        Exception.__init__(self, message)

class Lock():
    def __init__(self, ip, app_name):
        self._path = os.path.join("Locks", os.path.join(ip))
        self.app_name = app_name
    
    def check_lock(self):
        if os.path.exists(self._path):
            _file = open(self._path, "r")
            for line in _file:
                if line == "%s\n" % self.app_name:
                    _file.close()
                    return True          
        return False
    
    def create_lock(self):
        _dir = os.path.dirname(self._path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
            
        _file = open(self._path, "a")
        _file.write("%s\n" % self.app_name)
        _file.close()
    
    def unlock(self):
        _file = open(self._path, "r")
        locks = _file.readlines()
        _file.close()
        _file = open(self._path, "w")
        for lock in locks:
            if lock != "%s\n" % self.app_name:
                _file.write(lock)
        _file.close()


def yes_or_no(question, default):
    '''
    Returns True if user answers Y and False if user answers N
    '''
    while True:
        print "%s (y/n) : (default answer is '%s')" % (question, default)
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