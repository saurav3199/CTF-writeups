
So back again with some writeups as there were not many good challenges in ctfs in past few months. 
I loved some of the challenges of this CTF, while the category wise challenges were good.

[Link to the challenges](https://2020.redpwn.net/challs)

## alien-transmissions-v2 -:
> description:

The aliens are at it again! We've discovered that their communications are in base 512 and have transcribed them in base 10. However, it seems like they used XOR encryption twice with two different keys! We do have some information:

1) This alien language consists of words delimitated by the character represented as 481
2) The two keys appear to be of length 21 and 19
3) The value of each character in these keys does not exceed 255
Find these two keys for me; concatenate their ASCII encodings and wrap it in the flag format.

challenge file : [encrypted.txt](assets/encrypted.txt)

77 solves | 481 points

### Solution:
NOTE: There was a change in challenge statement that key's length does not exceed 128 as it was readable.

#### Tl;dr : This challenge looked impossible to solve once as how can I predict where will '481' occur in the encrypted text so after lot of approaches I finally reach to this one. 

So challenge statement was clear that there is a bunch of xor encrypted base512 characters represented in base10. And there is fixed key1 and key2 because it is part of our flag.
That means
```
cyclic(key1) ^ cyclic(key2) ^ original_message = given_ciphertext
```
Let the cryptanalysis begin. We know that the given_ciphertext and we know key1 & key2 but original_message is completely random so there is no way we can get the keys , as for any possible set of keys there can be a valid original message.

But there was this catch that make this challenge easier that the alien messages are separated by 481. So think of it like there are bunch of words having length [2-20] consisting of base512 characters delimited by 481.
Then 481 will occur the most than other possible characters in original message.

Based on that we can just divide the data into chunks of lcm(19,21) `Reason: as we will have key1[i%21]^key2[i%19] be same` and obtain the most occured element in each row to be 481.

Let's check the counter first to be sure

```python
from collections import Counter
import string

f= open("encrypted.txt","r").read().split("\n")
lim = 21*19
lis = [[] for i in range(lim)]

for ind in range(len(f)):
	el = f[ind]
	lis[ind%(lim)].append(el)

cols = []
for row in lis:
	x = Counter(row)
	print(x)

```

Output:
```
Counter({'470': 250, '78': 12, '74': 12, '485': 11, '31': 11, '91': 11, '267': 11, '328': 10, .......
Counter({'422': 246, '182': 12, '331': 11, '407': 10, '381': 10, '446': 10, '15': 10, '17': 10, .....
.....
```
So it was obvious now. Then we have key1[i]^key2[j]^(most_common^481) to be the original message and we have lcm(19,21) equations, so we can just easily pick one index and get the other chars easily. 


Here is our final [script](assets/alien.py):

```python
from collections import Counter
import string

f= open("encrypted.txt","r").read().split("\n")
lim = 21*19
lis = [[] for i in range(lim)]

for ind in range(len(f)):
	el = f[ind]
	lis[ind%(lim)].append(el)

cols = []
for row in lis:
	x = Counter(row)
	cols.append(x.most_common(1)[0][0])

for i in range(lim):
	cols[i] = int(cols[i]) ^ 481

key1 = ["*" for i in range(21)]
key2 = ["*" for i in range(19)]

for i in range(128): # checking for only readable characters
	key1[0] = chr(i)
	for j in range(19):
		key2[(21*j)%19] = chr(cols[21*j]^i)
	k2 = "".join(key2)
	if k2.isprintable():
		for m in range(21):
			key1[m%21] = chr(ord(k2[m%19])^cols[m])
		k1 = "".join(key1)
		if k1.isprintable():
			print("probable flag : flag{"+k1+k2+"}")
```
We got this [output](assets/output.txt) here
> Flag : flag{h3r3'5_th3_f1r5t_h4lf_th3_53c0nd_15_th15}
