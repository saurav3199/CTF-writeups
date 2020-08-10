#!/usr/bin/env python3

from Crypto.Util.number import isPrime, getPrime, getRandomRange, bytes_to_long
from flag import flag

def keygen():
    p = getPrime(1024)
    q = p**2 + (1<<256)
    while not(isPrime(q)):
        q += 2
    n = p**2 * q
    while True:
        g = getRandomRange(2, n-1)
        if pow(g, p-1, p**2) != 1:
            break
    return (g, n), p

def encrypt(pubkey, msg):
    g, n = pubkey
    msgint = bytes_to_long(msg)
    encint = pow(g, msgint, n)
    return encint

wfile = open('output.txt', 'w')

pubkey, privkey = keygen()

print(privkey)
wfile.write('g = ' + str(pubkey[0]) + '\n')
wfile.write('n = ' + str(pubkey[1]) + '\n')

encint = encrypt(pubkey, flag)
wfile.write('enc = ' + str(encint) + '\n')

wfile.close()

