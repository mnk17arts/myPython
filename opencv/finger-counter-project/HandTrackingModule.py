"""
HAND TRACKING MODULE

In this project I have created a module(HandTrackingModule), which is very useful other hand tracking related projects
like virtual paint project,  gesture volume control etc. In this project, we detect hands and observe the status of the
fingers and also the position or locations of the landmarks of the hand.

packages req: !! opencv, mediapipe !!
              math, time, datetime

code by : Madhapur Nitish kumar
github profile:  https://github.com/mnk17arts
any kind of suggestions are welcomed : mailto:mnk17arts@gmail.com

  thank you :)
"""
import cv2
import mediapipe as mp
import time  # for checking frame rate
import math
import datetime

class handDetector():
    def __init__(self,mode = False, maxHands = 2, detecCon = 0.5, trackCon = 0.5):
        """Initializes a handDetector object.

           Args:
             mode: Whether to treat the input images as a batch of static
               and possibly unrelated images, or a video stream.
             maxHands: Maximum number of hands to detect.
             detecCon: Minimum confidence value ([0.0, 1.0]) for hand
               detection to be considered successful.
             trackCon: Minimum confidence value ([0.0, 1.0]) for the
               hand landmarks to be considered tracked successfully.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detecCon = detecCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detecCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIDs = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
    def findHands(self, img, draw = True):
        """
        detect hands in the given image and draws (flag) their landmarks on that image
        :param img: image in which detection of hands take place
        :param draw: flag for drawing landmarks on the detected hands
        :return img: image
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results)  # <class 'mediapipe.python.solution_base.SolutionOutputs'>
        # print(results.multi_hand_landmarks)
        #  None (or)
        # [landmark {
        #   x: 0.07492467
        #   y: 0.6441997
        #   z: 3.7653067e-06
        # }]
        if self.results.multi_hand_landmarks:
            for handlns in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlns, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0 , draw=True, boundbox=False):
        """
        finds the position of the detected hand
        :param img: Image in which hand is detected
        :param handNo: hand number of, which hand we want to find position (must be a number.. 0,1,2..)
        :param draw: flag to draw the position points on the image
        :param boundbox: flag to draw bounding box around the hand
        :return lnList: list of the landmarks of the hand
        :return bbox: bounding box values [list]
        """
        xlist = []  # x values
        ylist = []  # y values
        self.bbox = []  # bounding box
        self.lnList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, ln in enumerate(myHand.landmark):
                # print(id, ln)
                """
                ex: gives ratio... so we must convert into pixels.. (img.shape gives height, width, center)
                15 x: 0.5091188
                y: 0.49165392
                z: -0.02362372
                """
                h, w, c = img.shape
                cx, cy = int(ln.x * w), int(ln.y * h)
                xlist.append(cx)
                ylist.append(cy)
                self.lnList.append([id, cx, cy])
                if draw:
                    # print(id, cx, cy)  # positions of landmark id
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            self.bbox = xmin-10, ymin-10, xmax+10, ymax+10

            if boundbox:
                cv2.rectangle(img, (self.bbox[0:2]), (self.bbox[2:]), (0, 255, 0), 2)

        if boundbox:
            return self.lnList, self.bbox
        else:
            return self.lnList

    def fingersUp(self):
        """
        using the landmark list of selected hand returns a list of 0's and 1's .
        where 0 is finger down(closed) and 1 is finger up(open)
        ex: [0,0,1,0,0] denotes middle finger is open and rest of the fingers are closed
        :return fingers: list of status of fingers in 0/1
        """
        # tips are 4,8,12,16,20
        fingers = []
        if len(self.lnList) != 0:
            if self.lnList[self.tipIDs[0]][1] < self.lnList[self.tipIDs[4]][1]:
                # for thumb - left hand
                if self.lnList[self.tipIDs[0]][1] < self.lnList[self.tipIDs[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                # for thumb - right hand
                if self.lnList[self.tipIDs[0]][1] > self.lnList[self.tipIDs[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # for other fingers..
            for id in range(1, 5):
                if self.lnList[self.tipIDs[id]][2] < self.lnList[self.tipIDs[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers
        return [None]

    def findDistance(self, p1, p2, img, draw=True):
        """
        takes an image and two points, And find displacement btw those points.
        :param p1: point 1
        :param p2: point 2
        :param img: image
        :param draw: flag to draw those points, center point and line btw them (on img )
        :return length: displacement btw p1 and p2
        :return img: img
        :return ABCpoints: list of p1,p2 and their centre
        """
        x1, y1 = self.lnList[p1][1:]  # p1 position
        x2, y2 = self.lnList[p2][1:]  # p2 position
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        ABCpoints = [x1, y1, x2, y2, cx, cy]
        return length, img, ABCpoints
def main():
    pTime = 0
    cap = cv2.VideoCapture(0)  # webcam no. 0
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lnList= detector.findPosition(img)
        if len(lnList) != 0:
            print(lnList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        # print(detector.fingersUp())
        cv2.rectangle(img, (20, 30), (200, 70), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"FPS : {str(int(fps))}", (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
        cv2.rectangle(img, (330, 450), (640, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"{str(datetime.datetime.now())}", (335, 475), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 140, 255), 1)
        cv2.imshow("Image", img)
        cv2.waitKey(1)  # delay of 1ms
if __name__ == '__main__':
    main()
