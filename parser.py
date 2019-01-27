import sys
from lxml import etree
from collections import namedtuple

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

# Iterate through every 'way' tag
for way in xmlRoot.findall("./way"):
	# Iterate through the 'nd' tag children of way
	for nd in (wayChild for wayChild in way.getiterator() if wayChild.tag == "nd"):
		# the 'ref' attr of an 'nd' tag corresponds with an 'id' attr of a 'node' tag
		# find the associated 'node' tag
		id = nd.attrib["ref"]
		node = xmlRoot.findall(".//*[@id='%s']" % id)[0]
		nodePoint = Point( \
			(float(node.attrib["lat"]) - mapCoordBounds.min.lat) / mapCoordDims.lat, \
			(float(node.attrib["lon"]) - mapCoordBounds.min.lon) / mapCoordDims.lon \
		)

		print("%d %d 0 255 255" % (nodePoint.lat * mapPixWidth, nodePoint.lon * mapPixHeight))
	exit()





