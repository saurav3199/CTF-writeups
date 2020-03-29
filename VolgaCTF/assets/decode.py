from pwn import *

def isQR(x, p):
    q = (p - 1) / 2
    return pow(x, q, p)

def func(y,p,ct_a,ct_b):
    output=-1
    if ((isQR(y, p) == 1) or (isQR(ct_a, p) == 1)):
        if isQR(ct_b, p) == 1:
            output = 1
        else:
            output = 0
    else:
        if isQR(ct_b, p) == 1:
            output = 0
        else:
            output = 1
    return str(output)

r=remote("guess.q.2020.volgactf.ru",7777)
y,p=eval(r.recvuntil("\n").split("=")[1])
print(y,p)
for i in range(1000):
    ct_a,ct_b=eval(r.recv())
    output=func(y,p,ct_a,ct_b)
    print(str(i)+": "+ output)
    r.sendline(output)
print(r.recv())
r.close()