import cv2 
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipId=[4, 8, 12 ,16, 20]

    def findHands(self, img, draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #Identifing hands code 
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx, cy= int(lm.x*w), int(lm.y*h)
                #Print(id. lm)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5,(255,0,255), cv2.FILLED)
        return self.lmlist

    def FingersUp(self): 
        fingers=[]
        # Thumb
        if self.lmlist[self.tipId[0]][1] < self.lmlist[self.tipId[0]-1][1]:
            # Here > as it is inverted image using cv2.clip(img)
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1,5):
            if self.lmlist[self.tipId[id]][2] < self.lmlist[self.tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    pTime=0
    cTime=0
    cap=cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success, img=cap.read()
        #Converting img to RGB and adding hands
        img=detector.findHands(img)
        lmlist=detector.findPosition(img)
        if len(lmlist)!=0:
            print(lmlist)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img, str(int(fps)), (100,100), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)
        cv2.imshow("Img", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()