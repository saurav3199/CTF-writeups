Writeup for solved challenge in DragonSectorCTF 2020

# **CRYPTO**

## Bit Flip I-:
> description:

Flip bits and decrypt communication between Bob and Alice.

`nc bitflip1.hackable.software 1337`

[task.tgz](assets/tasks.tgz)


```python
#!/usr/bin/python3

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
import hashlib
import os
import base64
from gmpy2 import is_prime

FLAG = open("flag").read()
FLAG += (16 - (len(FLAG) % 16))*" "


class Rng:
  def __init__(self, seed):
    self.seed = seed
    self.generated = b""
    self.num = 0

  def more_bytes(self):
    self.generated += hashlib.sha256(self.seed).digest()
    self.seed = long_to_bytes(bytes_to_long(self.seed) + 1, 32)
    self.num += 256


  def getbits(self, num=64):
    while (self.num < num):
      self.more_bytes()
    x = bytes_to_long(self.generated)
    self.num -= num
    self.generated = b""
    if self.num > 0:
      self.generated = long_to_bytes(x >> num, self.num // 8)
    return x & ((1 << num) - 1)


class DiffieHellman:
  def gen_prime(self):
    prime = self.rng.getbits(512)
    iter = 0
    while not is_prime(prime):
      iter += 1
      prime = self.rng.getbits(512)
    print("Generated after", iter, "iterations")
    return prime

  def __init__(self, seed, prime=None):
    self.rng = Rng(seed)
    if prime is None:
      prime = self.gen_prime()

    self.prime = prime
    self.my_secret = self.rng.getbits()
    self.my_number = pow(5, self.my_secret, prime)
    self.shared = 1337

  def set_other(self, x):
    self.shared ^= pow(x, self.my_secret, self.prime)

def pad32(x):
  return (b"\x00"*32+x)[-32:]

def xor32(a, b):
  return bytes(x^y for x, y in zip(pad32(a), pad32(b)))

def bit_flip(x):
  print("bit-flip str:")
  flip_str = base64.b64decode(input().strip())
  return xor32(flip_str, x)


alice_seed = os.urandom(16)

while 1:
  alice = DiffieHellman(bit_flip(alice_seed))
  bob = DiffieHellman(os.urandom(16), alice.prime)

  alice.set_other(bob.my_number)
  print("bob number", bob.my_number)
  bob.set_other(alice.my_number)
  iv = os.urandom(16)
  print(base64.b64encode(iv).decode())
  cipher = AES.new(long_to_bytes(alice.shared, 16)[:16], AES.MODE_CBC, IV=iv)
  enc_flag = cipher.encrypt(FLAG)
  print(base64.b64encode(enc_flag).decode())
```


### Solution: 

On analysing the challenge script we can deduce that [Diffie Hellman Key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) was done by Bob with alice multiple times. We only have the control over bit-flip and as the challenge description suggested we have to make the use of it to get the alice seed (because recovering seed for Bob is not easy).

There's a strange piece of information was given to us in the form of number of iterations used to calculate prime.

Let's have a look over Rng as how prime was generated:
In getbits function, this block was never visited when 512 is sent to self.num:
```python
if self.num > 0:
      self.generated = long_to_bytes(x >> num, self.num // 8)
```
thus allowing self.generated to be clean again for the next call . That's the flaw in the code which means prime for seed = i and i+2 will be same. 

Manually testing the code:
```
seed =  b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'                                             
Generated after 83 iterations                                                                 
prime = 3217336996812784199323541050098699361781489187527078355681535168764692913032949200158631425936108602790839091441050033248993143847385123136499734649619637                                                                                                      

seed = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'                                                         
Generated after 82 iterations                                                                 
prime = 3217336996812784199323541050098699361781489187527078355681535168764692913032949200158631425936108602790839091441050033248993143847385123136499734649619637  
```

So if we flip the second last bit then it's 0 if the iteration count decreased otherwise 1.

The implementation for rest of the bytes are tricky and in the end we have to brute for the last byte as its either 0 or 1.

#### Implementation:


Suppose we find upto X'th bit , then we have to guess  for `.....x10100b` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (last bit is b and it's undecided)<br/>
we can have iteration count &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for `.....x00000b`<br/>
and 
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; for                         `.....011111b` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(by flipping the bits)<br/>

as the difference between them is 2 so we will have one less iteration count if the bit was 1 otherwise 0.

Solution [script](/solve.py):

In beginning we have to solve POW which is same as asked in [GoogleCTF'17](https://github.com/google/google-ctf/blob/master/2017/quals/2017-pwn-cfi/challenge/hashcash.py).

```python
from pwn import *
from base64 import *
from Crypto.Util.number import *
from Crypto.Cipher import AES
import subprocess
from task import Rng , DiffieHellman

def POW(r):
   print("----------Solving POW-----------")
   command = r.recv().strip().split(b": ")[-1]
   hashed = subprocess.check_output(command,shell=True).strip()
   r.sendline(hashed)
   print("----------Solved----------------")

def sendloop(r,i: int):
   r.recv()
   a = b64encode(long_to_bytes(i,32))
   r.sendline(a)
   iters = int(r.recvline().strip().split(b" ")[2])
   bob_number = int(r.recvline().strip().split(b" ")[-1])   # bob number
   iv = b64decode(r.recvline().strip())      # IV
   ciphertext = b64decode(r.recvline().strip())    # ciphertext
   return iters,bob_number,iv,ciphertext


def get_flag(seed,bob_number,iv,ciphertext):
   alice = DiffieHellman(long_to_bytes(int(seed,2)))
   shared = pow(bob_number,alice.my_secret,alice.prime)
   cipher = AES.new(long_to_bytes(shared,16)[:16] , AES.MODE_CBC , IV= iv)
   flag = cipher.decrypt(ciphertext)
   return flag


r = remote("bitflip1.hackable.software",1337)
POW(r)
bits = ""

for pos in range(1,128):
   nums = 0 if bits=='' else int(bits,2)*2
   flippedbit = 1<<pos | ((nums//2)^((1<<(pos-1))-1))*2
   iters1, iters2 = sendloop(r,nums)[0], sendloop(r,flippedbit)[0]
   assert iters2 != 0         # to check they generate the same prime, if not rerun script
   bits = "1" + bits if iters1 +1 == iters2 else "0" + bits

iters,bob_number,iv,ciphertext = sendloop(r,0)
#guessing LSB
flag = get_flag(bits+"0",bob_number,iv,ciphertext)
print(flag)
flag = get_flag(bits+"1",bob_number,iv,ciphertext)
print(flag)

r.close()
```

Running the script gives the result: 
```
/DragonSectorCTF$ python solve.py 
[+] Opening connection to bitflip1.hackable.software on port 1337: Done
----------Solving POW-----------
----------Solved----------------
Generated after 286 iterations
b'DrgnS{T1min9_4ttack_f0r_k3y_generation}\n        '
Generated after 253 iterations
b'XI\x18T\x1c\xd0m\x81\xc8\x06=\xb81\x93\xa9\x01X\xb3}\xf06\xea\xf2\x95_\x87E\xa2\x14z\x9d\xbd;1\xd1\x01\xd6\xc4))\x1bO\xe7\xf0\xbaxeC'
[*] Closed connection to bitflip1.hackable.software port 1337
```

Here is our flag: `DrgnS{T1min9_4ttack_f0r_k3y_generation}`
Voila!
