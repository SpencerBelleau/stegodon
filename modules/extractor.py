import os, sys, subprocess
from random import randint
from PIL import Image
from funcs import *

args = sys.argv

imageName = args[1]
result = scan(imageName)
dimensions = Image.open(args[1])
dimensions = dimensions.size
if(result[0] and (result[3] < maxSizeForChannel(result[2], dimensions))):
	print("File Found: " + result[1])
	print("Channel:    " + str(result[2]))
	print("Size:       " + str(result[3]) + " bytes")
else:
	print("No file found to extract.")
	sys.exit(-1)
if(len(args) > 2):
	fileName = args[2]
else:
	fileName = result[1]
	
print("File will be extracted as " + fileName)
if(len(args) > 2):
	if(not args[2] == "noprompt"):
		if(len(args) > 3):
			if(not args[3] == "noprompt"):
				input("Press enter to continue...")
		else:
			input("Press enter to continue...")
			
#input("Press enter to continue...")
print("Opening image...")
try:
	image = Image.open(imageName)
except:
	print("Error opening image " + str(imageName) + " (is it actually an image file?)")
	sys.exit(-1)
print("Converting to RGB...")
image = image.convert("RGB")
image = image.getdata()

print("Extracting...")
__, _, index = extractNameData(image, result[2]) #We don't really need anything but the index points

fileData = extractFileData(image, result[2], index[0], index[1])
print("Saving extracted file...")

#make the appropriate directory
try:
	os.makedirs(os.path.dirname(fileName), exist_ok=True)
except:
	pass
f = open(fileName, 'wb')
f.write(fileData)
f.close()
print("Done!")