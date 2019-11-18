from pwn import *
import time

r =  remote('ctfchallenges.ritsec.club',8001)
output=r.recv().split()
output[3:-2]=[]
nums=list(map(int,output))
print(nums)

p = process(['./a.out']+[str(i) for i in nums])

data=p.recvall().strip().split(" ")
print(data)
r.recvuntil('number?')
r.sendline(data[0])
r.interactive()
r.close()