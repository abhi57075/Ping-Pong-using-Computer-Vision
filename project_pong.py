import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png",cv2.IMREAD_UNCHANGED)  # Removing the transparency from the ball image
# We dont want to do any processing on the ball image, just import the image
imgBat1 = cv2.imread("Resources/bat1.png",cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png",cv2.IMREAD_UNCHANGED)

detector = HandDetector(detectionCon=0.8, maxHands=2)

ballPos = [300,100]
speedX = 15
speedY = 15
gameOver = False
maxStreakScore = [0,0]
score = [0,0]
highest = 0

while 1:

    success, img = cap.read()
    imgRaw = img.copy()
    img = cv2.flip(img,1) # Since we want to flip it in the horizontal direction we use the id 1, 0 for vertical
    # But now our hand detections will be wrong so we will use flipType function

    # Find hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)
    # if we don't want to display the points on our hands then we write
    # hands = detector.findHands(img, flipType=False, draw = False)

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0) # 0.2 and 0.8 should always be equal to 1

    cv2.putText(img, "PLAYER 2", (800, 610), cv2.FONT_HERSHEY_COMPLEX, 1, (25,0,51), 2)
    cv2.putText(img, f"SCORE : {score[1]}", (750, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    cv2.putText(img, f"CURRENT STREAK : {maxStreakScore[0]}", (750, 680), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv2.putText(img, "PLAYER 1", (350, 610), cv2.FONT_HERSHEY_COMPLEX, 1, (25,0,51), 2)
    cv2.putText(img, f"SCORE : {score[0]}", (300, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    cv2.putText(img, f"CURRENT STREAK : {maxStreakScore[0]}", (300, 680), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    # Draw the ball
    img = cvzone.overlayPNG(img, imgBall, ballPos) # (300,100) is the starting position

    # Check for hands
    if hands:
        for hand in hands:
            x,y,w,h = hand['bbox'] # bbox stands for bounding box
            h1,w1,gv = imgBat1.shape # gv -> garbage value not to be used further
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415) # 20 is the minimum value and 415 is the maximum value, we used this so that the bat does not go out of the image
            # y1 have decided the possible movements of the bat in y direction from 20 to 415           

            if hand['type'] == 'Left':
                img = cvzone.overlayPNG(img, imgBat1, (59,y1))
                if 59 <= ballPos[0] <= 59+w1 and y1-h1//2 <= ballPos[1] <= y1+h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    maxStreakScore[0] += 1

            if hand['type'] == 'Right':
                img = cvzone.overlayPNG(img, imgBat2, (1195,y1))
                if 1195-50 <= ballPos[0] <= 1195 and y1-h1//2 <= ballPos[1] <= y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 30 # will give us the illusion that the bat has hit the ball
                    maxStreakScore[1] += 1

    if ballPos[0] < 40:
        score[1]+=1
        ballPos = [1000,100]
        speedX = -15
        speedY = 15
        
        if highest < max(maxStreakScore):
            highest = max(maxStreakScore)
        maxStreakScore = [0,0]

    elif ballPos[0] > 1200:
        score[0]+=1
        ballPos = [300,100]
        speedX = 15
        speedY = 15
        
        if highest < max(maxStreakScore):
            highest = max(maxStreakScore)
        maxStreakScore = [0,0]
    
    if max(score) == 3:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img, "Press Q to quit", (539,445), cv2.FONT_HERSHEY_PLAIN, 1.5, (255,255,255), thickness = 2)
        cv2.putText(img, str(str(score[0])+" - "+str(score[1])).zfill(2), (565, 360), cv2.FONT_HERSHEY_COMPLEX, 1.5, (200,0,200), 5)
        if score[0] > score[1]:
            cv2.putText(img,"PLAYER 1 WINS !!!",(460,620),cv2.FONT_HERSHEY_SIMPLEX, 2, (200,255,255), thickness = 4)
        else:
            cv2.putText(img,"PLAYER 2 WINS !!!",(460,620),cv2.FONT_HERSHEY_SIMPLEX, 2, (200,255,255), thickness = 4)
        cv2.putText(img, str(f" -> MAX STREAK SCORE : {highest}"), (500, 665), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)

    # If the game is not over move the ball 
    else: 
        # Move the ball
        if ballPos[1] >= 500 or ballPos[1] <= 10: # Bouncing off the wall condition
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY
    
    img[580:700, 20:233] = cv2.resize(imgRaw, (213,120))

    cv2.imshow("AIR PING-PONG",img)

    key = cv2.waitKey(1)

    if key == ord('r'):
        ballPos = [100,100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0,0]
        imgGameOver = cv2.imread("Resources/gameOver.png") # we need to write this bcoz if we dont then our new score will be re written on the previous gameOver screen
    
    elif key == ord('q'):
        break
        cv2.destroyAllWindows()