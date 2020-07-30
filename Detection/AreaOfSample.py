# This code analyzes an image and computes the area, in terms of pixels, of various isolated objects. The main filters used are
# grayscale, Gaussian blur, and thresholding. Image data is read in real time using a connected video camera. The area is calculated 
# with the use of moments and therefore includes notation from linear algebra. 

import cv2
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import imutils

# 0 denotes the default system webcam. MAY NEED TO BE CHANGED FOR SYSTEMS WITH 2 CAMERAS!!! 
cap = cv2.VideoCapture(0)       

def ProcessImage():
    
    # Pauses for certain period of time (in milliseconds) before reading the data from the camera and storing it in the "img" array
    cv2.waitKey(500)        
    success, img = cap.read() 
    
    # The following lines apply various filters to our image. These are grayscale, Gaussian blur, and thresholding
    grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                   
    blurredImg = cv2.GaussianBlur(grayScale, (5,5), 0)                                                                                                                  
    ret, thresholdImg = cv2.threshold(blurredImg, 160, 255, cv2.THRESH_BINARY)  
    
    # Looks for contours within our image and returns a list, then stores the returned list
    cnts = cv2.findContours(thresholdImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)       
    cnts = imutils.grab_contours(cnts)                                                  

    for i in cnts:
        
        # Computes the moment for each contour
        M = cv2.moments(i)      
        
        # Filter out lines as they do not have an area. M["m00"] denotes area. 
        if M["m00"] == 0:       
            print ("line")

        else:
            
            # Computes the X value of the center point of an object by dividing the first X value of the object by the object's total area. 
            xCenter = M["m10"] / M["m00"]       
            xCenter = int(xCenter)
            
            # Computes the Y value of the center point of an object by dividing the first Y value of the object by the object's total area. 
            yCenter = M["m01"] / M["m00"]
            yCenter = int(yCenter)
            
            # Draw contours, mark center point, and display area, all on the raw image. 
            cv2.drawContours(img, cnts, -1, (0,255,0), 3)
            cv2.circle(img, (xCenter,yCenter), 7, (0,255,0), -1)
            cv2.putText(img, str(M["m00"]), (xCenter + 20, yCenter + 20), cv2.FONT_HERSHEY_SIMPLEX, .75, (255,0,0), 1, cv2.LINE_AA)


    cv2.imshow("Raw Image", img)

while True:
    
    # This if statement allows the program to be shut down when the RIGHT SHIFT key is pressed. 
    if keyboard.is_pressed("right shift"):
        print("Shutting Down")
        exit()

    else:
        ProcessImage()
