#!/usr/bin/env python
import re
import base64
import hashlib
from pwn import*
import numpy as np
from gmpy2 import *

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


def triplets(limit):
    a=b=c=0
    m=2
    q=[]
    while c<limit:
        for n in range(1,m):
            a=m*m-n*n
            b=2*m*n
            c=m*m+n*n
            if c>limit:
                break
            if gcd(gcd(a,b),c)==1:
                q.append(sorted([a,b,c]))
        m+=1
    return q

lis=triplets(16000000)
lis=sorted(lis,key=lambda l:l[::-1])
print("The number of triplets generated:" +str(len(lis)))
file=open("triplets_list.txt","w")
file.write('\n'.join(str(j) for j in lis))

r=remote("challs.xmas.htsp.ro",14004)

target=r.recv().split()[-1]
print(target)
foundhash=breakit(target)
print(foundhash)
r.sendline(foundhash)
level=0
while 1:
    level+=1
    if level>10:
        print(r.recv())
        r.close()
        exit()
    print(r.recvuntil(":\n"))
    resp=r.recv().split()
    index=int(resp[3][:-3])
    ans=lis[index-1]
    data=','.join(str(i) for i in ans)
    print(data)
    r.sendline(data)
    print(r.recvuntil("\n"))

r.close()
