#!/usr/bin/env python

aList = [ 0, 1, 'Two', 3, 'Four', 'V', 6]
eList = [ 'A', 'B', 'C' ]

print aList

print "0th element = %s" % aList[0]
print "5th element = %s" % aList[5]
print "Last element = %s" % aList[-1]

print "2nd-4th = %s" % aList[2:5]
print "0th-Last but one = %s" % aList[:-1]

aList[0] = 'Zero'
print aList

aList.insert(-1, 'Actual Six')
print aList

aList.extend(eList)
print aList

# Lists are generic arrays
# Syntax = [
# 1.list.append(elem) -- adds a single element to the end of the list. ... 
# 2.list.insert(index, elem) -- inserts the element at the given index, shifting elements to the right.
# 3.list.extend(list2) adds the elements in list2 to the end of the list.
# https://developers.google.com/edu/python

