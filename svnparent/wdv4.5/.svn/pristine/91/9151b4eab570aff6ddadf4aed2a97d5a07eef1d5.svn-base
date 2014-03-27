'''
Created on 26-Mar-2014

@author: Abhimanyu
'''


import sys

f = open(sys.argv[1], "r")
o = open("%s_indented"%sys.argv[1], "w")

for line in f:
    i=0
    line = list(line)
    while line[i] == "\t":
        line[i] = "&nbsp&nbsp&nbsp&nbsp"
        i+=1
    o.write("".join(line))
    


