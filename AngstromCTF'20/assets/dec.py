from numpy import *
from PIL import Image
from gmpy2 import *

flag = Image.open(r"enc.png")
img = array(flag)

key = [41, 37, 23]

invkey=[invert(k,251) for k in key]

a, b, c = img.shape

for x in range (0, a):
    for y in range (0, b):
        pixel = img[x, y]
        for i in range(0,3):
            pixel[i] = pixel[i] * invkey[i] % 251
        img[x][y] = pixel

dec = Image.fromarray(img)
dec.save('flag.png')
