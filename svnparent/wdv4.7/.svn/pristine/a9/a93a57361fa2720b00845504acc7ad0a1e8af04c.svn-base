'''
Created on 26-Mar-2014

@author: Abhimanyu
'''


import sys

f = open(sys.argv[1], "r")
o = open(sys.argv[2], "w")
count = 0

for line in f:
    count+=1
    i=0
    line = list(line)
    while line[i] == "\t":
        line[i] = "&nbsp&nbsp&nbsp&nbsp"
        i+=1
    o.write("".join(line))

print "done."
print "%d lines prosessed" %count


