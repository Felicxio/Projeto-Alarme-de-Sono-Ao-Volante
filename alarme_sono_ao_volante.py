# =============================================================================
# DETECTOR DE SONOLÊNCIA E BOCEJO COM ALARME SONORO
# Autor: João Victor Assunção Pereira(Felicxio) 
# Data: 03/10/2025
# =============================================================================

# Importando as bibliotecas
from scipy.spatial import distance as dist
from imutils import face_utils
from playsound import playsound
import threading
import imutils
import dlib
import cv2
import time

#DEFININDO FUNÇÕES CHAVE

#FUNÇÃO PARA TOCAR O ALARME SONORO EM UMA THREAD SEPARADA
def sound_alarm(path):
    playsound(path)

#FUNÇÃO PARA CALCULAR A PROPORÇÃO DE ABERTURA DO OLHO (EYE ASPECT RATIO - EAR)
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

#FUNÇÃO PARA CALCULAR A PROPORÇÃO DE ABERTURA DA BOCA (MOUTH ASPECT RATIO - EAR)
def mouth_aspect_ratio(mouth):
    # Calcula a distância entre os pontos verticais do lábio interno
    A = dist.euclidean(mouth[13], mouth[19]) # Pontos 62 e 68 (do mapa de 68 pontos)
    B = dist.euclidean(mouth[14], mouth[18]) # Pontos 63 e 67
    C = dist.euclidean(mouth[15], mouth[17]) # Pontos 64 e 66
    # Calcula a distância horizontal entre os cantos da boca
    D = dist.euclidean(mouth[12], mouth[16]) # Pontos 61 e 65

    mar = (A + B + C) / (3.0 * D)
    return mar
#FUNÇÃO PARA CALCULAR A POSIÇÃO NORMALIZADA DA SOBRANCELHA (NEP)
def normalized_eyebrow_position(eyebrow, eye):
    #Pega o ponto central superior do olho e o ponto central da sobrancelha
    eye_top = eye[2]
    eyebrow_center = eyebrow[2]

    #calcula a distância vertical 
    vertical_dist = dist.euclidean(eye_top, eyebrow_center)

    #calcula a distância horizontal do olho para normalização
    horizontal_dist = dist.euclidean(eye[0], eye[3])
    if horizontal_dist == 0: #Verificação para evitar erro de divisão por zero
        return 0
    
    #calcula a posição normalizada
    nep = vertical_dist / horizontal_dist
    return nep

#caminho para o arquivo de som do alarme
ALARM_SOUND_PATH = r"E:\Projetos\Projeto - Alarme Sono Ao dirigir\Alarme\alarme.mp3"

#CONSTANTES PARA OS OLHOS (EAR)

EAR_THRESH = 0.25 #LIMIAR PARA O EAR. SE ABAIXO DISSO = OLHO FECHADO // POSSÍVEL NECESSIDADE DE AJUSTE
EAR_CONSEC_FRAMES = 25 # Nº DE FRAMES CONSECUTIVOS COM O OLHO FECHADO PARA DISPARAR O ALARME

#CONTANTES PARA A BOCA (BOCEJO)
MAR_THRESH = 0.30 # LIMIAR DO MAR. ACIMA DISSO = BOCEJO // POSSÍVEL NECESSIDADE DE AJUSTE
MAR_CONSEC_FRAMES = 20 # Nº DE FRAMES CONSECUTIVOS COM A BOCA ABERTA PARA DISPARAR O ALARME

#CONSTANTE PARA A SOBRANCELHA(EM CONJUNTO COM A BOCA)
NEP_THRESH = 0.90 #imagine que é um sensor de altura, isso aqui é um limiar para ver a sobrancelha está mais levantada que o normal.

#INICIALIZANDO CONTADORES DE FRAMES E DA FLAG DE ALARME
EYE_COUNTER = 0
MOUTH_COUNTER = 0
ALARM_ON = False

#AQUI O MODELO PRÉ-TREINADO DO Dlib É CARREGADO
print("[INFO] O preditor de marcos faciais está sendo carregado...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#AQUI OS PONTOS CHAVES DO ROSTO SÃO MAPEADOS
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
(lbStart, lbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
(rbStart, rbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

#AQUI INICIA A PARTE DE CAPTURA DO OPENCV

print("[INFO] Iniciando a captura de vídeo...")
cap = cv2.VideoCapture(0) # 0 = Primeira webcam conectada ao pc
time.sleep(1.0) #pausa para a câmera inicializar

#loop de captura e pré-processamento
while True:
    ret, frame = cap.read() # ret = retorno , frame = imagem
    if not ret: #se ret = false, não foi possível capturar o frame
        break

    frame = imutils.resize(frame, width=800) #redimensiona o frame para uma largura de 800 pixels (você pode aumentar o tamanho da tela aqui, mas isso pode ser custoso dependendo do computador), mantendo a proporção.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converte o frame colorido para escala de cinza.
    rects = detector(gray, 0) #roda o detector de faces do Dlib em escala de cinza.

    for rect in rects: #itera sobre cada retângulo de rosto detectado.
        shape = predictor(gray, rect) #busca os pontos chaves do rosto
        shape = face_utils.shape_to_np(shape) #converte para um array numpy

        #extração de coordenadas (x, y) para cada parte do rosto
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]
        leftEyebrow = shape[lbStart:lbEnd]
        rightEyebrow = shape[rbStart:rbEnd]

        #calculando as métricas para o frame atual
        ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0 #calcula a média do ear dos dois olhos
        mar = mouth_aspect_ratio(mouth)
        nep = (normalized_eyebrow_position(leftEyebrow, leftEye) + normalized_eyebrow_position(rightEyebrow, rightEye)) / 2.0 #calcula a média do nep

        #desenhando os contornos de cada parte do rosto no frame original para visualização.
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0,255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0,255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (0,255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(leftEyebrow)], -1, (0,255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEyebrow)], -1, (0,255, 0), 1)

        #--------LÓGICA DO ALARME---------
        #Lógica para o alarme de sonolência (olhos).
        if ear < EAR_THRESH: #Se ear abaixo do limiar
            EYE_COUNTER += 1
            if EYE_COUNTER >= EAR_CONSEC_FRAMES: #Se o contador atingiu o número de frames consecutivos
                if not ALARM_ON: #se alarme ainda não estiver tocando
                    ALARM_ON = True #ativa a flag de alarme
                    #criando uma nova thread para tocar o som, evitando que o vídeo congele
                    t = threading.Thread(target=sound_alarm, args=(ALARM_SOUND_PATH,))
                    t.daemon = True
                    t.start()
                
                #escreve a mensagem de alerta de sonolência na tela.
                cv2.putText(frame, "ALERTA DE SONO!", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            EYE_COUNTER = 0 #RESET PARA EVITAR ACUMULO, ACONTECE SE OLHO ABRIR
            ALARM_ON = False #FLAG DE ALARME DESATIVADA

        #Lógica para o alarme de bocejo (boca e sobrancelhas)
        if mar > MAR_THRESH and nep > NEP_THRESH: #se limiar de boca e de sobrancelha acima
            MOUTH_COUNTER +=1 #Incrementa contador de frames
            if MOUTH_COUNTER >= MAR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True #ativa a flag de alarme
                    #criando uma nova thread para tocar o som, evitando que o vídeo congele
                    t = threading.Thread(target=sound_alarm, args=(ALARM_SOUND_PATH,))
                    t.daemon = True
                    t.start()

                cv2.putText(frame, "ALERTA DE BOCEJO!", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            MOUTH_COUNTER = 0
            if EYE_COUNTER == 0: #visa desligar a flag do alarme se o dos olhos também não estiver ativo.
                ALARM_ON = False
        
        cv2.putText(frame, f"EAR: {ear:.2f}", (600,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        cv2.putText(frame, f"MAR: {mar:.2f}", (600,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        cv2.putText(frame, f"NEP: {nep:.2f}", (600,90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    
    cv2.imshow("Detector de Sono ao Volante", frame) #Mostra a janela com o frame final

    if cv2.waitKey(1) & 0xFF == ord("q"): #espera 1 ms. Se q for pressionado...
        break #...interrompe o loop while

# ---- BLOCO DE LIMPEZA FINAL -----
print("[INFO] Encerrando o programa...")
cap.release() #libera o dispositivo webcam
cv2.destroyAllWindows() #fecha todas as janelas abertas pelo openCV
