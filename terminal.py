'''
Created on 14-Feb-2014
hellop
@author: Abhimanyu
'''


auth_actions = ("deploy", "rollback", "update")

import argparse
import sys

import deploy
import update
import rollback
import utilities

PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"

arguments = argparse.ArgumentParser(description="AlphaInstaller")
arguments.add_argument("action")
arguments.add_argument("app_name")
arguments.add_argument("-v", "--version", metavar="", default=False)

args = arguments.parse_args()

print "Initiating %s procedure..." % (args.action.upper())


if args.action in auth_actions:
    '''
    Calling module based on the action provided as command line argument.
    '''
    try:
        locals()[args.action].ignite(args.app_name, args.version)
    except utilities.FatalError:
        print utilities.FatalError.message()
else:
    print "%s is not a valid action." % (args.action)