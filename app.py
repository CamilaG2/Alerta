import streamlit as st
from PIL import Image
from pathlib import Path
import os

# Importamos funciones propias del proyecto
from src.utils import extraer_frames_video
from src.alerts import cargar_modelo, predecir_frame
from ultralytics import YOLO

# -----------------------------
# CONFIGURACIÓN INICIAL DE LA APP
# -----------------------------
st.set_page_config(page_title="TransMilenio Sentinel", layout="wide")
st.title("🚨 TransMilenio Sentinel – Detección de riesgos en video")

# Interfaz para subir un video
st.sidebar.markdown("📤 Sube un video .mp4 para analizar")
video_file = st.sidebar.file_uploader("Selecciona un video", type=["mp4"])

# -----------------------------
# CUANDO EL USUARIO SUBE UN VIDEO
# -----------------------------
if video_file is not None:
    video_name = Path(video_file.name).stem
    temp_video_dir = Path("temp")
    temp_video_dir.mkdir(exist_ok=True)

    # Guardamos temporalmente el archivo
    video_path = temp_video_dir / video_file.name
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    # Mostramos el video subido en la app
    st.video(str(video_path))
    st.success("✅ Video cargado. Extrae frames y analiza.")

    # Botón para iniciar el análisis
    if st.button("🔍 Procesar video"):
        st.info("📸 Extrayendo frames y detectando objetos...")

        # -----------------------------
        # EXTRAEMOS FRAMES DEL VIDEO
        # -----------------------------
        frame_dir = f"data/frames_app/{video_name}"
        os.makedirs(frame_dir, exist_ok=True)
        frames = extraer_frames_video(str(video_path), frame_dir)

        # -----------------------------
        # CARGAMOS LOS MODELOS
        # -----------------------------
        modelo_yolo = YOLO("yolov8n.pt")
        modelo_clasificador = cargar_modelo("modelo_clasificador.h5")
        clases = ["aglomeracion", "inundacion", "robo", "trancon"]

        alertas_detectadas = 0

        # -----------------------------
        # PROCESAMOS CADA FRAME
        # -----------------------------
        for frame_path in frames:
            st.markdown(f"### Frame: {Path(frame_path).name}")

            # Clasificación del frame con MobileNetV2
            clase_idx, _ = predecir_frame(modelo_clasificador, frame_path)
            clase = clases[clase_idx]
            st.write(f"🧠 Clasificación: **{clase.upper()}**")

            # Detección de objetos con YOLOv8
            result = modelo_yolo(frame_path)[0]
            result_img = result.plot()
            st.image(result_img, caption="🔎 Detección YOLO")

            # Si se detecta una clase crítica, mostramos una alerta
            if clase in ["robo", "inundacion", "trancon"]:
                st.error(f"🚨 ALERTA: {clase.upper()} detectado")
                alertas_detectadas += 1

        # -----------------------------
        # MENSAJE FINAL
        # -----------------------------
        if alertas_detectadas == 0:
            st.success("✅ No se detectó ningún peligro en este video.")
