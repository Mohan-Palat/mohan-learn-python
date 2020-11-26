#!/usr/bin/env python

s = "this is a string, a"

print '<'+s+'>'
print '<'+s[-2:]+'>'
print '<'+s[:-3]+'>'
print '<'+s[:-3]+s[-2:]+'>'

# https://stackoverflow.com/questions/1010961/string-slicing-python
# s = "this is a string, a"
# where ','(comma) will always be the 3rd last character, aka s[-3].
# I am thinking of ways to remove the ',' but can only think of 
# converting the string into a list, deleting it, and converting it back to a string. 
# This however seems a bit too much for simple task. 
# How can i accomplish this in a simpler way?

# Normally, you would just do:
# s = s[:-3] + s[-2:]
# The s[:-3] gives you a string up to, but not including, the comma you want removed ("this is a string") and 
# the s[-2:] gives you another string starting one character beyond that comma (" a").
# Then, joining the two strings together gives you what you were after ("this is a string a").



