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

 ###Solution:
 
 I opened up my hexeditor HXD a great tool to change and view the hexes of file quite easily
 I see messed up bytes in beginning
 
 <img src="assets/misc/hxd.png" width="550px" height="150px" >
 
 
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
![64](assets/misc/64word.png)


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



