#! /usr/bin/python2

#! /usr/bin/python2
import imageio
import png
import numpy as np

# load image and delete alpha channel
IMG = imageio.imread("small.png")

MAX_ROWS = IMG.shape[1]
MAX_COLS = IMG.shape[0]

# IMG[:,:,1:3] = 0


def update_pixel(row,col,r,g,b,a):
	global IMG
	temp = [r,g,b,a]
	for i in xrange(len(temp)):
		IMG[row,col,i] = temp[i]

def write_png():
	global IMG
	print IMG.shape
	file_handle = open('walks.png', 'wb')
	w = png.Writer(IMG.shape[1], IMG.shape[0], alpha=True)
	w.write(file_handle, np.reshape(IMG, (IMG.shape[0], IMG.shape[1]*IMG.shape[2])))
	file_handle.close()


def expand_sidewalk_pixel(row, col, r, g, b, a):
	global MAX_ROWS, MAX_COLS
	for i in xrange(row-2, row+2):
		for j in xrange(col-2, col+2):
			if (i > 0) and (i < IMG.shape[0]) and (j > 0) and (j < IMG.shape[1]):
				update_pixel(i, j, 255, 0,0,255)

def wipe():
	global IMG
	for i in xrange(IMG.shape[0]):
		for j in xrange(IMG.shape[1]):
			if IMG[i][j][0] != 255:
				IMG[i][j][3] = 0

def main():
	global IMG, MAX_ROWS, MAX_COLS
	for i in xrange(IMG.shape[0]):
		print "%d / %d" % (i,IMG.shape[0])
		for j in xrange(IMG.shape[1]):
			r,g,b,a  = IMG[i,j,:]
			if max([r,g,b]) == r and r-b > 20:
				if all([(m != n) for m, n in zip((255,0,0),(r,g,b))]): # if pix hasnt been touched by parser yet
					expand_sidewalk_pixel(i,j,r,g,b,a)
	write_png()

if __name__ == "__main__":
	main()
