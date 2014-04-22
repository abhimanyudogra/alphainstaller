'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import paramiko
import scp
import os
import socket
import sys

import XMLInfoExtracter
import utilities


class RemoteFactory(object):
    '''
    Factory module that selects relevant remote target machine based on the preferences mentioned in settings XML.
    Containts a deploy wrapper module, which calls the respective deploy method for every target machine the app
     is being deployed on.
    '''
    def __init__(self, parent_xml_data):
        parse_obj = XMLInfoExtracter.TgtXMLParserFactory(parent_xml_data["tgt_xml_location"], parent_xml_data["tgt_xml_version"])
        self.target_machine_data = parse_obj.parse()
        self.parent_xml_data = parent_xml_data

    def get_relevant_obj(self, parent_xml_data):
        '''
        Selects the remote server interaction module.
        '''
        if self.target_machine_data["transmit_method"] == "SCP_paramiko":
            return SCP_paramiko(self.target_machine_data)
        

    def check_state(self):
        pass
        
    def build_server_queue(self, server_resume_data):
        _queue = []
        for server in self.target_machine_data["target_machines"]:
            if server["ip_address"] not in server_resume_data["completed_servers"]:
                checkpoint = 0
                for partial_server in server_resume_data["partially_completed_servers"]:
                    if partial_server[0] == server["ip_address"]:
                        checkpoint = partial_server[1]
                _queue.append((server,checkpoint))
        return _queue
            

    def deploy(self, log_obj, server_resume_data, app_name):
        '''
        Calls the deploy method for every target machine.
        '''
        _queue = self.build_server_queue(server_resume_data)
        while _queue:
            server_and_checkpoint = _queue.pop(0)
            server = server_and_checkpoint[0]
            checkpoint = server_and_checkpoint[1]
            lock_obj = utilities.Lock(server["ip_address"], app_name)
            if lock_obj.check_lock():
                question = "The app is currently being deployed/modified on target server %s. Do you want to add this server to the end of queue?"
                if utilities.yes_or_no(question, "y"):
                    _queue.append(server_and_checkpoint)
            else:           
                log_obj.add_log("Deploying app on server : %s" % server["ip_address"])
                lock_obj.create_lock()
                if server["transmission_method"] == "SCP_paramiko":
                    try:
                        self.remote_obj = SCP_paramiko(self.parent_xml_data, server)
                        self.remote_obj.deploy(log_obj, checkpoint)
                    except socket.error:
                        question = "A network problem has occurred while remotely accessing server %s. Please make sure the \
                        system is connected to the server. Do you wish to continue with remaining servers?" % server["ip_address"]
                        if not utilities.yes_or_no(question, 'n'):
                            raise utilities.FatalError("User chose to terminate action after encountering an error while deplying on remote machines.")
                log_obj.mark_server_checkpoint(server["ip_address"])
                lock_obj.unlock()      


class SCP_paramiko(object):
    '''
    Concrete remote server interaction module that relies on third party modules, Paramiko and scp-paramiko
     for setting up connection, executing commands on remote machine and transmitting data.
    '''
    def __init__(self, parent_xml_data, server_data):
        self.server_data = server_data
        self.binary_files = XMLInfoExtracter.get_binary_paths(parent_xml_data["bin_xml_location"], parent_xml_data["bin_xml_version"])
        self.config_files = XMLInfoExtracter.get_config_file_paths(parent_xml_data["cfg_xml_location"], parent_xml_data["cfg_xml_version"])
        self.script_files = XMLInfoExtracter.get_scr_paths(parent_xml_data["scr_xml_location"], parent_xml_data["scr_xml_version"])

    def display_activity(self, stdout, stderr):
        '''
        Prints the output from the target machine.
        '''
        oup = stdout.read()
        err = stderr.read()
        if oup:
            print oup
        if err:
            print err

    def linker(self, ssh):
        '''
        Links the files in main production folder with actual files present in Release folder.
        '''
        for _binary in self.binary_files["bin_data"]:
            source_path = os.path.join(self.server_data["release_folder_location"], _binary["code_base_location"])
            link_path = os.path.join(self.server_data["prod_folder_location"], _binary["target_location"])
            stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path), source_path, link_path))
            type(stdin)
            self.display_activity(stdout, stderr)

        if (self.config_files):
            for _file in self.config_files["config_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], _file["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], _file["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path), source_path, link_path))
                type(stdin)
                self.display_activity(stdout, stderr)

        if (self.script_files):
            for script in self.script_files["script_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], script["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], script["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path), source_path, link_path))
                type(stdin)
                self.display_activity(stdout, stderr)

    def extracter(self, ssh):
        '''
        Extracts the Alphainstaller package.
        '''
        stdin, stdout, stderr = ssh.exec_command("cd %s;tar -zxvf %s;rm -v %s" % (self.server_data["release_folder_location"],
                                                                                  "alphainstaller.tar.gz", "alphainstaller.tar.gz"))
        type(stdin)
        self.display_activity(stdout, stderr)

    def SSH_connector(self):
        '''
        Uses paramiko to establish a SSH connection to remote server.
        '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server_data["ip_address"], username=self.server_data["ssh_username"], password=self.server_data["ssh_password"])
        stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s" % (self.server_data["release_folder_location"]))
        type(stdin)
        self.display_activity(stdout, stderr)
        return ssh
    

    def deploy(self, log_obj, start_from_cp):
        '''
        Driver module. Calls all sub-modules to transmit package, extract it and establish final connections.
        '''
        ip_address = self.server_data["ip_address"]
        log_obj.add_log("Setting up SSH connection with %s" % self.server_data["ip_address"])
        ssh = self.SSH_connector()

        log_obj.add_log("Setting up SCP client.")
        scp_obj = scp.SCPClient(ssh.get_transport())

        if (start_from_cp <= log_obj.checkpoint_id):
            log_obj.add_log("Sending files.")
            scp_obj.put("alphainstaller.tar.gz", self.server_data["release_folder_location"])
            log_obj.mark_remote_checkpoint("Package successfully uploaded.", ip_address)
        else:
            log_obj.skip_checkpoint()
        
        if (start_from_cp <= log_obj.checkpoint_id):
            log_obj.add_log("Extracting 'alphainstaller.tar.gz'")
            self.extracter(ssh)
            log_obj.mark_remote_checkpoint("Package successfully extracted.", ip_address)
        else:
            log_obj.skip_checkpoint()

        if (start_from_cp <= log_obj.checkpoint_id):
            log_obj.add_log("Establishing links to install application.")
            self.linker(ssh)
            log_obj.mark_remote_checkpoint("Links successfully established.", ip_address)
        else:
            log_obj.skip_checkpoint()

        ssh.close()