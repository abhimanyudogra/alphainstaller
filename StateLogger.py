'''
Created on 21-Apr-2014

@author: Abhimanyu
'''
from hashlib import sha1
import os
import re
import XMLInfoExtracter

class StateCreater():
    def __init__(self, session, parent_xml_data):
        self.session = session
        self.temp_state_file = os.path.join(session["temp_folder_location"], "statefile.txt")
        self.binary_files = XMLInfoExtracter.get_binary_paths(parent_xml_data["bin_xml_location"],
                                                               parent_xml_data["bin_xml_version"])
        self.config_files = XMLInfoExtracter.get_config_file_paths(parent_xml_data["cfg_xml_location"],
                                                                    parent_xml_data["cfg_xml_version"])
        self.script_files = XMLInfoExtracter.get_scr_paths(parent_xml_data["scr_xml_location"],
                                                            parent_xml_data["scr_xml_version"])
        
    def create_statefile(self):
        state_f = open(self.temp_state_file, "w")
        state_f.write("[BINARIES]\n")
        
        for _binary in self.binary_files["bin_data"]:
            source_path = os.path.join(self.session["temp_folder_location"], _binary["code_base_location"])
            _hash = sha1(open(source_path).read())            
            state_f.write("%s : %s\n" % (source_path, _hash.hexdigest()))
        
        state_f.write("[CONFIGS]\n")
        if (self.config_files):
            for _file in self.config_files["config_data"]:
                source_path = os.path.join(self.session["temp_folder_location"], _file["code_base_location"])
                _hash = sha1(open(source_path).read())            
                state_f.write("%s : %s\n" % (source_path, _hash.hexdigest()))
        
        state_f.write("[SCRIPTS]\n")    
        if (self.script_files):
            for script in self.script_files["script_data"]:
                source_path = os.path.join(self.session["temp_folder_location"], script["code_base_location"])
                _hash = sha1(open(source_path).read())            
                state_f.write("%s : %s\n" % (source_path, _hash.hexdigest()))
        
        state_f.close()

    def store_statefile(self, ip_address):
        final_state_dir = os.path.join("States", ip_address)
        
        if not os.path.exists(final_state_dir):
            os.makedirs(final_state_dir)
        
        final_state_file = os.path.join(final_state_dir, self.session["app_name"])        
        src = open(self.temp_state_file, "r")
        des = open(final_state_file, "w")
        des.write(src.read())        
        src.close()
        des.close()

class LocalStateCheck():
    def __init__(self, session, ip_address):
        self.session = session
        self.ip_address = ip_address
    
    def get_hashes(self, location):
        hashes = {}
        state_f = open(location, "r")
        hash_re = re.compile(" : ")
        for line in state_f.readlines():
            if hash_re.search(line):
                data = line.split(" : ")
                hashes[data[0]] = data[1]
                state_f.close()
        return hashes       

    def display(self, diff):
        types = ["changed::", "new::", "deleted::", "unchanged::"]
        for _type in types:
            if diff[_type]:
                for _file in diff[_type]:
                    print _type, _file
            
    def diff(self):
        local_statefile = os.path.join(os.path.join("States", self.ip_address), self.session["app_name"])
        remote_statefile = os.path.join(self.session["temp_folder_location"], "statefile.txt")
        local_hashes = self.get_hashes(local_statefile)
        remote_hashes = self.get_hashes(remote_statefile)
        
        diff = {}
        diff["new::"] = []
        diff["deleted::"] = []
        diff["changed::"] = []
        diff["unchanged::"] = []
        
        for _file in local_hashes.keys():
            if _file in remote_hashes.keys():
                if local_hashes[_file] == remote_hashes[_file]:
                    diff["unchanged::"].append(_file)
                else:
                    diff["changed::"].append(_file)
            else:
                diff["new::"].append(_file)
                
        for _file in remote_hashes.keys():
            if _file not in local_hashes.keys():
                diff["deleted::"].append(_file)
        
        print "Displaying diff between the new version of app and what is already present on server."
        self.display(diff)
        