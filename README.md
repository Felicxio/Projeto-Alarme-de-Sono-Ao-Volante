# 🚗 Detector de Sonolência e Bocejo ao Volante

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)
![dlib](https://img.shields.io/badge/dlib-19.x-orange)

Sistema de Visão Computacional em tempo real que utiliza a webcam para monitorar o motorista e emitir alertas sonoros ao detectar sinais de fadiga, como fechamento prolongado dos olhos ou bocejos robustos.

---

## 📸 Demonstração



https://github.com/user-attachments/assets/fa37e2c4-f5cf-45be-9662-c3bb0380aba1



---

## 📖 Sobre o Projeto

Acidentes de trânsito causados por fadiga são um problema grave e recorrente. Este projeto busca oferecer uma solução de baixo custo utilizando apenas uma webcam e técnicas de Visão Computacional para aumentar a segurança do motorista.

O sistema foi construído em Python e se baseia em quatro teorias principais:
1.  **Processamento Digital de Imagens:** Para tratar os frames da webcam e prepará-los para análise.
2.  **Detecção de Marcos Faciais:** Utilizando a biblioteca **Dlib** e seu modelo pré-treinado de 68 pontos, o sistema mapeia com precisão a geometria do rosto do motorista.
3.  **Análise Geométrica:** Métricas robustas como o **EAR (Eye Aspect Ratio)**, **MAR (Mouth Aspect Ratio)** e **NEP (Normalized Eyebrow Position)** são calculadas para transformar os marcos faciais em dados numéricos que representam a abertura dos olhos e da boca.
4.  **Análise de Séries Temporais:** O sistema analisa os dados ao longo do tempo, usando contadores de frames para diferenciar uma piscada normal de um sinal de sonolência, e um simples falar de um bocejo genuíno, tornando os alertas mais precisos.

---

## ✨ Funcionalidades

-   ✅ **Monitoramento em Tempo Real:** Análise contínua do rosto do motorista através da webcam.
-   👁️ **Detecção de Sonolência:** Dispara um alarme se os olhos permanecerem fechados por um período prolongado (baseado no EAR).
-    **Detecção Robusta de Bocejo:** Dispara um alarme ao detectar a combinação de boca muito aberta (MAR) e sobrancelhas levantadas (NEP), reduzindo falsos positivos.
-   🔊 **Alarme Sonoro:** Emite um alerta sonoro para despertar o motorista, executado em uma thread separada para não interferir na análise de vídeo.
-   📊 **Feedback Visual:** Exibe os contornos faciais e os valores de EAR, MAR e NEP na tela para depuração e calibração.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **OpenCV:** Para captura de vídeo e funções de processamento de imagem.
-   **Dlib:** Para detecção de faces e predição de marcos faciais.
-   **NumPy:** Para manipulação eficiente de arrays de imagem.
-   **SciPy:** Para cálculos de distância euclidiana.
-   **Playsound:** Para a execução do alarme sonoro.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o projeto em sua máquina local.

#### **Pré-requisitos**
-   Python 3.10+
-   Git
-   CMake e um compilador C++ (necessário para a instalação do Dlib, veja as [instruções de instalação do dlib](https://gist.github.com/valhallen/e3655455321557d0792131590c37754c)).

#### **Instalação e Execução**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Felicxio/Visao_computacional_com_cv2_projetos-.git](https://github.com/Felicxio/Visao_computacional_com_cv2_projetos-.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd <nome-da-pasta-do-projeto>
    ```

3.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar
    python -m venv venv
    # Ativar (Windows)
    .\venv\Scripts\activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install opencv-python numpy scipy dlib imutils playsound==1.2.2
    ```
    
5.  **Baixe o modelo pré-treinado do Dlib:**
    -   Faça o download do arquivo em: [shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
    -   Descompacte o arquivo e coloque o `shape_predictor_68_face_landmarks.dat` na pasta principal do projeto.

6.  **Execute o script principal:**
    ```bash
    python main.py
    ```
Pressione 'q' na janela da webcam para encerrar o programa.

---

## 🔧 Calibração

Os valores de limiar (thresholds) no código foram definidos com base em testes iniciais, mas podem precisar de ajustes para o seu rosto e condições de iluminação.

-   `EAR_THRESH`: Diminua se o alerta de sono for muito sensível; aumente se ele não detectar.
-   `MAR_THRESH` e `NEP_THRESH`: Observe os valores de MAR e NEP na tela com o rosto relaxado e durante um bocejo para encontrar os limiares ideais.

---

## 👨‍💻 Autor

-   **João Victor Assunção Pereira** - [Felicxio](https://github.com/Felicxio)

Projeto desenvolvido com o auxílio do assistente Gemini.
