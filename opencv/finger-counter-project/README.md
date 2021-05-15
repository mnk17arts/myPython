# Finger Counter Project Using Hand Tracking - OpenCv

In this project input is given through webcam. When a hand is tracked down our project gives the output of the Number
which was shown by user's hand.

> Packages :  
+ cv2
+ HandTrackingModule.py
+ datetime
+ time
+ os

### Explanation:
If hand is tracked then
1. check status(1 or 0) of thumb
   * left hand...
     if x ordinate of thumb tip is less than that of pinky finger tip, then its left hand...else right hand
     if x ordinate of thumb tip is less than that of thumb ip, then thumb is open(appends 1)... else closed(0)
   * right hand...
     if x ordinate of thumb tip is less than that of thumb ip, then thumb is closed(0)... else opened(1)
2. check status of remaining fingers...
    if y ordinate of a finger tip is less than that of its pip, then that finger is open(1)... else closed(0)
3. through this status list recognise the number showed in input...

> Hand landmarks list... <br>
> ![handlandmarks](https://user-images.githubusercontent.com/71878747/118373592-63aee580-b5d5-11eb-9fe7-a0fcf00cab1d.jpg)

> ### A small glimpse of this  project.. 👇  
> https://user-images.githubusercontent.com/71878747/118373781-29921380-b5d6-11eb-9efa-868fd62a6054.mp4







Note: Maximum one hand is tracked in this project.

##### Other works 🎊
⭐ [`Hand tracking Project`](https://github.com/mnk17arts/myPython/blob/main/opencv/hand-tracking-module/README.md) 
⭐ [`Face Recognition Project`](https://github.com/mnk17arts/myPython/tree/main/opencv/face-recognition-project) 
⭐ [`Volume Control using Hand tracking`]() <br/>
⭐ [`Virtual Painting using Hand Tracking`](https://github.com/mnk17arts/myPython/tree/main/opencv/virtual-paint-project) 
⭐ [`QR and Barcode detector and decoder`]() 
⭐ [`Sample Survey Form Page`](https://github.com/mnk17arts/myHtmlCssJs/tree/main/survey-from) <br/>
⭐ [`Product Landing Page`](https://github.com/mnk17arts/myHtmlCssJs/tree/main/product-landing-page) 
⭐ [`Tribute Page`](https://github.com/mnk17arts/myHtmlCssJs/tree/main/tribute-page)  
⭐ [`Technical Documentation Page`](https://github.com/mnk17arts/myHtmlCssJs/tree/main/technical-documentation-page) 
⭐ [`Sample Personal Portfolio Page`](https://github.com/mnk17arts/myHtmlCssJs/tree/main/personal-portfolio-page)  


any kind of suggestions are welcomed : mailto:mnk17arts@gmail.com

made with py❤️
