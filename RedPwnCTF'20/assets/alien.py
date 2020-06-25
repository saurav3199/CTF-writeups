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

for i in range(128):
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