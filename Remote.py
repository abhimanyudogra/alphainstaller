'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import paramiko
import scp
import os
import re
import socket

import XMLInfoExtracter
import StateLogger
import utilities
PATH_SETTINGS_XML = "XMLfiles/alphainstaller_settings.xml"


class RemoteOperator(object):
    '''
    Factory module that selects relevant remote target machine based on the preferences mentioned in settings XML.
    Containts a deploy wrapper module, which calls the respective deploy method for every target machine the app
     is being deployed on.
    '''
    def __init__(self, session, parent_xml_data):
        self.session = session
        parse_obj = XMLInfoExtracter.TgtXMLParserFactory(parent_xml_data["tgt_xml_location"], 
                                                         parent_xml_data["tgt_xml_version"])
        self.target_machine_data = parse_obj.parse()
        self.parent_xml_data = parent_xml_data

    def get_relevant_obj(self, parent_xml_data):
        '''
        Selects the remote server interaction module.
        '''
        if self.target_machine_data["transmit_method"] == "SCP_paramiko":
            return SCP_paramiko(self.target_machine_data)
        
    def build_server_queue(self, server_resume_data):
        '''
        Returns a queue of tuple pairs.
        Member 1 of the tuple pair contains the server address.
        Member 2 of the tuple pair contains the checkpoint from which the operations must be performed on that server.
        By default, Member 2 is 0, implying all operations have to be performed.
        '''
        _queue = []
        for server in self.target_machine_data["target_machines"]:
            if server["ip_address"] not in server_resume_data["completed_servers"]:
                checkpoint = 0
                for partial_server in server_resume_data["partially_completed_servers"]:
                    if partial_server[0] == server["ip_address"]:
                        checkpoint = partial_server[1]
                _queue.append((server,checkpoint))
        return _queue
    
    def check_state(self, ip_address):
        state_file_path = os.path.join(os.path.join("States", ip_address), self.session["app_name"])
        if self.session["action"] == "deploy":
            if os.path.exists(state_file_path):
                question = "A statefile of app %s on server %s was found, implying the app has already "\
                "been deployed on the server before.\nDo you wish to continue? Answering 'n' will cause "\
                "alphainstaller to drop operations on this server." % (self.session["app_name"], ip_address)
                if utilities.yes_or_no(question, XMLInfoExtracter.get_default("continue_if_state_exists"), self.session["silent"]):
                    question = "Do you wish to  'update' rather than 'deploy' for this server?\n"\
                     "Answering 'n' will force Alphainstaller to run in 'deploy' mode"
                    if utilities.yes_or_no(question, XMLInfoExtracter.get_default("convert_to_update_if_state_exists"), self.session["silent"]):
                        self.session["action"] = "update"    
                    return True
                else:
                    return False
            else:
                return True
        
        elif self.session["action"] == "update":
            if not os.path.exists(state_file_path):
                question = "The state file of %s for server %s was not found. Which implies that the "\
                "alphainstaller doesn't remember the app previously being deployed on that server.\n This "\
                "will some features to not be available, like local and remote diffs.\n Do you wish to continue? "\
                "Answering 'n' will cause alphainstaller to drop operations on this server." % (self.session["app_name"], ip_address)
                if utilities.yes_or_no(question, XMLInfoExtracter.get_default("force_if_state_not_found"), self.session["silent"]):
                    self.session["action"] = "deploy"
                    return True
                else:
                    return False
     
    def display_local_diff(self, ip_address):    
        diff_obj = StateLogger.LocalStateCheck(self.session, ip_address)
        diff_obj.local_diff()      

    def install(self, log_obj, server_resume_data):
        '''
        Calls the deploy method for every target machine.
        '''
        _queue = self.build_server_queue(server_resume_data)
        state_obj = StateLogger.LocalStateManager(self.session, self.parent_xml_data)
        state_obj.create_statefile()
        action_backup = self.session["action"]
        
        while _queue:
            green_light = True
            self.session["action"] = action_backup
            server_and_checkpoint = _queue.pop(0)
            server = server_and_checkpoint[0]
            checkpoint = server_and_checkpoint[1]
            
            if self.check_state(server["ip_address"]):                
                if self.session["action"] == "update":
                    self.display_local_diff(server["ip_address"])
                    question = "Are you satisfied with the diff? Selecting 'n' will make AlphaInstaller skip the procedures for the current server."
                    if not utilities.yes_or_no(question, XMLInfoExtracter.get_default("local_diff_satisfaction"), self.session["silent"]):
                        green_light = False
                        
                if green_light:           
                    lock_obj = utilities.Lock(server["ip_address"], self.session["app_name"])
                    if lock_obj.check_lock():
                        question = "The app is currently being deployed/modified on target server %s.\n"\
                        "Do you want to add this server to the end of queue?" % server["ip_address"]
                        if utilities.yes_or_no(question, XMLInfoExtracter.get_default("enqueue_if_locked"), self.session["silent"]):
                            _queue.append(server_and_checkpoint)
                    else:           
                        log_obj.add_log("Deploying app on server : %s" % server["ip_address"])
                        lock_obj.create_lock()
                        if server["transmission_method"] == "SCP_paramiko":
                            try:
                                self.remote_obj = SCP_paramiko(self.session, self.parent_xml_data, server)
                                self.remote_obj.deploy(log_obj, checkpoint)
                            except socket.error:
                                lock_obj.unlock() 
                                question = "A network problem has occurred while remotely accessing server %s. Please make sure the"\
                                "system is connected to the server. Do you wish to add this server to the back of queue for future"\
                                "consideration? Otherwise the server will be dropped." % server["ip_address"]
                                if utilities.yes_or_no(question, XMLInfoExtracter.get_default("enqueue_if_network_error"), self.session["silent"]):
                                    _queue.append((server, log_obj.checkpoint_id))
                                    log_obj.reset_cp()
                                    continue
                            except:
                                lock_obj.unlock()
                                question = "An error halted the operations on server %s .Do you wish to add this server to the back of"\
                                "queue for future consideration? Otherwise the server will be dropped."
                                if utilities.yes_or_no(question, XMLInfoExtracter.get_default("enqueue_if_error"), self.session["silent"]):
                                    _queue.append((server, log_obj.checkpoint_id))
                                    log_obj.reset_cp()
                                    continue
                        state_obj.store_statefile(server["ip_address"])
                        log_obj.mark_server_checkpoint(server["ip_address"])
                        lock_obj.unlock()      


class SCP_paramiko(object):
    '''
    Concrete remote server interaction module that relies on third party modules, Paramiko and scp-paramiko
     for setting up connection, executing commands on remote machine and transmitting data.
    '''
    def __init__(self, session, parent_xml_data, server_data):
        self.server_data = server_data
        self.session = session
        self.binary_files = XMLInfoExtracter.get_binary_paths(parent_xml_data["bin_xml_location"],
                                                               parent_xml_data["bin_xml_version"])
        self.config_files = XMLInfoExtracter.get_config_file_paths(parent_xml_data["cfg_xml_location"],
                                                                    parent_xml_data["cfg_xml_version"])
        self.script_files = XMLInfoExtracter.get_scr_paths(parent_xml_data["scr_xml_location"],
                                                            parent_xml_data["scr_xml_version"])

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
            stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path),
                                                                                       source_path, link_path))
            type(stdin)
            self.display_activity(stdout, stderr)
            
        if (self.config_files):
            for _file in self.config_files["config_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], _file["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], _file["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path),
                                                                                           source_path, link_path))
                type(stdin)
                self.display_activity(stdout, stderr)

        if (self.script_files):
            for script in self.script_files["script_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], script["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], script["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" % (os.path.dirname(link_path),
                                                                                           source_path, link_path))
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
        
    def store_state(self, ssh):
        stdin, stdout, stderr = ssh.exec_command("find %s -type l -print0 | sort -z | xargs -0 sha1sum" % self.server_data["prod_folder_location"])
        type(stdin)
        r_diff_obj = StateLogger.RemoteStateManager(self.server_data["ip_address"], self.server_data["prod_folder_location"])
        r_diff_obj.update_server_state(stdout)
        
    def check_state(self, ssh):
        stdin, stdout, stderr = ssh.exec_command("find %s -type l -print0 | sort -z | xargs -0 sha1sum" % self.server_data["prod_folder_location"])
        type(stdin)
        r_diff_obj = StateLogger.RemoteStateCheck(self.server_data["ip_address"], self.server_data["prod_folder_location"])
        return r_diff_obj.remote_diff(stdout)
    
    def cleaner(self, ssh):
        old_state_location = os.path.join(os.path.join("States",self.server_data["ip_address"]), self.session["app_name"])
        old_state = open(old_state_location, "r")
        hash_re = re.compile(" : ")
        for line in old_state:
            if hash_re.search(line):
                line_data = line.split(" : ")
                stdin, stdout, stderr = ssh.exec_command("rm -v %s" % os.path.join(self.server_data["prod_folder_location"], line_data[0]))
                type(stdin)
                self.display_activity(stdout, stderr)            
            
    def SSH_connector(self):
        '''
        Uses paramiko to establish a SSH connection to remote server.
        '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server_data["ip_address"], username=self.server_data["ssh_username"], 
                    password=self.server_data["ssh_password"])
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
        
        green_light = True

        if self.session["action"] == "update":
            if self.check_state(ssh):
                question = "Are you satisfied with the diff? Selecting 'n' will make AlphaInstaller skip the procedures for the current server."            
                if not utilities.yes_or_no(question, XMLInfoExtracter.get_default("remote_diff_satisfaction"), self.session["silent"]):
                    green_light = False

        if green_light:   
            if (start_from_cp <= log_obj.checkpoint_id):
                log_obj.add_log("Sending files.")
                scp_obj.put(os.path.join(self.session["temp_folder_location"], "alphainstaller.tar.gz"),
                            self.server_data["release_folder_location"])
                log_obj.mark_remote_checkpoint("Package successfully uploaded.", ip_address)
            else:
                log_obj.skip_checkpoint()

            if (start_from_cp <= log_obj.checkpoint_id):
                log_obj.add_log("Extracting package")
                self.extracter(ssh)
                log_obj.mark_remote_checkpoint("Package successfully extracted.", ip_address)
            else:
                log_obj.skip_checkpoint()
            
            if self.session["action"] == "update": 
                if (start_from_cp <= log_obj.checkpoint_id):
                    log_obj.add_log("Removing old files.")
                    self.cleaner(ssh)
                    log_obj.mark_remote_checkpoint("Old app files removed.", ip_address)
                else:
                    log_obj.skip_checkpoint()

            if (start_from_cp <= log_obj.checkpoint_id):
                log_obj.add_log("Establishing links to install application.")
                self.linker(ssh)
                log_obj.mark_remote_checkpoint("Links successfully established.", ip_address)
            else:
                log_obj.skip_checkpoint()

            if (start_from_cp <= log_obj.checkpoint_id):
                log_obj.add_log("Storing server state.")
                self.store_state(ssh)
                log_obj.mark_remote_checkpoint("Server state recorded.", ip_address)
            else:
                log_obj.skip_checkpoint()

        ssh.close()