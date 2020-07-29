from __future__ import print_function
from imutils import perspective, contours
from scipy.spatial import distance as dist
import numpy as np
import cv2 as cv
import tkinter as tk
import imutils

# # the image you want to use
# image_file = "readin.jpg"
# # the save-as name you'd like
# saveas = "saveas.png"

# or, if you'd rather...
from sys import argv
this_script, image_file, saveas = argv

# When is a contour too small to count? Is a contour a contour, no matter how small?
contour_threshold = 100

def order_points(points):
    # Sort based on x coord of given points.
    xSort = points[np.argsort(points[:0]), :]

    #take side extremes
    leftMost = xSort[:2, :]
    rightMost = xSort[2:, :]

    # sort by y
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (topLeft, bottomLeft) = leftMost

    # use euclidian geometry... longest distance between our defined
    # top left point (lowest combined corrdinates) is our bottom right point.
    # otherwise it's hard to tell which is top right and which is bottom
    diag = dist.cdist(topLeft[np.newaxis], rightMost, "euclidian") [0]
    (bottomRight, topRight) = rightMost[np.argsort(diag)[::-1], :]

    # return these coordinates for later use - starting at top left anchor
    # and staying clockwise, for my sanity
    return np.array([topLeft, topRight, bottomRight, bottomLeft], dtype="float32")

# now let's test this out on an image.
# to define this image, head to line 16
image = cv.imread(image_file)

# convert to gray because we need 2D arrays
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # to do: try scikitimage as well
# re: skimage... I can't get it to work, so they must be working fundamentally differently.

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
    # ignore too-small contours
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

# if the image is bigger than the screen, this will keep it in sight.
# this really should have its own cv.stuff already.
def show_image():
    screen_info = tk.Tk()
    screen_width = screen_info.winfo_screenwidth()
    screen_height = screen_info.winfo_screenheight()
    scale_width = screen_width / image.shape[1]
    scale_height = screen_height / image.shape[0]
    scale = min(scale_width, scale_height)
    # Resized
    window_width = int(image.shape[1]*scale)
    window_height = int(image.shape[0]*scale)
    return window_width, window_height
    # return window_height

window_width, window_height = show_image()

# Define the winodw title so you don't have to write it out 1000 times.
window_title = "Press esc to quit, or press s to save as %s" %saveas
cv.namedWindow(window_title, cv.WINDOW_NORMAL)
cv.resizeWindow(window_title, show_image())
cv.moveWindow(window_title, 0, 0)

# # ------ This section exists only for testing
# cv.imshow(window_title, edged)
# cv.waitKey(0)
# # ------ End testing section

# I think I say this too much but ... show us the money
cv.imshow(window_title, image)
k = cv.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv.imwrite(saveas, image)
    cv.destroyAllWindows()
