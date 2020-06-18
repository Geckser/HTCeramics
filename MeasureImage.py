import sys
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.draw import disk
from skimage.color import rgb2gray
from skimage import io, data, measure, morphology, color
from skimage.measure import label, regionprops,regionprops_table
from skimage.util import img_as_ubyte
from skimage.transform import rotate
script,target = sys.argv

img = io.imread(target)
xc, yc, t = img.data.shape
grayscale = rgb2gray(img)
img = img_as_ubyte(
   grayscale[0:xc, 0:yc])
#image size




#The section below here I think is actually aimed at measuring the pictures

label_img =label(img)
regions = regionprops(label_img)

fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.gray)



for props in regions:
    x0 = xc
    y0 = yc

    x1 = x0 + .5 * props.minor_axis_length
    y1 = y0 - .5 * props.minor_axis_length
    x2 = x0 - .5 * props.major_axis_length
    y2 = y0 - .5 * props.major_axis_length

    ax.plot((x0, x1), (y0,y1), '-r', linewidth=2.5)
    ax.plot((x0,x2), (y0,y2), '-r', linewidth=2.5)
    ax.plot(x0,y0, '.g', markersize=15)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx,by,'-b', linewidth=2.5)

ax.axis((0,1200,1200,0))
plt.show()



print("x1 is:", x1)
print("x y coordinates are:", x0, ",", y0 )
print("centroid is", props.centroid)
print("orientation is: ", props.orientation)
print("area is", props.area)
print("radius is:", props.major_axis_length)