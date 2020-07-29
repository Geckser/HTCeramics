import cv2 as cv
from scipy.spatial import distance as dist
import numpy as np

# # the image you want to use
# image_file = "alumina_chips.jpg"
# # the save-as name you'd like
# saveas = "testedge3.png"

# or, if you'd rather...
from sys import argv
this_script, image_file, saveas = argv


# to define this image, look above.
image = cv.imread(image_file)

# convert to gray because we need 2D arrays
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # to do: try scikitimage as well
# this is some fancy stuff... make it harder to detect edges on purpose.
# in an attempt to compensate for not having real images to test it on rn
gray_image = cv.GaussianBlur(gray_image, (5, 5), 0)

# to do: play with thresholds
edged = cv.Canny(gray_image, 30, 75)
# dilating and eroding helps close gaps
edged = cv.dilate(edged, None, iterations = 1)
edged = cv.erode(edged, None, iterations = 1)

cv.imshow('Press esc to quit or press s to save as %s' %saveas, edged)
k = cv.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv.imwrite(saveas, edged)
    cv.destroyAllWindows()
