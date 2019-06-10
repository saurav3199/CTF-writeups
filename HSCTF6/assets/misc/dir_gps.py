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
            
    
