import cv2
import numpy as np
import matplotlib.pyplot as plt


#Object detection from a stable camera
objDetect = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


cap = cv2.VideoCapture(r"C:\Users\Alex_\Downloads\24103-339549402_small.mp4")


#Entering the initial ROI for tracking
initRet, initFrame = cap.read()
initROI = cv2.selectROI('ROI', initFrame)
cv2.imshow('Initial frame', initFrame)
cv2.destroyAllWindows()


class TrackedObj():
    def __init__(self, posList):
        self.posList = posList

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    #Applying mask to frame
    mask = objDetect.apply(frame)

    #Removing shadows from the tracking
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    #Determining the contours of the image
    contours, heir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for ct in contours:

        #Determining the area of elements in the image to remove background noise
        ctArea = cv2.contourArea(ct)
        if ctArea > 100:
            

            x, y, w, h = cv2.boundingRect(ct)
            centralPoint = (int((2*x+w)/2), int((2*y+h)/2))
            

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
        

    newROI = frame[int(initROI[1]):int(initROI[1]+initROI[3]),  
                int(initROI[0]):int(initROI[0]+initROI[2])] 
    

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('ROI', newROI)

    killVal = cv2.waitKey(1)
    if killVal == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()