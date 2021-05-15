"""
FINGER COUNTER - OPENCV

In this project input is given through webcam. When a hand is tracked down our project gives the output of the Number
which was shown by user's hand.

packages : ** cv2
           ** HandTrackingModule  (HandTrackingModule.py )
              os
              time
              datetime

explanation:
if hand is tracked then
    1. check status(1 or 0) of thumb
       * left hand...
         if x ordinate of thumb tip is less than that of pinky finger tip, then its left hand...else right hand
         if x ordinate of thumb tip is less than that of thumb ip, then thumb is open(appends 1)... else closed(0)
       * right hand...
         if x ordinate of thumb tip is less than that of thumb ip, then thumb is closed(0)... else opened(1)
    2. check status of remaining fingers...
        if y ordinate of a finger tip is less than that of its pip, then that finger is open(1)... else closed(0)
    3. through this status list recognise the number showed in input...

    refer [https://user-images.githubusercontent.com/71878747/118373592-63aee580-b5d5-11eb-9fe7-a0fcf00cab1d.jpg] for tip, ip, pip of fingers...

hand landmarks:
  WRIST = 0
  THUMB_CMC = 1
  THUMB_MCP = 2
  THUMB_IP = 3
  THUMB_TIP = 4
  INDEX_FINGER_MCP = 5
  INDEX_FINGER_PIP = 6
  INDEX_FINGER_DIP = 7
  INDEX_FINGER_TIP = 8
  MIDDLE_FINGER_MCP = 9
  MIDDLE_FINGER_PIP = 10
  MIDDLE_FINGER_DIP = 11
  MIDDLE_FINGER_TIP = 12
  RING_FINGER_MCP = 13
  RING_FINGER_PIP = 14
  RING_FINGER_DIP = 15
  RING_FINGER_TIP = 16
  PINKY_MCP = 17
  PINKY_PIP = 18
  PINKY_DIP = 19
  PINKY_TIP = 20

ps: HandTrackingModule is my python file consisting of
    class handDetector()
         method findHands()
         method findPosition()

code by : Madhapur Nitish kumar
github profile:  https://github.com/mnk17arts
any kind of suggestions are welcomed : mailto:mnk17arts@gmail.com

  thank you :)
"""

import cv2
import time
import os
import datetime
import HandTrackingModule as htm  # **must be in same folder



def main():
    # webcam
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)  # input...
    cap.set(3, wCam)
    cap.set(4, hCam)

    # frame rate ( fps )
    cTime = 0
    pTime = 0

    # for displaying finger images (showing numbers...0,1,2,3,4,5)
    folderpath = "fingerimages"  # folder containing those finger images...
    myList = os.listdir(folderpath)
    overLayList = []  # list of those finger images...
    # print(myList)  # crosschecking...
    for imPath in myList:
        image = cv2.imread(f'{folderpath}/{imPath}')
        # print(f'{folderpath}/{imPath}')  # crosschecking...
        overLayList.append(image)

    # print(len(overLayList))  # crosschecking...

    detector = htm.handDetector(detecCon=0.75, maxHands=1)  # instance of handDetector

    tipIDs = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

    # process...
    while True:

        success, img = cap.read()  # returns (True, array)
        img = detector.findHands(img)  # tracks hand in the input...
        lnList = detector.findPosition(img, draw=False)  # gets position of landmarks of all fingers...
        # print(lnList)  #crosscheking... (21 lm)

        if len(lnList) != 0:
            """
            if hand is tracked then
            1. check status(1 or 0) of thumb
               * left hand...
                 if x ordinate of thumb tip is less than that of pinky finger tip, then its left hand...else right hand
                 if x ordinate of thumb tip is less than that of thumb ip, then thumb is open(appends 1)... else closed(0)
               * right hand...
                 if x ordinate of thumb tip is less than that of thumb ip, then thumb is closed(0)... else opened(1)
            2. check status of remaining fingers...
                if y ordinate of a finger tip is less than that of its pip, then that finger is open(1)... else closed(0)
            3. through this status list recognise the number showed in input...
            
            refer [https://user-images.githubusercontent.com/71878747/118373592-63aee580-b5d5-11eb-9fe7-a0fcf00cab1d.jpg] for tip, ip, pip of fingers...
            
            """
            # tips are 4,8,12,16,20
            fingers = []

            if lnList[tipIDs[0]][1] < lnList[tipIDs[4]][1]:
                # for thumb - left hand
                if lnList[tipIDs[0]][1] < lnList[tipIDs[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # for thumb - right hand
                if lnList[tipIDs[0]][1] > lnList[tipIDs[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # for other fingers..
            for id in range(1,5):
                if lnList[tipIDs[id]][2] < lnList[tipIDs[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)  # list of states(open or close) of fingers...
            totalFingers = fingers.count(1)
            print(totalFingers)

            # for displaying number showed on screen...
            cv2.rectangle(img, (20, 225), (170, 425), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 25)

            # for overlaying those finger images on result...
            h, w, c = overLayList[totalFingers].shape
            img[0:h, 0:w] = overLayList[totalFingers]

        # frames per second...
        cTime = time.time()
        fps = 1 / (cTime-pTime)
        pTime = cTime

        # fps, time, extra text
        cv2.rectangle(img, (440, 30), (620, 70), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"FPS : {str(int(fps))}", (450, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
        cv2.rectangle(img, (330, 450), (640, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"{str(datetime.datetime.now())}", (335, 475), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 140, 255), 1)
        cv2.rectangle(img, (140, 70), (620, 110), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, 'for accuracy face fair side to cam', (150, 100), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (0, 0, 255), 2)

        # result
        cv2.imshow("image", img)  # output...
        cv2.waitKey(1)  # keep 1ms delay

if __name__ == '__main__':
    main()
