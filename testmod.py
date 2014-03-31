'''
Created on 18-Feb-2014

@author: Abhimanyu
'''
import os
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.164.253.216', username='Abhimanyu',password='alphascript')
stdin, stdout, stderr = ssh.exec_command("pwd")
type(stdin)
for line in stdout:
    print line

stdin, stdout, stderr = ssh.exec_command("cd infra;pwd;mkdir lulz")
type(stdin)
for line in stdout:
    print line

stdin, stdout, stderr = ssh.exec_command("pwd")
type(stdin)
for line in stdout:
    print line


