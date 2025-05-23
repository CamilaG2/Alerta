'''
from src.frames import procesar_videos

if __name__ == "__main__":
    procesar_videos()


from src.classify import entrenar_clasificador

if __name__ == "__main__":
    entrenar_clasificador()


from src.alerts import cargar_modelo, generar_alertas

if __name__ == "__main__":
    modelo = cargar_modelo("modelo_clasificador.h5")
    generar_alertas(modelo)



from src.detector import detectar_en_frames

if __name__ == "__main__":
    detectar_en_frames()


from src.comparar_alertas import comparar_modelos

if __name__ == "__main__":
    comparar_modelos()
'''
from src.frames import procesar_videos
from src.classify import entrenar_clasificador
from src.detector import detectar_en_frames
from src.comparar_alertas import comparar_modelos
import subprocess

if __name__ == "__main__":
    print("📥 PASO 1: Ejecutando descarga de videos...")
    subprocess.run(["python", "src/download.py"])

    print("🎞️ PASO 2: Extrayendo frames desde los videos...")
    procesar_videos()

    print("🧠 PASO 3: Entrenando clasificador...")
    entrenar_clasificador()

    print("📦 PASO 4: Detectando personas con YOLOv8...")
    detectar_en_frames()

    print("📊 PASO 5: Comparando alertas YOLO vs Clasificador...")
    comparar_modelos()

    print("\n✅ Todo el pipeline ha sido ejecutado con éxito.")
