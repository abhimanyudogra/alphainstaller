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

import authorization
import install
import rollback
import utilities

PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"

def authorize():
    '''
    Authorizes user based on OS login username and password.
    The username is then used to mark the user against the action in log entries.
    '''
    username = authorization.verify()
    if username:
        print "Access granted."
        return username
    else:
        sys.exit()

arguments = argparse.ArgumentParser(description="AlphaInstaller")
arguments.add_argument("action")
arguments.add_argument("app_name")
arguments.add_argument("version")
arguments.add_argument("-s", "--silent", action="store_true")
arguments.add_argument("-t", "--time", default="0")

args = arguments.parse_args()

print "Initiating %s procedure..." % (args.action.upper())
session = {"app_name" : args.app_name, "version" : args.version, "action" : args.action, "silent" : args.silent, "time" : args.time}

s = sched.scheduler(time.time, time.sleep)

if args.action in auth_actions:
    '''
    Calling module based on the action provided as command line argument.
    '''
    session["username"] = authorize()
    _params = (session)
    if args.action == "deploy" or args.action == "update":
        s.enter(float(args.time)*1, 1, install.ignite, _params)
        s.run()
    elif args.action == "rollback":
        rollback.ignite()
        
else:
    print "%s is not a valid action." % (args.action)