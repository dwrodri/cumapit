#!/usr/bin/python2

import imageio
import png
import numpy as np
import sys
import math
from collections import namedtuple

if len(sys.argv) != 2:
	print("%s <campusMap.png>" % sys.argv[0])
	exit()

IMG = imageio.imread(sys.argv[1])

Point = namedtuple("Point",["x","y"])

def update_pixel(row,col,r,g,b,a):
	global BASE_IMG
	temp = [r,g,b,a]
	for i in xrange(len(temp)):
		IMG[row,col,i] = temp[i]

def write_png():
	global IMG
	file_handle = open('doors.png', 'wb')
	w = png.Writer(IMG.shape[1], IMG.shape[0], alpha=True)
	w.write(file_handle, np.reshape(IMG, (IMG.shape[0], IMG.shape[1]*IMG.shape[2])))
	file_handle.close()

def in_bounds(p):
	global IMG
	return p.x > 0 and p.x < IMG.shape[1] and p.y > 0 and p.y < IMG.shape[0]

def distance(p1,p2):
	return math.sqrt(((p2.x - p1.x) ** 2) + ((p2.y - p1.y) ** 2))

def draw_circle(c,r):
	rad = float(r)
	for i in range(c.y - r, c.y + r + 1):
		for j in range(c.x - r, c.x + r + 1):
			p = Point(j,i)
			if in_bounds(p) and distance(p, c) <= rad:
				update_pixel(p.y, p.x, 0, 255, 0, 255)

def main():
	global IMG

	# start transparent
	for i in xrange(IMG.shape[0]):
		for j in xrange(IMG.shape[1]):
			update_pixel(i,j,0,0,0,0)

	# make all doors green
	for line in sys.stdin:
		splitLine = line.strip().split(' ')
		point = Point(int(splitLine[3]), int(splitLine[2]))
		draw_circle(point,10)

	write_png()

'''
	for i in xrange(len(IMG.shape[0])):
		for j in xrange(len(IMG.shape[1])):
			r,g,b,a = IMG[i,j,:]
			expand_sidewalk_pixel(i,j,r,g,b,a)
	write_png()
'''

main()
