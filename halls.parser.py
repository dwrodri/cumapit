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
	global IMG
	temp = [r,g,b,a]
	for i in xrange(len(temp)):
		IMG[row,col,i] = temp[i]

def write_png(fn):
	global IMG
	file_handle = open(fn, 'wb')
	w = png.Writer(IMG.shape[1], IMG.shape[0], alpha=True)
	w.write(file_handle, np.reshape(IMG, (IMG.shape[0], IMG.shape[1]*IMG.shape[2])))
	file_handle.close()

def in_bounds(p):
	global IMG
	return p.x > 0 and p.x < IMG.shape[1] and p.y > 0 and p.y < IMG.shape[0]

def draw_line(x1,y1,x2,y2,r,g,b,a):

	# straight line up and down
	if x1 == x2:
		for y in range(min(y1,y2), max(y1,y2)+1):
			if not in_bounds(Point(x1,y)):
				break
			update_pixel(y,x1,r,g,b,a)
		return

	slope = float(y2 - y1) / float(x2 - x1)

	if math.fabs(slope) > 1.0:
		slope = 1.0 / slope
		if y1 > y2:
			y1, y2 = y2, y1
			x1, x2 = x2, x1

		x = float(x1)
		for y in range(y1, y2+1):
			if not in_bounds(Point(int(x),y)):
				break
			update_pixel(y,int(x),r,g,b,a)
			x += slope
		return

	# make it definitely go left to right
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1

	y = float(y1)
	for x in range(x1, x2+1):
		if not in_bounds(Point(x,int(y))):
			break
		update_pixel(int(math.floor(y)),x,r,g,b,a)
		y += slope

def main():
	global IMG

	# read in the file
	splitLines = []
	for line in sys.stdin:
		splitLines += [line.strip().split(' ')]

	# start transparent
	for i in xrange(IMG.shape[0]):
		for j in xrange(IMG.shape[1]):
			update_pixel(i,j,0,0,0,0)

	# draw all the halls
	for splitLine in splitLines:
		if splitLine[0] != "Hallway":
			continue

		point0 = splitLines[int(splitLine[1])]
		point1 = splitLines[int(splitLine[2])]

		draw_line( \
			int(point0[3]), int(point0[2]), \
			int(point1[3]), int(point1[2]), \
			0, 255, 255, 255 \
		)
	write_png("halls.png")

main()
