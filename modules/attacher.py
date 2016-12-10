import os, sys, subprocess
from random import randint
from PIL import Image
from funcs import *

args = sys.argv

#get args
imageName = args[1]
fileName = args[2]
outName = args[3]
padSwitch = args[4]
if(padSwitch == "+pad"):
	padding = True
else:
	padding = False
if(len(args) > 5):
	if(args[5] == "noprompt"):
		prompt = False
else:
	prompt = True

#Open the image and make sure it's alright
try:
	firstImage = Image.open(imageName)
except:
	print("Error opening image " + str(imageName) + " (is it actually an image file?)")
	sys.exit(-1)
dimensions = firstImage.size

#Scan block here
result = scan(args[1])
if(result[0] and (result[3] < maxSizeForChannel(result[2], dimensions))):
	print("File Found: " + result[1])
	print("Channel:    " + str(result[2]))
	print("Size:       " + str(result[3]) + " bytes")
	overWrite = ""
	while (not overWrite == "Y"):
		if(prompt):
			overWrite = input("There is already a file present, ok to overwrite? (Y/n)")
			if(overWrite == "n"):
				sys.exit(-1)
			elif(not overWrite == "Y"):
				print("Please enter Y or n")
		else:
			overWrite = "Y"

#find a good distribution for the information
channel = getValidChannel(os.path.getsize(fileName), dimensions)
if(channel == -1):
	print("File too big")
	sys.exit(-1)

##Actually start the operation
#convert the image
print("Writing to channel " + str(channel))
if(prompt):
	input("Press enter to continue...")
print("Converting to RGB...")
firstImage = firstImage.convert("RGB")
print("Getting pixel data...")
firstImageData = firstImage.getdata()

#prep the file data
print("Preparing file data...")
fileData = createNameData(os.path.basename(fileName), channel)
fileData.extend(createFileData(fileName, channel))

#now, put the data into the image
print("Writing...")
firstImageData = writeData(firstImageData, fileData, channel, padding=padding)
print("Creating result...")
outImage = Image.new('RGB', dimensions)
outImage.putdata(firstImageData)

#make the output directory
print("Saving result...")
try:
	os.makedirs(os.path.dirname(outName), exist_ok=True)
except:
	pass
outImage.save(outName)
print("Done!")