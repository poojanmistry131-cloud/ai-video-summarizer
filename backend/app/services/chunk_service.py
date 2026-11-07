import subprocess
import os
import glob
import shutil

CHUNK_DIR = "data/chunks"
CHUNK_DURATION = 90

def chunk_audio(audio_path: str) -> list:
    os.makedirs(CHUNK_DIR, exist_ok=True)
    for f in glob.glob(os.path.join(CHUNK_DIR, "chunk_*.wav")):
        os.remove(f)

    chunk_pattern = os.path.join(CHUNK_DIR, "chunk_%03d.wav")

    command = [
        "ffmpeg", "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(CHUNK_DURATION),
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        chunk_pattern
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError(f"Chunking failed:\n{result.stderr.decode('utf-8')}")

    chunk_files = sorted(glob.glob(os.path.join(CHUNK_DIR, "chunk_*.wav")))

    if not chunk_files:
        fallback = os.path.join(CHUNK_DIR, "chunk_000.wav")
        shutil.copy(audio_path, fallback)
        chunk_files = [fallback]

    return chunk_files