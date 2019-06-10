A High School CTF event.

![score](assets/misc/score.PNG)

We tried to solve challenges as much as possible we can and as a reult we secured 23 position globally.

![image](assets/screencapture-ctf-hsctf-challenges-2019-06-08-12_20_54.png)

Challenge  Name | Points | Flag
------------ | ------------- | ---------------
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |
 | |


So I will try to discuss the challenges i loved the most here:


# MISC

## Hidden Flag-:
> description: 


<img src="assets/misc/hiddenflag.png" width="450px" height="400px" >

 ### Solution:
 
 I opened up my hexeditor HXD a great tool to change and view the hexes of file quite easily and
 I see messed up bytes in beginning.
 
 <img src="assets/misc/hxd.png" width="550px" height="100px" >
 
 
 Then at the end of the file i see some text `key is invisible`.
 So then i realise that the bytees must be xored with the key and we got it by this [script](assets/misc/fixchall.py).
 
```python
import binascii
from itertools import cycle,izip

f=open("chall.png")
g=(f.read())
key="invisible"
ciphered = ''.join(chr(ord(c)^ord(k)) for c,k in izip(g, cycle(key)))
l=open("fixed.png","a+")
l.write(ciphered)

```
That's it :smiley:

<img src="assets/misc/fixed.png" width="550px" height="250px" >
 
## 64+Word -:
> description: 

<img src="assets/misc/64word.png" width="450px" height="400px" >

### Solution :
So from the description we see the word search and challenge name is 64+. So we need to do base64 word search of flag.
Be sure as the base64 encode texts are multiple of 4 . So chose the texts accordingly.Here is the [Script](/assets/misc/ord64.py)

```
from  base64 import *
file=open("64word.txt")
data=file.read().split("\n")
o=0
while o<100:
    g=data[o:]
    for q in range(100):
        j=q
        s=""
        for i in g:
            if j>=len(i):
                break
            s+=i[j]
            j+=1
        possible_text=(b64decode(s[:4*(len(s)//4)]))
        if "hsctf{" in possible_text[:6]:
            end_ind=possible_text.find('}')+1
            print("The flag is "+ possible_text[:end_ind] )
            exit(0)
    o+=1

```

then there is the flag:`The flag is hsctf{b4s3_64_w0rd_s3arch3s_ar3_fu9?}`

## Broken gps-:
> description:
Input Format:
<img src="assets/misc/brokengps1.png" width="400px" height="600px" >

A challenge to test some coding skills.

### Solution:
Here's the [script](assets/misc/dir_gps.py) thats explain it all.

```
import math

suffix=".txt"
flag=""
dirs=["east","west","south","north","northwest","northeast","southeast","southwest"]
for i in range(1,13):
    up=0
    right=0
    filename=str(i)+suffix
    f=open(filename)
    h=(f.read()).split()
    for q in range(int(h[0])):
        pos=dirs.index(h[q+1])
        if pos==0 or pos==5 or pos==6:
            right+=1
        if pos==1 or pos==4 or pos==7:
            right-=1
        if pos==3 or pos==4 or pos==5:
            up+=1
        if pos==2 or pos==6 or pos==7:
            up-=1
    flag+=chr(round(math.sqrt(up*up+right*right)*2)%26+97)
print('hsctf{'+flag+'}')
            
```
and here is the output:
>hsctf{garminesuckz}

## RealReversal-:
> description: 

<img src="assets/misc/realreversal.png" width="400px" height="400px" >

### Solution:
On opening file we see 

<img src="assets/misc/revd.png" width="850px" height="150px" >

Reversing the file means reversing the hexes.So one liner will do that 

```open("reversed_reversed.txt", "wb").write(open("reversed.txt", "rb").read()[::-1])```

and on opening reversed file you see utf-8 chars

<img src="assets/misc/utf8.png" width="900px" height="100px" >

Explanation:Why it happens that on the reverse bytes we can't see any characters, because 

>UTF-8 is a variable width character encoding capable of encoding all 1,112,064 valid code points in Unicode using one to four 8-bit bytes.

So on reversing 8 bytes it messed up as it reversed in two parts of four and four.Thus resulting in random chars.
So you can see the flag now:`hsctf{utf8_for_the_win}`
