#!/usr/bin/python3

from PIL import Image

imgHorizontalPixelDensity = 1
imgWidth = 816


def main():
	(sz, bimg) = loadImage("test.jpg")
	bdata = convertToBinary(sz, bimg)
	

# Convert input image to compliant binary image:
def convertToBinary((wd, ht), img):
	rv = bytearray()
	rowsPerLine = 8	 # rows of image data per line of printer data

	for lineStartNum in range(0, ht, rowsPerLine): # For each block of rows that make a line
		# Emit the appropriate headers:
		rv.append(27) 				# Set image mode
		rv.append(ord('K'))			# Single density
		rv.append(imgWidth % 256) 	# Low byte of image width
		rv.append(imgWidth // 256) 	# High byte of image width

		for i in range(wd): # For each column of pixels
			colVal = 0 # The value that encodes all the states in this column
			cPin = 0b10000000 # The moving filter
			for j in range(lineStartNum, min(lineNum + rowsPerLine, ht)):
				if img[i,j] == 0: # If this pin should be triggered.
					colVal |= cPin
				cPin >>= 1
			rv.append(colVal) # Add the column to the output

		# We're done with this line, emit a newline character:
		rv.append(ord('\r')) # Yes, the printer is that old.
		rv.append(ord('\n'))

	for i in range(4): # Trailing newlines:
		rv.append(ord('\r')) # Yes, the printer is that old.
		rv.append(ord('\n'))


def loadImage(fname):
	img_original = Image.open(fname).convert("L")

	# Resize it to the desired dimensions.
	(wd, ht) = img_original.size
	ht = (ht * imgWidth) // (wd * imgHorizontalPixelDensity)
	wd = imgWidth
	# An extra row and column keeps 
	img_resized = img_original.resize((wd + 1, ht + 1))
	pix = img_resized.load()
	# img_resized.show()

	# http://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
	for y in range(ht):
		for x in range(wd):
			oldpixel = pix[x,y]
			newpixel = 0 if oldpixel < 128 else 255
			pix[x,y] = newpixel
			quant_error = oldpixel - newpixel
			if x > 0:
				pix[x - 1, y + 1] = pix[x - 1, y + 1] + quant_error * 3/16
			pix[x + 1, y    ] = pix[x + 1, y    ] + quant_error * 7/16
			pix[x    , y + 1] = pix[x    , y + 1] + quant_error * 5/16
			pix[x + 1, y + 1] = pix[x + 1, y + 1] + quant_error * 1/16

	img_resized.show()

	#return ((wd, ht), [[True if pix[i,j] == 0 else False for i in range(wd)] for j in range(ht)])
	return ((wd, ht), pix)


if __name__ == "__main__":
	main()