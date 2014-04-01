'''
Created on 18-Feb-2014

@author: Abhimanyu
'''
import os
import paramiko
import scp


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.164.253.216', username='Abhimanyu',password='alphascript')
stdin, stdout, stderr = ssh.exec_command("m")
type(stdin)
for line in stdout:
    print line

scp = scp.SCPClient(ssh.get_transport())
scp.put('temp/Package/app.tar.gz', '')


