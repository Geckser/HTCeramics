from __future__ import print_function
from imutils import perspective, contours
from scipy.spatial import distance as dist
import numpy as np
import cv2 as cv
import imutils

# # the image you want to use
# image_file = "readin.jpg"
# # the save-as name you'd like
# saveas = "saveas.png"

# or, if you'd rather...
from sys import argv
this_script, image_file, saveas = argv

contour_threshold = 100

def order_points(points):
    # Sort based on x coord
    xSort = points[np.argsort(points[:0]), :]

    #take side extremes
    leftMost = xSort[:2, :]
    rightMost = xSort[2:, :]

    # sort by y
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (topLeft, bottomLeft) = leftMost

    # use euclidian geometry... longest distance between our defined
    # top left point (lowest combined corrdinates) is our bottom right point.
    # otherwise it's hard to tell which is top and which is bottom
    diag = dist.cdist(topLeft[np.newaxis], rightMost, "euclidian") [0]
    (bottomRight, topRight) = rightMost[np.argsort(diag)[::-1], :]

    # return these coordinates for later use - starting at top left anchor
    # and staying clockwise
    return np.array([topLeft, topRight, bottomRight, bottomLeft], dtype="float32")

# now let's test this out on an image.
# to define this image, head to line 6
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

contour_list = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contour_list = imutils.grab_contours(contour_list)

# sort from left to right
(contour_list, _) = contours.sort_contours(contour_list)

# loop over contours
for (i, j) in enumerate(contour_list):
    # ignore small contours
    if cv.contourArea(j) < contour_threshold:
        continue
    # we're going to draw a box
    box = cv.minAreaRect(j)
    box = cv.boxPoints(box)
    box = np.array(box, dtype ="int")
    cv.drawContours(image, [box], -1, (0, 255, 0), 2)
    # show me the money! Print each box to console
    print("Object #{}:".format(i+1))
    print(box)
    # so NOW we're going to use the ordering we deciphered earlier.
    rectangle = perspective.order_points(box)
    # and print them
    print(rectangle.astype("int"))
    print("")
    # put the object number at the topLeft corner
    # mostly so we can see wtf it's doing
    cv.putText(image, "#{}".format(i+1),
        (int(rectangle[0][0] - 15), int(rectangle[0][1] - 15)),
        cv.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255),2)
        #FONT_HERSHEY_SIMPLEX is the first option in the dropdown

# I think I say this too much but ... show us the money
cv.imshow('Press esc to quit or press s to save as %s' %saveas, image)
k = cv.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv.imwrite(saveas, image)
    cv.destroyAllWindows()
