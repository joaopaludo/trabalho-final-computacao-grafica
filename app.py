import cv2
import numpy as np

# Definição das cores para desenhar contornos na imagem
AZUL_BGR = (255, 0, 0)
VERDE_BGR = (0, 255, 0)
VERMELHO_BGR = (0, 0, 255)
PRETO_BGR = (0, 0, 0)
BRANCO_BGR = (255, 255, 255)



# Função para contar as fichas
def contarFichas(contornos):
    contador = 0

    for ficha in contornos:
        area = cv2.contourArea(ficha)

        # Considera apenas fichas com circularidade próxima de 1 e área > 500
        if area > 1500:
            contador += 1
            cv2.drawContours(imagem, [ficha], -1, (0, 255, 255), 3)

    return contador



# Leitura da imagem e conversões
imagem = cv2.imread('images/prod2.png')

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)



# Definição dos limites de valores das cores em HSV para a busca das fichas
vermelho_inf1 = np.array([0, 50, 50])
vermelho_sup1 = np.array([10, 255, 255])
mascara_vermelho1 = cv2.inRange(imagem_hsv, vermelho_inf1, vermelho_sup1)
vermelho_inf2 = np.array([0, 50, 50])
vermelho_sup2 = np.array([10, 255, 255])
mascara_vermelho2 = cv2.inRange(imagem_hsv, vermelho_inf2, vermelho_sup2)
mascara_vermelho = cv2.bitwise_or(mascara_vermelho1, mascara_vermelho2)

verde_inf = np.array([35, 50, 50])
verde_sup = np.array([85, 255, 255])
mascara_verde = cv2.inRange(imagem_hsv, verde_inf, verde_sup)

azul_inf = np.array([100, 50, 50])
azul_sup = np.array([140, 255, 255])
mascara_azul = cv2.inRange(imagem_hsv, azul_inf, azul_sup)

preto_inf = np.array([0, 0, 0])
preto_sup = np.array([180, 255, 50])
mascara_preto = cv2.inRange(imagem_hsv, preto_inf, preto_sup)

branco_inf = np.array([0, 0, 200])
branco_sup = np.array([180, 55, 255])
mascara_branco = cv2.inRange(imagem_hsv, branco_inf, branco_sup)



# Definição dos contornos de cada cor na imagem
contornos_vermelho, _ = cv2.findContours(mascara_vermelho, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_verde, _ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_azul, _ = cv2.findContours(mascara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornor_preto, _ = cv2.findContours(mascara_preto, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_branco, _ = cv2.findContours(mascara_branco, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Contadores para cada cor de ficha
fichas_vermelhas_encontradas = contarFichas(contornos_vermelho)
fichas_verdes_encontradas = contarFichas(contornos_verde)
fichas_azuis_encontradas = contarFichas(contornos_azul)
fichas_pretas_encontradas = contarFichas(contornor_preto)
fichas_brancas_encontradas = contarFichas(contornos_branco)



# Cálculo do valor das fichas
pontos_ficha_branca = 5
pontos_ficha_vermelha = 10
pontos_ficha_verde = 20
pontos_ficha_azul = 50
pontos_ficha_preta = 100

soma = fichas_brancas_encontradas * pontos_ficha_branca + \
            fichas_vermelhas_encontradas * pontos_ficha_vermelha + \
            fichas_verdes_encontradas * pontos_ficha_verde + \
            fichas_azuis_encontradas * pontos_ficha_azul + \
            fichas_pretas_encontradas * pontos_ficha_preta

cv2.putText(imagem, f'Pontuacao: {soma}', (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

cv2.imshow("Resultado", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()
