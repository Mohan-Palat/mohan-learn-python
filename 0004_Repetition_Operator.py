#!/usr/bin/env python

i = 25
s = 15 * '0'

print '015 Decimal = %015d' % i

print 'Repeat 0 15 = %s' % s

s += str(i)
print 's += i      = %s' % s

print 'Slice Only  = %s' % s[-15:] 

print 'Slice Repet = %s' % (15 * '0' + str(i))[-15:]

a = (15 * '0' + str(i))[-15:]
print 'Assigned    = ' + a

# In this example, printf is simpler, but for assigning we need the Slice Operation

