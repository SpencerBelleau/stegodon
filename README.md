Stegodon
=====
####Requires pillow, use `pip install pillow` if you don't have it.

Recode of steganosaurus, a project I made in multimedia class. This one is better in nearly every way. This python script will let you put files inside of lossless images, as well as scan for them and extrct them.
Here's how to use it.

Attaching a file
----------------
`py stegodon.py -a image file outfile`

`image` is the image that you're going to attach the file to, `file` is the file you want to attach, and `outfile` is the name of the result image that contains the file. `outfile` should be a *.png or some other lossless format.
You can also use `-ap` if you want to pad the rest of the file with junk data. This will increase the resulting file size but makes the steganography harder to visually detect in most cases.

Scanning for a file
-------------------
`py stegodon.py -s image`

`image` is the image you want to check. This will run a basic scan for valid files by checking the pixel data in the image. If something is found, it will output the name, file size, and "channel" that the file is stored on.

Extracting a file
-----------------
`py stegodon.py -e image [outfile]`

`image` is the image you're going to extract a file from, `[outfile]` is an optional parameter which will rename the extracted file.

Create a diff
-------------
`py stegodon.py -d image1 image2 outfile`

`image1` and `image2` are two images files of any type that you want to compare. `outfile` is an image that represents the differences in pixel data between the two compared images.
`outfile` will have quite a bit of "snow" in it most of the time, and the color of the pixels represents which channels were altered. In the case of non-altered pixels the original pixel is placed in the proper position in the diff image.

Other stuff
-----------

"Channel" refers to how the data is distributed in the image. At best the program will use LSB-style alterations where each channel will at most be altered by 1/255, but it can increase the magnitude of the alteration up to 15/255 in order to condense the data.

Related to the above, it is technically possible for the scanner to detect a file that isn't there, but highly unlikely.

You can use --attach, --diff, --scan, --extract, and --attach-pad instead of -a, -d, -s, -e, -ap.

You can add `noprompt` to the end of an argument chain directed at attacher.py or extractor.py in order to make the program not pause and wait for the user to ok the operation. I guess if you want to hook this up to a web service that would help.

This program isn't really done, so there might be small bugs.