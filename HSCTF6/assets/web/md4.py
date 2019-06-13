import hashlib
import re,sys
from Crypto.Hash import MD4

def breakit():
    prefix="0e"
    s=0
    while 1:
                s+=1
                st=prefix+str(s)
                hashed_s= hashlib.new('md4', st).hexdigest()
                if hashed_s[:2]=="0e" and hashed_s[2:].isdigit():
                    print "[+] found! md4( {} ) ---> {}".format(st, hashed_s)
                    sys.exit(0)
                if s%10000000==0:
                    print("[+] %d iterations done"%(s))

breakit()
