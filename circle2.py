

import sys
import matplotlib.pyplot as alt
import matplotlib
import numpy as np

import skimage
from skimage import io, data, measure, morphology, color

from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.color import rgb2gray

# When calling the function, target is the file you want to analyze, save is y|n, saveas is the filename you'd like to save the new image as.
# This is to compare color out vs color in.
# Comment this line out if you do not want to save the image.
#script, target, save, saveas = sys.argv

# Comment this line out if you want to save the image.
script, target = sys.argv
print('Do you wnat to edit any of the parameters? (y/n)')
yes_no = input()
#
if yes_no == 'y':
    number_of_circles = input('How many circles are present?')
    max_radius = input('What is the maximum radius')
    min_radius = input('What is the minimum radius')
else:
    number_of_circles = 1
    max_radius = 500
    min_radius = 250
# Read in an image from the directory specified when you call the function in Python

img = io.imread(target)
xc, yc, t = img.data.shape

grayscale = rgb2gray(img)  # To use the later image analyis, the initial image must be converted to grayscale

image = img_as_ubyte(
    grayscale[0:xc, 0:yc])  # converts the image to a specific file format that can later be analysed
# the array after 'grayscale' holds the size of the image.

edges = canny(image, sigma=3, low_threshold=max_radius*.1, high_threshold=max_radius*.2)  # canny identifies any edges on the shape
# sigma is required standard deviation, low and high threshold are the bounds for linking edges
# It is recommended that you use 10% of the max possible cirlce size for the low_threshold and twice that for the high threshold

h_radii = np.arange(min_radius, max_radius, 5)  # The first two are used to identify the high and low end of radii to search for
# This will need to be adjusted as different files are uploaded.

hough_res = hough_circle(edges, h_radii)  # function that calculates a 3D array where a very similar circle can live.
# It takes in the number of pixels that will be used to create the


print("Analysis almost complete...")

accums, x, y, radius = hough_circle_peaks(hough_res, h_radii, total_num_peaks=number_of_circles)
# the hough_cirlce_peaks function takes the imaginary 'hough circle', the anticipated radii, and the anticiapted number of circles
# it uses this to find the Peak values in 'hough space', the positions of the circles and the radii of the circles

print(radius)
# Prints the radii of the identified circles

fig, ax = alt.subplots(ncols=1, nrows=1, figsize=(10, 4))
image = color.gray2rgb(image)
for center_y, center_x, radius in zip(y, x, radius):  # This for loop draws the circles that were generated earlier
    circy, circx = circle_perimeter(center_y, center_x, radius,
                                    shape=image.shape)
    image[circy, circx] = (220, 20, 20)

ax.imshow(image)  # This loads the edited image into the environment

alt.show()  # this takes the uploaded image and displays it for the user

#if save == "y":
 #   io.imsave(saveas, image)
  #  print(f"Image saved as {saveas}.")
#else:
 #   quit()
