from quadtree import LQTLD
from algos import a_star
import imageio
import png
import math
import numpy as np

IMG = imageio.imread("daddy.png")
MAX_ROWS = IMG.shape[1]
MAX_COLS = IMG.shape[0]

def main():
	global IMG
	occ_map = IMG[:,:,3] & 1
	occ_map = IMG[:,:,3] ^ 1
	biggest = max(occ_map.shape)
	occ_map = occ_map.tolist()
	new_dim = 2 ** int(math.log(biggest, 2) + 1)
	row_pad_dim = new_dim - len(occ_map[0])
	col_pad_dim = new_dim - len(occ_map)
	for row in occ_map:
		row.extend([1]*row_pad_dim)
	for i in xrange(col_pad_dim):
		occ_map.append([1]*new_dim)
	tree = LQTLD(occ_map, 1)
	tree.generate_debug_png('tree_debug.png')
	args = []
	with open("/dev/stdout") as file_handle:
		args = file_handle.readlines()
		args = map(int, map(split,args))
	start_row, start_col = args[0]
	end_row, end_col = args[1]		
	start_index = tree.get_containing_cell_index(start_row, start_col)
	end_index = tree.get_containing_cell_index(end_row, end_col)
	path = a_star(start_index, end_index, tree)
	
	print occ_map.dtype
	print occ_map[:100,:100]
	
if __name__ == "__main__":
	main()
