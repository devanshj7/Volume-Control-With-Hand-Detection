import cv2
import mediapipe as mp


cap=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils      # plotting those 21 points on img




while True:
    success,img=cap.read()

    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)

    # print(results)
    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)

                if id==0:                                                         # for wrist point
                    cv2.circle(img, (cx,cy), 5, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)



    cv2.imshow("Tushar",img)
    cv2.waitKey(1)




