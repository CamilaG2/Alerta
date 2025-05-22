# Importamos las librerías necesarias
import gradio as gr
from pathlib import Path
import os
from src.utils import extraer_frames_video  # Función personalizada para extraer frames del video
from src.alerts import cargar_modelo, predecir_frame  # Cargar modelo y predecir cada frame
from ultralytics import YOLO  # Modelo YOLOv8 para detección de objetos
from PIL import Image  # Para mostrar imágenes

# Cargamos los modelos una vez para no recargarlos por cada frame
modelo_yolo = YOLO("yolov8n.pt")
modelo_clasificador = cargar_modelo("modelo_clasificador.h5")

# Nombres de las clases según el orden del entrenamiento
clases = ["aglomeracion", "inundacion", "robo", "trancon"]

# Esta función se ejecuta cuando se sube un video
def procesar_video(video):
    temp_dir = Path("temp_gradio")
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Guardamos el video subido en disco para poder procesarlo
    video_path = temp_dir / video.name
    with open(video_path, "wb") as f:
        f.write(video.read())

    # Creamos carpeta para almacenar los frames extraídos
    video_name = Path(video.name).stem
    frame_dir = f"data/frames_app/{video_name}"
    os.makedirs(frame_dir, exist_ok=True)

    # Extraemos frames del video
    frames = extraer_frames_video(str(video_path), frame_dir)

    resultados = []  # Lista de imágenes con detecciones
    alertas = []     # Lista de textos con alertas

    # Procesamos cada frame uno por uno
    for frame_path in frames:
        # Clasificamos el frame con el modelo entrenado (MobileNetV2)
        clase_idx, _ = predecir_frame(modelo_clasificador, frame_path)
        clase = clases[clase_idx]

        # Detectamos personas con YOLOv8
        result = modelo_yolo(frame_path)[0]
        img = result.plot()  # Imagen con cajas dibujadas

        # Añadimos texto de resultado y posible alerta
        alertas.append(f"{Path(frame_path).name}: {clase.upper()}")
        if clase in ["robo", "inundacion", "trancon"]:
            alertas.append(f"🚨 ALERTA: {clase.upper()} detectado")

        # Guardamos imagen procesada + texto de clasificación
        resultados.append((Image.fromarray(img), f"{clase.upper()}"))

    # Si no hubo alertas, lo indicamos
    return resultados, "\n".join(alertas) if alertas else "✅ No se detectó ningún peligro."

# Interfaz con Gradio
demo = gr.Interface(
    fn=procesar_video,
    inputs=gr.Video(label="Sube un video .mp4"),
    outputs=[
        gr.Gallery(label="Frames procesados"),   # Galería de imágenes con detección
        gr.Textbox(label="Alertas generadas")     # Cuadro de texto con las alertas
    ],
    title="Bogotá Watcher (Gradio Edition)",
    description="Clasificación de escenas y detección de riesgos urbanos a partir de video."
)

# Ejecutamos la app localmente si se llama desde terminal
if __name__ == "__main__":
    demo.launch()
