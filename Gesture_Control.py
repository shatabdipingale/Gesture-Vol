import cv2 as cv
import time
import numpy as np
import Hand_Tracking_Module as htm
import math as mp

#Pycaw libraries- these libraries are used to adjust the volume control of pc 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

vol=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)

min_vol=vol[0]
max_vol=vol[1]

volbar=400

detector=htm.handDetector(detectionCon=0.6)

wcam=640
hcam=720

cap=cv.VideoCapture(0)
cap.set(3,wcam) # 3 is the id of width cam
cap.set(4,hcam)

ptime=0

volper=0
while True:
    suc,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    
    if(len(lmlist)!=0):
        #print(lmlist[4],lmlist[8]) # 4 landmark value is for thumb and 8 for index finge
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]

        cx=(x1+x2)//2
        cy=(y1+y2)//2
        
        cv.circle(img,(x1,y1),15,(259,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),15,(259,0,255),cv.FILLED)

        cv.line(img,(x1,y1),(x2,y2),(255,255,255),3)

        cv.circle(img,(cx,cy),15,(259,0,255),cv.FILLED)
        length=mp.hypot(x2-x1,y2-y1)
        if(length<50):
            cv.circle(img,(cx,cy),15,(0,255,0),cv.FILLED)
        
        #print(length)
        #used min max normalization
        #val=length
        #new_max=0
        #new_min=-65.25
        #ma=310
        #mi=4

        #ans=(((val-mi)*(new_max-new_min))/(ma-mi))+ new_min
        v=np.interp(length,[50,290],[min_vol,max_vol])
        volbar=np.interp(length,[50,290],[400,150])
        volper=np.interp(length,[50,290],[0,100])

        #cv.rectangle(img,(50,150),(85,400) ,(0,255,0),3)
        
        volume.SetMasterVolumeLevel(v, None)
        
    cv.rectangle(img,(50,150),(85,400) ,(0,255,0),3)
    cv.rectangle(img,(50,int(volbar)),(85,400) ,(0,255,0),cv.FILLED)
    cv.putText(img,f'{int (volper)}%',(40,460),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv.putText(img,f'FPS: {int(fps)}',(35,60),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),3)
    cv.imshow("Image",img)
    cv.waitKey(1)
