'''
Created on 11-Mar-2014

@author: Abhimanyu
'''
import pam
from getpass import getpass

import utilities


def verify():
    '''
    Verifies username and password. Returns the username for logging purposes, if access is granted.
    '''
    while True:
        print "Username: ",
        username = raw_input()
        password = getpass()
        if(pam.authenticate(username, password)):
            return username
        else:
            if not utilities.yes_or_no("Invalid username or password. Do you want to try again?", "y"):
                break

    return False
