import cv2
import mediapipe
import numpy as np
import HandTrackingModule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# 
wCam, hCam = 640, 480          #preferred - 640,480
# 

cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


detector=htm.handDetector(detectionCon=0.7)      # more accuracy 0.7         # made a hand object out here 



devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume=cast(interface, POINTER(IAudioEndpointVolume))                     #initializations

volRange = volume.GetVolumeRange()         
minVol = volRange[0]      # corresponding to -65.25
maxVol = volRange[1]      # corresponding to 0.0
vol=0
volBar=400
volPer=0



while True:
    success, img=cap.read()
    img = detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        # print(lmList[4], lmList[8])

        x1,y1=lmList[4][1],lmList[4][2]     # getting coordinates for thumb in variables
        x2,y2=lmList[8][1],lmList[8][2]     # getting coordinates for index finger
        cx,cy=(x1+x2)//2, (y1+y2)//2          # getting coordinates for the center of the line joining 2 points


        cv2.circle(img, (x1,y1), 15, (52,71,21), cv2.FILLED)   #special pointing out thumb
        cv2.circle(img, (x2,y2), 15, (0,140,255), cv2.FILLED)   #for index finger

        cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 3)   # for drawing line in between those 2 points
        cv2.circle(img, (cx,cy), 15, (255,255,255), cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)  # length of the line
        # print(length)

        # Hand Range (13-280)
        # Volume Range (-65.25-0 )   #convert this hand range into volume range

        vol = np.interp(length, [13,280], [minVol,maxVol])    #convert hand range to volume range
        volBar = np.interp(length, [13,280], [400,150])
        volPer = np.interp(length, [13,280], [0,100])
        print(int(length), vol)         # eg. 280,0.0     13,-65.25
        volume.SetMasterVolumeLevel(vol, None)     #giving range to SetMasterVolumeLevel

        if length<50:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)      # when length reaches less than 50 center turns green coloured


    cv2.rectangle(img, (50,150), (85,400), (0,140,255), 3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (255,255,255), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40,450), cv2.FONT_HERSHEY_COMPLEX, 1,(52,71,21),3)


    cv2.imshow("Happy Independence Day", img)
    cv2.waitKey(1)
    
