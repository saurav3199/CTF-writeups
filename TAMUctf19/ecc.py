import numpy as np
prime = 412220184797
def point_add(P, Q):
    m = (Q[1] - P[1])/(Q[0] - P[0])
    xr = m**2 - (Q[0] + P[0])
    yr = m*(P[0] - xr) - P[1]
    return np.array([xr,yr])%prime

def point_double(P):
    Q = P
    A = 10717230661382162362098424417014722231813
    m = 3*(Q[0]**2 + A)/(2*Q[1])
    xr = m**2 - (Q[0] + P[0])
    yr = m*(P[0] - xr) - P[1]
    return np.array([xr,yr])%prime

def double_and_add(P,n):
    if n==0:
        return np.array([0,0])
    elif n == 1:
        return P
    elif n % 2 == 1:
        return point_add(P, double_and_add(P, n-1))
    else:
        return double_and_add(point_double(P), n/2)


G = np.array([56797798272,349018778637])
A = np.array([61801292647,228288385004])
B = np.array([196393473219,35161195210])

arr = []


for i in range(11):
    res = double_and_add(G,i)
    if res[0] == A[0]:
        print("A", i, res)
    if res[0] == B[0]:
        print("B", i, res)
    if res[0] not in arr:
        print(i, res)
        arr.append(res[0])
