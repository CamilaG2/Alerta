import cv2
import os
from pathlib import Path

# Esta función extrae frames de un video cada cierto número de segundos
def extraer_frames(video_path, salida_dir, intervalo_segundos=1):
    video_name = Path(video_path).stem  # Nombre del video sin extensión
    salida_path = Path(salida_dir) / video_name
    salida_path.mkdir(parents=True, exist_ok=True)  # Crear carpeta de salida si no existe

    cap = cv2.VideoCapture(str(video_path))  # Cargar el video
    fps = cap.get(cv2.CAP_PROP_FPS)  # Obtener la tasa de frames por segundo
    intervalo_frames = int(fps * intervalo_segundos)  # Cuántos frames saltar

    i, guardados = 0, 0  # Contadores

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Si no hay más frames, salimos del loop

        # Guardamos un frame cada cierto intervalo
        if i % intervalo_frames == 0:
            out_path = salida_path / f"frame_{guardados:03}.jpg"
            cv2.imwrite(str(out_path), frame)
            guardados += 1
        i += 1

    cap.release()  # Cerramos el video
    print(f"🖼️ {guardados} frames guardados para {video_name}")

# Esta función procesa todos los videos en la carpeta de entrada
def procesar_videos(entrada_dir="data/raw", salida_dir="data/frames"):
    Path(salida_dir).mkdir(parents=True, exist_ok=True)

    for archivo in os.listdir(entrada_dir):
        if archivo.endswith(".mp4"):
            ruta = os.path.join(entrada_dir, archivo)
            extraer_frames(ruta, salida_dir)
