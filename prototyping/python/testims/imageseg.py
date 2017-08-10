import numpy as np
import scipy.ndimage
import skimage.feature
import skimage.transform
import sklearn
import matplotlib.pyplot as plt
from collections import Counter
import skimage.morphology
import skimage.measure
import matplotlib.patches as patches


def convertToFloat(im):
	for i in range(0, len(im)):
		for j in range(0, len(im[i])):
			im[i][j]=float(im[i][j])

	return im

def showImageAndPause(im, grayscale=False):
	if(grayscale):
		plt.imshow(im, cmap='gray')
	else:
		plt.imshow(im)

	plt.show()


def mostCommon(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

def findBackGroundColor(im, spacing = 25):
	borderPixels = []
	i = 0
	while(i<im.shape[1]):
		borderPixels.append(im[0][i])
		borderPixels.append(im[im.shape[0]-1][i])
		i+=spacing
	i = 0
	while(i<im.shape[0]):
		borderPixels.append(im[i][0])
		borderPixels.append(im[i][im.shape[1]-1])
		i+=spacing

	return(mostCommon(borderPixels))

def getBorderSeeds(im, spacing = 50):
	borderPixels = []
	i=0

	while(i<im.shape[1]):
		borderPixels.append([0, i])
		borderPixels.append([im.shape[0]-1, i])
		i+=spacing

	i = 0

	while(i<im.shape[0]):
		borderPixels.append([i, 0])
		borderPixels.append([i, im.shape[1]-1])
		i+=spacing

	return borderPixels

def getNeighbors(point, x, y):
	ret = []
	if(point[0]<x-1):
		ret.append([point[0]+1, point[1]])
	if(point[0]>0):
		ret.append([point[0]-1, point[1]])

	if(point[1]<y-1):
		ret.append([point[0], point[1]+1])
	if(point[1]>0):
		ret.append([point[0], point[1]-1])

	return ret



def getBinaryImage(im):
	binaryImage = np.ones(im.shape)
	seeds = getBorderSeeds(im)
	pixelsDone = []
	while(len(seeds)>0):
		#print(len(seeds))
		curPoint = seeds[0]
		binaryImage[curPoint[0], curPoint[1]]=0
		seeds.remove(curPoint)
		pixelsDone.append(curPoint)
		curNeighbors = getNeighbors(curPoint, im.shape[0], im.shape[1])
		for n in curNeighbors:
			if(not n in seeds and not n in pixelsDone):
				if(abs(im[curPoint[0], curPoint[1]]-im[n[0], n[1]])<10):
					seeds.append(n)

	

	steps = 1

	for i in range(0, steps):
		binaryImage = skimage.morphology.erosion(binaryImage, skimage.morphology.square(3))

	for i in range(0, steps):
		binaryImage = skimage.morphology.dilation(binaryImage, skimage.morphology.square(3))

	

		steps = 5
	for i in range(0, steps):
		binaryImage = skimage.morphology.opening(binaryImage)


	return binaryImage

def getBinaryImage2(im):
	bc = findBackGroundColor(im)
	binaryImage = np.zeros(im.shape)
	for i in range(0, im.shape[0]):
		for j in range(0, im.shape[1]):
			if(im[i][j]==bc):
				binaryImage[i][j]=255

	#binaryImage = getSubSample(binaryImage, 10)

	steps = 50

	for i in range(0, 5):
		binaryImage = skimage.morphology.opening(binaryImage, skimage.morphology.square(20))
	return binaryImage

def convertBinaryImageToGray(im):
	x = np.zeros(im.shape)

	for i in range(0, im.shape[0]):
		for j in range(0, im.shape[1]):
			if(im[i][j]):
				x[i][j]=1

	return x

def getMaxElement(im):
	ret = 0
	for i in range(0, im.shape[0]):
		for j in range(0, im.shape[1]):
			if(im[i][j]>ret):
				ret = im[i][j]
	return ret


def getTops(imlabels):
	imlabels= np.array(imlabels)
	numlabels = getMaxElement(imlabels)
	ret = []
	for i in range(0, numlabels+1):
		ret.append(0)
	topsseen = []
	x = 0
	while(len(topsseen)<numlabels+1 and x<imlabels.shape[0]):
		for y in range(0, imlabels.shape[1]):
			isSeen = int(imlabels[x][y]) in topsseen
			if not isSeen:
				topsseen.append(int(imlabels[x][y]))
				ret[int(imlabels[x][y])]=x
		x+=1
	return ret

def getBottoms(imlabels):
	imlabels= np.array(imlabels)
	numlabels = getMaxElement(imlabels)
	ret = []
	for i in range(0, numlabels+1):
		ret.append(0)
	botsseen = []
	x = imlabels.shape[0]-1
	while(len(botsseen)<numlabels+1 and x>=0):
		for y in range(0, imlabels.shape[1]):
			isSeen = int(imlabels[x][y]) in botsseen
			if not isSeen:
				botsseen.append(int(imlabels[x][y]))
				ret[int(imlabels[x][y])]=x
		x-=1
	return ret

def getLefts(imlabels):
	imlabels= np.array(imlabels)
	numlabels = getMaxElement(imlabels)
	ret = []
	for i in range(0, numlabels+1):
		ret.append(0)
	leftsseen = []
	y =  0
	while(len(leftsseen)<numlabels+1 and y<imlabels.shape[1]):
		for x in range(0, imlabels.shape[0]):
			isSeen = int(imlabels[x][y]) in leftsseen
			if not isSeen:
				leftsseen.append(int(imlabels[x][y]))
				ret[int(imlabels[x][y])]=y
		y+=1
	return ret

def getRights(imlabels):
	imlabels= np.array(imlabels)
	numlabels = getMaxElement(imlabels)
	ret = []
	for i in range(0, numlabels+1):
		ret.append(0)
	rightseen = []
	y =  imlabels.shape[1]-1
	while(len(rightseen)<numlabels+1 and y>=0):
		for x in range(0, imlabels.shape[0]):
			isSeen = int(imlabels[x][y]) in rightseen
			if not isSeen:
				rightseen.append(int(imlabels[x][y]))
				ret[int(imlabels[x][y])]=y
		y-=1
	return ret

	
def getRectangles(imlabels):
	tops = getTops(imlabels)
	bots = getBottoms(imlabels)
	lefts = getLefts(imlabels)
	rights = getRights(imlabels)

	ret = []

	for i in range(len(tops)):
		ret.append([(lefts[i], tops[i]), rights[i]-lefts[i], bots[i]-tops[i]])

	return ret[1:]


def getSubSample(im, step):
	ret = []
	for i in im[0::step]:
		ret.append(i[0::step])

	return np.array(ret)


def imageRead(filename, flat = True):
	im = scipy.ndimage.imread(filename, flatten=flat)
	return np.array(im)

def expandRectangles(rs, scale):
	ret = []
	for r in rs:
		ret.append([(r[0][0]*scale, r[0][1]*scale), r[1]*scale, r[2]*scale])

	return ret

def getImageSectionColor(im, x, y, r, c):
	print(im.shape)
	print(x)
	print(y)
	print(r)
	print(c)
	ret = []
	for xi in range(x, x+r):
		curRow = []
		for yi in range(y, y+c):
			curRow.append(im[xi][yi])
		ret.append(curRow)
	return ret


fn = 'testims/0017.jpeg'

i1 = imageRead(fn)
icolor = imageRead(fn, False)
print(icolor.shape)
print('Image loaded.')

i2 = getBinaryImage(getSubSample(i1, 10));



all_labels = skimage.measure.label(i2)

fig, ax = plt.subplots(1)

rects = getRectangles(all_labels)
rects = expandRectangles(rects, 10)

ax.imshow(icolor)
#ax.axis('off')

for r in rects:
	if(r[1]>100 and r[2]>100):
		ax.add_patch(patches.Rectangle(r[0], r[1], r[2], linewidth = 2, edgecolor = 'r', fill = False))
plt.show()


for r in rects:
	if(r[1]>100 and r[2]>100):
		plt.imshow(getImageSectionColor(icolor, r[0][1], r[0][0], r[2], r[1]))
		plt.show()










