from math import *


stars=open("STAR_TABLES.agc").read()
stars=stars.split("\n")
dis=[[0 for i in range(3)] for j in range(40)] 
for i in stars:
    s=i.split(" ")
    val=float(s[0])
    pos=int(s[1])
    dis[pos][ord(s[2])-ord('X')]=val



def calc_distance(f,s):
    return sqrt((dis[f][0]-dis[s][0])**2+(dis[f][1]-dis[s][1])**2+(dis[f][2]-dis[s][2])**2)


flag=''
d=open('distances.txt').read()
d=d.split('\n')
for i in d:
    axes=i.split(' ')
    first=int(axes[1])
    second=int(axes[-1])
    flag+=chr(int(calc_distance(first,second)*100))

print(flag)
