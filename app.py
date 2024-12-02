import cv2
import numpy as np

LIMITES_CORES = {
    "vermelho": (np.array([0, 127, 140], np.uint8), np.array([180, 192, 178], np.uint8)),
    "verde": (np.array([25, 52, 72], np.uint8), np.array([102, 255, 255], np.uint8)),
    "azul": (np.array([100, 80, 100], np.uint8), np.array([140, 255, 180], np.uint8)),
    "preto": (np.array([0, 0, 0]), np.array([180, 255, 90])),
    "branco": (np.array([0, 0, 200]), np.array([180, 55, 255]))
}

VALORES_FICHAS = {
    "branco": 5,
    "vermelho": 10,
    "verde": 20,
    "azul": 50,
    "preto": 100
}

def identificar_cor(circulo, imagem_hsv):
    x, y, raio = circulo
    mascara = np.zeros(imagem_hsv.shape[:2], dtype="uint8")
    cv2.circle(mascara, (x, y), int(raio * 0.9), 255, -1)

    for cor, (inf, sup) in LIMITES_CORES.items():
        mascara_cor = cv2.inRange(imagem_hsv, inf, sup)
        intersecao = cv2.bitwise_and(mascara, mascara_cor)
        if cv2.countNonZero(intersecao) > 0.6 * np.pi * raio**2:
            return cor
    return "desconhecida"

def detectar_fichas(imagem):
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imagem_suavizada = cv2.medianBlur(imagem_cinza, 5)
    circulos = cv2.HoughCircles(
        imagem_suavizada,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=15,
        param1=85,
        param2=30,
        minRadius=20,
        maxRadius=100
    )
    imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    total_pontuacao = 0
    fichas_por_cor = {cor: 0 for cor in VALORES_FICHAS}

    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for circulo in circulos[0, :]:
            x, y, raio = circulo
            cor = identificar_cor((x, y, raio), imagem_hsv)

            if cor in VALORES_FICHAS:
                fichas_por_cor[cor] += 1
                total_pontuacao += VALORES_FICHAS[cor]
                cv2.circle(imagem, (x, y), raio, (0, 255, 0), 2)

    cv2.putText(imagem, f'Pontuacao: {total_pontuacao}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    cv2.imshow("Fichas Detectadas", imagem)

    print(f"Detalhamento de fichas por cor: {fichas_por_cor}")
    print(f"Pontuação total: {total_pontuacao}")

video_path = "video/chips.mp4"

video = cv2.VideoCapture(video_path)

while True:
    _, imagem = video.read()
    detectar_fichas(imagem)

    if cv2.waitKey(5) & 0xFF == 27:
        break
