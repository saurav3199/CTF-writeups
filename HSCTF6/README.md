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
## Verbose-:
> description: 

<img src="assets/misc/verbose.PNG" width="450px" height="400px" >

## Hidden Flag-:
> description: 


<img src="assets/misc/hiddenflag.png" width="450px" height="400px" >

 ### Solution:
 
 I opened up my hexeditor HXD a great tool to change and view the hexes of file quite easily and
 I see messed up bytes in beginning.
 
 <img src="assets/misc/hxd.png" width="550px" height="100px" >
 
 
 Then at the end of the file i see some text `key is invisible`
 So then i realise that the bytees must be xored with the key and we got it by this [script](assets/misc/fixchall.py)
 
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



## Broken gps-:
> description: 
![b1](assets/misc/brokengps1.png)
![b2](assets/misc/brokengps2.png)


## Keith_Bot-:
> description: 
![kb](assets/misc/keithbot.png)

## Locked_up-:
> description: 
![lu](assets/misc/lockedup.png)


## RealReversal-:
> description: 
![rr](assets/misc/realreversal.png)



