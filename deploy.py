'''
Created on 11-Mar-2014

@author: Abhimanyu
'''

import sys
import authorization
import XMLparser
import RepositoryInteraction

def authorize():
    if authorization.verify():
        print "Access granted."
    else:
        sys.exit()
        
        
def getClient(repo_type, source, target):
    if repo_type == "svn":
        return RepositoryInteraction.SVNCheckout(source, target)   

    
    
def ignite(app_name, version):
    authorize()
    print "Gathering information about %s." % (app_name)
    app_data  = XMLparser.parse(app_name, version)
    
    #repository_checkout(app_data["repo_location"], config_data["temp_folder_address"])
    
    CheckoutClient = getClient(app_data["repo_type"], app_data["repo_location"], app_data["temp_folder_address"])
    CheckoutClient.checkout_code()
    

    
    
    
    
    
    
    