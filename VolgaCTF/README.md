Few of the challenges that we were able to solve this time. Going to explain one of them.



# **CRYPTO**

## Guess-:
> description:

Try to guess all encrypted bits and get your reward!

[server.py](assets/server.py)

nc guess.q.2020.volgactf.ru 7777


### Solution: 

Well looking to the server script file, we couldn't find anything vulnerable to be exploited. After thinking and thinking my teammate found [the link](https://github.com/weikengchen/attack-on-libgcrypt-elgamal/blob/master/attack_libgcrypt.py) that was very helpful. Actually its the challenge present already on the web. I don't know why it was copied. It was an attack over ElGamal Implementation of libgcrypt. 

So I just used some part of the code from there and then made a connection between the netcat server and after 1000 turns we we got the flag. I tried to understand the vulnerability but I couldn't :disappointed:!

```python
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
    print(str(i)+output)
    r.sendline(output)
print(r.recv())
r.close()
```

Here is the flag : `VolgaCTF{B3_c4r3ful_with_4lg0rithm5_impl3m3nt4ti0n5}`



