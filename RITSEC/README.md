A jeopardy styled CTF : RITSEC CTF 2019 is a security-focused competition


We tried to solve challenges as much as possible we can and as a result we secured 22rd position globally.



# **MISC**

## Onion Layer Encoding-:
> description:

Encoding is not encryption, but what if I just encode the flag with base16,32,64? If I encode my precious flag for 150 times, surely no one will be able to decode it, right?

### Solution:

So we were given a large file with multiple  base encoded ciphertext

So we need to check the base first then decode it . To avoid this I actually took help of try catch error to do it fast .Here is the [script](script/onion.py):

```python
import base64
flag=open("onionlayerencoding.txt","r").read()
while "RITSEC" not in str(flag):
    try:
        flag=base64.b16decode(flag)
    except:
        try:
            flag=base64.b32decode(flag)
        except:
            flag=base64.b64decode(flag)

print(flag)
```
It give us the flag : __RITSEC{0n1On_L4y3R}__

PS: Weird thing is that its not 150 times it was 32 times only. Idk why :(



## Lunar Lander-:
> description: 

Starman!

We are trying to troubleshoot the guidance computer. You should already have the star tables, so we just need you to double check some of the distances for us. We aren't sure about the precision though so you may need to play with it.


### Solution:

We were given with the [distances.txt](scripts/distances.txt) file i.e. distances between Stars:

 ```
Star 18 => Star 11
Star 5 => Star 26
Star 25 => Star 5
Star 1 => Star 33
Star 34 => Star 2
Star 18 => Star 25
Star 17 => Star 9
Star 28 => Star 20
Star 34 => Star 6
Star 20 => Star 15
Star 36 => Star 34
Star 17 => Star 16
Star 9 => Star 11
Star 28 => Star 12
Star 13 => Star 16
Star 32 => Star 26
Star 29 => Star 30
Star 17 => Star 16
Star 7 => Star 12
Star 16 => Star 13
Star 22 => Star 17
Star 11 => Star 18
Star 1 => Star 33
Star 5 => Star 29
```

Everybody find it difficult or guessing enough before a hint arrived which said 

> *If you lost your copy of 'STAR TABLES', you should be able to find the 'open source' version*

So I searched for Star tables github and look for various codes until I found this one <https://github.com/chrislgarry/Apollo-11/blob/master/Comanche055/STAR_TABLES.agc> .On understanding the code I found the x,y,z coordiantes of stars were given. Reformatted that file using regex to get [this](scripts/STAR_TABLES.agc) file

```
+.8342971408 37 X
-.2392481515 37 Y
-.4966976975 37 Z
+.8139832631 36 X
-.5557243189 36 Y
+.1691204557 36 Z
+.4541086270 35 X
-.5392368197 35 Y
+.7092312789 35 Z
.................
.................
```
Well why we need to calculate distance? Will it give the flag ? On checking for first pair of stars I got something like 1.14 that is nothing but ascii code of 'R' i.e. 114

So we just need to calculate the distance between stars given to us. So I [scripted](scripts/obtain_stars.py) it

```python
from math import *

stars=open("STAR_TABLES.agc").read().split("\n")
dis=[[0 for i in range(3)] for j in range(40)] 
for i in stars:
    s=i.split(" ")
    val=float(s[0])
    pos=int(s[1])
    dis[pos][ord(s[2])-ord('X')]=val

def calc_distance(f,s):
    return sqrt((dis[f][0]-dis[s][0])**2+(dis[f][1]-dis[s][1])**2+(dis[f][2]-dis[s][2])**2)

flag=''
d=open('distances.txt').read().split('\n')
for i in d:
    axes=i.split(' ')
    first,second=int(axes[1]),int(axes[-1])
    flag+=chr(int(calc_distance(first,second)*100))

print(flag)
```

Tada :It spits out the flag: __ritsec{leap_4_th3_stars}__



