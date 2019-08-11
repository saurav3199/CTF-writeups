ASIS members conducted excellent crypto CTF.I will recommend everyone to solve it by themselves ,you will learn new concepts by solving them.
Here are some of them I was able to solve it.

## roXen -:
> description: 

Relationship with a cryptographer!
The Girlfriend: All you ever care about is crypto! I am sick of it! It's me or crypto!

The Cryptographer boyfriend: You meant to say it's you [XOR](roxen.py) cryptography.

The Girlfriend: I am leaving you.



22 solves

### Solution:
 
The given script:

```python
#!/usr/bin/env python

from Crypto.Util.number import *
from secret import exp, flag, nbit

assert exp & (exp + 1) == 0

def adlit(x):
    l = len(bin(x)[2:])
    return (2 ** l - 1) ^ x

def genadlit(nbit):
    while True:
        p = getPrime(nbit)
        q = adlit(p) + 31337
        if isPrime(q):
            return p, q

p, q = genadlit(nbit)
e, n = exp, p * q

c = pow(bytes_to_long(flag), e, n)

print 'n =', hex(n)
print 'c =', hex(c)
```
Lets, start from the top:

So exp&(exp+1)==0 that just means exp must be a [Mersenne number](http://mathworld.wolfram.com/MersenneNumber.html). Then adlit(x) is returning  the xored of passed number with the next biggest possible number with same length of bits which means basically that returned number contains reversed bits of passed number then i realised that it's nothing difficult if you know the bits length you can just subtract the number from that max length bit number.
>For eg. adlit(44) + 44 = 63, adlit(120) +adlit(120) =127.
Simple isn't it

So we know n is 2048 bits long so p and q might be 1024 bits prime number.Let's check for it. 
`p+adlit(p)==2**1024-1`
So we get two equations from here `p+q=2**1024+31336` and `p*q=n`. Two equations two vars->quadratic `p**2 -(2**1024 +31336)*p + n = 0`.  Sympy will do the work.Using solve() for quadratic function we get: 
```
p = 91934396941118575436929554782758166784623142015203107928295225306949429527662253180027648166060067602233902389535868116051536080388999480377007211745229221564969130373120800620379012435790356909945473565305296926519232706950561924532325538399351352696805684504904629096892037592742285758390953849377910498739
q = 87834916545113015336000964296144306577174555879027549345134855850783246277838709952680829156347468418886211490335525241607253688425417142115840218894244902812798763051744684655923207165455737209507609386779708842318917975391900956941587572141475884466544826179681669143055208345737430546444402480246313669813
```
That was long thinking much left to travel ::wink::

Then, bruting public exponent

```python
while i :
    i+=1
    e=2**i-1
    if(gcd(e,h)==1):
        d=invert(e,h)
        if "CCTF" in (long_to_bytes(pow(c,d,n))):
            print (long_to_bytes(pow(c,d,n)))
            exit(0)
```
No result it went further around 100000 bits.
So i don't know the maths here but i was quite sure that it should be less than 2048 as then it will be greater than n.
Then I approached admin Factoreal for it. Then he told me what happen if gcd(e,phi) not equal to 1. So after tinkering around with my teammates I come to the point that's not possible LOL because we don't know but then I realised it that I have seen this things before after searching we get to know we can use precision for it. And we solved this after solving Clever girl question which boosted up our confidence for going with precision.


So here was the final [script](script.py):


```python
from Crypto.Util.number import *
import gmpy2
import pwn

gmpy2.get_context().precision=10000

def adlit(x):
    l = len(bin(x)[2:])
    return (2 ** l - 1) ^ x

p = 91934396941118575436929554782758166784623142015203107928295225306949429527662253180027648166060067602233902389535868116051536080388999480377007211745229221564969130373120800620379012435790356909945473565305296926519232706950561924532325538399351352696805684504904629096892037592742285758390953849377910498739
q = 87834916545113015336000964296144306577174555879027549345134855850783246277838709952680829156347468418886211490335525241607253688425417142115840218894244902812798763051744684655923207165455737209507609386779708842318917975391900956941587572141475884466544826179681669143055208345737430546444402480246313669813
n = 0x3ff77ad8783e006b6a2c9857f2f13a9d896297558e7c986c491e30c1a920512a0bad9f07c5569cf998fc35a3071de9d8b0f5ada4f8767b828e35044abce5dcf88f80d1c0a0b682605cce776a184e1bcb8118790fff92dc519d24f998a9c04faf43c434bef6c0fa39a3db7452dc07ccfced9271799f37d91d56b5f21c51651d6a9a41ee5a8af17a2f945fac2b1a0ea98bc70ef0f3e37371c9c7b6f90d3d811212fc80e0abcd5bbefe0c6edb3ca6845ded90677ccd8ff4de2c747b37265fc1250ba9aa89b4fd2bdfb4b4b72a7ff5b5ee67e81fd25027b6cb49db610ec60a05016e125ce0848f2c32bff33eed415a6d227262b338b0d1f3803d83977341c0d3638f
c = 0x2672cade2272f3024fd2d1984ea1b8e54809977e7a8c70a07e2560f39e6fcce0e292426e28df51492dec67d000d640f3e5b4c6c447845e70d1432a3c816a33da6a276b0baabd0111279c9f267a90333625425b1d73f1cdc254ded2ad54955914824fc99e65b3dea3e365cfb1dce6e025986b2485b6c13ca0ee73c2433cf0ca0265afe42cbf647b5c721a6e51514220bab8fcb9cff570a6922bceb12e9d61115357afe1705bda3c3f0b647ba37711c560b75841135198cc076d0a52c74f9802760c1f881887cc3e50b7e0ff36f0d9fa1bfc66dff717f032c066b555e315cb07e3df13774eaa70b18ea1bb3ea0fd1227d4bac84be2660552d3885c79815baef661

assert isPrime(p)
assert isPrime(q)
assert adlit(p) + 31337 == q
assert p*q == n

h = (p-1)*(q-1)

for i in range(4096):
    e = 2**i - 1
    f = gmpy2.gcd(e,h)
    try: 
        d = gmpy2.invert(e//f,h)
        m = long_to_bytes(pow(gmpy2.mpz(pow(c,d,n)),1/f))
        #print(pow(gmpy2.mpz(pow(c,d,n)),1/3))
        if b"CCTF" in m:
            print("i = ", i)
            print(m)
    except:
        continue
 ```
 
 >Flag:CCTF{it5_3a5y_l1k3_5uNd4y_MOrn1N9}
 
 
 
 
