import os, sys, subprocess
from random import randint
from PIL import Image
from funcs import *

args = sys.argv
result = scan(args[1])
dimensions = Image.open(args[1])
dimensions = dimensions.size
if(result[0] and (result[3] < maxSizeForChannel(result[2], dimensions))):
	print("File Found: " + result[1])
	print("Channel:    " + str(result[2]))
	print("Size:       " + str(result[3]) + " bytes")
else:
	print("No File Found")
	try:
		thing = Image.open(args[1])
	except:
		print("Error opening image " + str(args[1]) + " (is it actually an image file?)")
		sys.exit(-1)
	dims = thing.size
	for i in range(2, 5):
		print("Size on channel " + str(i) + ": " + str(maxSizeForChannel(i, dims)) + " bytes (including filename)")
	print("Size on channel " + str(7) + ": " + str(maxSizeForChannel(7, dims)) + " bytes (including filename)")
	print("Size on channel " + str(16) + ": " + str(maxSizeForChannel(16, dims)) + " bytes (including filename)")