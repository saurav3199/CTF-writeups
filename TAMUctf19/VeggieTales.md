# Description:
It's my favorite show to watch while practicing my python skills! I've seen episode 5 at least 13 times.

nc pwn.tamuctf.com 8448

Difficulty: easy-medium

2.23 1:58 pm CST: Added hint to description

# Solution:

So if you look at the episode no. 5 you see pickle intending us to check for pickle vulnerability

When you see the pickle documentation:

***Warning** The pickle module is not secure against erroneous or maliciously constructed data.
Never unpickle data received from an untrusted or unauthenticated source.*

So on searching for exploiting vulnerablity we found a [link](https://blog.nelhage.com/2011/03/exploiting-pickle/)

we wrote a [script](https://github.com/saurav3199/CTF-writeups/blob/master/TAMUctf19/veggie.py) based on that


# Caution:

Don't try to test it locally as it messes.You know the warning as well.
