import cv2
import numpy as np

imagem = cv2.imread('images/fichas-teste.jpg')

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 90, 70])
upper_red = np.array([10, 255, 255])
mascara = cv2.inRange(imagem_hsv, lower_red, upper_red)

contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

fichas_vermelhas_encontradas = 0
for contorno in contornos:
    area = cv2.contourArea(contorno)
    if area > 500:
        fichas_vermelhas_encontradas += 1
        cv2.drawContours(imagem, [contorno], -1, (0, 255, 0), 3)

cv2.putText(imagem, f'Fichas vermelhas: {fichas_vermelhas_encontradas}', (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow("Resultado", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
