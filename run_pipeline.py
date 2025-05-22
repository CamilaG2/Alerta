from src.download import descargar_videos
from src.frames import procesar_videos
from src.classify import entrenar_clasificador
from src.detector import detectar_en_frames
from src.comparar_alertas import comparar_modelos

if __name__ == "__main__":
    # -----------------------------
    # Paso 1: Descargar los videos desde TikTok
    # -----------------------------
    print("⬇️ Descargando videos...")
    urls = [
        "https://www.tiktok.com/@rcnradiocolombia/video/7266222798954138886",
        "https://www.tiktok.com/@seguridad_bogota/video/7453973210762169606",
        # Agrega los demás links aquí...
    ]
    descargar_videos(urls, output_dir="data/raw")

    # -----------------------------
    # Paso 2: Extraer frames de los videos
    # -----------------------------
    print("\n🖼️ Extrayendo frames de los videos...")
    procesar_videos(entrada_dir="data/raw", salida_dir="data/frames")

    # -----------------------------
    # Paso 3: Entrenar el clasificador
    # -----------------------------
    print("\n🔧 Entrenando modelo clasificador...")
    entrenar_clasificador(
        data_dir="data/clasificador",
        modelo_salida="modelo_clasificador.h5",
        epochs=7
    )

    # -----------------------------
    # Paso 4: Detectar personas con YOLO en los frames
    # -----------------------------
    print("\n🔍 Ejecutando detección con YOLO...")
    detectar_en_frames(
        input_dir="data/frames",
        output_dir="data/detecciones",
        modelo_path="yolov8n.pt",
        umbral_aglomeracion=5
    )

    # -----------------------------
    # Paso 5: Comparar predicciones entre modelos
    # -----------------------------
    print("\n📊 Comparando predicciones...")
    resultados = comparar_modelos(
        path_frames="data/frames",
        modelo_clasificador="modelo_clasificador.h5",
        modelo_yolo="yolov8n.pt",
        umbral_aglomeracion=5
    )

    # -----------------------------
    # Resumen final
    # -----------------------------
    coincidencias = sum(1 for r in resultados if r["coincide"])
    print(f"\n✅ Coincidencias clasificador + YOLO: {coincidencias} de {len(resultados)} frames analizados")
