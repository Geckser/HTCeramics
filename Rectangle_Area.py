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
from skimage.draw import (line, polygon,
                          circle_perimeter,
                          ellipse, ellipse_perimeter,
                          bezier_curve)

img = io.imread(file)
red_multiplier = [1, 0, 0]
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

# basic info on out image
print(type(img))
print("image type: ", img.dtype)

fig = plt.figure()

# converts from rgb which is 3d array to grey scale which is a 2d array
grayscale = rgb2gray(img)
threshold = skfilt.threshold_otsu(grayscale)


def CalcCornerPoints(linesArray, xMean, yMean, xValues, yValues, stopLength):
    indexValue = 0
    for i in linesArray:
        potMaxVal = math.sqrt((xMean - xValues[indexValue]) ** 2 + (yMean - yValues[indexValue]) ** 2)
        potMaxValList.append(potMaxVal)
        potMaxValIndex.append(indexValue)
        indexValue = indexValue + 1
    xMax = 0
    yMax = 0
    xMin = 1000000
    yMin = 1000000
    for z in xValues:
        if z > xMax:
            xMax = z
        if z < xMin:
            xMin = z
    for y in yValues:
        if y > yMax:
            yMax = y
        if y < yMin:
            yMin = y
    maxValTuple = (xMax, yMax)
    maxValList.append(maxValTuple)
    maxValTuple = (xMax, yMin)
    maxValList.append(maxValTuple)
    maxValTuple = (xMin, yMax)
    maxValList.append(maxValTuple)
    maxValTuple = (xMin, yMin)
    maxValList.append(maxValTuple)
    area = (xMax - xMin) * (yMax - yMin)
    print("The area is: ", area, "pixels")
    return maxValList


def DrawRectangle(maxValList, possibleLength):
    print("h")


# This applies the canny filter to our image and finds the edges


edgesArray = feature.canny(grayscale, sigma=3)
# print ("edges: ", type(edgesArray), " Shape: ", edgesArray.shape)

linesList = (probabilistic_hough_line(edgesArray, threshold=10, line_gap=3))

linesArray = np.asarray(linesList)
# print ("lines shape", linesArray.shape)
print(linesArray)
for i in linesArray[:, 0, 0]:
    print("Line #", lineNum, )

    print("x1 ----- ", linesArray[sheetNum, 0, 0])
    xValues.append(linesArray[sheetNum, 0, 0])

    print("y1 ----- ", linesArray[sheetNum, 0, 1])
    yValues.append(linesArray[sheetNum, 0, 1])

    print("x2 ----- ", linesArray[sheetNum, 1, 0])
    xValues.append(linesArray[sheetNum, 1, 0])

    print("y2 ----- ", linesArray[sheetNum, 1, 1])
    yValues.append(linesArray[sheetNum, 1, 1])

    lineNum = lineNum + 1
    sheetNum = sheetNum + 1

sheetNum = 0
xMean = statistics.mean(xValues)
yMean = statistics.mean(yValues)

stopLength = len(linesArray) - 4
maxValList = CalcCornerPoints(linesArray, xMean, yMean, xValues, yValues, stopLength)
xMax = 0
yMax = 0
xMin = 1000000
yMin = 1000000
for z in xValues:
    if z > xMax:
        xMax = z
    if z < xMin:
        xMin = z
for y in yValues:
    if y > yMax:
        yMax = y
    if y < yMin:
        yMin = y

# print("maxValList: ", maxValList)
DrawRectangle(maxValList, possibleLength)

# This loads the our images into subplots and removes axis

ax1 = fig.add_subplot(141)
ax1 = plt.imshow(img)

# ax1.axis('off')
# ax1.title ('Original Image', fontsize = 15)

ax2 = fig.add_subplot(142)
ax2 = plt.imshow(grayscale, cmap='Greys_r')

# ax[1].axis('off')
# ax2.title ('Edges', fontsize = 15)
xc, yc = grayscale.data.shape

ax3 = plt.subplots(ncols=2, nrows=1, figsize=(xc, yc))


poly = np.array((
    (yMax+10, xMin-10),
    (yMax+10, xMax+10),
    (yMin-10, xMax+10),
    (yMin-10, xMin-10),
))
rr, cc = polygon(poly[:, 0], poly[:, 1], img.shape)
img[rr, cc, 1] = 1
ax3 = plt.imshow(img, cmap='Greys_r')
# ax4 = plt.imshow(linePointHist, cmap = 'Greys_r')
# ax[2].axis('off')
# ax3.title ('Lines', fontsize = 15)

fig.tight_layout()
# show() function makes the image visable to viewer
plt.show()
