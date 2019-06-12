from functools import reduce
from gmpy2 import *

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * invert(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def crack_unknown_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return crack_unknown_multiplier(states, modulus)


st=input("enter the states:")
g=st
for i in range(len(g)):
	g[i]^= 29486316         # the lucky number
#print("treasure",g)        #check for purpose 
flag="hsctf{"
m=[]
for i in range(len(flag)):
	if g[i]%ord(flag[i])==0:
		m+=[g[i]//ord(flag[i])]
		

n,k,d = crack_unknown_modulus(m)
print('modulo-> %d \t multiplier-> %d \t increment -> %d ' % (n,k,d))
state = m[-1]

w=[m[0]]
for q in range(1,70):
    w+= [(w[q-1]*k+d) % n]       # the sequence

if m==w[:6]:
    print("this worked")         # usual check
ans=[]
for i in range(70):
    ans+=[g[i]//w[i]]            #generating flag

print(''.join(chr(i) for i in ans))
