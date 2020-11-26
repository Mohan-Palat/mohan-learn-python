#!/usr/bin/env python

import sys

class HelloWorld(object):
    """ A Hello World Class """

    stava = 25

    def __init__(self, name):
        """ Initialize with name for the object """
        self.name = name
        print "My Name is", self.name
        print "I belong to" 
    
    def set_age(self, age=0):
        """ Introduce and initialize age attribute """
        self.age = age
    
    def print_attribs(self):
        """ Display Attributes """
        names = self.name.split()
        print "The name is %s. %s %s." % (names[1], names[0], names[1]) 

print 'ARGC', len(sys.argv)
if len(sys.argv) > 1: 
    hw = HelloWorld(sys.argv[1])
else:
    hw = HelloWorld('Maltova Navarathnakurma')
hw.print_attribs()    
print 'Static Variable', hw.stava



