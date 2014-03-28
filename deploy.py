'''
Created on 11-Mar-2014

@author: Abhimanyu
'''

import sys
import authorization
import XMLInfoExtracter
import RepositoryInteraction
import AppBuilder

def authorize():
    if authorization.verify():
        print "Access granted."
    else:
        sys.exit()        

def checkout(app_name, repo_type,repo_location, target):
    CheckoutObj = RepositoryInteraction.CheckoutFactory(repo_type, repo_location, target)
    CheckoutObj.checkout_code(app_name)
    
def ignite(app_name, version):
    authorize()
    print "Gathering information about %s version %s." % (app_name, version)
    app_data = XMLInfoExtracter.get_info(app_name, version)    
    
    #repository_checkout(app_data["repo_location"], config_data["temp_folder_address"])
    print "Checking out data from repository."
    checkout(app_name, app_data["app_xml_data"]["repo_type"], app_data["app_xml_data"]["repo_location"], app_data["parent_xml_data"]["temp_folder_address"])
    
    print "Building code base."
    AppBuilder.build(app_data["parent_xml_data"]["temp_folder_address"])
    
    
    
    
    
    
    