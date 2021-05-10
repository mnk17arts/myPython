"""
VIRTUAL PAINTER - OPENCV

In this project I have created a virtual paint project using OpenCv and other packages. We can draw on the 
Screen(out image) using fingers(moving in the webcam viewport area). For drawing we use our index finger open. There are
 5 different colors available in this project and an eraser to erase drawn work. For selection we use our index and 
 middle fingers open. We can even change the brush and rubber size through the changing values in the respected variables
 .

packages :  cv2
            numpy
            time
            os
            HandTrackingModule.py

steps involved:
-> import the image
-> find hand landmarks
-> check which fingers are up. SELECT when two fingers are up
-> if selection mode - when two fingers are up... SELECT
-> if drawing mode - index finger is up

Note: Maximum one hand is tracked in this project.

code by : Madhapur Nitish kumar
github profile:  https://github.com/mnk17arts
any kind of suggestions are welcomed : mailto:mnk17arts@gmail.com

  thank you :)

"""


import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm  # **must be in same folder

#########################    VARIABLES
brushThickness = 10
eraserThickness = 50
#########################

headerpath = "virtualpaint"
myList = os.listdir(headerpath)
# print(myList)
overLayList = []

for impath in myList:
    image = cv2.imread(f'{headerpath}/{impath}')
    overLayList.append(image)
# print(len(overLayList))

header = overLayList[0]
drawColor = (0,0,225)  # red color (note: color in BGR)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height




detector = htm.handDetector(detecCon=0.85, maxHands=1)
xp, yp = (0, 0)
imgCanvas = np.ones((720, 1280, 3), np.uint8)  # creating a black canvas on which we can draw..
                    # size (h, w, channels) # unsigned integers [0,255]
# imgCanvas.fill(255)  # or imgCanvas[:] = 255 # white canvas
while True:
    # 1. import the image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flips image to overcome mirror thing

    # 2. find hand landmarks
    img = detector.findHands(img, draw=True)  # detect hand on our image
    lnList = detector.findPosition(img, draw=False)
    img2 = img
    if len(lnList) != 0:
        # print(lnList)  # array of [id, x, y]...

        x1, y1 = lnList[8][1:]
        x2, y2 = lnList[12][1:]

    # 3. check which fingers are up. SELECT when two fingers are up
        fingers = detector.fingersUp()
        # print(fingers)  # ex: [1, 0, 1, 0, 1]

    # 4. if selection mode - when two fingers are up... SELECT
        if fingers[1] and fingers[2]:
            # print("selection mode")
            xp, yp = (0, 0)
            # checking for the click
            """
            height = 137 (avg h of header... as i cropped manually .. not every header height is same)
            width = 1280
            red w = [402, 534]
            yellow w = [544, 676]
            blue w = [690, 823]
            green w = [840, 972]
            black w = [984, 1117]
            eraser w = [1142, 1274]
            """
            if y1 < 137:
                if 402 < x1 < 534 :
                    header = overLayList[0]
                    drawColor = (0, 0, 255)  # red color
                elif 544 < x1 < 676:
                    header = overLayList[1]
                    drawColor = (0, 255, 255)  # yellow color
                elif 690 < x1 < 823:
                    header = overLayList[2]
                    drawColor = (255, 255, 0)  # sky blue color
                elif 840 < x1 < 972:
                    header = overLayList[3]
                    drawColor = (0, 255, 0)  # green color
                elif 984 < x1 < 1117:
                    header = overLayList[4]
                    drawColor = (255, 255, 255)  # white color
                elif 1142 < x1 < 1274:
                    header = overLayList[5]
                    drawColor = (0, 0, 0)   # black color
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

    # 5. if drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("drawing mode")
            """
            we need to draw based on our points. For that we need starting and ending point.
            method 1 : using simple points... single circle... movement ..another circle... but when the movement is
            rapid.. it doesnt work properly.
            method 2 : using line.. requires 2 points 
            
            end point : ( x1, y1 )
            starting point : (xp, yp ) 
            
            * before using imgCanvas the drawn line was disappearing as well in every iteration
            * after making imgCanvas we blend our img and imgCanvas. but this method make screen to look dull
            * we used another method (cv2.cvtColor....threshold...and many more..
            
            """
            if y1 > 137:
                if xp == 0 and yp == 0:  # if not used, in starting it will draw line from origin
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)


            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1


    """
    LIL COMPLICATED
    plan: 
    * convert imgCanvas to black n white..n wherever ters black cnvrt into white and werevr ters a color cnvrt into black
    * and then adding it to our img using bitwise technique
    steps:
    1. converting imgCanvas BGR to GRAY (gray image) and then  gray to binary image and then inverting it
    2. converting imgInv to BGR to add it to our original img
    """
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)  # bgr to gray
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)  # gray to binary and then invert it
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)  # gray to bgr  [
    img = cv2.bitwise_and(img, imgInv)  # AND operation... 
    img = cv2.bitwise_or(img, imgCanvas)  # OR operation...


    # setting header image
    h, w, c = header.shape  # size of header images...

    # adding text and colors on header
    cv2.circle(header, (500, 100), 20, (0, 0, 255), cv2.FILLED)
    cv2.circle(header, (642, 100), 20, (0, 255, 255), cv2.FILLED)
    cv2.circle(header, (789, 100), 20, (255, 255, 0), cv2.FILLED)
    cv2.circle(header, (938, 100), 20, (0, 255, 0), cv2.FILLED)
    cv2.circle(header, (1083, 100), 20, (255, 255, 255), cv2.FILLED)
    cv2.circle(header, (1240, 100), 20, (0, 0, 0), cv2.FILLED)
    cv2.putText(header, "MNK17ARTS'", (120, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
    cv2.putText(header, "VIRTUAL PAINT", (120, 110), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
    img[0:h, 0:w] = header  # header on img


    ## blending img and imgCanvas into 1 (img)
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv2.imshow("Image", img)  # shows image
    cv2.imshow("Canvas", imgCanvas)  # shows Canvas image 
    cv2.imshow("inv",imgInv)  # imgInv
    cv2.waitKey(1)  # delay of 1ms
