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
import Compresser
import Remote
from ParserDepot import AlphainstallerXMLParser 

PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"


def authorize():
    if authorization.verify():
        print "Access granted."
    else:
        sys.exit()  
              
def gather_settings():
    settings_obj = AlphainstallerXMLParser(PATH_SETTINGS_XML)
    return settings_obj.parse()

def gather_app_data(app_name, app_version, location, version):
    parent_xml_obj = XMLInfoExtracter.ParentXMLParserFactory(location, version)
    return parent_xml_obj.parse(app_name, app_version)

def checkout(code_base_version, repo_type, repo_location, target):
    if os.path.exists(target):
        if os.listdir(target):            
            rmtree(target)            
            os.mkdir(target)            
    else: 
        os.mkdir(target)
        
    version_path = os.path.join(repo_location, "v%s"%code_base_version)
    checkout_obj = RepositoryInteraction.CheckoutFactory(repo_type, version_path, target)
    checkout_obj.checkout_code()
    

def builder(temp_location, builder_location, builder_type):    
    location = os.path.join(temp_location, builder_location)
    build_obj =  AppBuilder.BuildFactory(location, builder_type)
    build_obj.build()
    
def compresser(file_compression, parent_xml_data):
    comp_obj = Compresser.CompresserFactory(file_compression)
    comp_obj.compress(parent_xml_data)
    
def remote_installer(parent_xml_data):    
    transmit_obj = Remote.RemoteFactory(parent_xml_data)
    transmit_obj.deploy() 
        
    
    

def ignite(app_name, code_base_version):
    authorize()
    print "Gathering alphainstaller settings."
    settings = gather_settings()
    
    print "Gathering information about %s version %s." % (app_name, code_base_version)
    parent_xml_data = gather_app_data(app_name, code_base_version, settings["parent_xml_location"], settings["parent_xml_version"])
    
    print "Checking out data from repository."
    checkout(code_base_version, settings["repo_type"], settings["repo_location"], settings["temp_folder_location"])
    
    print "Building code base."
    os.chdir(settings["temp_folder_location"])
    builder(settings["temp_folder_location"], settings["builder_file_location"], settings["builder_type"])
    
    print "Compressing files for deployment."
    compresser(settings["file_compression"], parent_xml_data)
    
    print "Preparing to deploy on remote servers."
    remote_installer(parent_xml_data)
    
    print "done"
    
    