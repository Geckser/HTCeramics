import numpy as np
import matplotlib.pyplot as plt
import sys
from skimage.draw import ellipse
from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray
from skimage import io, data, measure, morphology, color
script, target = sys.argv
img = io.imread(target)
xc, yc, t = img.data.shape

grayscale = rgb2gray(img)  # To use the later image analyis, the initial image must be converted to grayscale

img = img_as_ubyte(
    grayscale[0:xc, 0:yc])

fig, (ax2) = plt.subplots(ncols=1, figsize=[xc, yc])
plt.gray()
ax2.imshow(img)
maxi = 0
mini = 0
# approximate / simplify coordinates of the two ellipses
for contour in find_contours(img, 0):
    coords = approximate_polygon(contour, tolerance=1)
    if len(contour) > 10:
        ax2.plot(coords[:, 1], coords[:, 0], '-r', linewidth=1)
        print(coords)
        for h in coords:
            print(coords.min())

    coords2 = approximate_polygon(contour, tolerance=10)
    if len(contour) > 10:
        ax2.plot(coords2[:, 1], coords2[:, 0], '-g', linewidth=1)
        print(coords2)
    if len(contour) > 10:
        print("Number of coordinates:", len(contour)/6, len(coords), len(coords2))

ax2.axis((0, xc, 0, yc))

plt.show()
