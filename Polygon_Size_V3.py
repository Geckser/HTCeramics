import numpy as np
import matplotlib.pyplot as plt
import sys
from skimage.color import rgb2gray, gray2rgb
from skimage.draw import line_nd
from skimage import io, measure, color
import skimage.filters as skfilt
from skimage.transform import probabilistic_hough_line
from skimage.util import img_as_ubyte
from skimage import feature
from itertools import product
import random
import statistics
import math
script, file = sys.argv

img = io.imread(file)
red_multiplier = [1,0,0]
lineNum = 1
sheetNum = 0
xValues = []
yValues = []
potMaxValList = []
maxValList = []
mergedMaxVal = []
potMaxValIndex = []
possibleLength = []
sideLength = []

#basic info on out image
print(type(img))
print("image type: ", img.dtype)

fig = plt.figure()

#converts from rgb which is 3d array to grey scale which is a 2d array
grayscale = rgb2gray(img)
threshold = skfilt.threshold_otsu(grayscale)

def CalcCornerPoints(linesArray, xMean, yMean, xValues, yValues, stopLength):
    indexValue = 0
    for i in linesArray:
        potMaxVal = math.sqrt((xMean - xValues[indexValue])**2 + (yMean - yValues[indexValue])**2)
        potMaxValList.append(potMaxVal)
        potMaxValIndex.append(indexValue)
        indexValue = indexValue + 1

    while len(potMaxValList) > stopLength:
        #mergedMaxVal.append(MergeLists(xValues[potMaxValList.index(max(potMaxValList))], yValues[potMaxValList.index(max(potMaxValList))]))
        maxValTuple = (xValues[potMaxValList.index(max(potMaxValList))], yValues[potMaxValList.index(max(potMaxValList))])
        maxValList.append(maxValTuple)
        #maxValList.append(yValues[potMaxValList.index(max(potMaxValList))])
        potMaxValList.remove(max(potMaxValList))

    return maxValList

def DrawRectangle(maxValList , possibleLength):
    for i in range(1000):
        startPoint = random.choice(maxValList)
        endPoint = random.choice(maxValList)
        possibleLength.append(math.sqrt((startPoint[0] - endPoint[0])**2 + (startPoint[1]-endPoint[1])**2))

    print (possibleLength)
    possibleLength = list(filter((0.0).__ne__, possibleLength))

    while len(sideLength) < 2:
        sideLength.append(min(possibleLength))
        possibleLength = list(filter((min(possibleLength)).__ne__, possibleLength))
    print (sideLength)
    print("AREA: ", sideLength[0]*sideLength[1])

#This applies the canny filter to our image and finds the edges
edgesArray = feature.canny(grayscale, sigma = 3)
print ("edges: ", type(edgesArray), " Shape: ", edgesArray.shape)

linesList = (probabilistic_hough_line(edgesArray, threshold = 10, line_gap = 3))

linesArray = np.asarray(linesList)
#print ("lines shape", linesArray.shape)
print (linesArray)
for i in linesArray[:, 0,0]:
    print("Line #",lineNum,)

    print("x1 ----- ", linesArray[sheetNum,0,0])
    xValues.append(linesArray[sheetNum,0,0])

    print("y1 ----- ", linesArray[sheetNum,0,1])
    yValues.append(linesArray[sheetNum,0,1])

    print("x2 ----- ", linesArray[sheetNum,1,0])
    xValues.append(linesArray[sheetNum,1,0])

    print("y2 ----- ", linesArray[sheetNum,1,1])
    yValues.append(linesArray[sheetNum,1,1])

    lineNum = lineNum + 1
    sheetNum = sheetNum + 1

sheetNum = 0
xMean = statistics.mean(xValues)
yMean = statistics.mean(yValues)

stopLength = len(linesArray) - 4
maxValList = CalcCornerPoints(linesArray, xMean, yMean, xValues, yValues, stopLength)
print("maxValList: ", maxValList)
DrawRectangle(maxValList, possibleLength)

#This loads the our images into subplots and removes axis

ax1 = fig.add_subplot(141)
ax1 = plt.imshow(img)

#ax1.axis('off')
#ax1.title ('Original Image', fontsize = 15)

ax2 = fig.add_subplot(142)
ax2 = plt.imshow(grayscale, cmap = 'Greys_r')

#ax[1].axis('off')
#ax2.title ('Edges', fontsize = 15)

ax3 = fig.add_subplot(143)
ax3 = plt.imshow(edgesArray, cmap = 'Greys_r')

#ax4 = plt.imshow(linePointHist, cmap = 'Greys_r')
#ax[2].axis('off')
#ax3.title ('Lines', fontsize = 15)

fig.tight_layout()
#show() function makes the image visable to viewer
plt.show()
