# 🛣️ Alarme de Sono ao Volante

Detector de sonolência e bocejo com **alarme sonoro automático**, usando visão computacional para alertar quando o motorista apresenta sinais de fadiga ou bocejo durante a direção.

Esse projeto usa **Python**, **OpenCV** e **dlib** para detectar expressões faciais em tempo real e emitir um alarme quando há risco de sonolência.

---

## 📷 Funcionalidades

✔ Detecta **olhos fechados por muitos frames** (EAR baixo)  
✔ Detecta **bocejos com sobrancelha elevada** (MAR + NEP altos)  
✔ Mostra métricas visuais na imagem  
✔ Toca um **alarme sonoro** sem travar a webcam  
✔ Compatível com **caminhos relativos**, ideal para **Docker**  
✔ Configurações podem ser ajustadas por variável de ambiente  

---

## 📁 Estrutura do Projeto

```text
Projeto-Alarme-de-Sono-Ao-Volante/
│
├── Dockerfile
├── requirements.txt
├── README.md
├── alarme_sono_v2.py
├── shape_predictor_68_face_landmarks.dat
└── Alarme/
    └── alarme.mp3
```

---

## 🚀 Como Usar

### 🧠 Pré‑requisitos

Instale as dependências:

```bash
pip install -r requirements.txt
```

Conteúdo do `requirements.txt`:

```
opencv-python
dlib
imutils
scipy
playsound
numpy
```

---

### 🎯 Executar localmente

1. Conecte uma webcam.
2. Coloque o arquivo `shape_predictor_68_face_landmarks.dat` na raiz do projeto.
3. Ajuste o som do alarme em `Alarme/alarme.mp3`.
4. Execute:

```bash
python alarme_sono_v2.py
```

---

## 🐳 Usando com Docker

### Build da imagem

```bash
docker build -t detector-sonolencia .
```

### Executar no Linux (com webcam)

```bash
docker run --rm   --device=/dev/video0:/dev/video0   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix:/tmp/.X11-unix   detector-sonolencia
```

⚠️ No Windows, o acesso à webcam via Docker é limitado. Para testes, recomenda-se usar vídeo gravado.

---

## ⚙️ Variáveis de Ambiente

| Variável | Descrição |
|--------|----------|
| `ALARM_SOUND_PATH` | Caminho para o áudio do alarme |
| `PREDICTOR_PATH` | Caminho para o modelo do dlib |

---

## 📊 Métricas

| Sigla | Significado |
|-----|------------|
| EAR | Eye Aspect Ratio |
| MAR | Mouth Aspect Ratio |
| NEP | Normalized Eyebrow Position |

---

## 📦 Observações

- O arquivo `shape_predictor_68_face_landmarks.dat` é necessário para o funcionamento do projeto

---

## 📄 Licença

MIT License

---

## 👤 Autor

**João Victor Assunção Pereira (Felicxio)**  
Projeto voltado para segurança veicular utilizando visão computacional.
