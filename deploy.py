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
import Remote

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
        
        
    version_path = os.path.join(repo_location, "v%s"%version)
    checkout_obj = RepositoryInteraction.CheckoutFactory(repo_type, version_path, target)
    checkout_obj.checkout_code()
    

def builder(temp_location, builder_location, builder_type):    
    location = os.path.join(temp_location, builder_location)
    build_obj =  AppBuilder.BuildFactory(location, builder_type)
    build_obj.build()
    
def compresser(binary_location, other_files):
    comp_obj = CompressModule.Compress(binary_location, other_files)
    comp_obj.compress()
    
def remote_installer(target_machines, app_name, version):
    for server in target_machines:
        transmit_obj = Remote.RemoteFactory(server)
        transmit_obj.deploy()
        
    
    

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

    print "Preparing to deploy on remote servers."
    remote_installer(app_data["cfg_xml_data"]["target_machines"], app_name, version)
    
    print "done"
    
    