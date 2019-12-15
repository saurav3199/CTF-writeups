from sympy import *
f=open("polly.txt","r").read()
x=symbols('x')
y=eval(f)
print(''.join([chr(y.subs(x,i)) for i in range(57)]))