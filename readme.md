# 👁️ Bogotá Watcher

**Bogotá Watcher** es un sistema inteligente que detecta posibles riesgos en videos relacionados con el entorno urbano, con especial atención en transporte público como TransMilenio.

Detecta automáticamente situaciones como:

- Robos
- Inundaciones
- Trancón (congestión vehicular)
- Aglomeraciones

El sistema usa redes neuronales profundas para analizar videos reales y generar alertas automáticas.

---

## 🧠 ¿Qué hace este proyecto?

1. Clasifica escenas peligrosas usando un modelo **MobileNetV2**.
2. Detecta personas con **YOLOv8** para identificar aglomeraciones.
3. Combina ambas tareas para validar coincidencias y generar alertas.
4. Presenta resultados de forma visual usando **Streamlit**.

---

## 🗂️ Estructura del proyecto
```
BogotaWatcher/
├── data/
│   ├── raw/           # Aca se almacenará los videos generados del doc download.py
│   ├── frames/        # Acá se almacenarán los frames extraidos generados por el doc frames.py
│   ├── clasificador/  # En esta carpeta se encontrará una clasificacion inicial reliazada
│       ├── aglomeracion/
│       ├── inundacion/
│       ├── robo/
│       ├── trancon/
│   ├── frames_app/    # Esta carpeta se generará al utilizar la app
│   ├── detecciones/   # Esta carpeta se generará al correr detector.py
├── src/
│   ├── alerts.py
│   ├── classify.py
│   ├── comparar_alertas.py
│   ├── detector.py
│   ├── download.py
│   ├── frames.py
│   └── utils.py
├── app.py                 # Interfaz web local con Streamlit
├── run_pipeline.py       # Ejecuta el pipeline completo
├── requirements.txt      # Dependencias necesarias
├── README.md             # Este archivo
├── modelo_clasificador.h5 # Este se crea al correr el archivo classify.py
├── yolov8n.pt


```

Se recomienda crear una carpeta llamada data y dentro de ella una llamada raw, esto con el objetivo de guardar lo generado en el archivo download.py y otra llamada frames para guardar lo generado en el archivo frames.py. Adicionalmente, para poder entrenar bien el modelo se recomienda usar la carpeta clasificador ya que en esta se encuentran 4 carpetas que contienen la base para entrenar el modelo.

---

## 🧾 ¿Cómo se puede usar?
| Método          | Herramienta | Ideal para         |
| --------------- | ----------- | ------------------ |
| `app.py`        | Streamlit   | Ejecución local 📍 |


## 🛠️ Instalación

1. Clona el repositorio:

git clone https://github.com/CamilaG2/Alerta.git
cd Alerta
python -m venv venv
venv\Scripts\activate      # En Windows
pip install -r requirements.txt

---

## 🔄 Flujo del proyecto

Este es el orden recomendado para ejecutar el sistema completo desde cero:

1. **Descargar videos** desde TikTok  
   👉 Ejecuta: `src/download.py`  
   Esto guarda los `.mp4` en `data/raw/`.

2. **Extraer frames** de los videos descargados  
   👉 Ejecuta: `src/frames.py`  
   Los frames se guardan en `data/frames/`.

3. **Entrenar el clasificador** con las carpetas del dataset personalizado  
   👉 Ejecuta: `src/classify.py`  
   Se genera el archivo `modelo_clasificador.h5`.

4. **Detectar personas con YOLOv8** en los frames  
   👉 Ejecuta: `src/detector.py`  
   Se guardan imágenes con detecciones en `data/detecciones/`.

5. **Comparar resultados** de ambos modelos  
   👉 Ejecuta: `src/comparar_alertas.py`  
   Esto imprime coincidencias entre ambos enfoques.

6. ✅ También puedes ejecutar todo automáticamente con:
   ```bash
   python run_pipeline.py


---

## 🔍 Tecnologías utilizadas

| Librería        | ¿Para qué se usa?                         |
| --------------- | ----------------------------------------- |
| `tensorflow`    | Clasificador de escenas con MobileNetV2   |
| `ultralytics`   | Detección de personas con YOLOv8          |
| `opencv-python` | Extracción de frames desde videos         |
| `gradio`        | Interfaz para la web en Hugging Face      |
| `streamlit`     | Interfaz local para pruebas               |
| `Pillow`        | Procesamiento y visualización de imágenes |
| `numpy`         | Cálculos y manipulación de arrays         |


---

## 📸 Créditos y dataset
Los videos utilizados fueron descargados desde cuentas públicas de TikTok enfocadas en noticias y seguridad en Bogotá. Las imágenes extraídas se agruparon en clases para crear un dataset personalizado.

---

## 📬 Autoría
Camila Garcia\\
Universidad del Rosario\\
Mayo 2025