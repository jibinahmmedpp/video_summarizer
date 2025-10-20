# stage1_download_audio.py
import sys
from yt_dlp import YoutubeDL

def download_audio(url, out_template="audio.%(ext)s"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stage1_download_audio.py <youtube_url> [output_filename.mp3]")
        sys.exit(1)
    url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "audio.mp3"
    download_audio(url, out_template=out)
    print(f"Saved audio to: {out}")
