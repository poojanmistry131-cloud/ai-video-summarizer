import whisper
import os
from threading import Lock

MODEL_SIZE = "base"
_model = None
_model_lock = Lock()


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                print(f"Loading Whisper model: {MODEL_SIZE} ...")
                _model = whisper.load_model(MODEL_SIZE)
                print("Whisper model loaded!")
    return _model

def transcribe_chunks(chunk_paths: list) -> str:
    if not chunk_paths:
        raise ValueError("No audio chunks provided.")

    for chunk_path in chunk_paths:
        if not os.path.exists(chunk_path):
            raise FileNotFoundError(f"Chunk not found: {chunk_path}")

    model = _get_model()
    full_transcript = []

    for i, chunk_path in enumerate(chunk_paths):
        print(f"Transcribing chunk {i+1}/{len(chunk_paths)}...")

        result = model.transcribe(
            chunk_path,
            fp16=False,
            language=None,
            verbose=False
        )

        text = result.get("text", "").strip()
        if text:
            full_transcript.append(text)

    combined = " ".join(full_transcript)

    if not combined.strip():
        raise ValueError("Transcription produced empty text.")

    return combined