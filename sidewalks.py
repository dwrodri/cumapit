#! /usr/bin/python2

#! /usr/bin/python2
import imageio
import png
import numpy as np

# load image and delete alpha channel
IMG = imageio.imread("campus.png")

def update_pixel(x,y,r,g,b,a):
	global IMG
	temp = [r,g,b,a]
	for i in xrange(len(temp)):
		IMG[y,x,i] = temp[i]

def write_png():
	global IMG
	file_handle = open('sidewalks.png', 'wb')
	w = png.Writer(7330, 2105, alpha=True)
	w.write(file_handle, np.reshape(IMG, (IMG.shape[0], IMG.shape[1]*IMG.shape[2])))
	file_handle.close()
	

def expand_sidewalk_pixel(row, col, r, g, b, a):
	if r > 120 && (r - b > 32) && (r - g > 20):  # if pixel is red
		if all([(m != n) for m, n in zip((255,0,0),(r,g,b))]): # if pix hasnt been touched by parser yet
			update_pixel(row, col, 255, 0,0, 255)

def main():
	global IMG
	for i in xrange(len(IMG.shape[0])):
		for j in xrange(len(IMG.shape[1])):
			r,g,b,a = IMG[i,j,:]
			expand_sidewalk_pixel(i,j,r,g,b,a)
	write_png()


		
