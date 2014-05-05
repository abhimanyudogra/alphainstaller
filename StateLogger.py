'''
Created on 21-Apr-2014

@author: Abhimanyu
'''
from hashlib import sha1
import os
import re
import XMLInfoExtracter

class LocalStateManager():
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
            state_f.write("%s : %s\n" % (_binary["target_location"], _hash.hexdigest()))
        
        state_f.write("[CONFIGS]\n")
        if (self.config_files):
            for _file in self.config_files["config_data"]:
                source_path = os.path.join(self.session["temp_folder_location"], _file["code_base_location"])
                _hash = sha1(open(source_path).read())            
                state_f.write("%s : %s\n" % (_file["target_location"], _hash.hexdigest()))
        
        state_f.write("[SCRIPTS]\n")    
        if (self.script_files):
            for script in self.script_files["script_data"]:
                source_path = os.path.join(self.session["temp_folder_location"], script["code_base_location"])
                _hash = sha1(open(source_path).read())            
                state_f.write("%s : %s\n" % (script["target_location"], _hash.hexdigest()))
        
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

class RemoteStateManager():
        def __init__(self, ip_address, prod_folder_location):
            self.ip_address = ip_address
            self.prod_folder_location = prod_folder_location
                    
        def update_server_state(self, hashes):
            state_file = os.path.join("States", os.path.join(self.ip_address, "server-state"))
            if not os.path.exists(os.path.dirname(state_file)):
                os.makedirs(os.path.dirname(state_file))            
            state_f = open(state_file, "w")                
            for line in hashes:
                line_data = line.split("  ")
                result = "%s : %s\n" % (os.path.relpath(line_data[1], self.prod_folder_location)[:-1], line_data[0])
                state_f.write(result)
                    
class StateCheck():
    '''
    Parent class for Local and Remote state checker classes. Defines the diff generator function.
    '''     
    def __init__(self):
        pass
    
    def generate_diff(self, old_hashes, new_hashes):
        diff = {}
        diff["new::"] = []
        diff["deleted::"] = []
        diff["changed::"] = []
        diff["unchanged::"] = []
        diff["moved::"] = []
        diff["renamed::"] = []

        for _hash1, _file1 in new_hashes.items():
            if old_hashes.has_key(_hash1):
                _file2 = old_hashes[_hash1]
                
                if _file2 == _file1:
                    diff["unchanged::"].append(new_hashes.pop(_hash1))                    
                    old_hashes.pop(_hash1)
                else:
                    if os.path.split(_file1)[1] == os.path.split(_file2)[1]:
                        diff["moved::"].append("%s --> %s" % (old_hashes.pop(_hash1), new_hashes.pop(_hash1)))
                    else:
                        diff["renamed::"].append("%s --> %s" % (old_hashes.pop(_hash1), new_hashes.pop(_hash1)))
            else:
                found_file = False
                for _hash2, _file2 in old_hashes.items():
                    if _file2 == _file1:
                        diff["changed::"].append(new_hashes.pop(_hash1))
                        old_hashes.pop(_hash2)
                        found_file = True
                        break                    
                if not found_file:
                    diff["new::"].append(new_hashes.pop(_hash1))
        
        for _hash in old_hashes.keys():
            diff["deleted::"].append(old_hashes.pop(_hash))
            
        return diff
        
        
        
class LocalStateCheck(StateCheck):
    def __init__(self, session, ip_address):
        StateCheck.__init__(self)
        self.session = session
        self.ip_address = ip_address
    
    def get_hashes(self, location):
        hashes = {}
        state_f = open(location, "r")
        hash_re = re.compile(" : ")
        for line in state_f.readlines():
            if hash_re.search(line):
                data = line.split(" : ")
                hashes[data[1][:-1]] = data[0]
                state_f.close()
        return hashes       

    def display(self, diff):
        types = ["changed::", "moved::", "renamed::", "new::", "deleted::", "unchanged::"]
        for _type in types:
            if diff[_type]:
                for _file in diff[_type]:
                    print _type, _file
            
    def local_diff(self):
        new_statefile = os.path.join(self.session["temp_folder_location"], "statefile.txt")
        old_statefile = os.path.join(os.path.join("States", self.ip_address), self.session["app_name"])
        new_hashes = self.get_hashes(new_statefile)
        old_hashes = self.get_hashes(old_statefile)
        diff = self.generate_diff(old_hashes, new_hashes)        
        print "Displaying diff between the new version of app and what is already present on server."
        self.display(diff)
        
class RemoteStateCheck(StateCheck):
    def __init__(self, ip_address, prod_folder_location):
        StateCheck.__init__(self)
        self.ip_address = ip_address
        self.prod_folder_location = prod_folder_location
        
    def get_hashes(self, location):
        state_f = open(location, "r")
        hashes = {}
        hash_re = re.compile(" : ")
        for line in state_f.readlines():
            if hash_re.search(line):
                data = line.split(" : ")
                hashes[data[1][:-1]] = data[0]
                state_f.close()
        return hashes
    
    def convert(self, new_hashes):
        hashes = {}
        for line in new_hashes:
            line_data = line.split("  ")
            hashes[line_data[0]] = os.path.relpath(line_data[1], self.prod_folder_location)[:-1]     
        return hashes
    
    def display(self, diff):
        types = ["changed::", "moved::", "renamed::", "new::", "deleted::"]
        changes_found = False
        for _type in types:
            if diff[_type]:
                for _file in diff[_type]:
                    print _type, _file
                changes_found = True
        return changes_found
    
    def remote_diff(self, new_hashes):
        old_server_state = os.path.join("States", os.path.join(self.ip_address, "server-state"))
        if not os.path.exists(old_server_state):
            print "Server state-file not found. Remote diff could not be generated."
            return False
        else:
            old_hashes = self.get_hashes(old_server_state)
            new_hashes = self.convert(new_hashes)
            diff = self.generate_diff(old_hashes, new_hashes)
            print "Displaying diff between the last recorded server state and the current state."
            if self.display(diff):
                return True
            else:
                print "No changes found."
                return False
        