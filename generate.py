#!/usr/bin/python3

from PIL import Image

imgHorizontalPixelDensity = 1
imgWidth = 816


def main():
	(sz, bimg) = loadImage("test.jpg")
	

# Convert input image to compliant binary image:
#def convertToBinary((wd, ht), img):


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

	return ((wd, ht), [[True if pix[i,j] == 0 else False for i in range(wd)] for j in range(ht)])
	# return ((wd, ht), pix)


if __name__ == "__main__":
	main()