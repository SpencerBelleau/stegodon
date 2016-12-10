import os, sys
from PIL import Image

args = sys.argv

try:
	i1 = Image.open(args[1])
	i2 = Image.open(args[2])
except:
	print("One or both images could not be opened.")
	sys.exit(-1)

#Do some checking to make sure the files can at least be changed
if(not i1.size == i2.size):
	print("Image files do not have the same dimensions.")
	sys.exit(-1)
print("Getting image data...")
i1 = i1.getdata()
i2 = i2.getdata()
newList = []
different = False
print("Getting diff...")
for i in range(len(i1)):
	if(i1[i][0] == i2[i][0] and i1[i][1] == i2[i][1] and i1[i][2] == i2[i][2]):
		newList.append(i1[i])
	else:
		if(not different):
			different = True
		newList.append((255 * (i1[i][0] == i2[i][0]), 255 * (i1[i][1] == i2[i][1]), 255 * (i1[i][2] == i2[i][2])))
if(different):
	print("Saving result...")
	try:
		os.makedirs(os.path.dirname(args[3]), exist_ok=True)
	except:
		pass
	outImage = Image.new('RGB', i1.size)
	outImage.putdata(newList)
	outImage.save(args[3])
	print("Done!")
else:
	print("Files are identical.")