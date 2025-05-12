import os
import yt_dlp
import uuid

TEMP_FOLDER = 'temp/song_request'

os.makedirs(TEMP_FOLDER, exist_ok = True)

def download_youtube_audio(url: str) -> str:
    '''Download Youtube Audio and returns path'''
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(TEMP_FOLDER, f'{unique_id}.%(ext)s')

    ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
        return mp3_filename
    
def cleanup(filepath: str):
    '''Removes existing mp3'''
    if os.path.exists(filepath):
        os.remove(filepath)
