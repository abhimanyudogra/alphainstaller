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
from Logger import Logger

PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"


def authorize():
    username = authorization.verify()
    if username:
        print "Access granted."
        return username
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
    
def remote_installer(log_obj, parent_xml_data):    
    transmit_obj = Remote.RemoteFactory(parent_xml_data)
    transmit_obj.deploy(log_obj) 
        
    
    

def ignite(app_name, code_base_version):
    username = authorize()
    log_obj = Logger(app_name, code_base_version, "deploy", username)
    log_obj.mark_checkpoint("Logged in")
    
    log_obj.add_log("Gathering alphainstaller settings.")
    settings = gather_settings()
    log_obj.mark_checkpoint("Gathered alphainstaller settings")
    
    log_obj.add_log("Gathering information about %s version %s." % (app_name, code_base_version))    
    parent_xml_data = gather_app_data(app_name, code_base_version, settings["parent_xml_location"], settings["parent_xml_version"])
    log_obj.mark_checkpoint("Gathered app information")
    
    log_obj.add_log("Checking out data from repository.")
    checkout(code_base_version, settings["repo_type"], settings["repo_location"], settings["temp_folder_location"])
    log_obj.mark_checkpoint("Checked out repository")
    
    log_obj.add_log("Building code base.")
    os.chdir(settings["temp_folder_location"])
    builder(settings["temp_folder_location"], settings["builder_file_location"], settings["builder_type"])
    log_obj.mark_checkpoint("Codebase built")
    
    log_obj.add_log("Compressing files for deployment.")
    compresser(settings["file_compression"], parent_xml_data)
    log_obj.mark_checkpoint("Files compressed")
    
    log_obj.add_log("Preparing to deploy on remote servers.")
    remote_installer(log_obj, parent_xml_data)
    log_obj.mark_checkpoint("App deployed on all servers.")
    
    log_obj.action_complete()
    
    