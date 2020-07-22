# Call this file with the image you want to parse as an argument in the CLI

import numpy
import matplotlib.pyplot as plt

from sys import argv
from skimage.io import imread, imsave
from skimage import filters, data
from skimage.util import compare_images
from skimage.color import rgb2gray, gray2rgb

# pull the file from command line
# # To do: learn GUI stuff
image = argv[1]
image = imread(image)

# grayscale to 2D array that ish
grey_image = rgb2gray(image)

# to call without needing to provide an argument every time.
edge_roberts = filters.roberts(grey_image)
edge_sobel = filters.sobel(grey_image)
edge_scharr = filters.scharr(grey_image)
edge_prewitt = filters.prewitt(grey_image)

# Plot them next to each other, on the same scale.
fig, axes = plt.subplots(nrows = 2, ncols = 2, sharex=True, sharey = True, figsize=(10,10))

# plot it in grayscale, label it with the edge operator being used
axes[0,0].imshow(edge_roberts, cmap=plt.cm.gray)
axes[0,0].set_title("Roberts")

axes[0,1].imshow(edge_sobel, cmap = plt.cm.gray)
axes[0,1].set_title("Sobel")

axes[1,0].imshow(edge_scharr, cmap=plt.cm.gray)
axes[1,0].set_title('Scharr')

axes[1,1].imshow(edge_prewitt, cmap=plt.cm.gray)
axes[1,1].set_title('Prewitt')

# Comment out if you want the numbers on the axes.
for ax in axes:
    for i in ax:
        i.axis('off')

# Show me the results, with less whitespace.
plt.tight_layout()
plt.show()

#mary
