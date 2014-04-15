'''
Created on 11-Mar-2014

@author: Abhimanyu
'''
import pam
import utilities
from getpass import getpass

def verify():
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
