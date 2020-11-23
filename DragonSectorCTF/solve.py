from pwn import *
from base64 import *
from Crypto.Util.number import *
from Crypto.Cipher import AES
import subprocess
from task import Rng, DiffieHellman


def POW(r):
   print("----------Solving POW-----------")
   command = r.recv().strip().split(b": ")[-1]
   hashed = subprocess.check_output(command, shell=True).strip()
   r.sendline(hashed)
   print("----------Solved----------------")


def sendloop(r, i: int):
   r.recv()
   a = b64encode(long_to_bytes(i, 32))
   r.sendline(a)
   iters = int(r.recvline().strip().split(b" ")[2])
   bob_number = int(r.recvline().strip().split(b" ")[-1])   # bob number
   iv = b64decode(r.recvline().strip())      # IV
   ciphertext = b64decode(r.recvline().strip())    # ciphertext
   return iters, bob_number, iv, ciphertext


def get_flag(seed, bob_number, iv, ciphertext):
   alice = DiffieHellman(long_to_bytes(int(seed, 2)))
   shared = pow(bob_number, alice.my_secret, alice.prime)
   cipher = AES.new(long_to_bytes(shared, 16)[:16], AES.MODE_CBC, IV=iv)
   flag = cipher.decrypt(ciphertext)
   return flag


r = remote("bitflip1.hackable.software", 1337)
POW(r)
bits = ""

for pos in range(1, 128):
   nums = 0 if bits == '' else int(bits, 2)*2
   flippedbit = 1 << pos | ((nums//2) ^ ((1 << (pos-1))-1))*2
   iters1, iters2 = sendloop(r, nums)[0], sendloop(r, flippedbit)[0]
   assert iters2 != 0         # to check they generate the same prime, if not rerun script
   bits = "1" + bits if iters1 + 1 == iters2 else "0" + bits

iters, bob_number, iv, ciphertext = sendloop(r, 0)
#guessing LSB
flag = get_flag(bits+"0", bob_number, iv, ciphertext)
print(flag)
flag = get_flag(bits+"1", bob_number, iv, ciphertext)
print(flag)

r.close()
