
## CHUNK NORRIS-:

> 98pts |  Easy

Chunk Norris is black belt in fast random number generation.


challenge.py
```python
#!/usr/bin/python3 -u

import random
from Crypto.Util.number import *
import gmpy2

a = 0xe64a5f84e2762be5
chunk_size = 64

def gen_prime(bits):
  s = random.getrandbits(chunk_size)

  while True:
    s |= 0xc000000000000001
    p = 0
    for _ in range(bits // chunk_size):
      p = (p << chunk_size) + s
      s = a * s % 2**chunk_size
    if gmpy2.is_prime(p):
      return p

n = gen_prime(1024) * gen_prime(1024)
e = 65537
flag = open("flag.txt", "rb").read()
print('n =', hex(n))
print('e =', hex(e))
print('c =', hex(pow(bits_to_long(flag), e, n)))
```

output.txt
```
n = 0xab802dca026b18251449baece42ba2162bf1f8f5dda60da5f8baef3e5dd49d155c1701a21c2bd5dfee142fd3a240f429878c8d4402f5c4c7f4bc630c74a4d263db3674669a18c9a7f5018c2f32cb4732acf448c95de86fcd6f312287cebff378125f12458932722ca2f1a891f319ec672da65ea03d0e74e7b601a04435598e2994423362ec605ef5968456970cb367f6b6e55f9d713d82f89aca0b633e7643ddb0ec263dc29f0946cfc28ccbf8e65c2da1b67b18a3fbc8cee3305a25841dfa31990f9aab219c85a2149e51dff2ab7e0989a50d988ca9ccdce34892eb27686fa985f96061620e6902e42bdd00d2768b14a9eb39b3feee51e80273d3d4255f6b19
e = 0x10001
c = 0x6a12d56e26e460f456102c83c68b5cf355b2e57d5b176b32658d07619ce8e542d927bbea12fb8f90d7a1922fe68077af0f3794bfd26e7d560031c7c9238198685ad9ef1ac1966da39936b33c7bb00bdb13bec27b23f87028e99fdea0fbee4df721fd487d491e9d3087e986a79106f9d6f5431522270200c5d545d19df446dee6baa3051be6332ad7e4e6f44260b1594ec8a588c0450bcc8f23abb0121bcabf7551fd0ec11cd61c55ea89ae5d9bcc91f46b39d84f808562a42bb87a8854373b234e71fe6688021672c271c22aad0887304f7dd2b5f77136271a571591c48f438e6f1c08ed65d0088da562e0d8ae2dadd1234e72a40141429f5746d2d41452d916
```


### Solution: 

We are given a challenge script file which takes contents of *flag.txt* file as a message and encrypts it using RSA cryptosystem. And then we are provided with "c" ciphertext and (n,e) public-key pair. Simple enough!


The security of RSA cryptosystem lies in the generation of the public-key. If the modulus used "n" is factorable then its easily breakable. And the challenge description also suggests that public key is generated by "fast random number generation technique" and that must be weak!!


Okay so let's debug gen_prime() function which takes number of bits as 1024:
```python
s = random.getrandbits(chunk_size)            # generate random 64 bits
s|= 0xc000000000000001     
for _ in range(16):
	p = p << 64 + s
	s = a*s%2**64
```

So the value of s changes after each loop and at the end, if the generated p is prime then it sent back otherwise the last value of s is reused again for the next generation. Though it will be again random so we don't need to take care of it.

In polynomial representation, we can represent p as
```
x = 2^64
p = (s)*(x^15) + (a*s)*(x^14) + (a*a*s)*(x^13) + ... + (a^15*s)
```

_Note : Each term is calculated modulo x and same will be used from now on, for e.g. here s is s%r._

Similarly, for next number q

```
q = (t)*(x^15) + (a*t)*(x^14) + (a*a*t)*(x^13) + ... + (a^15*t)
```

Multiplying p * q
```python
n = (s*t)*x^30 
	+ ( (a*s)*(t) +  (s)*(a*t) )*x^29 
	+ ( (a*a*s)*(t) + (a*s)*(a*t) +(s)*(a*a*t) )*x**28
	+ ...
	+ ( (a^14*s)*(a^15*t) + (a^15*s)*(a^14*t) )*x
	+ ( (a^15*s)*(a^15*t) )*1
```

<hr/>

So we need to take two things into notice:
1) Overflow
2) Number of terms needed in the polynomial expression to solve for s & t.



For 1st case, overflow can be caused here because of multiplication( treat it same as we encounter overflow in a decimal multiplication) and as a result, we greedily can take use of first 64 bits of n and last 64 bits of n. That answers for our second case as well. If we manage to get required s & t from that then we can regenerate p and q from it.


* For the first half:   First 64 bits of (s\*t) ==  First 64 bits of N

> Is it right? No, because we didn't account for the overflow that can be caused by the addition of the next 64 bits of(s\*t) and between the second expression. The maximum value of that overflow can be 1.


* For the second half:

> If we have to take care about values under modulo x then last value is `a^30*s*t` so we can simply calculate last 64 bits of (s\*t) as
`inverse(a^30,x)*(Last 64 bytes of N)`


Let's find them first:
```python
r = 2**64
first_half = n//(2**(2048-64)) - 1
second_half = inverse(a**30,r)*(n%r) %r

seed_prduct = first_half*r + second_half
print(hex(seed_product))
# 0xab802dca026b182478adce5060bd0eb1
```
And then factorise (s\*t) to get s & t together to get the primes accordingly.
So we can factorize this 128-bit number easily either using online sources like [factordb](http://factordb.com/) or [alperton program](https://www.alpertron.com.ar/ECM.HTM) which uses fast algorithms like [ECM](https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization) and [SIQS](http://www.mersennewiki.org/index.php/Self-Initializing_Quadratic_Sieve).

`3 * 5 * 41 * 43 * 509 * 787 * 31601 * 258737 * 28110221 * 93627982031`

And using those factors calculate p & q to get the flag :)


```python
from Crypto.Util.number import *

p = 152502124356100186048786584829816790951655306938554698381698516601140428798527485382577251685142660191666259802101357483152615284884054484645840626070726530443669580292854859145584666559430830034877567195195160870921467137859654581026067555226827127667674180022694309303154807908193178891551927991884659577259 
q = 141964956842752227248825926479699850723242530500694299313985420916497490762457584872482228917124059114703818621232802014903763726586933292312009226271853350101621181936884771804789258383198041375410984842224059398802858374416574235073826923494095170442408144974244355981836859001182779710177024561285836339787

assert n == p*q
h = (p-1)*(q-1)
d = inverse(e,h)
print(long_to_bytes(pow(c,d,n)).decode())
```


This is our final simple solution script:

```python
from Crypto.Util.number import *
import gmpy2
from sympy import divisors

n = 0xab802dca026b18251449baece42ba2162bf1f8f5dda60da5f8baef3e5dd49d155c1701a21c2bd5dfee142fd3a240f429878c8d4402f5c4c7f4bc630c74a4d263db3674669a18c9a7f5018c2f32cb4732acf448c95de86fcd6f312287cebff378125f12458932722ca2f1a891f319ec672da65ea03d0e74e7b601a04435598e2994423362ec605ef5968456970cb367f6b6e55f9d713d82f89aca0b633e7643ddb0ec263dc29f0946cfc28ccbf8e65c2da1b67b18a3fbc8cee3305a25841dfa31990f9aab219c85a2149e51dff2ab7e0989a50d988ca9ccdce34892eb27686fa985f96061620e6902e42bdd00d2768b14a9eb39b3feee51e80273d3d4255f6b19
e = 0x10001
c = 0x6a12d56e26e460f456102c83c68b5cf355b2e57d5b176b32658d07619ce8e542d927bbea12fb8f90d7a1922fe68077af0f3794bfd26e7d560031c7c9238198685ad9ef1ac1966da39936b33c7bb00bdb13bec27b23f87028e99fdea0fbee4df721fd487d491e9d3087e986a79106f9d6f5431522270200c5d545d19df446dee6baa3051be6332ad7e4e6f44260b1594ec8a588c0450bcc8f23abb0121bcabf7551fd0ec11cd61c55ea89ae5d9bcc91f46b39d84f808562a42bb87a8854373b234e71fe6688021672c271c22aad0887304f7dd2b5f77136271a571591c48f438e6f1c08ed65d0088da562e0d8ae2dadd1234e72a40141429f5746d2d41452d916

chunk_size ,  bits = 64 , 1024
a = 0xe64a5f84e2762be5
r = 2**chunk_size

first_half = n//(2**(2048-64)) - 1
second_half = inverse(a**30,r)*(n%r) %r
seed_product = first_half*r + second_half

def getprime(s):
	p = 0
	for _ in range(bits // chunk_size):
		p = (p << chunk_size) + s
		s = a * s % 2**chunk_size
	return p if gmpy2.is_prime(p) else 0

candidates = divisors(seed_product)
for each in candidates:
	s,t = each , seed_product//each
	p,q = getprime(s),getprime(t)
	if p*q == n:break

h = (p-1)*(q-1)
d = inverse(e,h)
print(long_to_bytes(pow(c,d,n)).decode())
```

> CTF{__donald_knuths_lcg_would_be_better_well_i_dont_think_s0__}

Voila!!