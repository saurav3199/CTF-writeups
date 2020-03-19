from pwn import *
from sympy.ntheory import totient

def tet(a,x,p):
    if p==1 or x==0:
        return 1 
    phi=totient(p)
    return pow(a,tet(a,x-1,phi),p)

r=remote("crypto.2020.chall.actf.co",20603)
level=1

while 1:
    if level>10:
        print(r.recv())
        exit()
    print(r.recvuntil("...\n"))
    details=r.recv()
    values=details.split("\n")[:-1]
    print(values)
    p=int(values[0].split()[-1])
    a=int(values[1].split()[-1])
    b=int(values[2].split()[-1])
    x=0
    while 1:
        c=tet(a,x,p)
        if c == b:
            break
        x+=1
    print("x value : "  + str( x ) )
    r.sendline(str(x))
    level+=1

r.close()