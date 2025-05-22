from ultralytics import YOLO
import cv2
import os
from pathlib import Path

# Esta función aplica el modelo YOLO a imágenes dentro de carpetas y genera detecciones
def detectar_en_frames(input_dir="data/frames", output_dir="data/detecciones", modelo_path="yolov8n.pt", umbral_aglomeracion=5):
    # Cargamos el modelo YOLO (por defecto, el modelo liviano yolov8n)
    model = YOLO(modelo_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)  # Crear carpeta de salida si no existe

    # Recorremos cada subcarpeta (un video) dentro de la carpeta de entrada
    for carpeta in os.listdir(input_dir):
        carpeta_path = Path(input_dir) / carpeta
        if not carpeta_path.is_dir():
            continue  # Saltamos si no es una carpeta

        # Creamos una carpeta de salida para guardar las imágenes con detecciones
        out_folder = Path(output_dir) / carpeta
        out_folder.mkdir(parents=True, exist_ok=True)

        # Recorremos las imágenes (frames) dentro de cada subcarpeta
        for img_name in os.listdir(carpeta_path):
            if img_name.endswith(".jpg"):
                img_path = str(carpeta_path / img_name)

                # Aplicamos el modelo YOLO a la imagen
                results = model(img_path)
                result = results[0]

                # Dibujamos las detecciones en la imagen
                img_result = result.plot()

                # Contamos cuántas personas hay en la imagen (class_id 0 = persona en el dataset COCO)
                conteo_personas = sum(1 for r in result.boxes.cls if int(r) == 0)

                # Guardamos la imagen con las cajas de detección
                out_path = str(out_folder / img_name)
                cv2.imwrite(out_path, img_result)

                # Mostramos por consola cuántas personas fueron detectadas
                print(f"✅ {img_name} → {conteo_personas} persona(s) detectadas")

                # Si hay muchas personas, generamos una alerta de aglomeración
                if conteo_personas >= umbral_aglomeracion:
                    print(f"🚨 ALERTA DE AGLOMERACIÓN: {conteo_personas} personas en {img_name} (video: {carpeta})")
