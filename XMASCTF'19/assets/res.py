#!/usr/bin/env python
import re
import base64
import hashlib
from pwn import*


def breakit(target):
    iters = 0
    while 1:
        s = str(iters)
        iters = iters + 1
        try:
            hashed_s = hashlib.sha256(s.decode("hex")).hexdigest()
        except:
            continue
        r = re.match('^0e[0-9]{27}', hashed_s)
        if hashed_s[-6:]==target:
            print "[+] found! sha256( {} ) ---> {}".format(s, hashed_s)
            return s
        if iters % 1000000 == 0:
            print "[+] current value: {}       {} iterations, continue...".format(s, iters)


r=remote("challs.xmas.htsp.ro",14004)       # server to connect 

target=r.recv().split()[-1]
print(target)
foundhash=breakit(target)
print(foundhash)
r.sendline(foundhash)
print(r.recv())
print(r.recv())

r.close()