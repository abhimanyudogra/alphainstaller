'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import paramiko
import scp
import os
import XMLInfoExtracter

class RemoteFactory(object):
    def __init__(self, parent_xml_data):       
        parse_obj = XMLInfoExtracter.TgtXMLParserFactory(parent_xml_data["tgt_xml_location"], parent_xml_data["tgt_xml_version"])
        self.target_machine_data = parse_obj.parse()
        self.parent_xml_data = parent_xml_data
          
    def get_relevant_obj(self, parent_xml_data):        
        if self.target_machine_data["transmit_method"] == "SCP_paramiko":
            return SCP_paramiko(self.target_machine_data)
        
    def deploy(self):
        for server in self.target_machine_data["target_machines"]:
            if server["transmission_method"] == "SCP_paramiko":
                self.remote_obj = SCP_paramiko(self.parent_xml_data, server)                
                self.remote_obj.deploy()
        
        

    
class SCP_paramiko(object):
    def __init__(self, parent_xml_data, server_data):
        self.server_data = server_data
        self.binary_files = XMLInfoExtracter.get_binary_paths(parent_xml_data["bin_xml_location"], parent_xml_data["bin_xml_version"])        
        self.config_files = XMLInfoExtracter.get_config_file_paths(parent_xml_data["cfg_xml_location"], parent_xml_data["cfg_xml_version"])        
        self.script_files = XMLInfoExtracter.get_scr_paths(parent_xml_data["scr_xml_location"], parent_xml_data["scr_xml_version"])
        
    def display_activity(self, stdout, stderr):        
        oup = stdout.read()
        err = stderr.read()        
        if oup:
            print oup
        if err:
            print err
            
    def parent_dir(self, path):
        return path.split("/")
        
      
    def linker(self, ssh):
        
        for _binary in self.binary_files["bin_data"]:
            source_path = os.path.join(self.server_data["release_folder_location"], _binary["code_base_location"])
            link_path = os.path.join(self.server_data["prod_folder_location"], _binary["target_location"])
            stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" %(os.path.dirname(link_path), source_path, link_path))
            type(stdin)
            self.display_activity(stdout, stderr)
        
        if (self.config_files):
            for _file in self.config_files["config_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], _file["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], _file["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" %(os.path.dirname(link_path), source_path, link_path))
                type(stdin)
                self.display_activity(stdout, stderr)
        
        if (self.script_files):
            for script in self.script_files["script_data"]:
                source_path = os.path.join(self.server_data["release_folder_location"], script["code_base_location"])
                link_path = os.path.join(self.server_data["prod_folder_location"], script["target_location"])
                stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s; ln -svf %s %s" %(os.path.dirname(link_path), source_path, link_path))
                type(stdin)
                self.display_activity(stdout, stderr)
            

            
    def extracter(self, ssh):        
        stdin, stdout, stderr = ssh.exec_command("cd %s;tar -zxvf %s;rm -v %s"%(self.server_data["release_folder_location"], "alphainstaller.tar.gz", "alphainstaller.tar.gz"))
        type(stdin)
        self.display_activity(stdout, stderr)
        
        
        
    def deploy(self):
        print "Setting up SSH connection with %s" % self.server_data["ip_address"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.server_data["ip_address"], username=self.server_data["ssh_username"], password=self.server_data["ssh_password"])
        stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s" %(self.server_data["release_folder_location"]))
        type(stdin)
        self.display_activity(stdout, stderr)
        
        print "Setting up SCP client."
        scp_obj = scp.SCPClient(ssh.get_transport())
        
        print "Sending files."
        scp_obj.put("alphainstaller.tar.gz", self.server_data["release_folder_location"])
        
        print "Extracting 'alphainstaller.tar.gz'"
        self.extracter(ssh)
        
        print "Establishing links to install application."
        self.linker(ssh)