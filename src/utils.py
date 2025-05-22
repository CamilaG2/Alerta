import cv2
from pathlib import Path

# Esta función extrae frames de un video y los guarda en una carpeta
def extraer_frames_video(video_path, salida_dir="data/frames_app", cada_segundos=1):
    # Crea la carpeta de salida si no existe
    Path(salida_dir).mkdir(parents=True, exist_ok=True)

    # Abre el video con OpenCV
    cap = cv2.VideoCapture(video_path)

    # Calculamos cuántos frames hay que saltar según los segundos indicados
    fps = cap.get(cv2.CAP_PROP_FPS)
    intervalo = int(fps * cada_segundos)

    i = 0
    guardados = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Si no se puede leer más frames, salimos del ciclo

        # Guardamos el frame cada cierto intervalo
        if i % intervalo == 0:
            frame_path = f"{salida_dir}/frame_{i:04d}.jpg"
            cv2.imwrite(frame_path, frame)  # Guardamos el frame como imagen
            guardados.append(frame_path)
        i += 1

    cap.release()  # Cerramos el video
    return guardados  # Devolvemos la lista de rutas guardadas
