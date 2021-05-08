"""
FACE RECOGNITION PROJECT

In this project, a face is detected from the camera source (given one) and compares it with the faces (images), which are
stored in the Image File. It can be used for taking "Attendance" using Face Recognition. For that firstly we have to store
 Images(faces) all the attendees.

explanation:
-> all images are in BGR format, so converted in RGB
-> then we get face encodings of those images
-> then we compare those face encodings of images(Image File) with face encodings of the image (face) from the webcam

Note: Maximum one face is recognised in the testing image source at a time. If anyone can modify this code to recognise
      more than one, they are welcome!

code by : Madhapur Nitish kumar
github profile:  https://github.com/mnk17arts
any kind of suggestions are welcomed : mailto:mnk17arts@gmail.com

  thank you :)
"""

import cv2
import face_recognition as fr
import time
import os
import datetime

class FaceRecognition():
    def rgbFlocEncoding(self, image, giveFl=True):
        """
        This method takes an image and
        1. converts it into RGB format
        2. Find it's face locations
        3. Find it's face encodings

        :param image: its an image of which we want to do the above things.
        :param giveFl: its a flag for weather we want face locations in return or not
        :return (if giveFL=True) faceLoc: face locations in the format [ top right btm left ]
                                 encodings: face encodings of the given image
                (if giveFl=False) encodings:face encodings of the given image
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR TO RGB

        try:
            faceLoc = fr.face_locations(image)[0]
            encodings = fr.face_encodings(image)[0]
        except Exception as e:
            faceLoc, encodings = None, None

        if giveFl:
            return faceLoc, encodings
        else:
            return encodings

    def compareFacesDistance(self, enimg, entest):
        """
        Compares the two face encodings given and returns a bool (True or False) and face distance btw them
        :param enimg: face encodings of the one from Image File
        :param entest: face encodings of the one from the Image source (webcam)
        :return match: array of a bool. [True] if faces match and [False] otherwise
                dist:  compare both the face encodings and get a "euclidean distance" for comparison face. The distance
                       tells you how similar the faces are.
        """
        match = fr.compare_faces([enimg], entest)
        dist = fr.face_distance([enimg], entest)
        return match, dist

def main():
    faceRec = FaceRecognition()  # object declaration
    imgPath = "imagefiles"  # name of the Image File
    classNames = []  # we will take names of all the images in this .. used while detailing in ouput..
    myList = os.listdir(imgPath)  # grab list of images in this path..
    draw = True  # flag for drawing rectangle of the webcam image
    pTime = 0  # previous time ... used for frame rate calculation
    encodingsList = [] # imagefiles encodings
    for imgname in myList:
        image = cv2.imread(f'{imgPath}/{imgname}')
        encode = faceRec.rgbFlocEncoding(image, giveFl=False)
        encodingsList.append(encode)
        classNames.append(os.path.splitext(imgname)[0])  # appending image names (without .ext) in classNames list..

    cap = cv2.VideoCapture(0)  # Image Source

    while True:  # frame rate calculation ( frames per sec )
        cTime = time.time()  # current time
        fps = 1 / (cTime - pTime)
        pTime = cTime

        _, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # for better FPS we resize the source image

        testFl, testEn = faceRec.rgbFlocEncoding(imgS)  # face locations and encodings of source img
        if testFl == None:  # if fail to recognise face in source image...
            cv2.rectangle(img, (20, 30), (200, 70), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, f"FPS : {str(int(fps))}", (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
            cv2.rectangle(img, (330, 450), (640, 480), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, f"{str(datetime.datetime.now())}", (335, 475), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 140, 255), 1)
            cv2.imshow('RESULT', img)
            cv2.waitKey(1)
            continue
        matchIndex = 0
        for encoding in encodingsList:  # comparing faces btw Image File and Image Source
            match, dist = faceRec.compareFacesDistance(encoding, testEn)
            if match[0]==True:
                break
            elif ((match[0]==False) and (matchIndex== (len(classNames)-1))):  # if face is recognised but doesnt match with any of the faces in image file
                cv2.putText(img, f'No match!!', (testFl[3] * 4, testFl[0] * 4 - 10),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            matchIndex += 1

        if draw:  # draws rectangle around face in source image
            cv2.rectangle(img, (testFl[3]*4, testFl[0]*4), (testFl[1]*4, testFl[2]*4), (255, 0, 255), 2)
        if matchIndex < len(classNames):  # if faces match...
            cv2.putText(img, f'{classNames[matchIndex]}', (testFl[3] * 4, testFl[0] * 4 - 10),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.rectangle(img, (20, 30), (200, 70), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"FPS : {str(int(fps))}", (30, 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 140, 255), 2)
        cv2.rectangle(img, (330, 450), (640, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f"{str(datetime.datetime.now())}", (335, 475), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 140, 255), 1)
        cv2.imshow('RESULT', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()


