import subprocess
import os

AUDIO_DIR = "data/audio"

def extract_audio(video_path: str) -> str:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_path = os.path.join(AUDIO_DIR, "audio.wav")

    if os.path.exists(audio_path):
        os.remove(audio_path)

    command = [
        "ffmpeg", "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        audio_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr.decode('utf-8')}")

    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio extraction failed.")

    return audio_path