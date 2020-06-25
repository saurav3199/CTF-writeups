#!/usr/bin/python3

from pwn import *
from Crypto.Util.number import isPrime
flag = ["*" for i in range(301)]

for i in range(2,302):
	if not isPrime(i):
		continue
	if "*" not in flag:
		exit()
	r = remote("2020.redpwnc.tf", 31284)
	r.recv()
	r.sendline(str(i-1))
	r.recv()
	r.sendline(str(i))
	xored = r.recv().split()[-1]
	for j in range(0,301,i):
		val = str((xored[j]-ord('0')) ^ 1) # Bit-Flipping
		if flag[j] == "*":
			flag[j] = val
		else:
			try:
				assert( val == flag[j])
			except:
				print("Logical Error") # to check the integrity
				exit()
	cur_flag = "".join(flag).replace("*","1")
	Current_flag = ""
	for part in range(0,len(cur_flag),7):
		Current_flag+=chr(int(cur_flag[part:part+7],2))
	print(f"Flag after {i} operations:{Current_flag}")
	r.close()

# flag{bits_leaking_out_down_the_water_spout}