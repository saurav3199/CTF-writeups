Hey guys back with another set of few writeups.

We did good and finished overall at 32nd in world and 1st in India.

![scores](assets/scores.png)

# **PPC**

## Orakel-:
> description:

We have finally linked up with the famous Lapland Oracle, that knows and sees all!
Can you guess his secret word?

Remote server: challs.xmas.htsp.ro 13000

### Solution: 

When we connect to the server,we were greeted with this

![image](assets/orakel_greeting.png)

We see that we can only send the alphabetic letters i.e [A-Z][a-z]. and for each string we get a number corresponding to it.
Sending random strings we get to know that it reaches a minima at certain length and that is random at each run.

![image](assets/orakel_guess.png)

The graph of function over value recieved at each character sent is not monotonic, its actually unimodal.
And on sending the correct composition of letters with the padding(to make the length required as expected) at end.Thus the perect searching algorithm to check each character at each run will be [ternary search](https://en.wikipedia.org/wiki/Ternary_search).


#### Several levels of optimization required:

So I tried to script it according to the algorithm as said here [ternary algo](https://cp-algorithms.com/num_methods/ternary_search.html) But that took around 80 chars right only out of 90 because of the complexity.

So contacting admin over this issue, he said there is also another version of ternary search that could help you with the better complexity. So after wandering around master's theorem I know, I'm using T(n)=T(2n/3) + 2  i.e. O(2\*log3(n)) and about that i can do better if i don't divide it into three parts rather dividing into just two parts and make the middle part 'void' . So that would make T(n)=T(n/2)+ 2 i.e. O(log2(n)). But that wasn't enough becuase of my algo procedure(that's my fault) . So after a bit of tinkering with minimizing the steps that I can use dictionary to not to send the same string again for evaluating function.

So that's the final [script](assets/opti_orakel.py) that will do the work:


```python
from pwn import *
import string
r=remote("challs.xmas.htsp.ro",13000)

r.recv()

char="a"               #for padding
l=1
h=200
length=0
steps=0
while l<h:
    mid1=(l+h)/2
    mid2=mid1+1
    r.sendline(mid1*char)
    key1=int(r.recv().split()[-5])
    r.sendline(mid2*char)
    key2=int(r.recv().split()[-5])
    steps+=2
    if(key1>key2):
        l=mid2
        print(mid2*char,key2)
        length=mid2
    else:
        h=mid1
        print(mid1*char,key1)
        length=mid1

print("length:",str(length))

dic={}
charset=sorted(string.letters)
flag="a"*length
for i in range(length):
    l=0
    h=len(charset)-1
    ans=0
    while l<h:
        mid1=(l+h)/2
        mid2=mid1+1

        c=charset[mid1]
        if(flag[:i]+c+flag[i+1:] in dic):
            key1=dic[flag[:i]+c+flag[i+1:]]
        else:
            r.sendline(flag[:i]+c+flag[i+1:])
            rec=r.recv()
            steps+=1
            if "MAS" in  rec:
                print(rec)
                r.interactive()
            else:
                key1=int(rec.split()[-5])
                dic[flag[:i]+c+flag[i+1:]]=key1

        d=charset[mid2]
        if(flag[:i]+d+flag[i+1:] in dic):
            key2=dic[flag[:i]+d+flag[i+1:]]
        else:
            r.sendline(flag[:i]+d+flag[i+1:])
            rec=r.recv()
            steps+=1
            if "MAS" in  rec:
                print(rec)
                r.interactive()
            else:
                key2=int(rec.split()[-5])
                dic[flag[:i]+d+flag[i+1:]]=key2
        if(key1>key2):
            print(flag[:i]+d+flag[i+1:],key2)
            l=mid2
            ans=mid2
        else:
            print(flag[:i]+c+flag[i+1:],key1)
            h=mid1
            ans=mid1
    flag=flag[:i]+charset[ans]+flag[i+1:]
    print("steps used so far: "+str(steps))
    print("Current target string: "+flag)


r.close()
```

Server response:

![image](assets/orakel_run0.png)
.............................................................................................

.............................................................................................

![image](assets/orakel_run2.png)
Full Response: [response](assets/response.txt)

Here is our flag:`X-MAS{7hey_h4t3d_h1m_b3c4use_h3_sp0k3_th3_truth}`

## Pythagoreic Pancakes-:
> description:

We got a weird transmission through space time from some guy that claims he's related to Santa Claus. He says that he has a really difficult problem that he needs to solve and he needs your help. Maybe it's worth investigating.

Remote server: nc challs.xmas.htsp.ro 14004

### Solution: 

When we connect to the server it asks to solve POW first to access it 
So I will be using this script for almost all challenges who required POW at the beginning.

```python
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
```

So now we can face the real challenge:

![image](assets/pyth_greeting.png)

So we are required to send the nth primitive pythagorean triplet in the requested order.And I am thinking that this n will increase over the levels.So I need to write a optimized code as , all ppc challenges are required to do.

So I searched wikilinks [wiki](https://en.wikipedia.org/wiki/Pythagorean_triple) and [formula that can generate it](https://en.wikipedia.org/wiki/Formulas_for_generating_Pythagorean_triples). And then I picked the euler formula for it.

#### NOTE : to avoid the triplets which are not 'primitive'  but generated and are in given form will be discarded using gcd. 

> a=k*(m\*m-n\*n) , b=k*(2\*m\*n) , c= k*(m\*m+n\*n)

That was an easy challenge overall i must say :) .

```python
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
```

![image](assets/pyth_flag.png) 



We got this full [response](assets/pyth_response.txt) for the above [script](assets/pyth_self.py)

Here is our flag:`X-MAS{Th3_Tr33_0f_pr1m1t1v3_Pyth4g0r34n_tr1ple5}`


