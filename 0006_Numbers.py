#!/usr/bin/env python

import decimal

i = 25
l = 2000000000000000000L
b = True
f = 25.12745678
c = 6.23 + 1.5j

print 'I = %d, L = %ld %ld' % (i, l, l + 9876543210)

print b
print "%d" % b 
b = not b
print b
print "%d" % b 

print 'Format 5.3f %5.3f' % f
print 'Format 05.3f %05.3f' % f

TWOPLACES = decimal.Decimal('0.01')
d = decimal.Decimal(str(f)).quantize(TWOPLACES)
print d
FIVEPLACES = decimal.Decimal('0.00001')
d = decimal.Decimal(str(f)).quantize(FIVEPLACES)
print d

# String Formatting
# https://docs.python.org/2/library/string.html#format-string-syntax
pi = 3.141592653589793
print '{0:.2f}'.format(pi)

# Integer
# Long (As much as there is virtual memory)
# Boolean (True - 1, False - 0)
# Floating Point
# Complex
# Decimal implemented as a class for more accuracy
# All numeric types (except complex) support the following operations, sorted by ascending priority 
# (operations in the same box have the same priority; 
#        all numeric operations have a higher priority than comparison operations):        
#         
# Operation      Result                                   Notes
# -------------- ---------------------------------------- -----
# x + y          sum of x and y    
# x - y          difference of x and y    
# x * y          product of x and y    
# x / y          quotient of x and y                      -1
# x // y         (floored) quotient of x and y            -5
# x % y          remainder of x / y                       -4
# -x             x negated    
# +x             x unchanged    
# abs(x)         absolute value or magnitude of x    
# int(x)         x converted to integer                   -2
# long(x)        x converted to long integer              -2
# float(x)       x converted to floating point    
# complex(re,im) a complex number with real part re, 
#                imaginary part im. im defaults to zero.    
# c.conjugate()  conjugate of the complex number c    
# divmod(x, y)   the pair (x // y, x % y)                 (3)(4)
# pow(x, y)      x to the power y    
# x ** y         x to the power y    
#         
# Notes: 
# (1)   For (plain or long) integer division, the result is an integer. 
#       The result is always rounded towards minus infinity: 1/2 is 0, (-1)/2 is -1, 1/(-2) is -1, and (-1)/(-2) is 0. 
#       Note that the result is a long integer if either operand is a long integer, regardless of the numeric value.  
# (2)   Conversion from floating point to (long or plain) integer may round or truncate as in C; 
#       see functions floor() and ceil() in the math module for well-defined conversions.  
# (3)   See section 2.1, ``Built-in Functions,'' for a full description. 
# (4)   Complex floor division operator, modulo operator, and divmod(). 
#       Deprecated since release 2.3. Instead convert to float using abs() if appropriate.
# (5)   Also referred to as integer division. The resultant value is a whole integer, 
#       though the result's type is not necessarily int. 
# 
# The decimal module was designed to support 
#       "without prejudice, both exact unrounded decimal arithmetic (sometimes called fixed-point arithmetic) 
#        and rounded floating-point arithmetic."

