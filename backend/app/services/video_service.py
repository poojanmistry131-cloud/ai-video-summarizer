import yt_dlp
import os
import requests
import re

VIDEO_DIR = "data/videos"

def is_youtube_url(url: str) -> bool:
    youtube_patterns = [
        r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/",
        r"(https?://)?(www\.)?youtu\.be/"
    ]
    return any(re.search(p, url) for p in youtube_patterns)

def download_video(url: str) -> str:
    os.makedirs(VIDEO_DIR, exist_ok=True)
    output_path = os.path.join(VIDEO_DIR, "input.mp4")

    if os.path.exists(output_path):
        os.remove(output_path)

    if is_youtube_url(url):
        return _download_youtube(url, output_path)
    elif url.lower().endswith(".mp4"):
        return _download_direct_mp4(url, output_path)
    else:
        return _download_youtube(url, output_path)

def _download_youtube(url: str, output_path: str) -> str:
    cookies_path = "cookies.txt"
    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "quiet": False,
        "noplaylist": True,
    }
    if os.path.exists(cookies_path):
        ydl_opts["cookiefile"] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Video download failed.")
    return output_path

def _download_direct_mp4(url: str, output_path: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, stream=True, headers=headers, timeout=60)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return output_path