import os, sys, subprocess, string, math, random, time
from PIL import Image

def breakDownSize(l):
	m = 0
	h = 0
	rh = 0
	while l > 255:
		l = l - 256
		m = m + 1
		if(m > 255):
			m = 0
			h = h + 1
			if(h > 255):
				h = 0
				rh = rh + 1
	return [l, m, h, rh]
	
def encodeInModulo(n, modVal, target): #Very simple, changes a number to have a given value when modulo-d with another number
	if(not n%modVal == target):
		if(n + modVal < 255): #normal mode
			while(not n % modVal == target):
				n = n + 1
		else:
			while(not n % modVal == target):
				n = n - 1
	return n

def getMaxLength(base): #Not sure if there's a real pattern here that can be done fast
	if(base == 2):
		return 8
	elif(base == 3):
		return 6
	elif(base >= 4 and base <= 6):
		return 4
	elif(base >= 7 and base <= 15):
		return 3
	else:
		return 2

def convertToBase(n, base, baseLength = -1): #only does numbers from 0 to 255
	converted = []
	if(baseLength == -1):
		baseLength = getMaxLength(base)
	for i in range(0, baseLength):
		converted.append(0)
	#should be a lot faster
	for i in reversed(range(0, baseLength)):
		while n >= pow(base, i):
			converted[i] = converted[i] + 1
			n = n - pow(base, i)
	return converted
	
def createNameData(name = "", base = 10):
	nameData = convertToBase(int(len(name)), base) #start with name length
	nameList = []
	for letter in name:
		nameList.append(convertToBase(ord(letter), base))
	for byte in nameList:
		nameData.extend(byte)
	return nameData
	
def createFileData(fileName, base):
	#format is size-l, size-m, size-h, [data]
	data = []
	fileSize = os.path.getsize(fileName)
	sizeBytes = breakDownSize(fileSize)
	for byte in sizeBytes:
		data.extend(convertToBase(byte, base))
	fileData = list(open(fileName, 'rb').read())
	for byte in fileData:
		data.extend(convertToBase(byte, base))
	return data
	
def writeData(image = [], data = [], base = 10, outerIndex = 0, innerIndex = 0, padding = False):
	#data is the processed list of integers
	#put in a length check here later
	newTuple = [image[outerIndex][0], image[outerIndex][1], image[outerIndex][2]]
	newPixList = []
	
	#info for printouts, produces neglible delay
	lastPercent = 0
	sys.stdout.write("0% Complete")
	
	for i in range(0, len(data)):
		newTuple[innerIndex] = encodeInModulo(image[outerIndex][innerIndex], base, data[i])
		innerIndex = innerIndex + 1
		if(innerIndex == 3):
			newPercent = int((i/len(data))*100)
			innerIndex = 0
			newPixList.append(tuple(newTuple))
			newTuple = [image[outerIndex][0], image[outerIndex][1], image[outerIndex][2]]
			outerIndex = outerIndex + 1
			if(newPercent > lastPercent):
				sys.stdout.write("\r" + str(newPercent) + "% Complete")
				lastPercent = lastPercent + 1
	#finish up the rest
	if(not padding):
		#get to a whole pixel
		while (not innerIndex == 0):
			innerIndex = innerIndex + 1
			if(innerIndex == 3):
				innerIndex = 0
				newPixList.append(tuple(newTuple))
				newTuple = [image[outerIndex][0], image[outerIndex][1], image[outerIndex][2]]
				outerIndex = outerIndex + 1
		#put in the rest
		remaining = list(image)[outerIndex:]
		newPixList.extend(remaining)
		sys.stdout.write("\r100% Complete\n")
	else:
		sys.stdout.write("\r100% Complete\n")
		print("Padding steganographic data...")
		random.seed(time.time())
		lastPercent = 0
		while(outerIndex < len(image)):
			newPercent = int((outerIndex/len(image))*100)
			pad = random.randint(0, base-1)
			newTuple[innerIndex] = encodeInModulo(image[outerIndex][innerIndex], base, pad)
			innerIndex = innerIndex + 1
			if(innerIndex == 3):
				innerIndex = 0
				newPixList.append(tuple(newTuple))
				newTuple = [image[outerIndex][0], image[outerIndex][1], image[outerIndex][2]]
				outerIndex = outerIndex + 1
				if(newPercent > lastPercent):
					sys.stdout.write("\r" + str(newPercent) + "% Complete")
					lastPercent = lastPercent + 1
		sys.stdout.write("\r100% Complete\n")
	return newPixList
	
def maxSizeForChannel(channel, dimensions):	
	#even accounts for the size bytes
	return (int((dimensions[0] * dimensions[1] * 3)/getMaxLength(channel)) - 5)
	
def getValidChannel(size, dimensions):
	for i in range(2, 128):
		if((maxSizeForChannel(i, dimensions) > size)):
			return i
	return -1
	
def scan(file): #Largely self-contained
	try:
		image = Image.open(file)
	except:
		print("Error opening image " + str(file) + " (is it actually an image file?)")
		sys.exit(-1)
	image = image.convert("RGB")
	image = image.getdata()
	sizeBytes = []
	
	for i in range(2, 17):
		try:
			name = extractNameData(image, i)
			outerIndex = name[2][0]
			innerIndex = name[2][1]
			for j in range(0, getMaxLength(i) * 4):
				sizeBytes.append(image[outerIndex][innerIndex] % i)
				innerIndex = innerIndex + 1
				if(innerIndex == 3):
					innerIndex = 0
					outerIndex = outerIndex + 1
			size = 0
			for j in range(0, 4):
				for k in range(0, getMaxLength(i)):
					size = size + ((sizeBytes[k + (getMaxLength(i)*j)] * pow(i, k)) * pow(256, j))
			if(size == 0):
				raise Exception("File size zero")
			return (True, name[0], i, size)
			break
		except Exception as e:
			pass
	return (False, "", 0, 0)

#Can throw exception if the filename is invalid
def extractNameData(image = [], base = 10, outerIndex = 0, innerIndex = 0):
	#make sure to add a size check here
	#now, get the data back out
	sizeByte = []
	outBytes = []
	name = ""
	#get the length from the first set
	for i in range(0, getMaxLength(base)):
		sizeByte.append(image[outerIndex][innerIndex] % base)
		innerIndex = innerIndex + 1
		if(innerIndex == 3):
			innerIndex = 0
			outerIndex = outerIndex + 1
	size = 0

	for i in range(0, getMaxLength(base)):
		size = size + (sizeByte[i] * pow(base, i))

	#now that we have that, get that many bytes out
	for i in range(0, (size * getMaxLength(base))):
		outBytes.append(image[outerIndex][innerIndex] % base)
		innerIndex = innerIndex + 1
		if(innerIndex == 3):
			innerIndex = 0
			outerIndex = outerIndex + 1
	
	for i in range(0, len(outBytes), getMaxLength(base)):
		n = 0
		for j in range(0, getMaxLength(base)):
			n = n + (outBytes[i+j] * pow(base, j))
		if(not chr(n) in string.printable):
			raise Exception("Filename Unprintable")
			n = "invalid"
			break
		else:
			name = name + chr(n)
	return(name, outBytes, [outerIndex, innerIndex]) #middle isn't strictly necessary
	
def extractFileData(image = [], base = 10, outerIndex = 0, innerIndex = 0): #oI and iI should never be 0 really
	#make sure to add a size check here
	#now, get the data back out
	sizeBytes = []
	outBytes = []
	data = []
	name = ""
	#get the length from the first set
	for i in range(0, getMaxLength(base) * 4):
		sizeBytes.append(image[outerIndex][innerIndex] % base)
		innerIndex = innerIndex + 1
		if(innerIndex == 3):
			innerIndex = 0
			outerIndex = outerIndex + 1
	size = 0
	#print(sizeBytes)
	#this is a mess, but will change the 3-byte filesize back into an int
	for i in range(0, 4):
		for j in range(0, getMaxLength(base)):
			size = size + ((sizeBytes[j + (getMaxLength(base)*i)] * pow(base, j)) * pow(256, i))
	#print(size)
	for i in range(0, (size * getMaxLength(base))):
		outBytes.append(image[outerIndex][innerIndex] % base)
		innerIndex = innerIndex + 1
		if(innerIndex == 3):
			innerIndex = 0
			outerIndex = outerIndex + 1
	
	for i in range(0, len(outBytes), getMaxLength(base)):
		n = 0
		for j in range(0, getMaxLength(base)):
			n = n + (outBytes[i+j] * pow(base, j))
		data.append(n)
	
	return bytearray(data) #ready to be written