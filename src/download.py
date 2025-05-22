from yt_dlp import YoutubeDL
from pathlib import Path

# Esta función descarga una lista de videos desde TikTok usando yt_dlp
def descargar_videos(video_urls, output_dir="data/raw"):
    # Creamos la carpeta de salida si no existe
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Opciones para guardar los videos como archivos mp4 en la ruta deseada
    opciones = {
        'format': 'mp4',  # Formato del video
        'outtmpl': f'{output_dir}/video_%(id)s.%(ext)s',  # Nombre de salida: video_ID.mp4
    }

    # Usamos YoutubeDL para descargar los videos desde las URLs
    with YoutubeDL(opciones) as ydl:
        ydl.download(video_urls)

# Si se ejecuta este script directamente, se descargan los videos listados abajo
if __name__ == "__main__":
    # Lista de enlaces de TikTok con contenido relacionado a seguridad y alertas
    urls = [
        "https://www.tiktok.com/@rcnradiocolombia/video/7266222798954138886",
        "https://www.tiktok.com/@seguridad_bogota/video/7453973210762169606",
        "https://www.tiktok.com/@seguridad_bogota/video/7443574213056777527",
        "https://www.tiktok.com/@j0hnrt9/video/7487425109532232966",
        "https://www.tiktok.com/@alertabogota104.4/video/7431627870595828997",
        "https://www.tiktok.com/@valeg_.29/video/7506718369387728134",
        "https://www.tiktok.com/@steve.r.m/video/7231951922595515654",
        "https://www.tiktok.com/@isabelag_08/video/7434558222985366839",
        "https://www.tiktok.com/@herli1999/video/7296254514749918469",
        "https://www.tiktok.com/@samuuuu.ell/video/7421344986647612678",
        "https://www.tiktok.com/@redmasnoticias/video/7506895468740283654",
        "https://www.tiktok.com/@angee_j01/video/7468414447468449030",
        "https://www.tiktok.com/@jhonguantivajoya/video/7168633569571605765",
        "https://www.tiktok.com/@saul.y/video/7289254458821856517",
        "https://www.tiktok.com/@noticiascaracol/video/7366258598819089670",
        "https://www.tiktok.com/@gerardosarmiento_veedoru/video/7238753432134225157"
    ]

    # Llamamos la función para descargar todos los videos
    descargar_videos(urls)
