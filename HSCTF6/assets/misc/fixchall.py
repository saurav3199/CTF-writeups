import binascii
from itertools import cycle,izip

f=open("chall.png")
g=(f.read())
key="invisible"
cyphered = ''.join(chr(ord(c)^ord(k)) for c,k in izip(g, cycle(key)))
l=open("fixed.png","a+")
l.write(cyphered)
