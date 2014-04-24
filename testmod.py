'''
Created on 18-Feb-2014

@author: Abhimanyu
'''



def h(e):
    e["a"] = "changed"   

def g():
    d = {"a":"S", "d": "D"}
    h(d)
    print d


g()

