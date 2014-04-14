'''
Created on 18-Feb-2014

@author: Abhimanyu
'''


f = open("Logs/app2/v4.7/log", "a+")

if not f.read():
    print "not empty"
    
f.write("lolx")

