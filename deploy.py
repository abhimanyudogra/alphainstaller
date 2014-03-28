'''
Created on 11-Mar-2014

@author: Abhimanyu
'''

import sys
import authorization
import XMLInfoExtracter
import RepositoryInteraction

def authorize():
    if authorization.verify():
        print "Access granted."
    else:
        sys.exit()
        

    
    
def ignite(app_name, version):
    authorize()
    print "Gathering information about %s version %s." % (app_name, version)
    app_data = XMLInfoExtracter.get_info(app_name, version)    
    
    #repository_checkout(app_data["repo_location"], config_data["temp_folder_address"])
    
    CheckoutObj = RepositoryInteraction.CheckoutFactory(app_data["app_xml_data"]["repo_type"], app_data["app_xml_data"]["repo_location"], app_data["parent_xml_data"]["temp_folder_address"])
    print "Checking out data from repository."
    CheckoutObj.checkout_code(app_name)
    

    
    
    
    
    
    
    