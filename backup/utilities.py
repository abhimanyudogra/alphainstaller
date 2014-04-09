'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

class FatalError(Exception):
    ''' Exception class for errors that force the application to terminate.
    '''
    def __init__(self, message):
        Exception.__init__(self, message)
    
    
