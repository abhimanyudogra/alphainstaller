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
import LogManager
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


def check_log(app_name, version):
    '''
    Checks the log file for the app + version for abrupt termination of last action.
    Presents user with choice to continue the last operation where it stopped or
     a fresh start.
    '''
    lc_obj = LogManager.LogChecker(app_name, version)
    if not lc_obj.check_successful_completion():
        if utilities.yes_or_no("Last action for this application and version was not successful, do you want to resume that operation?", "y"):
            return lc_obj.get_resume_data()
    return 0, {"completed_servers":[], "partially_completed_servers":[]}

def gather_settings():
    '''
    Parses alphainstaller settings XML to obtain the mode of operation and other configurations.
    '''
    settings_obj = AlphainstallerXMLParser(PATH_SETTINGS_XML)
    return settings_obj.parse()


def gather_app_data(app_name, app_version, location, version):
    '''
    Parses parent XML to obtain addresses to the rest of the XML's for the specific app + version.
    '''
    parent_xml_obj = XMLInfoExtracter.ParentXMLParserFactory(location, version)
    return parent_xml_obj.parse(app_name, app_version)


def checkout(code_base_version, repo_type, repo_location, target):
    '''
    Checks the code base out of the repository to a temporary folder which is mentioned in the settings XML.
    '''
    if os.path.exists(target):  # Creating temporary folder if it doesn't exist
        if os.listdir(target):
            rmtree(target)      # Clearing temporary folder off previous junk content
            os.mkdir(target)
    else:
        os.mkdir(target)
    version_path = os.path.join(repo_location, "v%s" % code_base_version)
    checkout_obj = RepositoryInteraction.CheckoutFactory(repo_type, version_path, target)
    checkout_obj.checkout_code()


def builder(temp_location, builder_location, builder_type):
    '''
    Builds the code base according to the information provided in the settings XML.
    '''
    location = os.path.join(temp_location, builder_location)
    build_obj = AppBuilder.BuildFactory(location, builder_type)
    build_obj.build()


def compresser(file_compression, parent_xml_data):
    ''' 
    Compresses all the files: Bins, config files etc associated with the app into a single package.
    Package type is configurable in settings XML
    '''
    comp_obj = Compresser.CompresserFactory(file_compression)
    comp_obj.compress(parent_xml_data)


def remote_installer(log_obj, parent_xml_data, server_resume_data, app_name):
    '''
    Summons the Remote.py module which handles all the remote operations.
    '''
    transmit_obj = Remote.RemoteFactory(parent_xml_data)
    transmit_obj.deploy(log_obj, server_resume_data, app_name)


def ignite(app_name, code_base_version):
    '''
    The driver module for deploy. Calls respective modules for the entire deployment process.
    '''
    username = authorize()
    log_obj = LogManager.Logger(app_name, code_base_version, "deploy", username)
    
    local_resume_cp, server_resume_data = check_log(app_name, code_base_version)

    log_obj.add_log("Gathering alphainstaller settings.")
    settings = gather_settings()

    log_obj.add_log("Gathering information about %s version %s." % (app_name, code_base_version))
    parent_xml_data = gather_app_data(app_name, code_base_version, settings["parent_xml_location"], settings["parent_xml_version"])
    
    

    if local_resume_cp <= log_obj.checkpoint_id:
        log_obj.add_log("Checking out data from repository.")
        checkout(code_base_version, settings["repo_type"], settings["repo_location"], settings["temp_folder_location"])
        log_obj.mark_local_checkpoint("Checked out repository")
    else:
        log_obj.skip_checkpoint()

    os.chdir(settings["temp_folder_location"])

    if local_resume_cp <= log_obj.checkpoint_id:
        log_obj.add_log("Building code base.")
        builder(settings["temp_folder_location"], settings["builder_file_location"], settings["builder_type"])
        log_obj.mark_local_checkpoint("Codebase built")
    else:
        log_obj.skip_checkpoint()

    if local_resume_cp <= log_obj.checkpoint_id:
        log_obj.add_log("Compressing files for deployment.")
        compresser(settings["file_compression"], parent_xml_data)
        log_obj.mark_local_checkpoint("Files compressed")
    else:
        log_obj.skip_checkpoint()
    
    
    log_obj.mark_local_complete()
    remote_installer(log_obj, parent_xml_data, server_resume_data, app_name)

    log_obj.action_complete()