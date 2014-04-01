'''
Created on 31-Mar-2014

@author: Abhimanyu
'''

import paramiko
import scp
from abc import ABCMeta, abstractmethod
import os

class RemoteFactory(object):
    def __init__(self, target_machine_data):
        self.transmitter_obj = self.get_relevant_obj(target_machine_data)
          
    def get_relevant_obj(self, target_machine_data):
        if target_machine_data["transmit_method"] == "SCP_paramiko":
            return SCP_paramiko(target_machine_data)
        
    def deploy(self):
        self.transmitter_obj.deploy()
        
        
class Remote(object):
    __metaclass__ = ABCMeta
    def __init__(self, target_machine_data):
        self.target_machine_data = target_machine_data
    
    @abstractmethod
    def deploy(self):
        pass
    
class SCP_paramiko(Remote):
    def __init__(self, target_machine_data):
        Remote.__init__(self, target_machine_data)
      
    def linker(self, ssh):
        binary_path = os.path.join(self.target_machine_data["release_folder_path"], self.target_machine_data["bin_source_path"])
        stdin, stdout, stderr = ssh.exec_command("ln -svf %s %s" %(binary_path, self.target_machine_data["bin_install_path"]))
        type(stdin)
        log  = stdout.read()
        print log
            
    def extracter(self, ssh):        
        stdin, stdout, stderr = ssh.exec_command("cd %s;tar -zxvf %s;rm -v %s"%(self.target_machine_data["release_folder_path"], "alphainstaller.tar.gz", "alphainstaller.tar.gz"))
        type(stdin)
        log  = stdout.read()
        print log
        
        
    def deploy(self):
        
        print "Setting up SSH connection with %s" % self.target_machine_data["ip_address"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.target_machine_data["ip_address"], username=self.target_machine_data["ssh_username"], password=self.target_machine_data["ssh_password"])
        stdin, stdout, stderr = ssh.exec_command("mkdir -pv %s" %(self.target_machine_data["release_folder_path"]))
        type(stdin)
        log  = stdout.read()
        print log
            
        print "Setting up SCP client."
        scp_obj = scp.SCPClient(ssh.get_transport())
        
        print "Sending files."
        scp_obj.put("alphainstaller.tar.gz", self.target_machine_data["release_folder_path"])
        
        print "Extracting 'alphainstaller.tar.gz'"
        self.extracter(ssh)
        
        print "Establishing links to install application."
        self.linker(ssh)