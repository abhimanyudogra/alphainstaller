'''
Created on 11-Mar-2014

@author: Abhimanyu
'''

import os
from shutil import rmtree
import sys
import authorization
import XMLInfoExtracter
import RepositoryInteraction
import AppBuilder
import CompressModule

def authorize():
    if authorization.verify():
        print "Access granted."
    else:
        sys.exit()        


def checkout(app_name, version,  repo_type, repo_location, target):
    if os.path.exists(target):
        if os.listdir(target):            
            rmtree(target)            
            os.mkdir(target)            
    else: 
        os.mkdir(target)
        
    target = os.path.join(target, "Source")
    os.mkdir(target)
    
    version_path = os.path.join(repo_location, "v%s"%version)
    checkout_obj = RepositoryInteraction.CheckoutFactory(repo_type, version_path, target)
    checkout_obj.checkout_code()
    

def builder(temp_location, builder_location, builder_type):
    codebase_location = os.path.join(temp_location, "Source")
    location = os.path.join(codebase_location, builder_location)
    build_obj =  AppBuilder.BuildFactory(location, builder_type)
    build_obj.build()
    
def compresser(binary_location, other_files):
    os.mkdir("Package")
    comp_obj = CompressModule.Compress(binary_location, other_files)
    comp_obj.compress()
    

def ignite(app_name, version):
    #authorize()
    print "Gathering information about %s version %s." % (app_name, version)
    app_data = XMLInfoExtracter.get_info(app_name, version)    
    
    print "Checking out data from repository."
    checkout(app_name, version, app_data["parent_xml_data"]["repo_type"], app_data["parent_xml_data"]["repo_location"], app_data["parent_xml_data"]["temp_folder_location"])
    
    print "Building code base."
    os.chdir(app_data["parent_xml_data"]["temp_folder_location"])
    builder(app_data["parent_xml_data"]["temp_folder_location"], app_data["parent_xml_data"]["build_file_location"], app_data["parent_xml_data"]["build_file_type"])
    
    print "Compressing files for deployment."
    compresser(app_data["app_xml_data"]["binary_location"], app_data["app_xml_data"]["optional_files"])

    print "Transmitting data to target machines."
    
    
    
    