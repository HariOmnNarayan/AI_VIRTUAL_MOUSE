import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
from playsound import playsound

wCam, hCam = 640, 480
frameR = 100  # frame readuction
smoothening = 7


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
plocX , plocY = 0 , 0
clocX , clocY = 0 , 0

ycurr = 0
xcurr = 0

detector = htm.handDetector(maxHands=1)
wScreen, hScreen = autopy.screen.size()

while True:
    playsoundis = False

    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        yprev = lmlist[8][2]
        xprev = lmlist[8][1]

        #print(x1, y1 ,x2 ,y2)

        # 3
        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # print(fingers)
        # TO MOVE THE CURSOR  # 0 1 0 0 0
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScreen))
            clocX = plocX + (x3- plocX)/smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.smooth_move(wScreen - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            plocX , plocY = clocX , clocY

        # TO CLICK MOUSE # 0 1 1 0 0
        if fingers[1] == 1 and fingers[2] == 1:
            length, img , lineInfo = detector.findDistance(8,12,img)
            #print(length)
            if length < 40:
                #cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        #TO SCREENSHOT # 1 1 1 1 1
        # name_of_img = "ha.png"
        # if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 and fingers[0] == 1:
        #     cv2.putText(img, "TAKING SS", (wCam - 250, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        #     autopy.bitmap.capture_screen().save(name_of_img)
        #     if playsoundis == False :
        #         playsound('screenshot.mp3')
        #         playsoundis = True

        # TO SCROLL  # 0 1 1 1 0
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 : # 0 1 1 1 0
            f1, w1 = lmlist[8][1:]
            f2, w2 = lmlist[12][1:]
            f3, w3 = lmlist[16][1:]
            cv2.circle(img, (f1, w1), 15, (0, 0, 0), cv2.FILLED)
            cv2.circle(img, (f2, w2), 15, (0, 0, 0), cv2.FILLED)
            cv2.circle(img, (f3, w3), 15, (0, 0, 0), cv2.FILLED)

            #print(ycurr - yprev )
            if ycurr - yprev < 0 :
                cv2.putText(img, "SCROLLING DOWN", (wCam-250, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                pyautogui.scroll(-1)
            if  ycurr - yprev > 0 :
                cv2.putText(img, "SCROLLING UP ", (wCam - 250, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                pyautogui.scroll(1)

            ycurr = yprev


        #swiping  the active window
        if fingers[0] == 1  :
            print(xcurr - xprev)
            if xcurr - xprev < 0 :
                pyautogui.keyDown('altleft')
                #pyautogui.hotkey('altleft', 'tab', 'tab')
                pyautogui.press('tab')
                #pyautogui.keyUp('altleft')

        xcurr = xprev

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)



    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
