'''
Created on 14-Feb-2014
hellop
@author: Abhimanyu
'''


auth_actions = {"deploy", "rollback", "update"}

import argparse
import sys
import time
import sched

import Authorization
import Install
import Rollback
from utilities import FatalError


PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"

def authorize():
    '''
    Authorizes user based on OS login username and password.
    The username is then used to mark the user against the action in log entries.
    '''
    username = Authorization.verify()
    if username:
        print "Access granted."
        return username
    else:
        sys.exit()

arguments = argparse.ArgumentParser(description="An application deployment system.")
arguments.add_argument("action", help="deploy/update/rollback")
arguments.add_argument("app_name", help="Name of the app to be deployed.")
arguments.add_argument("version", help="Version tag of the codebase from where the app is to be checked out.")
arguments.add_argument("-s", "--silent", action="store_true", 
                       help="Turns silent mode on. After authorization, AlphaInstaller works without any interruption."\
                        "All questions that are otherwise asked are now automatically answered using the default responses "\
                        "stored in the settings XML.")
arguments.add_argument("-t", "--time", default="0", help="")
args = arguments.parse_args()

try: 
    assert args.action in auth_actions
except AssertionError:
    print "%s is not a recognized command. Please refer the documentation by using the '--help' argument." % args.action
    sys.exit()
try:
    float(args.time)
except ValueError:
    print "%s is not a valid number. For documentation, use '--help' argument." % args.time
    sys.exit()
    
print "Initiating %s procedure..." % (args.action.upper())

session = {"app_name" : args.app_name, "version" : args.version, "action" : args.action, "silent" : args.silent, "time" : args.time}
s = sched.scheduler(time.time, time.sleep)

'''
Calling module based on the action provided as command line argument.
'''
try:
    session["username"] = authorize()
    if args.action == "deploy" or args.action == "update":
        s.enter(float(args.time)*1, 1, Install.ignite, (session,))
        s.run()
    elif args.action == "rollback":
        Rollback.ignite()
            
    else:
        print "%s is not a valid action." % (args.action)
except FatalError as FE:
    print "ERROR:: " + FE.message
except KeyboardInterrupt:
    print "\nAlphainstaller forced to shut down."
    