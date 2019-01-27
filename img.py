#! /usr/bin/python2
import imageio
import png
import numpy as np

# load image and delete alpha channel
IMG = imageio.imread("campus.png")
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
	
def draw_line(x1,y1,x2,y2,r,g,b):

	# straight line up and down
	if x1 == x2:
		for y in range(min(y1,y2), max(y1,y2)+1):
			try:
				update_pixel(x1,y,r,g,b)
			except:
				continue
		return

	# make it definitely go left to right
	if x1 > x2:
		x1, x2 = x2, x1

	slope = float(y2 - y1) / float(x2 - x1)
	y = float(y1)
	for x in range(x1, x2+1):
		try:
			update_pixel(x1,y,r,g,b)
		except:
			continue
		y += slope

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
		draw_line(args[i-1][0], args[i-1][1], args[i][0], args[i][1], 255, 0, 0)
	write_png()
		
   
if __name__ == "__main__":
	main() 
