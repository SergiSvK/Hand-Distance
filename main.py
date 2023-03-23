import math

import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# hand detector
detector = HandDetector(detectionCon=0.8)

# Find function
x = [300, 245, 203, 170, 145, 130, 112, 103, 93, 87, 80, 75, 73, 67, 62, 59, 57]
y = [28, 25, 30, 35, 40, 45, 50, 55, 68, 65, 70, 75, 80, 85, 90, 95, 180]

coff = np.polyfit(x, y, 2)

# loop
while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)

    if hands:
        lmList = hands[0]["lmList"]
        x, y, w, h = hands[0]["bbox"]

        if len(lmList) >= 21:
            x1, y1, z1 = lmList[5]
            x2, y2, z2 = lmList[17]

            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distance_cm = int(A * distance ** 2 + B * distance + C)

            cv2.rectangle(img, (x, y), (x + w, y + h), (225, 0, 225), 3)
            cvzone.putTextRect(img, f"{distance_cm} cm", (x, y))

    cv2.imshow("Image", img)
    cv2.waitKey(1)
