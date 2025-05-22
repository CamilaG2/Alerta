import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from pathlib import Path

# Esta función carga el modelo entrenado desde un archivo .h5
def cargar_modelo(modelo_path="modelo_clasificador.h5"):
    return tf.keras.models.load_model(modelo_path)

# Esta función toma un frame (imagen) y lo clasifica usando el modelo
def predecir_frame(modelo, frame_path, img_size=224):
    # Cargamos la imagen y la redimensionamos al tamaño que espera el modelo
    img = image.load_img(frame_path, target_size=(img_size, img_size))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0) / 255.0  # Normalizamos los valores entre 0 y 1
    pred = modelo.predict(x)  # Hacemos la predicción
    clase_predicha = np.argmax(pred)  # Tomamos la clase con mayor probabilidad
    return clase_predicha, pred

# Esta función recorre todos los frames de una carpeta y genera alertas si detecta algo peligroso
def generar_alertas(modelo, frames_dir="data/frames", clases=None):
    # Lista de clases que maneja el modelo
    if clases is None:
        clases = ["aglomeracion", "inundacion", "robo", "trancon"]

    # Recorremos cada subcarpeta (cada video)
    for carpeta in os.listdir(frames_dir):
        carpeta_path = os.path.join(frames_dir, carpeta)
        if not os.path.isdir(carpeta_path):
            continue  # Saltamos si no es una carpeta

        # Recorremos todos los archivos de imagen dentro de esa carpeta
        for frame_file in os.listdir(carpeta_path):
            if frame_file.endswith(".jpg"):
                frame_path = os.path.join(carpeta_path, frame_file)
                clase_idx, _ = predecir_frame(modelo, frame_path)
                clase = clases[clase_idx]

                # Si la clase predicha es una alerta (robo, inundación o trancon), la imprimimos
                if clase in ["robo", "inundacion", "trancon"]:
                    print(f"🚨 ALERTA: Se detectó '{clase.upper()}' en {frame_file} del video '{carpeta}'")
