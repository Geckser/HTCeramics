import numpy as np
import matplotlib.pyplot as plt
import sys

from skimage import measure,io, color
from skimage.color import rgb2gray
from skimage.util import img_as_ubyte
script, target = sys.argv

img = io.imread(target)

xc, yc,t = img.data.shape

grayscale = rgb2gray(img)
image = img_as_ubyte(
   grayscale[0:xc, 0:yc])


contours = measure.find_contours(image, .1)



fig, ax = plt.subplots()
ax.imshow(img, cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:,1], contour[:,0], linewidth=2)
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()