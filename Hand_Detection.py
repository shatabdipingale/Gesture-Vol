import cv2 as cv
import mediapipe as mp
import time

cap=cv.VideoCapture(0)
# formaltiy just to start using this model.
mpHands=mp.solutions.hands

hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

pastime=0
while True:
    
    success,img=cap.read()
    # Need to convert in rgb as mediapipe takes rgb image
    imgRGB=cv.cvtColor(img,cv.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    #a=cv.waitKey(50)

    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for id,lm in enumerate(hand.landmark):
                h,w,c=img.shape
                # ratio of the image is given so if we multiply then we get the exact pixel
                cx,cy= int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)

                if(id==20):
                    cv.circle(img,(cx,cy),19,(0,255,255), cv.FILLED)
            mpDraw.draw_landmarks(img,hand,mpHands.HAND_CONNECTIONS)
    #if(a==ord("e")):
        #break

    curtime=time.time()
    fps=1/(curtime-pastime)
    pastime=curtime
    cv.putText(img,"FPS "+ str(int(fps)),(10,70), cv.FONT_HERSHEY_PLAIN,3,(255,255,255),3) 
    cv.imshow('Image',img)
    cv.waitKey(1)
