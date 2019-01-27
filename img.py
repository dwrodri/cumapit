#! /usr/bin/python2
import imageio
import png
import numpy as np

# load image and delete alpha channel
IMG = imageio.imread("DA_MAP.png")
print IMG.shape
IMG = np.delete(IMG,-1,axis=-1)
print IMG.shape

def update_pixel(x,y,r,g,b):
    global IMG
    temp = [r,g,b]
    for i in xrange(len(temp)):
        IMG[x,y,i] = temp[i]

def main():
    global IMG
    lines = []
    with open('/dev/stdin') as file_handle:
        lines = file_handle.readlines()
    for line in lines:
        print line.strip()
        
   
if __name__ == "__main__":
    main() 
