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
		IMG[y,x,i] = temp[i]

def write_png():
	global IMG
	file_handle = open('output.png', 'wb')
	w = png.Writer(7330, 2105)
	w.write(file_handle, np.reshape(IMG, (IMG.shape[0], IMG.shape[1]*IMG.shape[2])))
	file_handle.close()
	

def main():
	global IMG
	lines = []
	args = []
	with open('/dev/stdin') as file_handle:
		lines = file_handle.readlines()
	for line in lines:
		temp = line.strip().split(' ')
		temp = map(int, temp)
		args.append(temp)
	for i in xrange(1, len(args)):
		start_x = args[i-1][1]
		end_x = args[i][1]
		start_y = [i-1][0]
		end_y = [i][0]
		dx = abs(end_x - start_x)
		dy = abs(end_y - start_y)
		slope = dy/dx if dx != 0 else 0
		for i in xrange(dx):
			print start_y + int(i * slope), start_x +i
			# update_pixel(start_y + int(i * slope), start_x +i, 0, 255, 255)
	write_png()
		
   
if __name__ == "__main__":
	main() 
