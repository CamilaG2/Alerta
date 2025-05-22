import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from ultralytics import YOLO
import os
from pathlib import Path

# Esta función compara las predicciones del clasificador y las de YOLO
def comparar_modelos(path_frames="data/frames", modelo_clasificador="modelo_clasificador.h5", modelo_yolo="yolov8n.pt", umbral_aglomeracion=5):
    # Cargamos el modelo de clasificación y el modelo YOLO
    model_clasificador = tf.keras.models.load_model(modelo_clasificador)
    model_yolo = YOLO(modelo_yolo)

    # Las clases que puede predecir el clasificador
    clases = ["aglomeracion", "inundacion", "robo", "trancon"]

    resultados = []

    # Recorremos todas las carpetas dentro del directorio de frames
    for carpeta in os.listdir(path_frames):
        carpeta_path = Path(path_frames) / carpeta
        if not carpeta_path.is_dir():
            continue

        # Recorremos los frames dentro de cada carpeta
        for frame in os.listdir(carpeta_path):
            if not frame.endswith(".jpg"):
                continue

            frame_path = str(carpeta_path / frame)

            # -------- Clasificación del frame --------
            img = image.load_img(frame_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0) / 255.0
            pred = model_clasificador.predict(x)
            clase_idx = np.argmax(pred)
            pred_clasificador = clases[clase_idx]

            # -------- Detección con YOLO --------
            result = model_yolo(frame_path)[0]
            # Contamos cuántas personas detectó (class_id 0 es 'person')
            conteo_personas = sum(1 for r in result.boxes.cls if int(r) == 0)
            alerta_yolo = conteo_personas >= umbral_aglomeracion

            # -------- Comparación --------
            # Coincide si YOLO detecta muchas personas y el clasificador predice aglomeración
            coincide = alerta_yolo and pred_clasificador == "aglomeracion"

            resultados.append({
                "video": carpeta,
                "frame": frame,
                "clasificador": pred_clasificador,
                "personas_detectadas": conteo_personas,
                "yolo_alerta": alerta_yolo,
                "coincide": coincide
            })

            # Mostramos el resultado por consola
            print(f"{frame} | Clasificador: {pred_clasificador} | Personas: {conteo_personas} | Coincide: {coincide}")

    return resultados
