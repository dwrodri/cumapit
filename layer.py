#!/usr/bin/python2

import imageio
import png
import numpy as np
import sys
import math
from collections import namedtuple

if len(sys.argv) < 4:
	print("too few args")
	print("%s <bottomLayer.png> ... <middleLayers> ... <topLayer.png> <outputFile.png>" % sys.argv[0])
	exit()

IMG_LIST = map(imageio.imread, [img for img in sys.argv[1:-1]])
BASE_IMG = IMG_LIST[0]
IMG = IMG_LIST[1]

Point = namedtuple("Point",["x","y"])

def update_pixel(row,col,r,g,b,a):
	global BASE_IMG
	temp = [r,g,b,a]
	for i in xrange(len(temp)):
		BASE_IMG[row,col,i] = temp[i]

def write_png():
	global BASE_IMG
	file_handle = open(sys.argv[-1], 'wb')
	w = png.Writer(IMG.shape[1], IMG.shape[0], alpha=True)
	w.write(file_handle, np.reshape(BASE_IMG, (BASE_IMG.shape[0], BASE_IMG.shape[1]*BASE_IMG.shape[2])))
	file_handle.close()

def layer_images():
	global BASE_IMG
	global IMG

	for i in xrange(BASE_IMG.shape[0]):
		print("row %d of %d" % (i,BASE_IMG.shape[0]))
		for j in xrange(BASE_IMG.shape[1]):

			for image in IMG_LIST[1:]:
				IMG = image

				r,g,b,a  = IMG[i,j,:]
				if a == 255:
					update_pixel(i,j,r,g,b,a)
	
def main():
	global IMG
	layer_images()
	write_png()

main()
