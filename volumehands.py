import cv2
import mediapipe as mp
import time
import numpy as np
import math
import handtrackingmodule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

device=AudioUtilities.GetSpeakers()
interface=device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume=cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]


cap=cv2.VideoCapture(0)
#wCam, hCam = 680, 420
#cap.set(3, wCam)
#cap.set(4, hCam)
pTime=0
detector=htm.handDetector()
vol=0
volBar=400
volPer=0
while True:
    success, img= cap.read()
    img= detector.findHands(img)
    llmarks=detector.findPosition(img)
    if len(llmarks)!=0:
        #print(llmarks[4], llmarks[8])
        x1, y1 = llmarks[4][1], llmarks[4][2]
        x2, y2 = llmarks[8][1], llmarks[8][2]
        cv2.circle(img, (x1,y1), 5, (255,255,0), 5)
        cv2.circle(img, (x2,y2), 5, (255,255,0), 5)
        cv2.line(img, (x1,y1), (x2,y2), (255,255,0), 4)
        cx, cy= (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx,cy), 5, (255,255,0), 5)
        
        length=math.hypot(x2-x1, y2-y1)
        #print(length)
        
        #Hand range is [50,300]
        #Vol range is [-65,0]
        vol = np.interp(length, [50,300], [minVol,maxVol])
        volBar = np.interp(length, [50,300], [400,150])
        volPer = np.interp(length, [50,300], [0,100])
        volume.SetMasterVolumeLevel(vol, None)
        print(int(length), vol)

        if length<50:
            cv2.circle(img, (cx,cy), 5, (255,0,255), 4)
    cv2.rectangle(img, (50,150), (85, 400), (255,0,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(img, f"{str(int(volPer))} %", (40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f"FPS: {str(int(fps))}", (70,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)