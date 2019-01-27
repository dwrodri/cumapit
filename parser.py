#! /usr/bin/python2
import sys
import numpy
from lxml import etree
from collections import namedtuple

######## Functions ######## 

def getID(node):
	return int(node.attrib["id"])

def binarySearch(arr, l, r, x): 
	while l <= r: 
		mid = l + (r - l)/2; 
		middle = getID(arr[mid])
		# Check if x is present at mid 
		if middle == x: 
			return mid 
		# If x is greater, ignore left half 
		elif middle < x: 
			l = mid + 1
		# If x is smaller, ignore right half 
		else: 
			r = mid - 1
	# If we reach here, then the element 
	# was not present 
	return -1


######## Command line arguments ######## 

# 1: osm xml filename

if len(sys.argv) != 2:
	print("nope")
	exit()

osmFilename = sys.argv[1]
mapPixWidth = 7330
mapPixHeight = 2105

######## Parse XML ######## 

xmlRoot = etree.parse(osmFilename).getroot()

Point = namedtuple("Point",["lat","lon"])
Bound = namedtuple("Bound",["min","max"])

boundsTag = xmlRoot.findall("./bounds")[0]
mapCoordBounds = Bound( \
	Point(float(boundsTag.attrib["minlat"]), float(boundsTag.attrib["minlon"])), \
	Point(float(boundsTag.attrib["maxlat"]), float(boundsTag.attrib["maxlon"])) \
)
mapCoordDims = Point( \
	mapCoordBounds.max.lat - mapCoordBounds.min.lat, \
	mapCoordBounds.max.lon - mapCoordBounds.min.lon \
)

allNodeElements = sorted(xmlRoot.findall("./node"), key=lambda x: x.attrib["id"])

# Iterate through every 'way' tag
for way in xmlRoot.findall("./way"):
	# Iterate through the 'nd' tag children of way
	for nd in (wayChild for wayChild in way.getiterator() if wayChild.tag == "nd"):
		# the 'ref' attr of an 'nd' tag corresponds with an 'id' attr of a 'node' tag
		# find the associated 'node' tag

		id_num = int(nd.attrib["ref"])
		node = allNodeElements[binarySearch(allNodeElements,0,len(allNodeElements)-1,id_num)]

		#node = allNodeElements[0]
		#for nodeElement in allNodeElements:
		#	if nodeElement.attrib["id"] == id_num:
		#		node = nodeElement
		#		break

		#node = list(filter(lambda x: x.attrib["id"] == id,allNodeElements))[0]

		#node = xmlRoot.findall(".//*[@id='%s']" % id)[0]
		nodePoint = Point( \
			(float(node.attrib["lat"]) - mapCoordBounds.min.lat) / mapCoordDims.lat, \
			(float(node.attrib["lon"]) - mapCoordBounds.min.lon) / mapCoordDims.lon \
		)

		print("%d %d 0 255 255" % (nodePoint.lat * mapPixWidth, nodePoint.lon * mapPixHeight))
	#exit()
