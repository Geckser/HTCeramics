import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.draw import disk

from skimage.measure import label, regionprops,regionprops_table
from skimage.transform import rotate
# This section draws the two ellipses. This can likely be deleted when we start importing images

#image size
image = np.zeros((600,600))
# center coordinate, radius
rr, cc = disk((200,200), 50)

image[rr,cc] = 1
image = rotate(image, angle=0, order=0)

#rr,cc = disk((400,300),100)
#image[rr,cc] = 1

label_img =label(image)
regions = regionprops(label_img)

#The section below here I think is actually aimed at measuring the pictures
fig, ax = plt.subplots()
ax.imshow(image, cmap=plt.cm.gray)

for props in regions:
    y0, x0 =props.centroid
    orientation = props.centroid
    orientation = props.orientation
    x1 = x0 +math.cos(orientation)*.5 * props.minor_axis_length
    y1 = y0 - math.sin(orientation) * .5* props.minor_axis_length
    x2 = x0 - math.sin(orientation) *.5*props.major_axis_length
    y2 = y0 - math.cos(orientation)* .5 * props.major_axis_length

    ax.plot((x0, x1), (y0,y1), '-r', linewidth=2.5)
    ax.plot((x0,x2), (y0,y2), '-r', linewidth=2.5)
    ax.plot(x0,y0, '.g', markersize=15)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx,by,'-b', linewidth=2.5)

ax.axis((0,600,600,0))
plt.show()



print("x1 is:", x1)
print("x y coordinates are:", x0, ",", y0 )
print("centroid is", props.centroid)
print("orientation is: ", props.orientation)
print("area is", props.area)