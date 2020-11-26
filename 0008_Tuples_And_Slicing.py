#!/usr/bin/env python

aTuple = ( 0, 1, 'Two', 3, 'Four', 'V', 6 )
eTuple = ( 'A', 'B', 'C' )

print aTuple

print "0th element = %s" % aTuple[0]
print "5th element = %s" % aTuple[5]
print "Last element = %s" % aTuple[-1]

print "2nd-4th = ", aTuple[2:5]
print "0th-Last but one = ",  aTuple[:-1]

print "aTuple[0] = 'Zero' is illegal"

print "aTuple.insert(-1, 'Actual Six') is illegal"

print "aTuple.extend(eTuple) is illegal"

# Tuples are generic arrays like lists, but read-only
# Syntax (
# https://developers.google.com/edu/python
# Unlike list, for tuple, all elements are not converted to string when using print

