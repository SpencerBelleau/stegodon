import os, sys, subprocess
from random import randint

try:
	from PIL import Image
except:
	print("pillow not installed, use 'pip install pillow'")
	sys.exit(-1)

args = sys.argv

###HELP STRINGS###
usage = '''\nUsage:\n  ''' + args[0]
##----------------------------------------------------------------------
default = usage + ''' <mode> [arguments for mode]

Modes:
  -a,  --attach        Attaches the provided file to an image
  -ap, --attach-pad    Attaches the provided file to an image, and pads the remaining pixels with junk data
  -e,  --extract       Extracts an attached image from image
  -s,  --scan          Scans an image for relevant properties and presence of attached files
  -d,  --diff          Compares two images and creates an output file that shows pixel differences
  
Entering a mode with no arguments will display help for that mode'''
##----------------------------------------------------------------------
atcHelp = usage + ''' -a image infile outfile

Description:
  Attaches the provided file to an image

Arguments:
  image                Image to attach file to
  infile               File to attach to image
  outfile              Name of output image'''
##----------------------------------------------------------------------
atcpHelp = usage + ''' -ap image infile outfile

Description:
  Attaches the provided file to an image, and pads the remaining pixels with junk data

Arguments:
  image                Image to attach file to
  infile               File to attach to image
  outfile              Name of output image'''
##----------------------------------------------------------------------
extHelp = usage + ''' -e image [outfile]

Description:
  Extracts an attached image from image

Arguments:
  image                Image to retrieve file from
  outfile              Name of output file (overrides default, optional)'''
##----------------------------------------------------------------------
scanHelp = usage + ''' -s image

Description:
  Scans an image for relevant properties and presence of attached files

Arguments:
  image                Image to check'''
##----------------------------------------------------------------------
diffHelp = usage + ''' -d image1 image2 outfile

Description:
  Compares two images and creates an output file that shows pixel differences

Arguments:
  image1               First image
  image2               Second image
  outfile              Name of output file (PNG)'''
##----------------------------------------------------------------------

#prepare to launch something using subprocess
command = [sys.executable]
for x in args[1:]:
	command.append(x)
###LOGIC###
if(len(args) == 1):
	print(default)
	os._exit(1)
if(command[1] == "-a" or command[1] == "--attach"):
	if(len(args) == 2):
		print(atcHelp)
	elif(len(args) != 5):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\attacher.py'
		command.append("-pad")
		subprocess.call(command)
		pass
elif(command[1] == "-ap" or command[1] == "--attach-pad"):
	if(len(args) == 2):
		print(atcpHelp)
	elif(len(args) != 5):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\attacher.py'
		command.append("+pad")
		subprocess.call(command)
		pass
elif(command[1] == "-e" or command[1] == "--extract"):
	if(len(args) == 2):
		print(extHelp)
	elif(len(args) > 4):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\extractor.py'
		subprocess.call(command)
elif(command[1] == "-s" or command[1] == "--scan"):
	if(len(args) == 2):
		print(scanHelp)
	elif(len(args) != 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\scanner.py'
		subprocess.call(command)
elif(command[1] == "-d" or command[1] == "--diff"):
	if(len(args) == 2):
		print(diffHelp)
	elif(len(args) != 5):
		print("Invalid number of arguments. Type 'py " + args[0] + " " + command[1] + "' for help")
	else:
		command[1] = 'modules\\diffImage.py'
		subprocess.call(command)
		pass
else:
	print("Invalid Mode.")
	print(default)