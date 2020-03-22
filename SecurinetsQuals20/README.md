Hey guys back with another set of few writeups.

We ended 15th this time :smile:


# **CRYPTO**

## Super Secure Safe-:
> description:

My friend , Anis_Bo$$ , has created a secure safe to hide his secret flag!

The only hint he gave me is : " Tic Toc Tic Toc ...".

I'm really lost .. Can you help me to find the way to break his safe and get the flag ?

HINT: key length = 16 , lowercase ..

Link - > https://web1.q20.ctfsecurinets.com/

Author: Tr'GFx

### Solution:

When we open the website we get `Sorry , Missing Key !`. 

So let's send the key in headers then see what we can get `Get the fuck outta here`.


So we need to send 16 length key and from the description we get the hint that it's something to do with clock or time. So I realized that its somewhat [Timing Attack](https://en.wikipedia.org/wiki/Timing_attack).
Then sending the key as of 16 length and check for each character one by one. So the correct character will give the time delay on which we can work.Approximately one second is added for the correct character. 
Storing the time delay on which we can select the next possible character. We can optimize it more if you know! :wink:

Here is the [Script](assets/securesafe.py):
```python
import requests
import datetime
import string

URL="https://web1.q20.ctfsecurinets.com/"
charset=string.ascii_lowercase


key=""
while len(key)<16:
    mx=0
    rest='*'
    for i in charset:
        sent=key+i
        sent+="a"*(16-len(sent))
        HEADERS = {'key':sent} 
        r = requests.get(url = URL, headers = HEADERS) 
        realtime=r.elapsed.total_seconds()
        if realtime>mx:
            mx=realtime
            rest=i
        print("The Current Time:"+str(realtime)+ " for "+ sent) # printing for debugging
    # 'Current Flag'
    key+=rest

print('the final key',key)
exit(0)


```
It popped out the 16 length key : `gprzoygsdbfjzaeg`

 
Then send this key to the server it will give the flag.
```python

HEADERS = {'key':key} 
r = requests.get(url = URL, headers = HEADERS)
print(r.text)
```

Here is our flag:`Securinets{iT$_@LL_@BouT_T1MiNG}` 

