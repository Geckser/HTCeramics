import cv2
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import imutils

cap = cv2.VideoCapture(0)

def ProcessImage():

    cv2.waitKey(500)
    success, img = cap.read()
    grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurredImg = cv2.GaussianBlur(grayScale, (5,5), 0)
    ret, thresholdImg = cv2.threshold(blurredImg, 160, 255, cv2.THRESH_BINARY)
    contours = cv2.findContours(thresholdImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for i in contours:
        M = cv2.moments(i)
        if M["m00"] == 0:
            print ("line")

        else:
            xCenter = M["m10"] / M["m00"]
            xCenter = int(xCenter)
            yCenter = M["m01"] / M["m00"]
            yCenter = int(yCenter)

            cv2.drawContours(img, contours, -1, (0,255,0), 3)
            cv2.circle(img, (xCenter,yCenter), 7, (0,255,0), -1)
            cv2.putText(img, str(M["m00"]), (xCenter + 20, yCenter + 20), cv2.FONT_HERSHEY_SIMPLEX, .75, (255,0,0), 1, cv2.LINE_AA)


    cv2.imshow("Raw Image", img)
    #cv2.imshow("Grayscale", grayScale)
    #cv2.imshow("Binary Threshold", thresholdImg)

while True:
    if keyboard.is_pressed("right shift"):
        print("Shutting Down")
        exit()

    else:
        ProcessImage()
