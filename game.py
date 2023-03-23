import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

# Configurar la cámara
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

# Configurar el detector de manos
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Definir la función para calcular la distancia en centímetros
# x es la distancia medida en píxeles y y es la distancia correspondiente en centímetros
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # La función es y = Ax^2 + Bx + C

# Variables del juego
cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
timeStart = time.time()
totalTime = 35

while True:

    # Capturar una imagen de la cámara
    success, img = cap.read()
    img = cv2.flip(img, 1)

    height, width, _ = img.shape

    # si el tiempo de juego no ha terminado
    if time.time() - timeStart < totalTime:

        # detectar las manos en la imagen
        hands = detector.findHands(img, draw=False)

        if hands:
            # Obtener las coordenadas de los puntos de referencia de la mano
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1, z1 = lmList[5]
            x2, y2, z2 = lmList[17]

            # Calcular la distancia entre los dedos índice y medio de la mano
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            # Calcular la distancia en centímetros utilizando la función definida anteriormente
            distanceCM = A * distance ** 2 + B * distance + C

            # Si la mano está lo suficientemente cerca del círculo
            if distanceCM < 40:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1

            # Dibujar un rectángulo alrededor de la mano en la imagen
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)

            # Mostrar la distancia en centímetros sobre el rectángulo
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

        # Si el contador está activado, esperar a que se complete la animación de cambio de color del círculo
        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (255, 0, 255)
                score += 1
                counter = 0

        # Dibujar Circulo
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # HUB - Tiempo y Puntaje
        timeText = f'Time: {int(totalTime - (time.time() - timeStart))}'
        cvzone.putTextRect(img, timeText, (width - 300, 75), scale=3, offset=20)

        scoreText = f'Score: {str(score).zfill(2)}'
        cvzone.putTextRect(img, scoreText, (60, 75), scale=3, offset=20)
    else:
        # Si el tiempo de juego ha terminado, mostrar la pantalla de Game Over
        gameOverRectPos = (int(width / 2 - 200), int(height / 2 - 80))
        yourScoreRectPos = (int(width / 2 - 155), int(height / 2 - 10))
        restartRectPos = (int(width / 2 - 115), int(height / 2 + 70))

        # Mostrar el puntaje final
        cvzone.putTextRect(img, 'Game Over', gameOverRectPos, scale=5, offset=30, thickness=7)
        cvzone.putTextRect(img, f'Your Score: {score}', yourScoreRectPos, scale=3, offset=20)
        cvzone.putTextRect(img, 'Press R to restart', restartRectPos, scale=2, offset=10)

    # Mostrar la imagen
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    # Si se presiona la tecla R, reiniciar el juego
    if key == ord('r'):
        timeStart = time.time()
        score = 0


# Complete game
