'''
Created on 11-Mar-2014

@author: Abhimanyu
'''
import pam
from getpass import getpass

def verify():
    tryagain = "y"
    while tryagain == "y":
        print "Username: ",
        username = raw_input()        
        password = getpass()
        if(pam.authenticate(username, password)):
            return username
        else:
            print "Invalid username or password. Do you want to try again? (Press 'y' to continue...): "
            tryagain = raw_input()
        
    return False
